"""
Invariant checks for CanonicalVolume and final assets.
"""

from typing import Tuple
import numpy as np
from models.volume import CanonicalVolume
from models.report import Report


def check_canonical_invariants(vol: CanonicalVolume) -> Report:
    report = Report()

    if vol.data.ndim != 3:
        report.error("NDIM", f"expected 3-D volume, got ndim={vol.data.ndim}")
    else:
        report.info("NDIM", "volume is 3-D")

    if vol.data.shape != vol.shape:
        report.error("SHAPE_MISMATCH", "data.shape does not match declared shape")

    if len(vol.spacing_mm) != 3 or any(s <= 0 for s in vol.spacing_mm):
        report.error("SPACING", f"invalid spacing: {vol.spacing_mm}")
    else:
        report.info("SPACING", f"spacing={vol.spacing_mm}")

    if not np.isfinite(vol.data).all():
        report.error("NAN_INF", "volume contains NaN or Inf")
    else:
        report.info("FINITE", "volume is finite")

    if vol.orientation not in {"RAS", "LPS", "LAI", "RPI", "unknown"}:
        # allow a small set; expand later if needed
        report.warning("ORIENTATION", f"unrecognised orientation code: {vol.orientation}")
    else:
        report.info("ORIENTATION", f"orientation={vol.orientation}")

    return report
