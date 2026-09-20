# Pipeline

Python scripts that convert a TotalSegmentator CT subject into web-ready assets.

## Planned Scripts

- `pick_subject.py` — select a subject that has the required organs fully inside the volume
- `build_assets.py` — reorient, crop, window the CT, create label volume, generate meshes, export binaries and metadata

## Requirements (planned)

- Python 3.10+
- nibabel
- numpy
- scikit-image
- trimesh
- fast-simplification (optional, for mesh decimation)

Exact dependency list and environment setup will be added once the scripts are written.
