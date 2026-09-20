"""
Orthogonal slice extraction helpers.

The actual PNG/JPEG writing can be added later; for now we focus on
producing correctly oriented index ranges and metadata that the
frontend (or a later stage) can use.
"""

from typing import Dict, Any, Tuple
import numpy as np


def slice_ranges(shape: Tuple[int, int, int]) -> Dict[str, range]:
    """Return index ranges for axial, coronal and sagittal."""
    ni, nj, nk = shape
    return {
        "axial": range(nk),      # fixed k
        "coronal": range(nj),    # fixed j
        "sagittal": range(ni),   # fixed i
    }


def extract_slice(
    volume: np.ndarray,
    plane: str,
    index: int,
) -> np.ndarray:
    """
    Return a 2-D slice.

    Orientation conventions (radiology style):
    - axial    : viewed from feet → patient left on image right
    - coronal  : facing the patient
    - sagittal : viewed from patient left
    """
    if plane == "axial":
        return volume[:, :, index]
    if plane == "coronal":
        return volume[:, index, :]
    if plane == "sagittal":
        return volume[index, :, :]
    raise ValueError(f"unknown plane: {plane}")


def slice_metadata(
    shape: Tuple[int, int, int],
    spacing_mm: Tuple[float, float, float],
    window_level: float,
    window_width: float,
) -> Dict[str, Any]:
    return {
        "shape": list(shape),
        "spacing_mm": list(spacing_mm),
        "window": {"level": window_level, "width": window_width},
        "planes": ["axial", "coronal", "sagittal"],
    }
