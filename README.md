# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. The project turns a CT study into 3D organ meshes and synchronized multi-planar views.

This is a learning and portfolio project only. It is not a medical device and must never be used for diagnosis.

## Current Focus

The processing pipeline is being completed first. The frontend will be built only after the pipeline produces a stable, verifiable asset package.

## Pipeline Status

| Stage                    | Status      |
|--------------------------|-------------|
| Config system            | Done        |
| CLI (explicit stages)    | Done        |
| Discovery / validation   | Done        |
| Orientation              | Done        |
| Window / crop            | Done        |
| Segmentation interface   | Done        |
| Mesh generation + export | Done        |
| End-to-end `build`       | Done        |
| Asset verification       | Done        |
| Full DICOM support       | Pending     |
| Comprehensive tests      | In progress |
| Frontend                 | Not started |

## Quick Start (once data is present)

```bash
cd pipeline
pip install -r requirements.txt

# discover subjects
python -m pipeline.cli discover ../data/raw

# validate one subject
python -m pipeline.cli validate ../data/raw/<subject>

# run full pipeline
python -m pipeline.cli build ../data/raw/<subject> --output ../assets

# verify the output
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

The frontend will only need to read `manifest.json` and the files it references.

## Project Layout

```
3d-ct-scan-explorer/
├── pipeline/          # active development
├── web/               # not started
├── docs/
├── PRD.md
└── README.md
```

## License & Data

Code will be MIT.  
CT data will use the public TotalSegmentator dataset (CC BY 4.0) with full attribution.

---
eluan216
