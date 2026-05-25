"""Offline tests for blueprint render / parse round-trips."""

from __future__ import annotations

import pathlib

from anaplan_kit.modeling.blueprint import parse_blueprint, render_module
from anaplan_kit.modeling.model import Disco, LineItem, Module


def _sample_module() -> Module:
    return Module(
        name="CAL01 Revenue Calculation",
        disco=Disco.CALC,
        line_items=[
            LineItem(
                "Gross Revenue",
                "Number",
                "Sum",
                ["L3 Cost Centre", "Time", "Versions"],
                "Volume * Price",
            ),
            LineItem("Margin %", "Number (%)", None, ["L3 Cost Centre"], None),
        ],
    )


def test_render_contains_badge_heading_and_header():
    md = render_module(_sample_module())
    assert "**DISCO:** Calc" in md
    assert "## CAL01 Revenue Calculation" in md
    assert "| Line Item | Format | Summary | Applies To | Formula |" in md


def test_round_trip_recovers_line_items():
    m = _sample_module()
    parsed = parse_blueprint(render_module(m))
    assert len(parsed) == 1
    p = parsed[0]
    assert p.name == m.name
    assert p.disco == Disco.CALC
    assert len(p.line_items) == 2

    a, b = p.line_items
    assert a.name == "Gross Revenue"
    assert a.format == "Number"
    assert a.summary == "Sum"
    assert a.applies_to == ["L3 Cost Centre", "Time", "Versions"]
    assert a.formula == "Volume * Price"

    assert b.name == "Margin %"
    assert b.summary is None
    assert b.formula is None
    assert b.applies_to == ["L3 Cost Centre"]


def test_disco_inferred_from_prefix():
    for prefix, disco in [
        ("DAT01 X", Disco.DATA),
        ("INP01 X", Disco.INPUTS),
        ("SYS01 X", Disco.SYSTEM),
        ("CAL01 X", Disco.CALC),
        ("OUT01 X", Disco.OUTPUTS),
    ]:
        m = Module(
            name=prefix, disco=disco, line_items=[LineItem("A", "Number", "Sum", ["Time"], None)]
        )
        parsed = parse_blueprint(render_module(m))
        assert parsed[0].disco == disco


def test_parse_tolerates_prose_and_multiple_tables():
    md = """
Some intro prose here.

## INP01 Assumptions — **Inputs**

What planners type.

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Volume | Number | Sum | CC × Time | input |

More prose between tables.

## CAL01 Revenue — **Calculations**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Gross Revenue | Number | Sum | CC × Time | `Volume * Price` |
"""
    modules = parse_blueprint(md)
    assert len(modules) == 2
    assert modules[0].name == "INP01 Assumptions"
    assert modules[0].disco == Disco.INPUTS
    assert modules[1].name == "CAL01 Revenue"
    assert modules[1].disco == Disco.CALC
    # The trailing " — **Inputs**" annotation is stripped from the name.
    assert "Inputs" not in modules[0].name


def test_parse_real_blueprint_file_does_not_crash():
    here = pathlib.Path(__file__).resolve().parents[2]
    bp = here / "blueprints" / "fpa-pl-planning" / "modules.md"
    md = bp.read_text(encoding="utf-8")
    modules = parse_blueprint(md)
    # The real file has many tables; we should recover several modules.
    assert len(modules) >= 8
    # Every parsed module has at least one line item.
    assert all(m.line_items for m in modules)
