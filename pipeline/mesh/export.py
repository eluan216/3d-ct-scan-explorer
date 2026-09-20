"""
Mesh export helpers.
"""

from pathlib import Path
from typing import Dict
import trimesh


def export_glb(meshes: Dict[str, trimesh.Trimesh], out_dir: Path) -> Dict[str, str]:
    """
    Write each mesh as a .glb file.

    Returns a mapping {label_name: relative_path}.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    paths = {}
    for name, mesh in meshes.items():
        path = out_dir / f"{name}.glb"
        mesh.export(path)
        paths[name] = str(path.relative_to(out_dir.parent))
    return paths
