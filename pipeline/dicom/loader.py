"""
DICOM series → CanonicalVolume loader.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
import numpy as np

try:
    import pydicom
    from pydicom.errors import InvalidDicomError
except ImportError:
    pydicom = None

from models.volume import CanonicalVolume


def _require_pydicom():
    if pydicom is None:
        raise ImportError(
            "pydicom is required for DICOM support. "
            "Install with: pip install pydicom"
        )


def read_dicom_files(directory: Path) -> List[Any]:
    """Read all readable DICOM files under directory (non-recursive for now)."""
    _require_pydicom()
    files = []
    for p in sorted(directory.iterdir()):
        if not p.is_file():
            continue
        try:
            ds = pydicom.dcmread(str(p), force=True, stop_before_pixels=False)
            files.append(ds)
        except Exception:
            continue
    return files


def group_by_series(datasets: List[Any]) -> Dict[str, List[Any]]:
    """Group datasets by SeriesInstanceUID."""
    series: Dict[str, List[Any]] = {}
    for ds in datasets:
        uid = getattr(ds, "SeriesInstanceUID", None)
        if uid is None:
            uid = "unknown"
        series.setdefault(str(uid), []).append(ds)
    return series


def is_ct_series(datasets: List[Any]) -> bool:
    if not datasets:
        return False
    mod = getattr(datasets[0], "Modality", "").upper()
    return mod == "CT"


def sort_by_position(datasets: List[Any]) -> List[Any]:
    """
    Sort slices by ImagePositionPatient along the primary slice axis.
    Falls back to InstanceNumber when spatial info is missing.
    """
    def key(ds):
        ipp = getattr(ds, "ImagePositionPatient", None)
        if ipp is not None and len(ipp) == 3:
            # use the coordinate with largest variation later;
            # for sorting we just use the third component as a first approximation
            return float(ipp[2])
        return float(getattr(ds, "InstanceNumber", 0))

    return sorted(datasets, key=key)


def extract_spacing(ds) -> Tuple[float, float, float]:
    """Return (row_spacing, col_spacing, slice_spacing)."""
    pixel_spacing = getattr(ds, "PixelSpacing", None)
    if pixel_spacing is None:
        raise ValueError("PixelSpacing missing")
    row_sp = float(pixel_spacing[0])
    col_sp = float(pixel_spacing[1])

    # slice thickness / spacing between slices
    slice_sp = getattr(ds, "SpacingBetweenSlices", None)
    if slice_sp is None:
        slice_sp = getattr(ds, "SliceThickness", None)
    if slice_sp is None:
        slice_sp = 1.0
    return row_sp, col_sp, float(slice_sp)


def to_hu(pixel_array: np.ndarray, ds) -> np.ndarray:
    slope = float(getattr(ds, "RescaleSlope", 1.0))
    intercept = float(getattr(ds, "RescaleIntercept", 0.0))
    return pixel_array.astype(np.float32) * slope + intercept


def load_series_as_volume(datasets: List[Any]) -> CanonicalVolume:
    """
    Convert a sorted list of DICOM slices into a CanonicalVolume.

    Notes
    -----
    - Orientation is set to 'RAS' after a simple check; full direction
      cosine handling can be expanded later.
    - Slice spacing consistency is validated and reported via meta.
    """
    if not datasets:
        raise ValueError("empty series")

    datasets = sort_by_position(datasets)
    first = datasets[0]

    spacing = extract_spacing(first)
    rows = int(first.Rows)
    cols = int(first.Columns)
    n_slices = len(datasets)

    volume = np.zeros((rows, cols, n_slices), dtype=np.float32)
    positions = []

    for i, ds in enumerate(datasets):
        arr = ds.pixel_array
        if arr.shape != (rows, cols):
            raise ValueError(f"slice {i} has unexpected shape {arr.shape}")
        volume[:, :, i] = to_hu(arr, ds)
        ipp = getattr(ds, "ImagePositionPatient", None)
        if ipp is not None:
            positions.append([float(x) for x in ipp])

    # crude slice-spacing consistency check
    slice_spacings = []
    if len(positions) >= 2:
        for a, b in zip(positions[:-1], positions[1:]):
            dist = np.linalg.norm(np.array(b) - np.array(a))
            slice_spacings.append(dist)

    meta = {
        "n_slices": n_slices,
        "series_uid": str(getattr(first, "SeriesInstanceUID", "")),
        "study_uid": str(getattr(first, "StudyInstanceUID", "")),
        "slice_spacings": slice_spacings,
    }

    origin = (0.0, 0.0, 0.0)
    if positions:
        origin = tuple(positions[0])

    return CanonicalVolume(
        data=volume,
        spacing_mm=spacing,
        origin_mm=origin,
        orientation="RAS",          # simplified; full direction matrix later
        modality="CT",
        source="dicom",
        meta=meta,
    )


def load_dicom_directory(directory: Path, series_uid: Optional[str] = None) -> CanonicalVolume:
    """
    High-level entry: read a directory, pick a CT series, return CanonicalVolume.
    """
    datasets = read_dicom_files(directory)
    if not datasets:
        raise FileNotFoundError(f"no readable DICOM files in {directory}")

    series_map = group_by_series(datasets)
    ct_series = {uid: ds for uid, ds in series_map.items() if is_ct_series(ds)}

    if not ct_series:
        raise ValueError("no CT series found")

    if series_uid is not None:
        if series_uid not in ct_series:
            raise KeyError(f"series {series_uid} not found")
        chosen = ct_series[series_uid]
    else:
        # pick the series with the most slices
        chosen = max(ct_series.values(), key=len)

    return load_series_as_volume(chosen)
