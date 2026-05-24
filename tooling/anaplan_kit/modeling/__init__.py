"""``anaplan_kit.modeling`` — offline modeling tools (no tenant required).

These helpers operationalize the kit's conventions (DISCO module types, naming
rules, formula gotchas, sizing) as *pure local logic*. Nothing here makes a
network call: a modeler can scaffold, lint and size a new feature entirely
offline before ever touching a live model.

Public API::

    from anaplan_kit.modeling import (
        Disco, LineItem, Module, Feature, Finding,
        check_formula, lint_module, lint_feature,
        cell_count, estimate_module, size_report,
        render_module, parse_blueprint,
        scaffold_module, scaffold_feature,
    )
"""

from __future__ import annotations

from .blueprint import parse_blueprint, render_module
from .formula import KNOWN_FUNCTIONS, check_formula
from .lint import has_errors, lint_feature, lint_module
from .model import Disco, Feature, Finding, LineItem, Module
from .scaffold import scaffold_feature, scaffold_module
from .sizing import cell_count, estimate_module, size_report

__all__ = [
    # model
    "Disco",
    "LineItem",
    "Module",
    "Feature",
    "Finding",
    # formula
    "check_formula",
    "KNOWN_FUNCTIONS",
    # lint
    "lint_module",
    "lint_feature",
    "has_errors",
    # sizing
    "cell_count",
    "estimate_module",
    "size_report",
    # blueprint
    "render_module",
    "parse_blueprint",
    # scaffold
    "scaffold_module",
    "scaffold_feature",
]
