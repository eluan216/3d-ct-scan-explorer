# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. The project turns a CT study into 3D organ meshes and synchronized multi-planar views.

This is a learning and portfolio project only. It is not a medical device and must never be used for diagnosis.

## Architecture

Input adapters produce a common intermediate representation:

```
DICOM directory ──► DicomSeriesLoader ──┐
                                        ▼
NIfTI subject   ──► NiftiLoader ────────► CanonicalVolume
                                        ▼
                               Preprocessing → Segmentation → Mesh / Slices
                                        ▼
                                   assets/ + manifest.json
```

Later stages never need to know whether the source was DICOM or NIfTI.

## Pipeline Status

| Area                         | Status      |
|------------------------------|-------------|
| CanonicalVolume abstraction  | Done        |
| NIfTI adapter                | Done        |
| DICOM series discovery       | Done        |
| DICOM → HU volume            | Done        |
| Slice ordering / validation  | Done        |
| Missing / duplicate detection| Done        |
| End-to-end `build`           | Done        |
| Asset verification           | Done        |
| Unit tests (core paths)      | In progress |
| Full DICOM edge-case suite   | In progress |
| Frontend                     | Not started |

## CLI

```bash
cd pipeline
pip install -r requirements.txt

python -m pipeline.cli discover <root>
python -m pipeline.cli validate <study-or-subject>
python -m pipeline.cli build <study-or-subject> --output ../assets
python -m pipeline.cli verify ../assets
```

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
When using public data, full attribution will be included (e.g. TotalSegmentator, CC BY 4.0).

---
eluan216
