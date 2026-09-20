"""Reversed slice order must still produce correct spatial volume."""

from types import SimpleNamespace
import numpy as np
from dicom.loader import sort_by_position


def make_ds(z, value):
    ds = SimpleNamespace()
    ds.ImagePositionPatient = [0.0, 0.0, float(z)]
    ds.InstanceNumber = int(z)
    ds.PixelSpacing = [1.0, 1.0]
    ds.Rows = 4
    ds.Columns = 4
    ds.RescaleSlope = 1.0
    ds.RescaleIntercept = 0.0
    ds.pixel_array = np.full((4, 4), value, dtype=np.int16)
    return ds


def test_sort_ignores_list_order():
    # intentionally reversed list order
    slices = [
        make_ds(30, 30),
        make_ds(10, 10),
        make_ds(20, 20),
        make_ds(0, 0),
    ]
    ordered = sort_by_position(slices)
    zs = [ds.ImagePositionPatient[2] for ds in ordered]
    assert zs == [0.0, 10.0, 20.0, 30.0]


def test_reversed_input_same_order_as_forward():
    forward = [make_ds(z, z) for z in [0, 5, 10, 15]]
    reversed_list = list(reversed(forward))
    assert [ds.ImagePositionPatient[2] for ds in sort_by_position(forward)] == \
           [ds.ImagePositionPatient[2] for ds in sort_by_position(reversed_list)]
