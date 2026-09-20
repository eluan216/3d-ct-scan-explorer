# Web Application

Next.js frontend that consumes the pipeline asset contract.

## Stack

- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- React Three Fiber + Drei
- Zustand for shared viewer state

## Milestones

### 1 – 3D meshes
- Load manifest + GLBs
- Orbit controls, visibility, selection
- Orientation indicator

### 2 – Synchronized slices
- Axial / Coronal / Sagittal panels
- Shared crosshair (i, j, k) from volume metadata
- Click/drag updates all views
- Radiology display orientation
- Bounds from actual volume shape
- Click mapping corrected for object-contain letterboxing

### 3 – Controls
- Slice position sliders (i / j / k)
- Mesh opacity
- Structure visibility (existing)
- Window level / width state (from metadata; display volume is pre-windowed)
- Reset all

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
