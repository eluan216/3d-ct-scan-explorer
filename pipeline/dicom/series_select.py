"""
Deterministic CT series selection rules.
"""

from typing import Dict, List, Any, Optional, Tuple
from models.report import Report


def select_ct_series(
    series_map: Dict[str, List[Any]],
    preferred_uid: Optional[str] = None,
) -> Tuple[Optional[List[Any]], Report]:
    """
    Choose one CT series according to clear rules.

    Rules (in order):
    1. If preferred_uid is given and exists → use it
    2. Prefer the CT series with the largest number of slices
    3. If still tied, prefer the one with the smallest SeriesInstanceUID (stable)
    4. If no CT series → error
    """
    report = Report()

    ct_series = {}
    for uid, ds_list in series_map.items():
        if not ds_list:
            continue
        mod = getattr(ds_list[0], "Modality", "").upper()
        if mod == "CT":
            ct_series[uid] = ds_list

    if not ct_series:
        report.error("NO_CT_SERIES", "no CT series found in study")
        return None, report

    if preferred_uid is not None:
        if preferred_uid in ct_series:
            report.info("SERIES_SELECTED", f"using preferred series {preferred_uid[:18]}…")
            return ct_series[preferred_uid], report
        report.error("PREFERRED_MISSING", f"preferred series {preferred_uid} not found")
        return None, report

    # largest slice count, then stable UID tie-break
    ranked = sorted(
        ct_series.items(),
        key=lambda kv: (-len(kv[1]), kv[0]),
    )
    chosen_uid, chosen = ranked[0]

    if len(ranked) > 1 and len(ranked[0][1]) == len(ranked[1][1]):
        report.warning(
            "SERIES_TIE",
            f"multiple CT series with {len(chosen)} slices; selected {chosen_uid[:18]}… by UID order",
        )
    else:
        report.info("SERIES_SELECTED", f"selected series {chosen_uid[:18]}… ({len(chosen)} slices)")

    return chosen, report
