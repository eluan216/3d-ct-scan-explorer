"""
NIfTI subject → CanonicalVolume loader.
"""

from pathlib import Path
from typing import Optional
import numpy as np
import nibabel as nib

from models.volume import CanonicalVolume
from preprocessing.orientation import to_canonical, get_axcodes


def load_nifti_subject(subject_dir: Path) -> CanonicalVolume:
    subject_dir = Path(subject_dir)
    ct_path = subject_dir / "ct.nii.gz"
    if not ct_path.exists():
        raise FileNotFoundError(f"ct.nii.gz not found in {subject_dir}")

    img = nib.load(str(ct_path))
    img = to_canonical(img)
    data = img.get_fdata().astype(np.float32)
    spacing = tuple(float(x) for x in img.header.get_zooms()[:3])

    # origin from affine
    origin = tuple(float(x) for x in img.affine[:3, 3])

    return CanonicalVolume(
        data=data,
        spacing_mm=spacing,
        origin_mm=origin,
        orientation=get_axcodes(img),
        modality="CT",
        source="nifti",
        meta={"subject": subject_dir.name},
    )


def load_existing_labels(subject_dir: Path, shape) -> Optional[np.ndarray]:
    """Load TotalSegmentator-style masks if present."""
    seg_dir = subject_dir / "segmentations"
    if not seg_dir.is_dir():
        return None

    from preprocessing.orientation import to_canonical

    label_map = {
        "liver": 1,
        "spleen": 2,
        "stomach": 3,
        "kidney_right": 4,
        "kidney_left": 5,
        "aorta": 6,
        "inferior_vena_cava": 7,
    }
    labels = np.zeros(shape, dtype=np.uint8)

    for name, lid in label_map.items():
        p = seg_dir / f"{name}.nii.gz"
        if p.exists():
            m = nib.load(str(p))
            m = to_canonical(m)
            mask = m.get_fdata() > 0
            labels[mask] = lid

    spine = np.zeros(shape, dtype=bool)
    for p in seg_dir.glob("vertebrae_*.nii.gz"):
        m = nib.load(str(p))
        m = to_canonical(m)
        spine |= m.get_fdata() > 0
    labels[spine] = 8

    return labels
