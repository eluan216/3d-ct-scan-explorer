"""
Canonical orientation handling.
"""

from typing import Tuple
import nibabel as nib
from nibabel.orientations import io_orientation, axcodes2ornt, ornt_transform
import numpy as np


def to_canonical(img: nib.Nifti1Image) -> nib.Nifti1Image:
    """Reorient image to closest RAS+ orientation."""
    orig = io_orientation(img.affine)
    target = axcodes2ornt("RAS")
    transform = ornt_transform(orig, target)
    return img.as_reoriented(transform)


def get_axcodes(img: nib.Nifti1Image) -> str:
    ornt = io_orientation(img.affine)
    codes = nib.orientations.ornt2axcodes(ornt)
    return "".join(codes)


def verify(img: nib.Nifti1Image, expected: str = "RAS") -> Tuple[bool, str]:
    actual = get_axcodes(img)
    if actual == expected:
        return True, f"orientation ok: {actual}"
    return False, f"orientation mismatch: got {actual}, expected {expected}"
