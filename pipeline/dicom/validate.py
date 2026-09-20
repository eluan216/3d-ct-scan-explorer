"""
Validate a single study or subject before processing.
"""

from pathlib import Path
from typing import Tuple, List
import nibabel as nib
import numpy as np


def validate_nifti_subject(path: Path) -> Tuple[bool, List[str]]:
    messages = []
    path = Path(path)

    ct_path = path / "ct.nii.gz"
    if not ct_path.exists():
        messages.append("FAIL: ct.nii.gz not found")
        return False, messages

    try:
        img = nib.load(str(ct_path))
        data = img.get_fdata()
    except Exception as e:
        messages.append(f"FAIL: cannot load CT – {e}")
        return False, messages

    if data.size == 0:
        messages.append("FAIL: empty volume")
        return False, messages

    if not np.isfinite(data).all():
        messages.append("FAIL: NaN or Inf values present")
        return False, messages

    spacing = img.header.get_zooms()[:3]
    if any(s <= 0 for s in spacing):
        messages.append(f"FAIL: invalid spacing {spacing}")
        return False, messages

    messages.append("OK: basic CT checks passed")
    return True, messages


def validate_study(path: Path) -> Tuple[bool, List[str]]:
    path = Path(path)
    if (path / "ct.nii.gz").exists():
        return validate_nifti_subject(path)

    # Future: DICOM validation path
    return False, ["FAIL: unsupported input format (expected NIfTI subject for now)"]
