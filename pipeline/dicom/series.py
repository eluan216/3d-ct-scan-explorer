"""
DICOM series utilities (placeholder for full DICOM support).
"""

from pathlib import Path
from typing import List, Dict, Any


def group_by_series(dicom_files: List[Path]) -> Dict[str, List[Path]]:
    """
    Group DICOM files by SeriesInstanceUID.
    Full implementation requires pydicom.
    """
    # Placeholder – will be implemented with pydicom
    return {}


def sort_slices(files: List[Path]) -> List[Path]:
    """
    Sort slices by ImagePositionPatient along the slice direction.
    """
    return files
