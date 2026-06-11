"""MCP server exposing the Anaplan Data Modeler Kit to AI agents.

Runs over **stdio** via the ``anaplan-kit-mcp`` console script (install the
``[mcp]`` extra). Two tool families:

* **Offline knowledge tools** — search/read the kit's Markdown (docs, cookbook,
  blueprints, tutorials, exercises), look up the formula reference, list
  cookbook recipes, and lint blueprint tables with the kit's real conventions
  linter. Pure local logic; always available.
* **Live Anaplan API tools** — thin wrappers over :class:`~anaplan_kit.AnaplanClient`
  (auth, metadata, imports/exports, actions). Credentials come from environment
  variables only (``ANAPLAN_EMAIL`` / ``ANAPLAN_PASSWORD`` plus optional
  ``ANAPLAN_WORKSPACE_ID`` / ``ANAPLAN_MODEL_ID``).

**Offline honesty invariant (load-bearing):** when credentials are not
configured, every live tool returns
``{"mode": "offline", "error": "no Anaplan credentials configured"}`` —
without raising and without attempting any network I/O. The public bot this
server backs runs with no credentials and must never pretend it touched a
tenant. Nothing in this module performs network access at import time.
"""

from __future__ import annotations

import os
from typing import Any

from mcp.server.fastmcp import FastMCP

from . import kitindex
from .auth import DEFAULT_AUTH_URL
from .client import DEFAULT_API_BASE, AnaplanClient
from .errors import AnaplanError
from .kitindex import KitRootNotFoundError
from .modeling.blueprint import parse_blueprint
from .modeling.lint import lint_module

ENV_EMAIL = "ANAPLAN_EMAIL"
ENV_PASSWORD = "ANAPLAN_PASSWORD"  # noqa: S105 - env var *name*, not a secret
ENV_WORKSPACE = "ANAPLAN_WORKSPACE_ID"
ENV_MODEL = "ANAPLAN_MODEL_ID"
# Endpoint overrides (used by offline tests; default to the public services).
ENV_AUTH_URL = "ANAPLAN_AUTH_URL"
ENV_API_BASE = "ANAPLAN_API_BASE"

_NO_CREDENTIALS = "no Anaplan credentials configured"

mcp = FastMCP("anaplan-kit")


# --- helpers -----------------------------------------------------------------


def _kit_root_error(exc: KitRootNotFoundError) -> dict[str, Any]:
    return {"error": str(exc), "hint": f"set {kitindex.ENV_ROOT} to the anaplan-kit checkout"}


def _offline_response() -> dict[str, Any]:
    """The structured no-credentials answer every live tool must return."""
    return {
        "mode": "offline",
        "error": _NO_CREDENTIALS,
        "hint": f"set {ENV_EMAIL} and {ENV_PASSWORD} in the server's environment to go live",
    }


def _live_client() -> AnaplanClient | None:
    """An :class:`AnaplanClient` from env credentials, or ``None`` when absent.

    Construction performs no network I/O — the first API call authenticates.
    """
    email = os.environ.get(ENV_EMAIL)
    password = os.environ.get(ENV_PASSWORD)
    if not email or not password:
        return None
    return AnaplanClient.from_credentials(
        email=email,
        password=password,
        auth_url=os.environ.get(ENV_AUTH_URL, DEFAULT_AUTH_URL),
        api_base=os.environ.get(ENV_API_BASE, DEFAULT_API_BASE),
    )


def _live_error(exc: AnaplanError) -> dict[str, Any]:
    """A structured (never-raising) report of a live API failure."""
    return {"mode": "live", "error": f"{type(exc).__name__}: {exc}"}


def _resolved_ids(
    workspace_id: str | None, model_id: str | None = None
) -> tuple[str | None, str | None]:
    """Fill missing workspace/model IDs from the environment."""
    return (
        workspace_id or os.environ.get(ENV_WORKSPACE) or None,
        model_id or os.environ.get(ENV_MODEL) or None,
    )


def _missing_id_error(name: str, env_var: str) -> dict[str, Any]:
    return {
        "mode": "live",
        "error": f"missing {name}: pass it as an argument or set {env_var}",
    }


# --- offline knowledge tools ---------------------------------------------------


