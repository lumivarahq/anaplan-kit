"""Offline tests for module / feature linting."""

from __future__ import annotations

from anaplan_kit.modeling.lint import has_errors, lint_feature, lint_module
from anaplan_kit.modeling.model import Disco, Feature, LineItem, Module


def _codes(findings):
    return {f.code for f in findings}


def _clean_module() -> Module:
    return Module(
        name="CAL01 Revenue",
        disco=Disco.CALC,
        line_items=[
            LineItem(
                "Gross Revenue", "Number", "Sum", ["L3 Cost Centre", "Time"], "Volume * Price"
            ),
            LineItem("Margin %", "Number (%)", "None", ["L3 Cost Centre"], None),
        ],
    )


def _dirty_module() -> Module:
    # SYS00 (should be SYS01), 'Is Actual Month?' (should be 'Is Actual?'),
    # a numeric line item with no summary, and a banned ANCESTOR() function.
    return Module(
        name="SYS00 Time Settings",
        disco=Disco.SYSTEM,
        line_items=[
            LineItem("Is Actual Month?", "Boolean", None, ["Time"], None),
            LineItem("Period Index", "Number", None, ["Time"], None),
            LineItem(
                "Parent CC", "List", None, ["L3 Cost Centre"], "ANCESTOR(ITEM(L3 Cost Centre))"
            ),
        ],
    )


def test_clean_module_has_no_errors():
    findings = lint_module(_clean_module())
    assert not has_errors(findings)


def test_dirty_module_finding_codes():
    findings = lint_module(_dirty_module())
    codes = _codes(findings)
    assert "SYS00_TIME" in codes
    assert "IS_ACTUAL_NAME" in codes
    assert "MISSING_SUMMARY" in codes
    assert "BANNED_FUNCTION" in codes


def test_bad_prefix_is_error():
    m = Module(name="CAL01 Revenue", disco=Disco.INPUTS, line_items=[])
    findings = lint_module(m)
    assert "BAD_PREFIX" in _codes(findings)
    assert has_errors(findings)


def test_correct_prefix_no_bad_prefix():
    m = Module(name="INP01 Assumptions", disco=Disco.INPUTS, line_items=[])
    assert "BAD_PREFIX" not in _codes(lint_module(m))


def test_empty_line_item_name_is_error():
    m = Module(
        name="INP01 Assumptions",
        disco=Disco.INPUTS,
        line_items=[LineItem("", "Number", "Sum", ["Time"], None)],
    )
    findings = lint_module(m)
    assert "EMPTY_NAME" in _codes(findings)
    assert has_errors(findings)


def test_numeric_missing_summary_default_warns():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("Val", "Number", "default", ["Time"], None)],
    )
    assert "MISSING_SUMMARY" in _codes(lint_module(m))


def test_numeric_with_summary_no_warning():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("Val", "Number", "Sum", ["Time"], None)],
    )
    assert "MISSING_SUMMARY" not in _codes(lint_module(m))


def test_formula_findings_get_module_arrow_location():
    m = Module(
        name="CAL01 X",
        disco=Disco.CALC,
        line_items=[LineItem("Val", "Number", "Sum", ["Time"], "ANCESTOR(x)")],
    )
    findings = lint_module(m)
    banned = [f for f in findings if f.code == "BANNED_FUNCTION"]
    assert banned
    assert banned[0].location == "CAL01 X → Val"


def test_unnamed_module_is_info_not_error():
    # A blueprint table the parser couldn't name must not raise a hard error.
    m = Module(name="", disco=Disco.CALC, line_items=[])
    findings = lint_module(m)
    assert "UNNAMED_MODULE" in _codes(findings)
    assert "BAD_PREFIX" not in _codes(findings)
    assert not has_errors(findings)


def test_lint_feature_merges_modules():
    feat = Feature(name="F", modules=[_clean_module(), _dirty_module()])
    findings = lint_feature(feat)
    assert has_errors(findings)  # the dirty module brings a banned function
    assert "SYS00_TIME" in _codes(findings)
