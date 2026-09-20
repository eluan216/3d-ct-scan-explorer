"""
End-to-end asset builder.

Given a subject directory and a PipelineConfig, produce the complete
assets/ tree and a manifest.json that the frontend can consume.
"""

from pathlib import Path
from typing import Optional
import json
import numpy as np
import nibabel as nib

from config import PipelineConfig
from preprocessing.orientation import to_canonical, verify as verify_orientation
from preprocessing.window import apply_window
from preprocessing.crop import crop_to_labels
from segmentation.threshold import ThresholdSegmentation
from mesh.generate import generate_all
from mesh.cleanup import basic_cleanup, remove_small_components
from mesh.export import export_glb
from models.metadata import VolumeMetadata, Manifest
from validation.volume import check_finite, check_non_empty, check_spacing


def load_nifti_subject(subject_dir: Path):
    ct_path = subject_dir / "ct.nii.gz"
    if not ct_path.exists():
        raise FileNotFoundError(f"ct.nii.gz not found in {subject_dir}")

    img = nib.load(str(ct_path))
    img = to_canonical(img)
    data = img.get_fdata()
    spacing = tuple(float(x) for x in img.header.get_zooms()[:3])
    return data, spacing, img


def load_existing_labels(subject_dir: Path, shape) -> Optional[np.ndarray]:
    """Load TotalSegmentator-style masks if present."""
    seg_dir = subject_dir / "segmentations"
    if not seg_dir.is_dir():
        return None

    label_map = {
        "liver": 1,
        "spleen": 2,
        "stomach": 3,
        "kidney_right": 4,
        "kidney_left": 5,
        "aorta": 6,
        "inferior_vena_cava": 7,
    }
    labels = np.zeros(shape, dtype=np.uint8)

    for name, lid in label_map.items():
        p = seg_dir / f"{name}.nii.gz"
        if p.exists():
            m = nib.load(str(p))
            m = to_canonical(m)
            mask = m.get_fdata() > 0
            labels[mask] = lid

    # spine = union of vertebrae_*
    spine = np.zeros(shape, dtype=bool)
    for p in seg_dir.glob("vertebrae_*.nii.gz"):
        m = nib.load(str(p))
        m = to_canonical(m)
        spine |= m.get_fdata() > 0
    labels[spine] = 8

    return labels


def build(subject_dir: Path, cfg: PipelineConfig) -> Path:
    subject_dir = Path(subject_dir)
    out = Path(cfg.output_path)
    out.mkdir(parents=True, exist_ok=True)
    (out / "volume").mkdir(exist_ok=True)
    (out / "meshes").mkdir(exist_ok=True)

    # 1. Load + orient
    volume, spacing, img = load_nifti_subject(subject_dir)
    ok, msg = verify_orientation(img)
    if cfg.require_orientation_check and not ok:
        raise RuntimeError(msg)

    # 2. Basic volume checks
    for check in (check_finite, check_non_empty):
        ok, msg = check(volume)
        if not ok:
            raise RuntimeError(msg)
    ok, msg = check_spacing(spacing)
    if not ok:
        raise RuntimeError(msg)

    # 3. Labels
    existing = load_existing_labels(subject_dir, volume.shape)
    seg = ThresholdSegmentation()
    meta = {"existing_labels": existing} if existing is not None else {}
    labels = seg.run(volume, spacing, meta)
    label_map = seg.label_map()

    # 4. Optional crop
    offset = np.array([0, 0, 0])
    if cfg.crop.enabled and existing is not None:
        volume, labels, offset = crop_to_labels(
            volume, labels, spacing, cfg.crop.margin_mm
        )

    # 5. Window
    volume_w = apply_window(volume, cfg.window.level, cfg.window.width)

    # 6. Write volume assets
    vol_path = out / "volume" / "volume.bin"
    volume_w.tofile(vol_path)

    center_mm = (np.array(volume_w.shape) * np.array(spacing)) / 2.0
    vol_meta = VolumeMetadata(
        shape=list(volume_w.shape),
        spacing_mm=list(spacing),
        origin_mm=list(offset.astype(float)),
        orientation="RAS",
        intensity_range=[float(volume_w.min()), float(volume_w.max())],
        window_level=cfg.window.level,
        window_width=cfg.window.width,
    )
    vol_meta.save(out / "volume" / "metadata.json")

    # 7. Meshes
    meshes = generate_all(labels, label_map, spacing, center_mm, cfg.mesh.max_faces)
    cleaned = {}
    for name, m in meshes.items():
        m = basic_cleanup(m)
        m = remove_small_components(m)
        cleaned[name] = m
    mesh_paths = export_glb(cleaned, out / "meshes")

    # 8. Manifest
    manifest = Manifest(
        pipeline_version=cfg.pipeline_version,
        subject_id=subject_dir.name,
        volume={
            "bin": "volume/volume.bin",
            "metadata": "volume/metadata.json",
        },
        meshes=mesh_paths,
        labels={name: {"id": lid} for lid, name in label_map.items()},
    )
    manifest.save(out / "manifest.json")

    # 9. Save config used for this run
    cfg.save(out / "pipeline_config.json")

    return out