@mcp.tool()
def search_kit(query: str, area: str | None = None, limit: int = 8) -> dict[str, Any]:
    """Search the Anaplan kit's docs, cookbook, blueprints, tutorials and exercises.

    Ranked keyword search (offline, no embeddings). Use `area` to narrow by
    path, e.g. "formulas", "cookbook", "methodology", "time-and-forecasting".
    Returns {path, title, heading, snippet, score} per hit — follow up with
    read_kit_doc(path) for the full document.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    results = kitindex.search(root, query, area=area, limit=limit)
    return {"query": query, "area": area, "results": results}


@mcp.tool()
def read_kit_doc(path: str, max_chars: int = 20000) -> dict[str, Any]:
    """Read one kit document by repo-relative path (e.g. "cookbook/README.md").

    Only Markdown files inside the kit can be read; long documents are
    truncated at max_chars (the response says so via "truncated": true).
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    try:
        return kitindex.read_doc(root, path, max_chars=max_chars)
    except (ValueError, FileNotFoundError) as exc:
        return {"error": str(exc), "path": path}


@mcp.tool()
def formula_reference(function_name: str) -> dict[str, Any]:
    """Look up an Anaplan function (e.g. CUMULATE, LOOKUP, SUM) in the kit's
    Anapedia-validated formula reference.

    Returns syntax, usage notes and the source doc path. If the function is
    unknown, returns the closest-matching function names instead.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    return kitindex.formula_lookup(root, function_name)


@mcp.tool()
def list_recipes(area: str | None = None) -> dict[str, Any]:
    """List the kit's cookbook recipes: title, one-line description, path, level.

    Optionally filter by area (e.g. "time-and-forecasting", "Data & Imports",
    "security"). Recipes are ready-to-use blueprints for real modeling tasks.
    """
    try:
        root = kitindex.find_kit_root()
    except KitRootNotFoundError as exc:
        return _kit_root_error(exc)
    recipes = kitindex.list_recipes(root, area=area)
    return {"area": area, "count": len(recipes), "recipes": recipes}


@mcp.tool()
def lint_blueprint(content: str) -> dict[str, Any]:
    """Lint Anaplan blueprint Markdown against the kit's modeling conventions.

    Parses every canonical "| Line Item | Format | Summary | Applies To |
    Formula |" table in the text and runs the kit's real linter (DISCO naming,
    summaries, banned functions, formula hygiene). Returns structured findings
    with severity ERROR/WARN/INFO and stable codes.
    """
    modules = parse_blueprint(content or "")
    findings: list[dict[str, Any]] = []
    counts = {"ERROR": 0, "WARN": 0, "INFO": 0}
    for module in modules:
        for finding in lint_module(module):
            counts[finding.severity] += 1
            findings.append(
                {
                    "severity": finding.severity,
                    "code": finding.code,
                    "message": finding.message,
                    "location": finding.location,
                }
            )
    return {
        "modules_parsed": len(modules),
        "module_names": [m.name or "<unnamed>" for m in modules],
        "findings": findings,
        "counts": counts,
        "ok": counts["ERROR"] == 0,
    }


# --- live Anaplan API tools ----------------------------------------------------


@mcp.tool()
def anaplan_connection_status() -> dict[str, Any]:
    """Report whether live Anaplan credentials are configured (never reveals values).

    mode "live" means ANAPLAN_EMAIL + ANAPLAN_PASSWORD are set; "offline"
    means live tools will refuse to run. Also reports whether default
    workspace/model IDs are configured.
    """
    email_set = bool(os.environ.get(ENV_EMAIL))
    password_set = bool(os.environ.get(ENV_PASSWORD))
    return {
        "mode": "live" if (email_set and password_set) else "offline",
        "configured": {
            ENV_EMAIL: email_set,
            ENV_PASSWORD: password_set,
            ENV_WORKSPACE: bool(os.environ.get(ENV_WORKSPACE)),
            ENV_MODEL: bool(os.environ.get(ENV_MODEL)),
        },
        "note": "credential values are never revealed; without credentials the live "
        "tools return mode=offline instead of contacting Anaplan",
    }


@mcp.tool()
def anaplan_list_workspaces() -> dict[str, Any]:
    """List Anaplan workspaces the configured account can access (live API)."""
    client = _live_client()
    if client is None:
        return _offline_response()
    try:
        return {"mode": "live", "workspaces": client.list_workspaces()}
    except AnaplanError as exc:
        return _live_error(exc)


@mcp.tool()
def anaplan_list_models(workspace_id: str | None = None) -> dict[str, Any]:
    """List Anaplan models in a workspace (live API).

    workspace_id defaults to the ANAPLAN_WORKSPACE_ID environment variable.
    """
    client = _live_client()
    if client is None:
        return _offline_response()
    workspace_id, _ = _resolved_ids(workspace_id)
    if not workspace_id:
        return _missing_id_error("workspace_id", ENV_WORKSPACE)
    try:
        return {
            "mode": "live",
            "workspace_id": workspace_id,
            "models": client.list_models(workspace_id),
        }
    except AnaplanError as exc:
        return _live_error(exc)


@mcp.tool()
def anaplan_model_metadata(
    model_id: str | None = None, workspace_id: str | None = None
) -> dict[str, Any]:
    """List a model's files, imports, exports, actions and processes (live API).

    IDs default to ANAPLAN_WORKSPACE_ID / ANAPLAN_MODEL_ID. This is the
    discovery call to find the IDs that anaplan_run_* tools need.
    """
    client = _live_client()
    if client is None:
        return _offline_response()
    workspace_id, model_id = _resolved_ids(workspace_id, model_id)
    if not workspace_id:
        return _missing_id_error("workspace_id", ENV_WORKSPACE)
    if not model_id:
        return _missing_id_error("model_id", ENV_MODEL)
    try:
        return {
            "mode": "live",
            "workspace_id": workspace_id,
            "model_id": model_id,
            "files": client.list_files(workspace_id, model_id),
            "imports": client.list_imports(workspace_id, model_id),
            "exports": client.list_exports(workspace_id, model_id),
            "actions": client.list_actions(workspace_id, model_id),
            "processes": client.list_processes(workspace_id, model_id),
        }
    except AnaplanError as exc:
        return _live_error(exc)


def _run_live_task(
    resource: str,
    resource_id: str,
    workspace_id: str | None,
    model_id: str | None,
) -> dict[str, Any]:
    """Shared run-and-wait path for actions/imports/exports/processes."""
    client = _live_client()
    if client is None:
        return _offline_response()
    workspace_id, model_id = _resolved_ids(workspace_id, model_id)
    if not workspace_id:
        return _missing_id_error("workspace_id", ENV_WORKSPACE)
    if not model_id:
        return _missing_id_error("model_id", ENV_MODEL)
    try:
        task = client.run_action_and_wait(workspace_id, model_id, resource, resource_id)
    except AnaplanError as exc:
        return _live_error(exc)
    return {
        "mode": "live",
        "workspace_id": workspace_id,
        "model_id": model_id,
        "resource": resource,
        "resource_id": resource_id,
        "task": task,
    }


@mcp.tool()
def anaplan_run_action(
    action_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run a generic Anaplan action (e.g. delete-from-list) and wait for it (live API).

    IDs default to ANAPLAN_WORKSPACE_ID / ANAPLAN_MODEL_ID.
    """
    return _run_live_task("actions", action_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_import(
    import_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan import action and wait for completion (live API).

    The import's source file must already hold the data to load.
    """
    return _run_live_task("imports", import_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_export(
    export_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan export action and wait for completion (live API).

    Produces the export file inside Anaplan; downloading it is a separate
    (file-transfer) step not exposed by this server.
    """
    return _run_live_task("exports", export_id, workspace_id, model_id)


@mcp.tool()
def anaplan_run_process(
    process_id: str, workspace_id: str | None = None, model_id: str | None = None
) -> dict[str, Any]:
    """Run an Anaplan process (ordered group of actions) and wait for it (live API)."""
    return _run_live_task("processes", process_id, workspace_id, model_id)


def main() -> None:
    """Entry point for the ``anaplan-kit-mcp`` console script (stdio transport)."""
    mcp.run()


if __name__ == "__main__":  # pragma: no cover
    main()
