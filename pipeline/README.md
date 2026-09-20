# Pipeline

Modular CT processing pipeline.

## Input Adapters

- `dicom/` – series discovery, validation with severity levels, HU conversion → `CanonicalVolume`
- `nifti/` – TotalSegmentator-style subjects → same `CanonicalVolume`

Downstream stages never depend on the original format.

## Severity Levels

| Level   | Meaning                                      |
|---------|----------------------------------------------|
| ERROR   | Pipeline cannot safely continue              |
| WARNING | Pipeline can continue; issue is recorded     |
| INFO    | Normal decision or successful check          |

## CLI

```bash
python -m pipeline.cli discover <root>
python -m pipeline.cli validate <path>
python -m pipeline.cli build <path> [--output assets]
python -m pipeline.cli verify <assets_dir>
```

## Running Tests

```bash
cd pipeline
pip install -r requirements.txt
pip install pytest
pytest tests/ -v
```

## Test Focus

- Failure behaviour (duplicates, missing geometry, NaNs, empty masks)
- Severity classification (ERROR vs WARNING)
- CanonicalVolume invariants
- Asset package and manifest integrity
- Mesh edge cases (empty label, tiny components)
- Both DICOM-style synthetic data and NIfTI paths

## Status

Core happy path and many failure cases are covered. Additional real-world DICOM fixtures can be added later without changing the adapter boundary.
