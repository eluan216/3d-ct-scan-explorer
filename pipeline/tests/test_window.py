"""Basic tests for windowing."""

import numpy as np
from preprocessing.window import apply_window


def test_window_output_range():
    vol = np.array([-1000, 0, 50, 100, 1000], dtype=np.float32)
    out = apply_window(vol, level=50, width=400)
    assert out.dtype == np.uint8
    assert out.min() >= 0
    assert out.max() <= 255
