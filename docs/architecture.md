# Architecture Notes

## Data Flow

1. Raw NIfTI CT + per-structure masks
2. Reorientation to consistent RAS+ orientation
3. Label volume construction (limited set of abdominal structures)
4. Cropping around the label bounding box with margin
5. CT windowing (typical soft-tissue window)
6. Marching cubes → light smoothing → decimation → GLB export
7. Raw uint8 volume binaries + JSON metadata for the frontend

## Coordinate Systems

- Pipeline works in patient RAS+ space
- Frontend converts to a right-handed Three.js-friendly frame centered on the volume
- Slice canvases follow standard radiology display conventions (patient left appears on the right side of axial/coronal images)

## Key Design Decisions

- Keep the web payload small by exporting only the needed structures and a cropped volume
- Single source of truth for crosshair position (voxel indices in the cropped volume)
- Explicit verification steps for anatomical orientation before considering the build complete
