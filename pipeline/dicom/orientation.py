"""
ImageOrientationPatient handling and affine construction.
"""

from typing import Tuple, Optional, List, Any
import numpy as np
from models.report import Report


def parse_iop(ds) -> Optional[np.ndarray]:
    """Return 6-element ImageOrientationPatient as float array, or None."""
    iop = getattr(ds, "ImageOrientationPatient", None)
    if iop is None or len(iop) < 6:
        return None
    return np.array([float(x) for x in iop[:6]], dtype=np.float64)


def direction_cosine_matrix(iop: np.ndarray) -> np.ndarray:
    """
    Build a 3x3 direction matrix from ImageOrientationPatient.

    Row 0 = row direction, Row 1 = column direction,
    Row 2 = slice direction (cross product).
    """
    row = iop[:3]
    col = iop[3:6]
    slc = np.cross(row, col)
    # normalise
    row = row / (np.linalg.norm(row) + 1e-12)
    col = col / (np.linalg.norm(col) + 1e-12)
    slc = slc / (np.linalg.norm(slc) + 1e-12)
    return np.stack([row, col, slc], axis=0)


def is_approximately_axial(iop: np.ndarray, tol: float = 0.1) -> bool:
    """
    True when the slice normal is close to superior-inferior (±Z).
    """
    mat = direction_cosine_matrix(iop)
    normal = mat[2]
    return abs(abs(normal[2]) - 1.0) < tol


def validate_orientation(datasets: List[Any]) -> Report:
    report = Report()
    if not datasets:
        report.error("EMPTY", "no datasets")
        return report

    iops = [parse_iop(ds) for ds in datasets]
    if any(i is None for i in iops):
        report.error("IOP_MISSING", "ImageOrientationPatient missing on one or more slices")
        return report

    # all slices should share the same orientation
    first = iops[0]
    for i, iop in enumerate(iops[1:], 1):
        if not np.allclose(iop, first, atol=1e-3):
            report.error("IOP_INCONSISTENT", f"ImageOrientationPatient differs at slice {i}")
            return report

    if not is_approximately_axial(first):
        report.warning("NON_AXIAL", "acquisition is oblique or non-axial")
    else:
        report.info("AXIAL", "acquisition is approximately axial")

    return report
