"""
Simple deterministic threshold-based segmentation.

This is intentionally basic so the pipeline can run without a trained model.
It will be replaced or extended by model-based methods later.
"""

from typing import Dict, Any
import numpy as np
from .base import SegmentationMethod


class ThresholdSegmentation(SegmentationMethod):
    """
    Placeholder that expects pre-existing masks (e.g. TotalSegmentator)
    or applies very rough HU thresholds for demonstration.
    """

    def __init__(self, label_map: Dict[int, str] | None = None):
        self._label_map = label_map or {
            1: "liver",
            2: "spleen",
            3: "stomach",
            4: "kidney_right",
            5: "kidney_left",
            6: "aorta",
            7: "inferior_vena_cava",
            8: "spine",
        }

    def run(self, volume: np.ndarray, spacing_mm: tuple, meta: Dict[str, Any]) -> np.ndarray:
        # If the caller already supplied a label volume, just return it.
        if "existing_labels" in meta:
            return meta["existing_labels"]

        # Extremely crude fallback thresholds (for testing only).
        # Real use should supply existing_labels from TotalSegmentator or a model.
        labels = np.zeros(volume.shape, dtype=np.uint8)
        # soft tissue range example – not clinically meaningful
        labels[(volume > 30) & (volume < 70)] = 1
        return labels

    def label_map(self) -> Dict[int, str]:
        return self._label_map.copy()
