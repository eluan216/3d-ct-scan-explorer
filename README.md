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
│   ├── dicom/
│   ├── nifti/
│   ├── preprocessing/
│   ├── segmentation/
│   ├── mesh/
│   ├── validation/
│   ├── tests/
│   └── docs/CONTRACT.md
├── web/               # Next.js viewer
├── assets/            # generated output (not committed)
├── docs/
├── PRD.md
└── README.md
```

---

## Requirements

**Pipeline**
- Python 3.10+
- See `pipeline/requirements.txt` (nibabel, numpy, scikit-image, trimesh, pydicom, scipy, Pillow)
- Also install: `pip install fast-simplification` (used by mesh simplification)

**Frontend**
- Node.js 18+
- Modern browser with WebGL

**Data (example)**
- [TotalSegmentator](https://zenodo.org/records/10047263) NIfTI + segmentations, or a local DICOM CT series
- Expected subject layout:
  ```
  <subject>/
    ct.nii.gz
    segmentations/
      liver.nii.gz
      spleen.nii.gz
      ...
  ```

---

## Installation & run

> Run pipeline commands **from inside** the `pipeline/` folder.  
> The code uses flat imports (`from config import ...`), so use `python cli.py ...` rather than `python -m pipeline.cli`.

### 1. Pipeline

```bash
cd pipeline
python -m venv .venv

# Windows PowerShell:
.\\.venv\Scripts\Activate.ps1

# macOS / Linux:
source .venv/bin/activate

pip install -r requirements.txt
pip install fast-simplification

python cli.py discover /path/to/data
python cli.py validate /path/to/data/<subject>
python cli.py build /path/to/data/<subject> --output ../assets
python cli.py verify ../assets
```

### 2. Frontend

```bash
cd web
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).  
Requires a sibling `assets/` directory containing `manifest.json` (produced by the pipeline).

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
| 3D meshes | GLB organs, orbit / pan / zoom, visibility toggles |
| MPR slices | Axial, coronal, sagittal with shared crosshair |
| Controls | Slice index sliders (i/j/k), mesh opacity, reset |
| Metadata | Dimensions, spacing (mm), orientation, structures, pipeline version |
| Robustness | WebGL check, mesh error boundary, missing-asset errors, mobile layout |

No patient-identifying information is shown in the UI.

---

## Demo

**[Watch the demo (≈52s)](https://drive.google.com/file/d/1j5YIkJg9D9K9xvKv-myd8AWwXLdpXm36/view?usp=drivesdk)**

Screen recording of the live viewer on subject `s0011` (TotalSegmentator-style layout):

- Orbit of multi-organ 3D meshes  
- Structure visibility toggles  
- Synchronized axial / coronal / sagittal crosshair  
- Slice index sliders  

File size ≈ 21 MB. Ensure the Drive link is set to **Anyone with the link** if viewers outside your account need access.

---

## Known limitations

- Display `volume.bin` is **pre-windowed** by the pipeline; live HU windowing in the browser is not implemented
- DICOM path covers series discovery, CT filtering, spatial sort, and basic geometry checks; uncommon multi-frame / non-axial cases may need more fixtures
- Segmentation uses supplied masks (e.g. TotalSegmentator) or a simple threshold fallback — not a clinical production model
- Meshes can look blocky at low face budgets; raise `max_faces` in config for smoother surfaces if needed
- No authentication, PHI handling, or regulatory compliance
- Large meshes may be heavy on low-end GPUs; renderer `dpr` is capped for stability

---

## Design principles

- **Contract-first** – pipeline and frontend meet at `manifest.json`
- **Fail explicitly** – ERROR vs WARNING vs INFO, not silent corruption
- **No PHI in the UI** by default
- **Test failure paths**, not only happy paths

---

## Status

**Feature-frozen for portfolio presentation.**  
Validated end-to-end on a real multi-organ CT subject with synchronized MPR views.

Further work should be bugfixes or documentation only unless the asset contract is intentionally versioned.

---

## License & attribution

Code: intended MIT (confirm before public release).  
When using TotalSegmentator data: Wasserthal et al., University Hospital Basel, **CC BY 4.0** — attribute in the app and this README.

---

eluan216
