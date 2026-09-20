"""Tests for mesh cleanup helpers."""

import numpy as np
import trimesh
from mesh.cleanup import basic_cleanup, remove_small_components


def test_basic_cleanup_does_not_crash():
    # simple tetrahedron
    verts = np.array([
        [0, 0, 0],
        [1, 0, 0],
        [0, 1, 0],
        [0, 0, 1],
    ], dtype=float)
    faces = np.array([
        [0, 1, 2],
        [0, 1, 3],
        [0, 2, 3],
        [1, 2, 3],
    ])
    mesh = trimesh.Trimesh(vertices=verts, faces=faces)
    cleaned = basic_cleanup(mesh)
    assert len(cleaned.faces) > 0
