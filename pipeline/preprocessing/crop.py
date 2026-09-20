"""
Cropping around a label mask with configurable margin.
"""

import numpy as np
from typing import Tuple


def crop_to_labels(
    volume: np.ndarray,
    labels: np.ndarray,
    spacing_mm: Tuple[float, float, float],
    margin_mm: float = 20.0,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Crop volume and labels to the bounding box of non-zero labels
    plus a margin expressed in millimetres.

    Returns:
        cropped_volume, cropped_labels, offset (ijk of the crop origin)
    """
    coords = np.argwhere(labels > 0)
    if len(coords) == 0:
        raise ValueError("no non-zero labels found for cropping")

    mins = coords.min(axis=0)
    maxs = coords.max(axis=0) + 1

    margin_vox = [int(np.ceil(margin_mm / s)) for s in spacing_mm]
    mins = np.maximum(mins - margin_vox, 0)
    maxs = np.minimum(maxs + margin_vox, volume.shape)

    slices = tuple(slice(int(a), int(b)) for a, b in zip(mins, maxs))
    return volume[slices].copy(), labels[slices].copy(), mins.astype(int)
