"""
Mesh integrity checks.
"""

from typing import Tuple
import trimesh


def check_mesh(mesh: trimesh.Trimesh) -> Tuple[bool, str]:
    if len(mesh.vertices) == 0 or len(mesh.faces) == 0:
        return False, "empty mesh"
    if not mesh.is_winding_consistent:
        return False, "inconsistent winding"
    return True, f"mesh ok ({len(mesh.vertices)} verts, {len(mesh.faces)} faces)"
