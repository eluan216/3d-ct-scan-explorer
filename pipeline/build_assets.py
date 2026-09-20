"""
Build web-ready assets from a selected TotalSegmentator subject.

Steps:
1. Reorient CT and masks to closest canonical orientation.
2. Build a compact label volume for the organs we care about.
3. Crop around the labels with a margin.
4. Apply a standard soft-tissue window.
5. Export raw volume binaries + metadata.
6. Generate simplified meshes and save as GLB.
"""

from pathlib import Path
import json
import numpy as np
import nibabel as nib
from nibabel.orientations import io_orientation, axcodes2ornt, ornt_transform, apply_orientation
from skimage import measure
import trimesh

# Label IDs used in the exported volume
LABEL_MAP = {
    "liver": 1,
    "spleen": 2,
    "stomach": 3,
    "kidney_right": 4,
    "kidney_left": 5,
    "aorta": 6,
    "inferior_vena_cava": 7,
}

SPINE_PREFIX = "vertebrae_"


def reorient_to_canonical(img: nib.Nifti1Image) -> nib.Nifti1Image:
    """Return a new image in the closest RAS+ orientation."""
    orig_ornt = io_orientation(img.affine)
    targ_ornt = axcodes2ornt("RAS")
    transform = ornt_transform(orig_ornt, targ_ornt)
    return img.as_reoriented(transform)


def load_and_reorient(path: Path) -> tuple[np.ndarray, np.ndarray, tuple]:
    img = nib.load(str(path))
    img = reorient_to_canonical(img)
    data = img.get_fdata()
    affine = img.affine
    spacing = img.header.get_zooms()[:3]
    return data, affine, spacing


def build_label_volume(seg_dir: Path, shape: tuple) -> np.ndarray:
    labels = np.zeros(shape, dtype=np.uint8)

    for name, lid in LABEL_MAP.items():
        path = seg_dir / f"{name}.nii.gz"
        if not path.exists():
            continue
        mask, _, _ = load_and_reorient(path)
        labels[mask > 0] = lid

    # Spine = union of all vertebrae_* masks
    spine_mask = np.zeros(shape, dtype=bool)
    for p in seg_dir.glob(f"{SPINE_PREFIX}*.nii.gz"):
        mask, _, _ = load_and_reorient(p)
        spine_mask |= mask > 0
    labels[spine_mask] = 8

    return labels


def crop_with_margin(volume: np.ndarray, labels: np.ndarray, spacing: tuple, margin_mm: float = 20.0):
    coords = np.argwhere(labels > 0)
    if len(coords) == 0:
        raise ValueError("No labels found for cropping.")

    mins = coords.min(axis=0)
    maxs = coords.max(axis=0) + 1

    margin_vox = [int(np.ceil(margin_mm / s)) for s in spacing]
    mins = np.maximum(mins - margin_vox, 0)
    maxs = np.minimum(maxs + margin_vox, volume.shape)

    slices = tuple(slice(int(a), int(b)) for a, b in zip(mins, maxs))
    return volume[slices], labels[slices], mins


def window_ct(ct: np.ndarray, level: float = 50.0, width: float = 400.0) -> np.ndarray:
    lo = level - width / 2
    hi = level + width / 2
    clipped = np.clip(ct, lo, hi)
    scaled = ((clipped - lo) / (hi - lo) * 255.0).astype(np.uint8)
    return scaled


def mesh_from_label(labels: np.ndarray, lid: int, spacing: tuple, center: np.ndarray):
    binary = (labels == lid).astype(np.float32)
    if binary.sum() == 0:
        return None

    verts, faces, normals, _ = measure.marching_cubes(binary, level=0.5, spacing=spacing)

    # Convert from (r, a, s) to a centered Three.js-friendly frame
    # x = -(r - c_r), y = (s - c_s), z = (a - c_a)
    verts_centered = np.empty_like(verts)
    verts_centered[:, 0] = -(verts[:, 0] - center[0])
    verts_centered[:, 1] = verts[:, 2] - center[2]
    verts_centered[:, 2] = verts[:, 1] - center[1]

    mesh = trimesh.Trimesh(vertices=verts_centered, faces=faces, process=True)
    mesh.fix_normals()

    # Simple decimation target
    target_faces = min(40000, len(mesh.faces))
    if len(mesh.faces) > target_faces:
        mesh = mesh.simplify_quadratic_decimation(target_faces)

    return mesh


def main(subject_dir: Path, out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "meshes").mkdir(exist_ok=True)

    ct_path = subject_dir / "ct.nii.gz"
    seg_dir = subject_dir / "segmentations"

    ct, affine, spacing = load_and_reorient(ct_path)
    labels = build_label_volume(seg_dir, ct.shape)

    ct_c, labels_c, offset = crop_with_margin(ct, labels, spacing)
    ct_w = window_ct(ct_c)

    # Volume center in mm (cropped space)
    shape = np.array(ct_w.shape)
    center_mm = (shape * np.array(spacing)) / 2.0

    # Write binaries (C-order uint8)
    ct_w.tofile(out_dir / "ct.bin")
    labels_c.tofile(out_dir / "labels.bin")

    meta = {
        "shape": [int(x) for x in shape],
        "spacing_mm": [float(x) for x in spacing],
        "crop_offset": [int(x) for x in offset],
        "center_mm": [float(x) for x in center_mm],
        "labels": {},
    }

    name_by_id = {v: k for k, v in LABEL_MAP.items()}
    name_by_id[8] = "spine"

    for lid, name in name_by_id.items():
        mask = labels_c == lid
        if not mask.any():
            continue
        coords = np.argwhere(mask)
        centroid = coords.mean(axis=0)
        meta["labels"][name] = {
            "id": lid,
            "centroid_ijk": [float(x) for x in centroid],
        }

        mesh = mesh_from_label(labels_c, lid, spacing, center_mm)
        if mesh is not None:
            mesh.export(out_dir / "meshes" / f"{name}.glb")

    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2))
    print(f"Assets written to {out_dir}")


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python build_assets.py <subject_dir> <output_dir>")
        raise SystemExit(1)
    main(Path(sys.argv[1]), Path(sys.argv[2]))
