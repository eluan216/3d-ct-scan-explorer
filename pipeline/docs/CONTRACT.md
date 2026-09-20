# Pipeline Contract (Frozen)

This document describes the stable interfaces that downstream consumers
(including the frontend) may rely on. Changes to these contracts require
an explicit version bump.

## 1. CanonicalVolume

```
data          : float32 array, shape (I, J, K)
spacing_mm    : (si, sj, sk) – all positive
origin_mm     : world coordinate of voxel (0,0,0)
orientation   : string, typically "RAS"
modality      : "CT"
source        : "dicom" | "nifti" | "golden" | …
meta          : free-form dict
```

Invariants:
- ndim == 3
- finite values only
- spacing > 0

## 2. Preprocessing API

- `to_canonical(img) → img`
- `apply_window(volume, level, width) → uint8 or float`
- `crop_to_labels(volume, labels, spacing, margin_mm) → volume, labels, offset`
- `resample_volume(...) / resample_labels(...)`

## 3. Segmentation API

```
class SegmentationMethod:
    run(volume, spacing_mm, meta) → label_volume (uint8)
    label_map() → {id: name}
```

## 4. Mesh API

```
mesh_from_label(labels, id, spacing, center) → Trimesh | None
generate_all(...) → {name: Trimesh}
basic_cleanup / remove_small_components
export_glb(meshes, out_dir) → {name: relative_path}
```

## 5. Asset Manifest

```json
{
  "pipeline_version": "0.1.0",
  "subject_id": "…",
  "volume": {
    "bin": "volume/volume.bin",
    "metadata": "volume/metadata.json"
  },
  "meshes": {
    "liver": "meshes/liver.glb",
    …
  },
  "labels": {
    "liver": {"id": 1},
    …
  }
}
```

Every path listed in the manifest must exist relative to the assets root.

## 6. Verification

`verify_assets(assets_dir)` returns `(ok: bool, report: str)`.
It fails if required files are missing or the manifest is inconsistent.

---

Frontend code must consume only the manifest and the files it references.
No frontend requirement may change the contracts above without a version bump.
