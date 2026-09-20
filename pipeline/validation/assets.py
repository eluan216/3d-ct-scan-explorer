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
        assets_dir / "manifest.json",
        assets_dir / "volume" / "volume.bin",
        assets_dir / "volume" / "metadata.json",
    ]

    for p in required:
        if p.exists():
            lines.append(f"OK  {p.relative_to(assets_dir)}")
        else:
            lines.append(f"MISSING  {p.relative_to(assets_dir)}")
            ok = False

    manifest_path = assets_dir / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            lines.append(f"Manifest keys: {list(manifest.keys())}")
        except Exception as e:
            lines.append(f"FAIL reading manifest: {e}")
            ok = False

    report = "\n".join(lines)
    return ok, report
