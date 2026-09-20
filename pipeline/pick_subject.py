"""
Select a suitable TotalSegmentator subject for the explorer.

A subject is considered usable when the required abdominal structures
are present and do not touch the superior or inferior ends of the volume.
Among valid subjects we prefer the one with the largest total organ volume.
"""

from pathlib import Path
import json
import nibabel as nib
import numpy as np

REQUIRED = [
    "liver",
    "spleen",
    "stomach",
    "kidney_left",
    "kidney_right",
    "aorta",
    "inferior_vena_cava",
]


def load_mask(path: Path) -> np.ndarray:
    img = nib.load(str(path))
    data = img.get_fdata()
    return (data > 0).astype(np.uint8)


def subject_is_valid(subject_dir: Path) -> tuple[bool, float]:
    seg_dir = subject_dir / "segmentations"
    if not seg_dir.is_dir():
        return False, 0.0

    total_volume = 0.0
    shape = None

    for name in REQUIRED:
        mask_path = seg_dir / f"{name}.nii.gz"
        if not mask_path.exists():
            return False, 0.0

        mask = load_mask(mask_path)
        if shape is None:
            shape = mask.shape
        elif mask.shape != shape:
            return False, 0.0

        if mask.sum() == 0:
            return False, 0.0

        # Reject if the structure touches the first or last slice
        # along the superior-inferior axis (axis 2 after canonical orientation).
        # We will reorient later; for now we use the raw data.
        z_proj = mask.any(axis=(0, 1))
        if z_proj[0] or z_proj[-1]:
            return False, 0.0

        total_volume += float(mask.sum())

    return True, total_volume


def main(raw_root: Path):
    candidates = []

    for subject_dir in sorted(raw_root.iterdir()):
        if not subject_dir.is_dir():
            continue
        if not (subject_dir / "ct.nii.gz").exists():
            continue

        valid, volume = subject_is_valid(subject_dir)
        if valid:
            candidates.append((subject_dir.name, volume))

    if not candidates:
        raise SystemExit("No valid subject found.")

    candidates.sort(key=lambda x: x[1], reverse=True)
    best_name, best_vol = candidates[0]

    result = {
        "selected_subject": best_name,
        "organ_voxel_count": best_vol,
        "candidates_checked": len(list(raw_root.iterdir())),
        "valid_candidates": len(candidates),
    }

    out_path = Path("selected_subject.json")
    out_path.write_text(json.dumps(result, indent=2))
    print(f"Selected: {best_name}  (organ voxels ≈ {best_vol:.0f})")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    import sys
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("../data/raw")
    main(root)
