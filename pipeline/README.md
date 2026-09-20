# Pipeline

Modular CT processing pipeline.

## Input Adapters

- `dicom/` – discovers series, validates slices, converts to HU, produces `CanonicalVolume`
- `nifti/` – loads TotalSegmentator-style subjects into the same `CanonicalVolume`

All subsequent stages operate only on `CanonicalVolume`.

## CLI

```bash
python -m pipeline.cli discover <root>
python -m pipeline.cli validate <path>
python -m pipeline.cli build <path> [--output assets] [--config config.json]
python -m pipeline.cli verify <assets_dir>
```

## Tests

```bash
cd pipeline
pytest tests/
```

## Current Coverage

- Canonical volume model
- DICOM series loading + basic spatial validation
- NIfTI loading + orientation
- Window / crop / mesh generation
- End-to-end asset package + verification
- Initial unit tests for hard cases (duplicates, spacing, missing assets, etc.)

Next: expand the test suite with more malformed DICOM fixtures and orientation edge cases.
