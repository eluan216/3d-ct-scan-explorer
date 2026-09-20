"""Tests for the final asset verification."""

from pathlib import Path
import json
import tempfile
from validation.assets import verify_assets


def test_missing_manifest_fails():
    with tempfile.TemporaryDirectory() as tmp:
        ok, report = verify_assets(Path(tmp))
        assert ok is False
        assert "MISSING" in report


def test_complete_minimal_assets_pass():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        (root / "volume").mkdir()
        (root / "volume" / "volume.bin").write_bytes(b"\x00" * 8)
        (root / "volume" / "metadata.json").write_text(json.dumps({
            "shape": [2, 2, 2],
            "spacing_mm": [1, 1, 1],
            "orientation": "RAS",
        }))
        (root / "manifest.json").write_text(json.dumps({
            "pipeline_version": "0.1.0",
            "subject_id": "test",
            "volume": {"bin": "volume/volume.bin", "metadata": "volume/metadata.json"},
            "meshes": {},
        }))
        (root / "pipeline_config.json").write_text("{}")

        ok, report = verify_assets(root)
        assert ok is True
