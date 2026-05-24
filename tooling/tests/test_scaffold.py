"""Offline tests for scaffolding."""

from __future__ import annotations

from anaplan_kit.modeling.blueprint import parse_blueprint
from anaplan_kit.modeling.lint import has_errors, lint_module
from anaplan_kit.modeling.model import Disco, LineItem
from anaplan_kit.modeling.scaffold import scaffold_feature, scaffold_module


def test_scaffold_feature_has_all_five_disco_prefixes():
    files = scaffold_feature("Headcount Bonus")
    blob = "\n".join(files.values())
    for prefix in ("DAT01", "INP01", "SYS01", "CAL01", "OUT01"):
        assert prefix in blob


def test_scaffold_feature_time_settings_named_sys01():
    files = scaffold_feature("X")
    assert "SYS01 Time Settings" in files["SYS01-time-settings.md"]
    assert "SYS00" not in "\n".join(files.values())


def test_scaffold_feature_uses_is_actual_not_is_actual_month():
    files = scaffold_feature("X")
    blob = "\n".join(files.values())
    assert "Is Actual?" in blob
    assert "Is Actual Month?" not in blob


def test_scaffold_feature_includes_readme():
    files = scaffold_feature("Headcount Bonus")
    assert "README.md" in files
    assert "Headcount Bonus" in files["README.md"]


def test_scaffold_feature_modules_lint_clean():
    files = scaffold_feature("X")
    # Each generated module blueprint should parse and lint without errors.
    for filename, md in files.items():
        if filename == "README.md":
            continue
        for module in parse_blueprint(md):
            assert not has_errors(lint_module(module)), filename


def test_scaffold_module_default_placeholders():
    md = scaffold_module("CAL01 Revenue", Disco.CALC, ["Time"])
    assert "## CAL01 Revenue" in md
    assert "Placeholder" in md


def test_scaffold_module_provided_line_items_get_dims():
    items = [LineItem("Revenue", "Number", "Sum")]
    md = scaffold_module("CAL01 Revenue", Disco.CALC, ["L3 Cost Centre", "Time"], items)
    modules = parse_blueprint(md)
    assert modules[0].line_items[0].applies_to == ["L3 Cost Centre", "Time"]


def test_scaffold_module_disco_badge():
    md = scaffold_module("OUT01 Report", Disco.OUTPUTS, ["Time"])
    assert "**DISCO:** Outputs" in md
