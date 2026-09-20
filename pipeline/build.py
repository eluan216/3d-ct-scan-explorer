"""
End-to-end asset builder.

Accepts either a NIfTI subject directory or a DICOM directory.
Both are converted to a CanonicalVolume before the rest of the
pipeline runs, keeping later stages input-agnostic.
"""

from pathlib import Path
from typing import Optional
import numpy as np

from config import PipelineConfig
from models.volume import CanonicalVolume
from models.metadata import VolumeMetadata, Manifest
from preprocessing.window import apply_window
from preprocessing.crop import crop_to_labels
from segmentation.threshold import ThresholdSegmentation
from mesh.generate import generate_all
from mesh.cleanup import basic_cleanup, remove_small_components
from mesh.export import export_glb
from validation.volume import check_finite, check_non_empty, check_spacing


def load_canonical(path: Path) -> CanonicalVolume:
    path = Path(path)
    if (path / "ct.nii.gz").exists():
        from nifti.loader import load_nifti_subject
        return load_nifti_subject(path)
    # assume DICOM directory
    from dicom.loader import load_dicom_directory
    return load_dicom_directory(path)


def load_labels_if_available(path: Path, shape) -> Optional[np.ndarray]:
    if (path / "segmentations").is_dir():
        from nifti.loader import load_existing_labels
        return load_existing_labels(path, shape)
    return None


def build(subject_dir: Path, cfg: PipelineConfig) -> Path:
    subject_dir = Path(subject_dir)
    out = Path(cfg.output_path)
    out.mkdir(parents=True, exist_ok=True)
    (out / "volume").mkdir(exist_ok=True)
    (out / "meshes").mkdir(exist_ok=True)

    # 1. Load through the appropriate adapter
    vol = load_canonical(subject_dir)

    # 2. Volume integrity checks
    if not vol.is_finite():
        raise RuntimeError("volume contains NaN or Inf")
    ok, msg = check_non_empty(vol.data)
    if not ok:
        raise RuntimeError(msg)
    ok, msg = check_spacing(vol.spacing_mm)
    if not ok:
        raise RuntimeError(msg)

    # 3. Labels (only available for NIfTI/TotalSegmentator subjects for now)
    existing = load_labels_if_available(subject_dir, vol.shape)
    seg = ThresholdSegmentation()
    meta = {"existing_labels": existing} if existing is not None else {}
    labels = seg.run(vol.data, vol.spacing_mm, meta)
    label_map = seg.label_map()

    # 4. Optional crop
    offset = np.array([0, 0, 0], dtype=int)
    data = vol.data
    spacing = vol.spacing_mm
    if cfg.crop.enabled and existing is not None:
        data, labels, offset = crop_to_labels(
            data, labels, spacing, cfg.crop.margin_mm
        )

    # 5. Window to uint8 for web delivery
    data_w = apply_window(data, cfg.window.level, cfg.window.width)

    # 6. Write volume assets
    data_w.tofile(out / "volume" / "volume.bin")

    center_mm = (np.array(data_w.shape) * np.array(spacing)) / 2.0
    vol_meta = VolumeMetadata(
        shape=list(data_w.shape),
        spacing_mm=list(spacing),
        origin_mm=list(offset.astype(float)),
        orientation=vol.orientation,
        intensity_range=[float(data_w.min()), float(data_w.max())],
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
    cfg.save(out / "pipeline_config.json")

    return out
