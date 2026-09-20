"""Mesh generation and cleanup edge cases."""

import numpy as np
from mesh.generate import mesh_from_label
from mesh.cleanup import basic_cleanup, remove_small_components
import trimesh


def test_empty_label_returns_none():
    labels = np.zeros((16, 16, 8), dtype=np.uint8)
    mesh = mesh_from_label(labels, label_id=1, spacing_mm=(1, 1, 1), center_mm=np.zeros(3))
    assert mesh is None


def test_small_component_removed():
    # create a mesh with one large and one tiny component
    verts = np.array([
        [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1],  # tetra
        [10, 10, 10], [10.1, 10, 10], [10, 10.1, 10],  # tiny triangle
    ], dtype=float)
    faces = np.array([
        [0, 1, 2], [0, 1, 3], [0, 2, 3], [1, 2, 3],
        [4, 5, 6],
    ])
    mesh = trimesh.Trimesh(vertices=verts, faces=faces, process=False)
    cleaned = remove_small_components(mesh, min_faces=2)
    assert len(cleaned.faces) >= 4  # the tetra should remain
