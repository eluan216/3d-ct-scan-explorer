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
| Area | Status |
|------|--------|
| CanonicalVolume + adapters (DICOM / NIfTI) | Done |
| Orientation, series selection, severity levels | Done |
| Mesh generation + verification | Done |
| Golden fixture + failure-focused tests | Done |
| Frozen contract (`pipeline/docs/CONTRACT.md`) | Done |

### Frontend (first milestone)
| Area | Status |
|------|--------|
| Next.js + TypeScript + Tailwind foundation | Done |
| Typed manifest + asset loader | Done |
| 3D GLB viewer (R3F) | Done |
| Structure list, visibility, selection | Done |
| Orientation indicator | Done |
| Loading / error states | Done |
| Synchronized slice views | Next |
| Window/level + volume controls | Next |

## Quick Start

```bash
# 1. Pipeline (once you have a subject)
cd pipeline
pip install -r requirements.txt
python -m pipeline.cli build /path/to/subject --output ../assets
python -m pipeline.cli verify ../assets

# 2. Frontend
cd ../web
npm install
npm run dev
```

Open http://localhost:3000. The app serves files from the sibling `assets/` directory.

## Contract

See [`pipeline/docs/CONTRACT.md`](pipeline/docs/CONTRACT.md).  
Frontend requirements must not modify pipeline interfaces without a version bump.

## License & Data

Code will be MIT.  
Public datasets (e.g. TotalSegmentator) will be fully attributed under their respective licenses.

---
eluan216
