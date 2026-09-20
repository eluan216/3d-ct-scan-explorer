"""
Discover DICOM series or NIfTI subjects under a root directory.
"""

from pathlib import Path
from typing import List, Dict, Any


def discover(root: Path) -> List[Dict[str, Any]]:
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
        if ct.exists():
            results.append({
                "type": "nifti_subject",
                "path": str(item),
                "has_ct": True,
                "has_segmentations": seg.is_dir(),
            })
            continue

        # DICOM heuristic: look for .dcm or files that pydicom can read
        dcm_files = list(item.glob("*.dcm")) + list(item.glob("*.DCM"))
        if dcm_files:
            results.append({
                "type": "dicom_directory",
                "path": str(item),
                "approx_file_count": len(dcm_files),
            })
            continue

        # also accept directories that contain many files without extension
        # (common in some DICOM exports)
        files = [p for p in item.iterdir() if p.is_file()]
        if len(files) > 10:
            results.append({
                "type": "possible_dicom_directory",
                "path": str(item),
                "file_count": len(files),
            })

    return results
