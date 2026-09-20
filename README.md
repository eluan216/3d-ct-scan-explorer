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

## Pipeline Status

| Area                              | Status   |
|-----------------------------------|----------|
| CanonicalVolume abstraction       | Done     |
| DICOM adapter + severity levels   | Done     |
| NIfTI adapter                     | Done     |
| Slice integrity checks            | Done     |
| End-to-end build + verify         | Done     |
| Structured ERROR/WARNING/INFO     | Done     |
| Invariant tests                   | Done     |
| Failure-focused test suite        | Done     |
| Frontend                          | Not started |

## Running the Pipeline

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

The suite emphasises failure behaviour: duplicate slices, missing geometry, non-contiguous InstanceNumbers, NaNs, empty masks, incomplete asset packages, and manifest inconsistencies.

## Asset Contract

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
