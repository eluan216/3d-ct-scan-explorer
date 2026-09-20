"""
Abstract segmentation contract.

Any concrete segmentation method (threshold, model-based, etc.)
must implement this interface so the rest of the pipeline stays
independent of how labels are produced.
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, Any
import numpy as np


class SegmentationMethod(ABC):
    """Base class for all segmentation backends."""

    @abstractmethod
    def run(self, volume: np.ndarray, spacing_mm: tuple, meta: Dict[str, Any]) -> np.ndarray:
        """
        Produce a label volume.

        Parameters
        ----------
        volume : CT volume (already oriented and optionally resampled)
        spacing_mm : voxel spacing
        meta : free-form metadata dictionary

        Returns
        -------
        labels : integer label volume (0 = background)
        """
        pass

    @abstractmethod
    def label_map(self) -> Dict[int, str]:
        """Return {label_id: anatomical_name}."""
        pass
