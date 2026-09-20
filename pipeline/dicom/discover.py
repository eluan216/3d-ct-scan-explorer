"""
Discover DICOM series or NIfTI subjects under a root directory.
"""

from pathlib import Path
from typing import List, Dict, Any
import json


def discover(root: Path) -> List[Dict[str, Any]]:
    """
    Return a list of candidate studies/subjects found under root.

    Currently supports:
    - Directories containing ct.nii.gz + segmentations/ (TotalSegmentator style)
    - Future: full DICOM series discovery
    """
    root = Path(root)
    results = []

    if not root.exists():
        return results

    for item in sorted(root.iterdir()):
        if not item.is_dir():
            continue

        # NIfTI / TotalSegmentator layout
        ct = item / "ct.nii.gz"
        seg = item / "segmentations"
        if ct.exists() and seg.is_dir():
            results.append({
                "type": "nifti_subject",
                "path": str(item),
                "has_ct": True,
                "has_segmentations": True,
                "segmentation_count": len(list(seg.glob("*.nii.gz"))),
            })
            continue

        # Placeholder for DICOM series detection
        # (will look for .dcm files and group by SeriesInstanceUID)

    return results
