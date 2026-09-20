"""
Tests for DICOM series validation with severity levels.
"""

from types import SimpleNamespace
import numpy as np
from dicom.validate_series import validate_series


def make_ds(instance, z, rows=8, cols=8):
    ds = SimpleNamespace()
    ds.InstanceNumber = instance
    ds.ImagePositionPatient = [0.0, 0.0, float(z)]
    ds.PixelSpacing = [1.0, 1.0]
    ds.Rows = rows
    ds.Columns = cols
    ds.Modality = "CT"
    ds.pixel_array = np.zeros((rows, cols), dtype=np.int16)
    return ds


def test_clean_series_has_no_errors():
    slices = [make_ds(i, i * 2.0) for i in range(5)]
    report = validate_series(slices)
    assert report.has_errors is False


def test_duplicate_position_is_error():
    slices = [
        make_ds(1, 0.0),
        make_ds(2, 0.0),  # duplicate
        make_ds(3, 2.0),
    ]
    report = validate_series(slices)
    assert report.has_errors is True
    assert any(m.code == "DUPLICATE_POSITION" for m in report.errors)


def test_missing_pixel_spacing_is_error():
    ds = make_ds(1, 0.0)
    del ds.PixelSpacing
    report = validate_series([ds])
    assert report.has_errors is True
    assert any(m.code == "PIXEL_SPACING_MISSING" for m in report.errors)


def test_non_contiguous_instance_is_warning():
    slices = [make_ds(1, 0.0), make_ds(3, 2.0), make_ds(4, 4.0)]  # missing 2
    report = validate_series(slices)
    assert report.has_errors is False
    assert any(m.code == "NON_CONTIGUOUS_INSTANCE" for m in report.warnings)
