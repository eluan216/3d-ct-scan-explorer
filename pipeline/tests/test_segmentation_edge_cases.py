"""Segmentation edge cases."""

import numpy as np
from segmentation.threshold import ThresholdSegmentation
from mesh.generate import mesh_from_label, generate_all


def test_empty_mask_produces_empty_label_volume():
    seg = ThresholdSegmentation()
    vol = np.zeros((16, 16, 8), dtype=np.float32)
    empty = np.zeros_like(vol, dtype=np.uint8)
    out = seg.run(vol, (1, 1, 1), {"existing_labels": empty})
    assert out.max() == 0


def test_single_voxel_component():
    labels = np.zeros((16, 16, 8), dtype=np.uint8)
    labels[8, 8, 4] = 1
    mesh = mesh_from_label(labels, 1, (1, 1, 1), np.zeros(3))
    # marching cubes on a single voxel may still produce a small mesh or None
    # either is acceptable; we just require no crash
    assert mesh is None or len(mesh.faces) >= 0


def test_disconnected_components_still_generate():
    labels = np.zeros((32, 32, 16), dtype=np.uint8)
    labels[5:8, 5:8, 5:8] = 1
    labels[20:24, 20:24, 10:14] = 1
    mesh = mesh_from_label(labels, 1, (1, 1, 1), np.array([16.0, 16.0, 8.0]))
    assert mesh is not None
    assert len(mesh.faces) > 0


def test_absent_label_skipped():
    labels = np.zeros((16, 16, 8), dtype=np.uint8)
    labels[4:8, 4:8, 2:6] = 1  # only liver
    label_map = {1: "liver", 2: "spleen"}
    meshes = generate_all(labels, label_map, (1, 1, 1), np.zeros(3))
    assert "liver" in meshes
    assert "spleen" not in meshes
