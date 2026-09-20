# Web Application

Next.js frontend that consumes the pipeline asset contract.

## Stack

- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- React Three Fiber + Drei
- Zustand for shared viewer state

## Milestones

### 1 – 3D meshes (done)
- Load manifest + GLBs
- Orbit controls, visibility, selection
- Orientation indicator

### 2 – Synchronized slices (done)
- Axial / Coronal / Sagittal panels
- Shared crosshair state (i, j, k) derived from volume metadata
- Click/drag in any plane updates the other two
- Display orientation follows radiology convention (patient left on image right for axial/coronal)
- Bounds taken from actual volume shape – nothing hardcoded

### Next
- Window/level and opacity controls
- Slice position sliders
- Study metadata panel

## Development

```bash
# from repo root, after pipeline has written assets/
cd web
npm install
npm run dev
```

The app serves `../assets` via a small API route during local development.

## Contract

Only reads `manifest.json` and the files it references.  
See `../pipeline/docs/CONTRACT.md`.
