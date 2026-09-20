"""Tests for the structured Report helper."""

from models.report import Report, Severity


def test_report_has_errors():
    r = Report()
    assert r.has_errors is False
    r.warning("W1", "something odd")
    assert r.has_errors is False
    r.error("E1", "fatal")
    assert r.has_errors is True
    assert len(r.errors) == 1
    assert len(r.warnings) == 1


def test_report_summary():
    r = Report()
    r.info("I1", "ok")
    r.error("E1", "bad")
    text = r.summary()
    assert "INFO" in text
    assert "ERROR" in text
