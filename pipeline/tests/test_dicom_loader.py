"""
Tests for DICOM loading and validation helpers.

These tests use synthetic data so they can run without real DICOM files.
"""

import numpy as np
from types import SimpleNamespace


def make_fake_ds(instance_number, position_z, rows=16, cols=16):
    ds = SimpleNamespace()
    ds.InstanceNumber = instance_number
    ds.ImagePositionPatient = [0.0, 0.0, float(position_z)]
    ds.PixelSpacing = [1.0, 1.0]
    ds.SliceThickness = 1.0
    ds.RescaleSlope = 1.0
    ds.RescaleIntercept = -1024.0
    ds.Rows = rows
    ds.Columns = cols
    ds.Modality = "CT"
    ds.SeriesInstanceUID = "1.2.3"
    ds.pixel_array = np.zeros((rows, cols), dtype=np.int16)
    return ds


def test_sort_by_position():
    from dicom.loader import sort_by_position
    slices = [
        make_fake_ds(3, 20),
        make_fake_ds(1, 0),
        make_fake_ds(2, 10),
    ]
    sorted_slices = sort_by_position(slices)
    zs = [ds.ImagePositionPatient[2] for ds in sorted_slices]
    assert zs == [0.0, 10.0, 20.0]


def test_duplicate_position_detection():
    from dicom.validate_series import check_duplicate_positions
    slices = [
        make_fake_ds(1, 0),
        make_fake_ds(2, 0),   # duplicate z
        make_fake_ds(3, 10),
    ]
    ok, msg = check_duplicate_positions(slices)
    assert ok is False
    assert "duplicate" in msg.lower()


def test_spacing_consistency():
    from dicom.validate_series import check_slice_spacing_consistency
    # consistent 5 mm spacing
    slices = [make_fake_ds(i, i * 5) for i in range(5)]
    ok, msg = check_slice_spacing_consistency(slices)
    assert ok is True

    # one large jump
    slices[3] = make_fake_ds(4, 100)
    ok, msg = check_slice_spacing_consistency(slices)
    assert ok is False
