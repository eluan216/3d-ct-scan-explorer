# 3D CT Scan Explorer

Format-agnostic medical-imaging pipeline that converts DICOM or NIfTI CT studies into validated canonical volumes and reproducible 3D/MPR assets, consumed by a Next.js + Three.js visualization client.

**Learning and portfolio use only. Not a medical device. Not for diagnosis.**

---

## What it does

1. **Ingest** CT data from DICOM series or NIfTI (e.g. TotalSegmentator layout)
2. **Normalize** to a `CanonicalVolume` (RAS+ orientation, known spacing, HU when available)
3. **Validate** with explicit ERROR / WARNING / INFO severity
4. **Process** – window, optional crop, segmentation interface, mesh generation
5. **Export** a stable asset package (`manifest.json` + volume + GLB meshes)
6. **Visualize** – interactive 3D organs + synchronized axial / coronal / sagittal slices

---

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
                         Next.js / React Three Fiber viewer
```

- Input adapters are interchangeable
- Downstream stages only see `CanonicalVolume`
- Frontend only reads the manifest and referenced files  
  → see [`pipeline/docs/CONTRACT.md`](pipeline/docs/CONTRACT.md)

---

## Repository layout

```
3d-ct-scan-explorer/
├── pipeline/          # Python processing pipeline
│   ├── cli.py
│   ├── dicom/         # DICOM discovery, validation, loader
│   ├── nifti/         # NIfTI adapter
│   ├── preprocessing/
│   ├── segmentation/
│   ├── mesh/
│   ├── validation/
│   ├── tests/
│   └── docs/CONTRACT.md
├── web/               # Next.js viewer
├── assets/            # generated output (not committed)
├── PRD.md
└── README.md
```

---

## Requirements

**Pipeline**
- Python 3.10+
- See `pipeline/requirements.txt` (nibabel, numpy, scikit-image, trimesh, pydicom, scipy)

**Frontend**
- Node.js 18+
- Modern browser with WebGL

**Data (example)**
- [TotalSegmentator small subset](https://zenodo.org/records/10047263) (NIfTI + segmentations), or a local DICOM CT series

---

## Installation & run

### 1. Pipeline

```bash
cd pipeline
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Discover subjects under a data root
python -m pipeline.cli discover /path/to/data

# Validate one subject
python -m pipeline.cli validate /path/to/data/<subject>

# Build assets
python -m pipeline.cli build /path/to/data/<subject> --output ../assets

# Verify the package
python -m pipeline.cli verify ../assets
```

### 2. Frontend

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).  
The app serves the sibling `assets/` directory during development.

### 3. Tests

```bash
cd pipeline
pip install pytest
pytest tests/ -v
```

---

## Viewer capabilities

| Feature | Description |
|---------|-------------|
| 3D meshes | GLB organs, orbit/pan/zoom, visibility, selection |
| MPR slices | Axial, coronal, sagittal with shared crosshair |
| Controls | Slice index sliders, mesh opacity, reset |
| Metadata | Dimensions, spacing (mm), orientation, structures, pipeline version |
| Robustness | WebGL check, mesh error boundary, missing-asset errors, mobile layout |

No patient-identifying information is shown in the UI.

---

## Demo checklist (for recording)

1. Load a built `assets/` package
2. Orbit the 3D view; toggle structure visibility
3. Click/drag crosshair in axial → coronal and sagittal update
4. Use slice sliders; confirm bounds
5. Adjust mesh opacity
6. Open metadata panel (dimensions, spacing, structures)
7. Show loading / missing-asset behavior if useful

Suggested length: 20–40 seconds. Place a GIF under `docs/demo.gif` and link it here when recorded.

---

## Known limitations

- Display `volume.bin` is **pre-windowed** by the pipeline; live HU windowing in the browser is not implemented
- Full DICOM support covers series discovery, CT filtering, spatial sort, and basic geometry checks; advanced multi-frame / non-axial edge cases may need more fixtures
- Segmentation currently uses supplied TotalSegmentator masks or a simple threshold placeholder – not a production clinical model
- No authentication, PHI handling, or regulatory compliance
- Large meshes can be heavy on low-end GPUs; `dpr` is capped for stability

---

## Design principles

- **Contract-first** – pipeline and frontend meet at `manifest.json`
- **Fail explicitly** – ERROR vs WARNING vs INFO, not silent corruption
- **No PHI in the UI** by default
- **Test failure paths**, not only happy paths

---

## Status

**Feature-frozen for portfolio presentation.**  
Further work should be bugfixes or documentation only unless the contract is intentionally versioned.

---

## License & attribution

Code: intended MIT (confirm before public release).  
When using TotalSegmentator data: Wasserthal et al., University Hospital Basel, **CC BY 4.0** – attribute in the app footer and this README.

---

eluan216
