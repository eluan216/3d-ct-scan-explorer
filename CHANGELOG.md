# Changelog

## 0.1.0 – Portfolio freeze

### Pipeline
- CanonicalVolume abstraction
- DICOM and NIfTI input adapters
- Orientation, series selection, severity-level validation
- Preprocessing (window, crop, resample helpers)
- Segmentation interface + threshold backend
- Mesh generation, cleanup, GLB export
- End-to-end `build` + `verify`
- Failure-focused tests and golden fixture
- Frozen contract documented in `pipeline/docs/CONTRACT.md`

### Frontend
- Next.js 14 + TypeScript + Tailwind
- Typed manifest consumer
- 3D GLB viewer (R3F)
- Synchronized axial / coronal / sagittal slices + crosshair
- Controls: slice sliders, opacity, reset
- Study metadata panel (no PHI)
- WebGL fallback, mesh error boundary, mobile layout

### Non-goals (explicitly out of scope for this freeze)
- Live HU windowing in the browser
- Production clinical segmentation models
- Regulatory compliance / PHI workflows
- Additional medical analysis features
