"""Geometry edge cases: single-slice, large spacing variation, missing metadata."""

from types import SimpleNamespace
import numpy as np
from dicom.validate_series import validate_series
from dicom.orientation import validate_orientation


def make_ds(z=0.0, spacing=(1.0, 1.0), rows=8, cols=8, iop=None):
    ds = SimpleNamespace()
    ds.InstanceNumber = 1
    ds.ImagePositionPatient = [0.0, 0.0, float(z)]
    ds.PixelSpacing = list(spacing)
    ds.Rows = rows
    ds.Columns = cols
    ds.Modality = "CT"
    ds.pixel_array = np.zeros((rows, cols), dtype=np.int16)
    if iop is not None:
        ds.ImageOrientationPatient = iop
    return ds


def test_single_slice_series_no_spacing_error():
    # single slice cannot assess spacing consistency – should not error
    report = validate_series([make_ds()])
    # may warn about missing positions for spacing, but must not hard-error on spacing
    spacing_errors = [m for m in report.errors if "SPACING" in m.code]
    assert len(spacing_errors) == 0


def test_missing_orientation_is_error():
    ds = make_ds()
    # no IOP
    report = validate_orientation([ds])
    assert report.has_errors is True


def test_large_spacing_variation_is_warning():
    slices = [
        make_ds(0),
        make_ds(1),
        make_ds(2),
        make_ds(20),  # big jump
    ]
    # assign increasing InstanceNumbers
    for i, ds in enumerate(slices):
        ds.InstanceNumber = i + 1
    report = validate_series(slices)
    assert report.has_errors is False or not any("SPACING" in m.code for m in report.errors)
    # should at least produce a warning or info about spacing
    assert len(report.messages) > 0
