"""
Volume-level quality checks.
"""

from typing import Tuple, List
import numpy as np


def check_finite(volume: np.ndarray) -> Tuple[bool, str]:
    if not np.isfinite(volume).all():
        return False, "Volume contains NaN or Inf"
    return True, "Volume is finite"


def check_non_empty(volume: np.ndarray) -> Tuple[bool, str]:
    if volume.size == 0 or volume.max() == volume.min():
        return False, "Volume is empty or constant"
    return True, "Volume has variation"


def check_spacing(spacing: tuple) -> Tuple[bool, str]:
    if any(s <= 0 for s in spacing):
        return False, f"Invalid spacing: {spacing}"
    return True, f"Spacing OK: {spacing}"
