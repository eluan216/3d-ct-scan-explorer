"""Orientation and IOP tests."""

from types import SimpleNamespace
import numpy as np
from dicom.orientation import (
    parse_iop,
    direction_cosine_matrix,
    is_approximately_axial,
    validate_orientation,
)


def make_axial_ds():
    ds = SimpleNamespace()
    # standard axial: row = X, col = Y, normal ≈ Z
    ds.ImageOrientationPatient = [1, 0, 0, 0, 1, 0]
    return ds


def make_oblique_ds():
    ds = SimpleNamespace()
    # tilted
    ds.ImageOrientationPatient = [0.9, 0.1, 0, -0.1, 0.9, 0.1]
    return ds


def test_axial_detection():
    iop = np.array([1.0, 0, 0, 0, 1.0, 0])
    assert is_approximately_axial(iop) is True


def test_oblique_detection():
    iop = np.array([0.7, 0.7, 0, -0.7, 0.7, 0])
    assert is_approximately_axial(iop) is False


def test_validate_missing_iop():
    ds = SimpleNamespace()
    report = validate_orientation([ds])
    assert report.has_errors is True
    assert any(m.code == "IOP_MISSING" for m in report.errors)


def test_validate_inconsistent_iop():
    ds1 = make_axial_ds()
    ds2 = make_oblique_ds()
    report = validate_orientation([ds1, ds2])
    assert report.has_errors is True
    assert any(m.code == "IOP_INCONSISTENT" for m in report.errors)


def test_direction_matrix_orthonormal():
    iop = np.array([1.0, 0, 0, 0, 1.0, 0])
    mat = direction_cosine_matrix(iop)
    # columns should be roughly unit length
    norms = np.linalg.norm(mat, axis=1)
    assert np.allclose(norms, 1.0, atol=1e-6)
