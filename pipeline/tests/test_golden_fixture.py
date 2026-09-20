"""
Golden fixture regression test.

Builds a synthetic but fully known CanonicalVolume, runs the downstream
path that does not need real DICOM files, and checks the resulting
asset package against expected invariants.
"""

import numpy as np
from pathlib import Path
import tempfile
import json

from models.volume import CanonicalVolume
from config import PipelineConfig
from preprocessing.window import apply_window
from preprocessing.crop import crop_to_labels
from segmentation.threshold import ThresholdSegmentation
from mesh.generate import generate_all
from mesh.cleanup import basic_cleanup
from mesh.export import export_glb
from models.metadata import VolumeMetadata, Manifest
from validation.assets import verify_assets
from validation.invariants import check_canonical_invariants


def make_golden_volume():
    """Create a deterministic 32³ volume with two synthetic organs."""
    data = np.zeros((32, 32, 32), dtype=np.float32)
    # soft-tissue-like values
    data[8:20, 8:20, 8:20] = 50.0   # "liver" region
    data[22:28, 22:28, 12:20] = 40.0  # "spleen" region

    labels = np.zeros((32, 32, 32), dtype=np.uint8)
    labels[8:20, 8:20, 8:20] = 1
    labels[22:28, 22:28, 12:20] = 2

    vol = CanonicalVolume(
        data=data,
        spacing_mm=(1.0, 1.0, 1.0),
        origin_mm=(0.0, 0.0, 0.0),
        orientation="RAS",
        source="golden",
        meta={"fixture": "golden"},
    )
    return vol, labels


def test_golden_end_to_end():
    vol, labels = make_golden_volume()

    # invariants on the volume itself
    inv = check_canonical_invariants(vol)
    assert inv.has_errors is False

    cfg = PipelineConfig()
    cfg.crop.enabled = True
    cfg.crop.margin_mm = 2.0

    # crop
    data_c, labels_c, offset = crop_to_labels(
        vol.data, labels, vol.spacing_mm, cfg.crop.margin_mm
    )
    assert data_c.shape == labels_c.shape
    assert data_c.shape[0] < 32  # should have shrunk

    # window
    data_w = apply_window(data_c, cfg.window.level, cfg.window.width)
    assert data_w.dtype == np.uint8

    # meshes
    center = (np.array(data_w.shape) * np.array(vol.spacing_mm)) / 2.0
    label_map = {1: "liver", 2: "spleen"}
    meshes = generate_all(labels_c, label_map, vol.spacing_mm, center, max_faces=5000)
    assert "liver" in meshes
    assert "spleen" in meshes

    # write a minimal asset package and verify it
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "volume").mkdir()
        (root / "meshes").mkdir()

        data_w.tofile(root / "volume" / "volume.bin")
        meta = VolumeMetadata(
            shape=list(data_w.shape),
            spacing_mm=list(vol.spacing_mm),
            origin_mm=list(offset.astype(float)),
            orientation="RAS",
            intensity_range=[float(data_w.min()), float(data_w.max())],
        )
        meta.save(root / "volume" / "metadata.json")

        cleaned = {k: basic_cleanup(m) for k, m in meshes.items()}
        mesh_paths = export_glb(cleaned, root / "meshes")

        manifest = Manifest(
            pipeline_version=cfg.pipeline_version,
            subject_id="golden",
            volume={"bin": "volume/volume.bin", "metadata": "volume/metadata.json"},
            meshes=mesh_paths,
            labels={n: {"id": i} for i, n in label_map.items()},
        )
        manifest.save(root / "manifest.json")
        cfg.save(root / "pipeline_config.json")

        ok, report = verify_assets(root)
        assert ok is True, report
