"""
Marching-cubes mesh generation from a label volume.
"""

from typing import Dict, Optional
import numpy as np
from skimage import measure
import trimesh


def mesh_from_label(
    labels: np.ndarray,
    label_id: int,
    spacing_mm: tuple,
    center_mm: np.ndarray,
    max_faces: int = 40000,
) -> Optional[trimesh.Trimesh]:
    """
    Extract a surface mesh for a single label.

    Coordinates are converted into a centered frame suitable for Three.js:
    x = -(r - c_r), y = (s - c_s), z = (a - c_a)
    """
    binary = (labels == label_id).astype(np.float32)
    if binary.sum() == 0:
        return None

    verts, faces, normals, _ = measure.marching_cubes(
        binary, level=0.5, spacing=spacing_mm
    )

    # RAS → centered Three.js frame
    centered = np.empty_like(verts)
    centered[:, 0] = -(verts[:, 0] - center_mm[0])
    centered[:, 1] = verts[:, 2] - center_mm[2]
    centered[:, 2] = verts[:, 1] - center_mm[1]

    mesh = trimesh.Trimesh(vertices=centered, faces=faces, process=True)
    mesh.fix_normals()

    if len(mesh.faces) > max_faces:
        mesh = mesh.simplify_quadratic_decimation(max_faces)

    return mesh


def generate_all(
    labels: np.ndarray,
    label_map: Dict[int, str],
    spacing_mm: tuple,
    center_mm: np.ndarray,
    max_faces: int = 40000,
) -> Dict[str, trimesh.Trimesh]:
    """Generate meshes for every non-zero label present."""
    meshes = {}
    for lid, name in label_map.items():
        if lid == 0:
            continue
        m = mesh_from_label(labels, lid, spacing_mm, center_mm, max_faces)
        if m is not None:
            meshes[name] = m
    return meshes
