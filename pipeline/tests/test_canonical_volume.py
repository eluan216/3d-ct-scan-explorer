"""Tests for the CanonicalVolume model."""

import numpy as np
from models.volume import CanonicalVolume


def test_intensity_range():
    data = np.array([[[-100, 0], [50, 200]]], dtype=np.float32)
    vol = CanonicalVolume(
        data=data,
        spacing_mm=(1.0, 1.0, 1.0),
        origin_mm=(0.0, 0.0, 0.0),
    )
    lo, hi = vol.intensity_range()
    assert lo == -100.0
    assert hi == 200.0


def test_is_finite():
    data = np.ones((4, 4, 4), dtype=np.float32)
    vol = CanonicalVolume(data=data, spacing_mm=(1, 1, 1), origin_mm=(0, 0, 0))
    assert vol.is_finite() is True

    data[0, 0, 0] = np.nan
    vol2 = CanonicalVolume(data=data, spacing_mm=(1, 1, 1), origin_mm=(0, 0, 0))
    assert vol2.is_finite() is False
