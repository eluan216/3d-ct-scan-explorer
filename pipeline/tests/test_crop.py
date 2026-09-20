"""Basic tests for cropping."""

import numpy as np
from preprocessing.crop import crop_to_labels


def test_crop_produces_smaller_volume():
    vol = np.zeros((50, 50, 50), dtype=np.float32)
    labels = np.zeros((50, 50, 50), dtype=np.uint8)
    labels[20:30, 20:30, 20:30] = 1

    cropped_vol, cropped_lab, offset = crop_to_labels(
        vol, labels, spacing_mm=(1.0, 1.0, 1.0), margin_mm=2.0
    )
    assert cropped_vol.shape[0] < 50
    assert cropped_lab.shape == cropped_vol.shape
