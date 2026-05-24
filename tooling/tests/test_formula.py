"""Offline tests for the formula static checks."""

from __future__ import annotations

from anaplan_kit.modeling.formula import KNOWN_FUNCTIONS, check_formula


def _codes(findings):
    return {f.code for f in findings}


def test_empty_formula_yields_nothing():
    assert check_formula("") == []
    assert check_formula("   ") == []
    assert check_formula(None) == []


def test_ancestor_is_banned():
    findings = check_formula("ANCESTOR(ITEM(L3 Cost Centre))")
    assert "BANNED_FUNCTION" in _codes(findings)


def test_isancestor_is_allowed():
    findings = check_formula("ISANCESTOR(Parent, Child)")
    assert "BANNED_FUNCTION" not in _codes(findings)


def test_children_is_banned():
    findings = check_formula("CHILDREN(ITEM(L2 Product))")
    assert "BANNED_FUNCTION" in _codes(findings)


def test_bracket_next_is_invalid():
    findings = check_formula("Sales[NEXT: 1]")
    assert "BRACKET_OFFSET" in _codes(findings)


def test_bracket_lag_offset_previous_invalid():
    assert "BRACKET_OFFSET" in _codes(check_formula("X[LAG: 2]"))
    assert "BRACKET_OFFSET" in _codes(check_formula("X[OFFSET: -1]"))
    assert "BRACKET_OFFSET" in _codes(check_formula("X[PREVIOUS: 1]"))


def test_function_form_offsets_are_ok():
    findings = check_formula("LAG(Sales, 1, 0)")
    assert "BRACKET_OFFSET" not in _codes(findings)


def test_single_keyword_multi_mapping_is_error():
    findings = check_formula("Source.LI[SUM: MapA, MapB]")
    assert "MULTI_MAPPING" in _codes(findings)


def test_double_keyword_mapping_is_ok():
    findings = check_formula("Source.LI[SUM: MapA, SUM: MapB]")
    assert "MULTI_MAPPING" not in _codes(findings)


def test_lookup_multi_mapping_error():
    findings = check_formula("Source.LI[LOOKUP: MapA, MapB]")
    assert "MULTI_MAPPING" in _codes(findings)


def test_unbalanced_parens():
    assert "UNBALANCED" in _codes(check_formula("SUM(Sales"))
    assert "UNBALANCED" in _codes(check_formula("Sales)"))


def test_unbalanced_brackets():
    assert "UNBALANCED" in _codes(check_formula("Source.LI[SUM: Map"))


def test_unbalanced_quote():
    assert "UNBALANCED" in _codes(check_formula("Versions.'Actual"))


def test_contraction_apostrophe_not_unbalanced():
    # English apostrophes in prose/description cells must not trip the quote check.
    assert "UNBALANCED" not in _codes(check_formula("the entity's local currency"))
    assert "UNBALANCED" not in _codes(check_formula("don't double-count children"))


def test_real_item_quote_balanced_pair_not_unbalanced():
    # A balanced Anaplan item quote is still recognised (no UNBALANCED finding).
    assert "UNBALANCED" not in _codes(check_formula("X = Versions.'Actual'"))


def test_balanced_complex_is_clean_of_unbalanced():
    findings = check_formula(
        "IF ISBLANK(Sales) THEN 0 ELSE Source.LI[LOOKUP: Map]"
    )
    assert "UNBALANCED" not in _codes(findings)


def test_select_warns_hardcoded():
    findings = check_formula("CAL04.P&L Amount[SELECT: Versions.Actual]")
    assert "HARDCODED_ITEM" in _codes(findings)


def test_dot_quote_warns_hardcoded():
    findings = check_formula("X = Versions.'Actual'")
    assert "HARDCODED_ITEM" in _codes(findings)


def test_nested_if_depth_over_three_warns():
    formula = "IF a THEN IF b THEN IF c THEN IF d THEN 1 ELSE 2 ELSE 3 ELSE 4 ELSE 5"
    findings = check_formula(formula)
    assert "NESTED_IF" in _codes(findings)


def test_shallow_if_chain_no_nested_warning():
    formula = "IF a THEN 1 ELSE IF b THEN 2 ELSE IF c THEN 3 ELSE 4"
    findings = check_formula(formula)
    assert "NESTED_IF" not in _codes(findings)


def test_unknown_function_is_info_not_error():
    findings = check_formula("FOOBAR(Sales)")
    assert "UNKNOWN_FUNCTION" in _codes(findings)
    assert all(f.severity != "ERROR" for f in findings if f.code == "UNKNOWN_FUNCTION")


def test_known_function_no_unknown_info():
    findings = check_formula("ROUND(Sales, 2)")
    assert "UNKNOWN_FUNCTION" not in _codes(findings)


def test_known_functions_sourced_from_cheatsheet():
    # A representative spread from the cheatsheet categories.
    for fn in ("SUM", "LOOKUP", "LAG", "CURRENTPERIODSTART", "ISANCESTOR", "RANK"):
        assert fn in KNOWN_FUNCTIONS


def test_location_is_propagated():
    findings = check_formula("ANCESTOR(x)", location="CAL01 → Foo")
    assert findings[0].location == "CAL01 → Foo"
