# Web Application

Next.js frontend that consumes the pipeline asset contract.

## Stack

- Next.js 14 (App Router) + TypeScript
- Tailwind CSS
- React Three Fiber + Drei
- Zustand for viewer state

## First Milestone

- Load `manifest.json`
- Display available structures
- Load and render GLB meshes
- Orbit / pan / zoom
- Visibility toggles + selection highlight
- Anatomical orientation indicator
- Loading and error states

Synchronized slice views and window/level controls come next.

## Development

```bash
# from repo root, after running the pipeline once
cd web
npm install
npm run dev
```

The app expects an `assets/` directory (produced by the pipeline) sitting next to `web/`.
A small API route serves those files during local development.

## Contract

This application only reads:

- `manifest.json`
- the volume / mesh / slice files referenced by the manifest

It never inspects DICOM or NIfTI source data.
See `../pipeline/docs/CONTRACT.md`.
