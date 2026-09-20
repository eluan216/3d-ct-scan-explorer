# End-to-end runbook (TotalSegmentator example)

## 1. Data

Download the small TotalSegmentator subset (or your own DICOM series):

```bash
mkdir -p data/raw
cd data/raw
# Example – adjust URL/path as needed for the small subset zip
# curl -L -o small.zip "https://zenodo.org/records/10047263/files/Totalsegmentator_dataset_small_v201.zip?download=1"
# unzip small.zip
```

Expected layout per subject:

```
<data>/sXXXX/
  ct.nii.gz
  segmentations/
    liver.nii.gz
    spleen.nii.gz
    ...
```

## 2. Build

```bash
cd pipeline
source .venv/bin/activate
python -m pipeline.cli validate ../data/raw/<subject>
python -m pipeline.cli build ../data/raw/<subject> --output ../assets
python -m pipeline.cli verify ../assets
```

Confirm `assets/manifest.json`, `assets/volume/`, and `assets/meshes/*.glb` exist.

## 3. View

```bash
cd web
npm run dev
```

Inspect:

- [ ] 3D organs render and orbit correctly
- [ ] Structure toggles work
- [ ] Crosshair in one MPR plane updates the other two
- [ ] Slice indices stay within bounds at corners
- [ ] Metadata panel shows shape, spacing (mm), orientation, structure list
- [ ] Missing assets show a clear error (optional: rename volume.bin temporarily)

## 4. Record demo

Capture 20–40s covering 3D + MPR sync + visibility + controls + metadata.  
Save as `docs/demo.gif` (or mp4) and link from the root README.

## 5. Freeze

Do not add features after a clean run unless fixing a real defect found above.
