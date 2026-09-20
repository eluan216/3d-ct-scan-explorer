# Pipeline

Modular processing pipeline for the 3D CT Scan Explorer.

## Design Goals

- Full lifecycle coverage
- Configuration-driven and reproducible
- Explicit failure handling
- Clear separation of concerns
- Stable asset contract for the frontend

## CLI Stages

```bash
python -m pipeline.cli discover <root>
python -m pipeline.cli validate <subject>
python -m pipeline.cli build <subject> [--output assets] [--config config.json]
python -m pipeline.cli verify <assets_dir>
```

Additional stage commands (preprocess / segment / mesh / slices) exist as placeholders and will be fully wired later. The primary reproducible entry point is `build`.

## Asset Contract

```
assets/
├── volume/
│   ├── volume.bin
│   └── metadata.json
├── meshes/
│   └── <label>.glb
├── manifest.json
└── pipeline_config.json
```

## Current Status

- [x] Config system
- [x] CLI with explicit stages
- [x] Discovery & validation
- [x] Orientation, window, crop
- [x] Segmentation interface + threshold backend
- [x] Mesh generation, cleanup, export
- [x] End-to-end `build` command
- [x] Asset verification
- [ ] Full DICOM series support
- [ ] Advanced resampling options
- [ ] Pre-rendered slice images
- [ ] Comprehensive test suite
- [ ] Model-based segmentation backends
