"""
Optional resampling to a target voxel spacing.
"""

import numpy as np
from typing import Tuple, Optional
from scipy.ndimage import zoom


def resample_volume(
    volume: np.ndarray,
    current_spacing: Tuple[float, float, float],
    target_spacing: Tuple[float, float, float],
    order: int = 1,
) -> Tuple[np.ndarray, Tuple[float, float, float]]:
    """
    Resample a 3-D volume to a new spacing using scipy.ndimage.zoom.

    order=1 is linear (suitable for CT intensities).
    For label maps use order=0 (nearest neighbour) separately.
    """
    if target_spacing is None:
        return volume, current_spacing

    factors = [c / t for c, t in zip(current_spacing, target_spacing)]
    resampled = zoom(volume, factors, order=order)
    return resampled, target_spacing


def resample_labels(
    labels: np.ndarray,
    current_spacing: Tuple[float, float, float],
    target_spacing: Tuple[float, float, float],
) -> np.ndarray:
    """Nearest-neighbour resampling for discrete label maps."""
    resampled, _ = resample_volume(labels.astype(np.float32), current_spacing, target_spacing, order=0)
    return resampled.astype(labels.dtype)
