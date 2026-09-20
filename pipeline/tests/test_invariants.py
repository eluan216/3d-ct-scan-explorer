"""Invariant checks on CanonicalVolume."""

import numpy as np
from models.volume import CanonicalVolume
from validation.invariants import check_canonical_invariants


def test_valid_volume_passes():
    data = np.random.randn(16, 16, 8).astype(np.float32)
    vol = CanonicalVolume(
        data=data,
        spacing_mm=(1.0, 1.0, 2.0),
        origin_mm=(0.0, 0.0, 0.0),
        orientation="RAS",
    )
    report = check_canonical_invariants(vol)
    assert report.has_errors is False


def test_nan_is_error():
    data = np.ones((8, 8, 4), dtype=np.float32)
    data[0, 0, 0] = np.nan
    vol = CanonicalVolume(
        data=data,
        spacing_mm=(1.0, 1.0, 1.0),
        origin_mm=(0.0, 0.0, 0.0),
    )
    report = check_canonical_invariants(vol)
    assert report.has_errors is True
    assert any(m.code == "NAN_INF" for m in report.errors)


def test_bad_spacing_is_error():
    data = np.ones((8, 8, 4), dtype=np.float32)
    vol = CanonicalVolume(
        data=data,
        spacing_mm=(1.0, -1.0, 1.0),
        origin_mm=(0.0, 0.0, 0.0),
    )
    report = check_canonical_invariants(vol)
    assert report.has_errors is True
