"""
CT window/level application.
"""

import numpy as np
from typing import Tuple


def apply_window(
    volume: np.ndarray,
    level: float = 50.0,
    width: float = 400.0,
    output_dtype=np.uint8,
) -> np.ndarray:
    """
    Apply a standard soft-tissue window and scale to the target dtype range.
    """
    lo = level - width / 2.0
    hi = level + width / 2.0
    clipped = np.clip(volume.astype(np.float32), lo, hi)

    if output_dtype == np.uint8:
        scaled = (clipped - lo) / (hi - lo) * 255.0
        return scaled.astype(np.uint8)

    # keep float for further processing if requested
    return clipped


def intensity_range(volume: np.ndarray) -> Tuple[float, float]:
    return float(np.min(volume)), float(np.max(volume))
