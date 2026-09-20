"""
Mesh cleanup utilities.
"""

import trimesh
import numpy as np


def remove_small_components(mesh: trimesh.Trimesh, min_faces: int = 50) -> trimesh.Trimesh:
    """Keep only connected components that have enough faces."""
    components = mesh.split(only_watertight=False)
    kept = [c for c in components if len(c.faces) >= min_faces]
    if not kept:
        return mesh
    return trimesh.util.concatenate(kept)


def basic_cleanup(mesh: trimesh.Trimesh) -> trimesh.Trimesh:
    """Remove degenerate faces and fix normals."""
    mesh.remove_degenerate_faces()
    mesh.remove_duplicate_faces()
    mesh.remove_unreferenced_vertices()
    mesh.fix_normals()
    return mesh
