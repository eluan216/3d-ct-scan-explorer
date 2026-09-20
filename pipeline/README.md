# Pipeline

Modular processing pipeline for the 3D CT Scan Explorer.

## Design Goals

- Full lifecycle coverage (discovery → validation → orientation → preprocessing → mesh → assets)
- Configuration-driven and reproducible
- Clear separation of concerns
- Failures are explicit rather than silent
- Predictable asset contract for the frontend

## Directory Layout

```
pipeline/
├── cli.py
├── config.py
├── dicom/
├── preprocessing/
├── segmentation/
├── mesh/
├── slices/
├── validation/
├── models/
├── tests/
└── requirements.txt
```

## Asset Contract

The pipeline produces:

```
assets/
├── volume/
│   ├── volume.bin
│   └── metadata.json
├── meshes/
│   └── <label>.glb
├── slices/          # optional pre-rendered slices
└── manifest.json
```

The frontend only needs to read `manifest.json` and the referenced files.

## Current Status

- Configuration system
- CLI skeleton
- DICOM/NIfTI discovery and basic validation
- Orientation helpers
- Volume and asset validation stubs
- Metadata models

Full end-to-end run wiring and mesh generation modules are next.
