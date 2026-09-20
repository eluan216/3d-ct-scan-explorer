"""
Detailed validation of a DICOM series before conversion to volume.
"""

from typing import List, Tuple, Any
import numpy as np


def check_missing_instance_numbers(datasets: List[Any]) -> Tuple[bool, str]:
    numbers = []
    for ds in datasets:
        n = getattr(ds, "InstanceNumber", None)
        if n is not None:
            numbers.append(int(n))
    if not numbers:
        return True, "no InstanceNumber attributes (skipped)"
    numbers = sorted(set(numbers))
    expected = list(range(numbers[0], numbers[-1] + 1))
    missing = sorted(set(expected) - set(numbers))
    if missing:
        return False, f"missing InstanceNumbers: {missing[:10]}{'…' if len(missing) > 10 else ''}"
    return True, "InstanceNumbers contiguous"


def check_duplicate_positions(datasets: List[Any]) -> Tuple[bool, str]:
    positions = []
    for ds in datasets:
        ipp = getattr(ds, "ImagePositionPatient", None)
        if ipp is not None:
            positions.append(tuple(float(x) for x in ipp))
    if len(positions) < 2:
        return True, "insufficient position data"
    unique = set(positions)
    if len(unique) < len(positions):
        return False, f"duplicate ImagePositionPatient values detected ({len(positions) - len(unique)} duplicates)"
    return True, "no duplicate positions"


def check_slice_spacing_consistency(datasets: List[Any], tol: float = 0.2) -> Tuple[bool, str]:
    positions = []
    for ds in datasets:
        ipp = getattr(ds, "ImagePositionPatient", None)
        if ipp is not None:
            positions.append(np.array([float(x) for x in ipp]))
    if len(positions) < 3:
        return True, "not enough slices to assess spacing"

    dists = [np.linalg.norm(positions[i+1] - positions[i]) for i in range(len(positions)-1)]
    median = float(np.median(dists))
    outliers = [d for d in dists if abs(d - median) > tol * median]
    if outliers:
        return False, f"inconsistent slice spacing (median={median:.3f}, outliers={len(outliers)})"
    return True, f"slice spacing consistent (≈{median:.3f} mm)"


def validate_series(datasets: List[Any]) -> Tuple[bool, List[str]]:
    messages = []
    ok = True

    checks = [
        check_missing_instance_numbers,
        check_duplicate_positions,
        check_slice_spacing_consistency,
    ]
    for fn in checks:
        passed, msg = fn(datasets)
        messages.append(("OK  " if passed else "FAIL") + "  " + msg)
        if not passed:
            ok = False

    return ok, messages
