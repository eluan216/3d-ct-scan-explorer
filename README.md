# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. The project turns a CT study into 3D organ meshes and synchronized multi-planar views.

This is a learning and portfolio project only. It is not a medical device and must never be used for diagnosis.

## Architecture

```
DICOM directory ──► DicomSeriesLoader ──┐
                                        ▼
NIfTI subject   ──► NiftiLoader ────────► CanonicalVolume
                                        ▼
                               Preprocessing → Segmentation → Mesh
                                        ▼
                                   assets/ + manifest.json
                                        ▼
                                     verify
```

Input adapters are interchangeable. Downstream stages only see `CanonicalVolume`.

## Pipeline Status

| Area                                 | Status |
|--------------------------------------|--------|
| CanonicalVolume + invariants         | Done   |
| DICOM adapter (orientation, series)  | Done   |
| Reversed-order slice handling        | Done   |
| Multi-series selection rules         | Done   |
| Severity levels (ERROR/WARNING/INFO) | Done   |
| Geometry & segmentation edge cases   | Done   |
| Golden fixture regression            | Done   |
| Frozen contract documentation        | Done   |
| Frontend                             | Not started |

## Contract

See [`pipeline/docs/CONTRACT.md`](pipeline/docs/CONTRACT.md) for the stable interfaces. Frontend work must consume only the published asset manifest and must not change pipeline contracts without a version bump.

## CLI

```bash
cd pipeline
pip install -r requirements.txt

python -m pipeline.cli discover <root>
python -m pipeline.cli validate <study>
python -m pipeline.cli build <study> --output ../assets
python -m pipeline.cli verify ../assets
```

## Tests

```bash
cd pipeline
pip install pytest
pytest tests/ -v
```

Coverage includes:

- oblique / missing / inconsistent orientation
- reversed slice ordering
- multiple CT series selection & ties
- single-slice and spacing-variation geometry
- empty / single-voxel / disconnected segmentation
- golden end-to-end fixture → verified assets
- both DICOM-style synthetic data and NIfTI paths

## Asset Package

```
assets/
├── volume/
│   ├── volume.bin
│   └── metadata.json
├── meshes/
│   └── <structure>.glb
├── manifest.json
└── pipeline_config.json
```

## License & Data

Code will be MIT.  
Public datasets will be fully attributed (e.g. TotalSegmentator, CC BY 4.0).

---
eluan216
