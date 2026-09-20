"""
Detailed validation of a DICOM series with ERROR / WARNING / INFO severity.
"""

from typing import List, Any
import numpy as np
from models.report import Report, Severity


def validate_series(datasets: List[Any]) -> Report:
    report = Report()

    if not datasets:
        report.error("EMPTY_SERIES", "no datasets provided")
        return report

    # --- InstanceNumber continuity (WARNING if gaps) ---
    numbers = []
    for ds in datasets:
        n = getattr(ds, "InstanceNumber", None)
        if n is not None:
            try:
                numbers.append(int(n))
            except (TypeError, ValueError):
                pass
    if numbers:
        numbers_sorted = sorted(set(numbers))
        expected = list(range(numbers_sorted[0], numbers_sorted[-1] + 1))
        missing = sorted(set(expected) - set(numbers_sorted))
        if missing:
            report.warning(
                "NON_CONTIGUOUS_INSTANCE",
                f"InstanceNumber gaps: {missing[:8]}{'…' if len(missing) > 8 else ''}",
            )
        else:
            report.info("INSTANCE_OK", "InstanceNumbers contiguous")
    else:
        report.info("INSTANCE_ABSENT", "no InstanceNumber attributes present")

    # --- Duplicate positions (ERROR) ---
    positions = []
    for ds in datasets:
        ipp = getattr(ds, "ImagePositionPatient", None)
        if ipp is not None and len(ipp) >= 3:
            positions.append(tuple(float(x) for x in ipp[:3]))
    if positions:
        if len(set(positions)) < len(positions):
            report.error(
                "DUPLICATE_POSITION",
                f"duplicate ImagePositionPatient values ({len(positions) - len(set(positions))} duplicates)",
            )
        else:
            report.info("POSITION_UNIQUE", "no duplicate positions")
    else:
        report.warning("POSITION_MISSING", "ImagePositionPatient not available")

    # --- Slice spacing consistency (WARNING if variation high) ---
    if len(positions) >= 3:
        pts = [np.array(p) for p in positions]
        dists = [float(np.linalg.norm(pts[i+1] - pts[i])) for i in range(len(pts)-1)]
        median = float(np.median(dists))
        if median > 0:
            outliers = [d for d in dists if abs(d - median) > 0.25 * median]
            if outliers:
                report.warning(
                    "SPACING_VARIATION",
                    f"slice spacing variation (median={median:.3f} mm, outliers={len(outliers)})",
                )
            else:
                report.info("SPACING_OK", f"slice spacing consistent (≈{median:.3f} mm)")

    # --- Required geometry for volume construction (ERROR if missing) ---
    first = datasets[0]
    if getattr(first, "PixelSpacing", None) is None:
        report.error("PIXEL_SPACING_MISSING", "PixelSpacing required to build volume")
    if getattr(first, "Rows", None) is None or getattr(first, "Columns", None) is None:
        report.error("ROWS_COLS_MISSING", "Rows/Columns required")

    return report
