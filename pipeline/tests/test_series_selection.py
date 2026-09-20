"""Multiple CT series selection rules."""

from types import SimpleNamespace
from dicom.series_select import select_ct_series


def make_series(uid, n_slices, modality="CT"):
    return [SimpleNamespace(Modality=modality, SeriesInstanceUID=uid) for _ in range(n_slices)]


def test_selects_largest_series():
    series_map = {
        "uid-a": make_series("uid-a", 10),
        "uid-b": make_series("uid-b", 25),
        "uid-c": make_series("uid-c", 5),
    }
    chosen, report = select_ct_series(series_map)
    assert chosen is not None
    assert len(chosen) == 25
    assert report.has_errors is False


def test_no_ct_series_is_error():
    series_map = {
        "uid-mr": make_series("uid-mr", 20, modality="MR"),
    }
    chosen, report = select_ct_series(series_map)
    assert chosen is None
    assert report.has_errors is True


def test_preferred_uid():
    series_map = {
        "uid-a": make_series("uid-a", 10),
        "uid-b": make_series("uid-b", 25),
    }
    chosen, report = select_ct_series(series_map, preferred_uid="uid-a")
    assert chosen is not None
    assert len(chosen) == 10


def test_tie_break_is_stable():
    series_map = {
        "uid-b": make_series("uid-b", 10),
        "uid-a": make_series("uid-a", 10),
    }
    chosen, report = select_ct_series(series_map)
    assert chosen is not None
    # smaller UID wins on tie
    assert chosen[0].SeriesInstanceUID == "uid-a"
    assert any(m.code == "SERIES_TIE" for m in report.warnings)
