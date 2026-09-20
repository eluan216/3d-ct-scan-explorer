# 3D CT Scan Explorer

Interactive viewer for abdominal CT scans. Generates 3D organ meshes from segmentation masks and keeps axial, coronal, and sagittal views synchronized to a single crosshair.

**This is a learning and portfolio project only. It is not a medical device and must never be used for diagnosis.**

## Project Structure

```
3d-ct-scan-explorer/
├── pipeline/           # Python scripts that prepare meshes and volume data
├── web/                # Next.js frontend
├── data/               # Local data (not committed)
├── docs/               # Additional notes
├── PRD.md
└── README.md
```

## High-Level Flow

1. Download a public CT + segmentation dataset.
2. Run the pipeline to pick a suitable subject, reorient, crop, window, and export meshes + volume binaries.
3. Serve the frontend. The web app loads the prepared assets and renders the 3D + MPR views.

## Status

- [x] Repository and PRD
- [ ] Pipeline scripts
- [ ] Frontend application
- [ ] Verification steps
- [ ] Deployment notes

## License & Attribution

Code will be released under MIT once the first working version is complete.  
CT data comes from the TotalSegmentator dataset (Wasserthal et al., University Hospital Basel) under CC BY 4.0. Full attribution will appear in the application footer and this README.

---
eluan216
