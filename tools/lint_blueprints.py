#!/usr/bin/env python3
"""Lint every blueprint under ``blueprints/`` with the Anaplan conventions linter.

Adds ``tooling/`` to ``sys.path`` so ``anaplan_kit`` is importable without
installing the package, and lints by absolute path so it works from any cwd.
Exit code is non-zero if the linter finds any ERROR (CI-friendly).

Usage::

    python tools/lint_blueprints.py
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "tooling"))

from anaplan_kit.modeling.cli import main  # noqa: E402  (after sys.path tweak)

if __name__ == "__main__":
    blueprints = os.path.normpath(os.path.join(_HERE, "..", "blueprints"))
    raise SystemExit(main(["lint", blueprints]))
