"""Offline tests for cell-count sizing."""

from __future__ import annotations

from anaplan_kit.modeling.model import Disco, LineItem, Module
from anaplan_kit.modeling.sizing import cell_count, estimate_module, size_report


def test_cell_count_product():
    assert cell_count({"A": 10, "B": 5}, 3) == 150


def test_cell_count_empty_dims_is_line_items():
    assert cell_count({}, 7) == 7


def test_cell_count_single_dim():
    assert cell_count({"Time": 36}, 20) == 720


def test_estimate_module_uses_union_of_applies_to():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[
            LineItem("A", "Number", "Sum", ["L3 Cost Centre", "Time"], None),
            LineItem("B", "Number", "Sum", ["Time", "Versions"], None),
        ],
    )
    sizes = {"L3 Cost Centre": 500, "Time": 36, "Versions": 3, "Unused": 99}
    # Union of dims = {CC, Time, Versions}; "Unused" not referenced so dropped.
    assert estimate_module(m, sizes) == 500 * 36 * 3 * 2


def test_estimate_module_ignores_dims_without_sizes():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("A", "Number", "Sum", ["Time", "Product"], None)],
    )
    # Only Time has a supplied size.
    assert estimate_module(m, {"Time": 36}) == 36


def test_size_report_under_threshold_no_warning():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("A", "Number", "Sum", ["Time"], None)],
    )
    count, findings = size_report(m, {"Time": 36})
    assert count == 36
    assert findings == []


def test_size_report_over_threshold_warns():
    m = Module(
        name="CAL01 Big",
        disco=Disco.CALC,
        line_items=[LineItem("A", "Number", "Sum", ["CC", "Time", "Product"], None)],
    )
    sizes = {"CC": 5000, "Time": 36, "Product": 200}
    count, findings = size_report(m, sizes, threshold=10_000_000)
    assert count == 5000 * 36 * 200
    assert any(f.code == "LARGE_MODULE" and f.severity == "WARN" for f in findings)


def test_size_report_custom_threshold():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("A", "Number", "Sum", ["Time"], None)],
    )
    _, findings = size_report(m, {"Time": 36}, threshold=10)
    assert any(f.code == "LARGE_MODULE" for f in findings)
