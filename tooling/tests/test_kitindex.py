"""Tests for the offline kit index (search, doc reads, formula reference, recipes).

Everything here is pure local file reading over the repo's own Markdown — no
network, no tenant, no mocking needed.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from anaplan_kit import kitindex
from anaplan_kit.kitindex import KitRootNotFoundError

REPO_ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture(autouse=True)
def _pin_kit_root(monkeypatch: pytest.MonkeyPatch) -> None:
    """Pin the kit root to this checkout so tests are deterministic."""
    monkeypatch.setenv(kitindex.ENV_ROOT, str(REPO_ROOT))


# --- root discovery ---------------------------------------------------------


def test_find_kit_root_from_env() -> None:
    assert kitindex.find_kit_root() == REPO_ROOT.resolve()


def test_find_kit_root_env_invalid(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv(kitindex.ENV_ROOT, str(tmp_path))
    with pytest.raises(KitRootNotFoundError):
        kitindex.find_kit_root()


def test_find_kit_root_walkup(monkeypatch: pytest.MonkeyPatch) -> None:
    # Without the env var the root is found by walking up from the package
    # (editable install) or the cwd (CI runs pytest from tooling/).
    monkeypatch.delenv(kitindex.ENV_ROOT, raising=False)
    root = kitindex.find_kit_root()
    assert (root / "cookbook").is_dir()
    assert (root / "SOURCES.md").is_file()


# --- search -------------------------------------------------------------------


def test_search_finds_cumulate_in_formula_docs() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "CUMULATE running total")
    assert results, "expected at least one hit"
    paths = [r["path"] for r in results]
    assert any("docs/02-formulas" in p for p in paths)
    top = results[0]
    assert set(top) == {"path", "title", "heading", "snippet", "score"}
    assert top["score"] >= results[-1]["score"]  # ranked, best first


def test_search_finds_data_hub_recipe() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "data hub", limit=8)
    assert any("data-hub" in r["path"] or "data_hub" in r["path"] for r in results)


def test_search_area_filter_restricts_paths() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "forecast", area="cookbook")
    assert results
    assert all(r["path"].startswith("cookbook/") for r in results)


def test_search_empty_query_returns_nothing() -> None:
    assert kitindex.search(kitindex.find_kit_root(), "   ") == []


def test_search_respects_limit() -> None:
    results = kitindex.search(kitindex.find_kit_root(), "module", limit=3)
    assert len(results) <= 3


# --- read_doc ------------------------------------------------------------------


def test_read_doc_returns_content() -> None:
    doc = kitindex.read_doc(kitindex.find_kit_root(), "cookbook/README.md")
    assert doc["path"] == "cookbook/README.md"
    assert "Cookbook" in doc["content"]
    assert doc["truncated"] is False


def test_read_doc_truncates() -> None:
    doc = kitindex.read_doc(kitindex.find_kit_root(), "README.md", max_chars=50)
    assert len(doc["content"]) == 50
    assert doc["truncated"] is True
    assert doc["total_chars"] > 50


def test_read_doc_rejects_path_escape() -> None:
    root = kitindex.find_kit_root()
    with pytest.raises(ValueError):
        kitindex.read_doc(root, "../../../etc/passwd.md")
    with pytest.raises(ValueError):
        kitindex.read_doc(root, "docs/../../outside.md")


def test_read_doc_rejects_absolute_path() -> None:
    with pytest.raises(ValueError):
        kitindex.read_doc(kitindex.find_kit_root(), "/etc/passwd.md")


def test_read_doc_rejects_non_markdown() -> None:
    with pytest.raises(ValueError):
        kitindex.read_doc(kitindex.find_kit_root(), "tooling/pyproject.toml")


def test_read_doc_missing_file() -> None:
    with pytest.raises(FileNotFoundError):
        kitindex.read_doc(kitindex.find_kit_root(), "docs/does-not-exist.md")


# --- formula reference -----------------------------------------------------------


def test_formula_lookup_finds_cumulate() -> None:
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "CUMULATE")
    assert result["found"] is True
    match = result["matches"][0]
    assert match["path"].startswith("docs/02-formulas/")
    assert "CUMULATE" in (match["syntax"] or "")
    assert match["content"]


def test_formula_lookup_is_case_insensitive_and_tolerates_parens() -> None:
    assert kitindex.formula_lookup(kitindex.find_kit_root(), "cumulate()")["found"] is True


def test_formula_lookup_unknown_returns_closest() -> None:
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "CUMULAT")
    assert result["found"] is False
    assert "CUMULATE" in result["closest"]


def test_formula_lookup_handles_combined_headings() -> None:
    # "### START / END" defines two functions in one heading.
    result = kitindex.formula_lookup(kitindex.find_kit_root(), "END")
    assert result["found"] is True


# --- cookbook recipes -------------------------------------------------------------


def test_list_recipes_returns_every_recipe_with_fields() -> None:
    recipes = kitindex.list_recipes(kitindex.find_kit_root())
    assert len(recipes) > 10
    for recipe in recipes:
        assert recipe["path"].startswith("cookbook/")
        assert recipe["title"]
        assert recipe["description"]


def test_list_recipes_area_filter() -> None:
    recipes = kitindex.list_recipes(kitindex.find_kit_root(), area="time-and-forecasting")
    assert recipes
    assert all(r["path"].startswith("cookbook/time-and-forecasting/") for r in recipes)
