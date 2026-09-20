# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. Turns a CT study into 3D organ meshes and synchronized multi-planar views.

**Learning / portfolio project only. Not a medical device. Not for diagnosis.**

## Architecture

```
DICOM ──┐
        ▼
NIfTI ──► CanonicalVolume → Pipeline → assets/ + manifest.json → Next.js viewer
```

The frontend is a pure consumer of the frozen asset contract.

## Status

### Pipeline
- CanonicalVolume + DICOM / NIfTI adapters
- Orientation, series selection, severity-level validation
- Mesh generation, asset package, verification
- Failure-focused tests + golden fixture
- Frozen contract: `pipeline/docs/CONTRACT.md`

### Frontend
- 3D GLB viewer (React Three Fiber)
- Synchronized axial / coronal / sagittal slices + crosshair
- Slice sliders, mesh opacity, structure visibility, reset
- Study metadata panel (no PHI)
- WebGL fallback, mesh error boundary, mobile layout
- Loading and missing-asset error states

## Quick Start

```bash
# Pipeline
cd pipeline
pip install -r requirements.txt
python -m pipeline.cli build /path/to/subject --output ../assets
python -m pipeline.cli verify ../assets

# Frontend
cd ../web
npm install
npm run dev
```

Open http://localhost:3000

## Contract

See [`pipeline/docs/CONTRACT.md`](pipeline/docs/CONTRACT.md).  
Frontend requirements must not modify pipeline interfaces without a version bump.

## License & Data

Code will be MIT.  
Public datasets (e.g. TotalSegmentator) will be fully attributed under their respective licenses.

---
eluan216
