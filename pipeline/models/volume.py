"""
Canonical volume representation used by the rest of the pipeline.

Both DICOM and NIfTI loaders must produce this object so that
preprocessing, segmentation and mesh stages stay input-agnostic.
"""

from dataclasses import dataclass, field
from typing import Tuple, Optional, Dict, Any
import numpy as np


@dataclass
class CanonicalVolume:
    """
    A 3-D CT volume in RAS+ orientation with known spacing and origin.

    intensity values are expected to be Hounsfield Units when the
    source provided rescale slope/intercept.
    """
    data: np.ndarray                          # shape (I, J, K)
    spacing_mm: Tuple[float, float, float]    # (si, sj, sk)
    origin_mm: Tuple[float, float, float]     # world origin of voxel (0,0,0)
    direction: Tuple[float, ...] = (1, 0, 0, 0, 1, 0, 0, 0, 1)  # row-major 3x3
    orientation: str = "RAS"
    modality: str = "CT"
    source: str = "unknown"                   # "dicom" | "nifti"
    meta: Dict[str, Any] = field(default_factory=dict)

    @property
    def shape(self) -> Tuple[int, int, int]:
        return tuple(self.data.shape)

    def is_finite(self) -> bool:
        return bool(np.isfinite(self.data).all())

    def intensity_range(self) -> Tuple[float, float]:
        return float(self.data.min()), float(self.data.max())
