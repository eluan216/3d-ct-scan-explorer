"""Segmentation interface and empty-mask behaviour."""

import numpy as np
from segmentation.threshold import ThresholdSegmentation


def test_empty_existing_labels():
    seg = ThresholdSegmentation()
    volume = np.zeros((16, 16, 8), dtype=np.float32)
    labels = np.zeros_like(volume, dtype=np.uint8)
    out = seg.run(volume, (1.0, 1.0, 1.0), {"existing_labels": labels})
    assert out.shape == volume.shape
    assert out.max() == 0


def test_label_map_contains_expected_keys():
    seg = ThresholdSegmentation()
    lm = seg.label_map()
    assert 1 in lm and lm[1] == "liver"
    assert 8 in lm and lm[8] == "spine"
