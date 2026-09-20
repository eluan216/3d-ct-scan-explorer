# Web Application

Next.js frontend that consumes the pipeline asset contract.

## Stack

- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- React Three Fiber + Drei
- Zustand for shared viewer state

## Features

1. **3D meshes** – GLB load, orbit, visibility, selection, orientation indicator
2. **Synchronized slices** – axial / coronal / sagittal + shared crosshair
3. **Controls** – slice sliders, opacity, window state, reset
4. **Study metadata** – dimensions, spacing, orientation, structures, pipeline version (no PHI)
5. **Robustness** – WebGL detection, mesh error boundary, missing-asset handling, mobile layout

## Development

```bash
cd web
npm install
npm run dev
```

Requires a sibling `assets/` directory produced by the pipeline.

## Contract

Only reads `manifest.json` and referenced files.  
See `../pipeline/docs/CONTRACT.md`.
