"""
Final asset verification against the expected contract.
"""

from pathlib import Path
from typing import Tuple
import json


def verify_assets(assets_dir: Path) -> Tuple[bool, str]:
    assets_dir = Path(assets_dir)
    lines = []
    ok = True

    required = [
        "manifest.json",
        "volume/volume.bin",
        "volume/metadata.json",
        "pipeline_config.json",
    ]

    for rel in required:
        p = assets_dir / rel
        if p.exists():
            lines.append(f"OK      {rel}")
        else:
            lines.append(f"MISSING {rel}")
            ok = False

    # manifest content checks
    manifest_path = assets_dir / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            for key in ("pipeline_version", "subject_id", "volume", "meshes"):
                if key not in manifest:
                    lines.append(f"FAIL    manifest missing key: {key}")
                    ok = False
                else:
                    lines.append(f"OK      manifest.{key}")

            # check that referenced mesh files exist
            for name, relpath in manifest.get("meshes", {}).items():
                mp = assets_dir / relpath
                if mp.exists():
                    lines.append(f"OK      mesh {name}")
                else:
                    lines.append(f"MISSING mesh {name} → {relpath}")
                    ok = False

        except Exception as e:
            lines.append(f"FAIL    reading manifest: {e}")
            ok = False

    # volume metadata checks
    meta_path = assets_dir / "volume" / "metadata.json"
    if meta_path.exists():
        try:
            meta = json.loads(meta_path.read_text())
            for key in ("shape", "spacing_mm", "orientation"):
                if key not in meta:
                    lines.append(f"FAIL    volume metadata missing: {key}")
                    ok = False
        except Exception as e:
            lines.append(f"FAIL    reading volume metadata: {e}")
            ok = False

    report = "\n".join(lines)
    return ok, report
