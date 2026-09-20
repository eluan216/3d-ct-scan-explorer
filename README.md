# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. The project generates 3D organ meshes and keeps axial, coronal and sagittal views synchronized.

This is a learning and portfolio project only. It is not a medical device and must never be used for diagnosis.

## Current Focus

The pipeline is being built first, before any frontend work.

Goals for the pipeline:

- Full CT lifecycle (discovery → validation → orientation → preprocessing → mesh generation → quality checks → frontend-ready assets)
- Configuration-driven and reproducible
- Explicit failure handling
- Clear separation of concerns
- Stable asset contract that the frontend will consume later

## Project Structure

```
3d-ct-scan-explorer/
├── pipeline/               # Modular processing pipeline (active development)
│   ├── cli.py
│   ├── config.py
│   ├── dicom/
│   ├── preprocessing/
│   ├── segmentation/
│   ├── mesh/
│   ├── slices/
│   ├── validation/
│   ├── models/
│   └── tests/
├── web/                    # Frontend (not started yet)
├── docs/
├── PRD.md
└── README.md
```

## Asset Contract (target)

```
assets/
├── volume/
│   ├── volume.bin
│   └── metadata.json
├── meshes/
│   └── <structure>.glb
├── slices/
└── manifest.json
```

## Status

- [x] Repository + PRD
- [x] Modular pipeline skeleton
- [x] Configuration system
- [x] CLI entry point
- [x] Discovery & basic validation
- [x] Orientation helpers
- [ ] Full preprocessing modules
- [ ] Mesh generation + cleanup
- [ ] End-to-end run wiring
- [ ] Automated verification suite
- [ ] Frontend (after pipeline is stable)

## License & Data

Code will be MIT once the first complete version is ready.  
CT data will use the public TotalSegmentator dataset (CC BY 4.0) with full attribution.

---
eluan216
