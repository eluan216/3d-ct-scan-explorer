"""
Validate a single study or subject before processing.
"""

from pathlib import Path
from typing import Tuple, List
import numpy as np


def validate_nifti_subject(path: Path) -> Tuple[bool, List[str]]:
    import nibabel as nib

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

    messages.append("OK: NIfTI subject basic checks passed")
    return True, messages


def validate_dicom_directory(path: Path) -> Tuple[bool, List[str]]:
    messages = []
    path = Path(path)

    try:
        from dicom.loader import read_dicom_files, group_by_series, is_ct_series
    except ImportError as e:
        messages.append(f"FAIL: {e}")
        return False, messages

    try:
        datasets = read_dicom_files(path)
    except Exception as e:
        messages.append(f"FAIL: cannot read DICOM files – {e}")
        return False, messages

    if not datasets:
        messages.append("FAIL: no readable DICOM files")
        return False, messages

    series_map = group_by_series(datasets)
    ct_series = {uid: ds for uid, ds in series_map.items() if is_ct_series(ds)}

    if not ct_series:
        messages.append("FAIL: no CT series found")
        return False, messages

    messages.append(f"OK: found {len(ct_series)} CT series")
    for uid, ds_list in ct_series.items():
        messages.append(f"  series {uid[:16]}… → {len(ds_list)} slices")

    return True, messages


def validate_study(path: Path) -> Tuple[bool, List[str]]:
    path = Path(path)
    if (path / "ct.nii.gz").exists():
        return validate_nifti_subject(path)
    return validate_dicom_directory(path)
