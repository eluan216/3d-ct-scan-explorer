"""
Orientation-specific validation helpers.
"""

from typing import Tuple
import nibabel as nib
from preprocessing.orientation import get_axcodes


def check_ras(img: nib.Nifti1Image) -> Tuple[bool, str]:
    codes = get_axcodes(img)
    if codes == "RAS":
        return True, "RAS orientation confirmed"
    return False, f"expected RAS, got {codes}"
