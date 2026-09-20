"""Asset package and manifest invariant tests."""

from pathlib import Path
import json
import tempfile
from validation.assets import verify_assets


def _write_minimal_assets(root: Path, with_mesh: bool = False):
    (root / "volume").mkdir(parents=True, exist_ok=True)
    (root / "volume" / "volume.bin").write_bytes(b"\x00" * 16)
    (root / "volume" / "metadata.json").write_text(json.dumps({
        "shape": [2, 2, 4],
        "spacing_mm": [1.0, 1.0, 1.5],
        "orientation": "RAS",
        "origin_mm": [0, 0, 0],
        "intensity_range": [0, 255],
    }))
    meshes = {}
    if with_mesh:
        (root / "meshes").mkdir(exist_ok=True)
        mesh_path = root / "meshes" / "liver.glb"
        mesh_path.write_bytes(b"glTF")  # not a real glb, just presence check
        meshes["liver"] = "meshes/liver.glb"

    (root / "manifest.json").write_text(json.dumps({
        "pipeline_version": "0.1.0",
        "subject_id": "test",
        "volume": {
            "bin": "volume/volume.bin",
            "metadata": "volume/metadata.json",
        },
        "meshes": meshes,
        "labels": {"liver": {"id": 1}} if with_mesh else {},
    }))
    (root / "pipeline_config.json").write_text("{}")


def test_complete_assets_pass():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_minimal_assets(root, with_mesh=True)
        ok, report = verify_assets(root)
        assert ok is True


def test_missing_volume_bin_fails():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_minimal_assets(root)
        (root / "volume" / "volume.bin").unlink()
        ok, report = verify_assets(root)
        assert ok is False
        assert "MISSING" in report


def test_manifest_missing_key_fails():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _write_minimal_assets(root)
        # corrupt manifest
        (root / "manifest.json").write_text(json.dumps({"pipeline_version": "0.1.0"}))
        ok, report = verify_assets(root)
        assert ok is False
