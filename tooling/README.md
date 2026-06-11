# `anaplan_kit` — Python client for the Anaplan REST API v2

A small, typed, well-documented Python package that wraps the **Anaplan
Integration API v2.0**: authentication, listing workspace/model metadata,
chunked file upload/download, and running imports / exports / actions /
processes as asynchronous (start-then-poll) tasks.

It is the only *runnable* code in this kit. For the conceptual walkthrough of
the same API, read [`../docs/04-integration/rest-api.md`](../docs/04-integration/rest-api.md).

> ⚠️ **Educational — needs a real Anaplan tenant + credentials to run live.**
> Anaplan is a SaaS platform; there is no offline tenant. The example scripts
> make real network calls and do nothing useful without a valid Anaplan
> account, workspace and model. **Credentials are read from environment
> variables and are never hard-coded or committed.** The test suite, by
> contrast, runs **fully offline** by mocking HTTP — no tenant required.

## What's inside

| File | Purpose |
| --- | --- |
| `anaplan_kit/errors.py` | Exception hierarchy (`AnaplanError` + subclasses) |
| `anaplan_kit/auth.py` | `Authenticator` / `AuthToken`: basic-auth login, token cache + refresh |
| `anaplan_kit/client.py` | `AnaplanClient`: session, `_request` with error handling, JSON parsing, retry |
| `anaplan_kit/metadata.py` | `list_workspaces`, `list_models`, `list_files/imports/exports/actions/processes` |
| `anaplan_kit/imports_exports.py` | chunked `upload_file` / `download_export`, `run_import`, `run_export`, and the single `run_action_and_wait` / `poll_task` lifecycle |
| `anaplan_kit/actions.py` | `run_process` (+ generic action), reusing the shared polling logic |
| `anaplan_kit/kitindex.py` | offline search/indexing over the repo's Markdown (kit-root discovery, ranked search, formula reference, recipe index) |
| `anaplan_kit/mcp_server.py` | MCP server (`anaplan-kit-mcp`): the kit + API client as AI-agent tools over stdio |

## Setup

```bash
cd tooling
python -m venv .venv && source .venv/bin/activate   # Python 3.10+
pip install -r requirements.txt                     # runtime (requests)
pip install -r requirements-dev.txt                 # + pytest, responses (for tests)
```

Or install the package itself (editable):

```bash
pip install -e .            # runtime deps
pip install -e ".[dev]"     # + test deps
```

## Environment variables

Copy `.env.example` to `.env` and fill in your own values (never commit `.env`):

| Variable | Meaning |
| --- | --- |
| `ANAPLAN_EMAIL` | Anaplan account email (basic-auth username) |
| `ANAPLAN_PASSWORD` | Anaplan account password |
| `ANAPLAN_WORKSPACE_ID` | Target workspace ID |
| `ANAPLAN_MODEL_ID` | Target model ID |

The examples read these via `os.environ`; load them into your shell however you
prefer (e.g. `export $(grep -v '^#' .env | xargs)` or your own dotenv loader).

## Usage snippets

Programmatic use:

```python
from anaplan_kit import AnaplanClient

client = AnaplanClient.from_credentials(email, password)
for ws in client.list_workspaces():
    print(ws["id"], ws["name"])
    for model in client.list_models(ws["id"]):
        print("  ", model["id"], model["name"])
```

### Example scripts (`examples/`)

Each reads config from environment variables and is runnable in principle
against a real tenant.

```bash
# 1. Discover the workspace / model / action IDs you need.
python examples/list_models.py

# 2. Upload a CSV and run a named import action; prints the result.
python examples/run_import.py <fileId> <importId> path/to/data.csv

# 3. Run an export action and download the produced file in chunks.
python examples/run_export.py <exportId> <fileId> out.csv

# 4. Run a process (ordered group of actions) and wait for completion.
python examples/run_process.py <processId>
```

## Running the tests (offline)

```bash
pip install -r requirements-dev.txt
pytest -q
```

The tests mock all HTTP with [`responses`](https://github.com/getsentry/responses),
so they pass with **no network and no Anaplan tenant**.

## Notes on the API shape

- **Auth:** `POST` with HTTP Basic auth to the auth service returns an
  `AnaplanAuthToken`; it is sent as `Authorization: AnaplanAuthToken <token>`
  and refreshed before expiry.
- **Async tasks:** running an import/export/action/process `POST`s to its
  `/tasks` endpoint for a `taskId`, then polls `/.../tasks/{taskId}` until the
  state is `COMPLETE`. A `result.successful == false` raises `AnaplanTaskError`
  (check the failure dump).
- **Chunked transfer:** uploads declare a chunk count then `PUT` each chunk;
  exports are downloaded by reassembling their chunks.

See [`../docs/04-integration/rest-api.md`](../docs/04-integration/rest-api.md)
for the full conceptual reference.

## Modeling tools (offline, no tenant needed)

The `anaplan_kit.modeling` subpackage helps you **design new features faster** by
operationalizing this kit's conventions ([DISCO](../docs/03-methodology/disco.md),
[naming](../templates/naming-conventions.md), the
[formula cheat sheet](../docs/02-formulas/cheatsheet.md), blueprint tables). It is
**pure local logic** — it never contacts an Anaplan tenant or the network, so you
can scaffold, lint and size a feature entirely offline before you ever open a model.

Run it via `python -m anaplan_kit.modeling …` or, once installed, the
`anaplan-model` console script.

### `scaffold` — start from a correct shape

```bash
# A full DISCO skeleton (DAT/INP/SYS/CAL/OUT + a README), printed as Markdown.
python -m anaplan_kit.modeling scaffold feature "Headcount Bonus"

# A single module skeleton with your dimensions and line items.
python -m anaplan_kit.modeling scaffold module "CAL01 Revenue" \
    --disco CALC --dims "L3 Cost Centre,Time,Versions" \
    --line-items "Gross Revenue:Number:Sum,Margin %:Number:None"
```

Each scaffold uses the correct prefix (`DAT01`, `INP01`, `SYS01 Time Settings`,
`CAL01`, `OUT01`), the canonical Time/Org dimensions, and the `Is Actual?` flag.

### `lint` — check a blueprint against the conventions

```bash
python -m anaplan_kit.modeling lint ../blueprints/fpa-pl-planning/modules.md
```

It parses every canonical `| Line Item | Format | Summary | Applies To | Formula |`
table in the file and reports findings by severity:

- **ERROR** — wrong DISCO prefix, empty line-item name, banned `ANCESTOR()` /
  `CHILDREN()`, `[NEXT: …]` bracket-offset misuse, single-keyword multi-mappings
  (`[SUM: a, b]`), or unbalanced `()` `[]` / quotes. Exit code is `1` if any ERROR.
- **WARN** — `SYS00` time-settings naming (use `SYS01`), `Is Actual Month?`
  (use `Is Actual?`), a numeric line item with no deliberate Summary, hard-coded
  list items (`SELECT:`), nested `IF` deeper than 3.
- **INFO** — a `WORD(` token not in the known-function list (it may be a newer
  function or a typo — never an error).

### `size` — back-of-envelope cell count

```bash
python -m anaplan_kit.modeling size \
    --dims "L3 Cost Centre=500,Time=36,Versions=3" --line-items 20
```

Prints `product(dimension sizes) × line items` and warns when the estimate
exceeds the threshold (default 10,000,000 cells) — the single most useful
*Performance* number to know before you build.

### Programmatic use

```python
from anaplan_kit.modeling import (
    Disco, Module, LineItem,
    lint_module, render_module, parse_blueprint, cell_count,
)

m = Module("CAL01 Revenue", Disco.CALC, [
    LineItem("Gross Revenue", "Number", "Sum",
             ["L3 Cost Centre", "Time"], "Volume * Price"),
])
print(render_module(m))         # Markdown blueprint
print(lint_module(m))           # list[Finding]
print(cell_count({"L3 Cost Centre": 500, "Time": 36}, 1))
```

The modeling tools are covered by the same offline `pytest` suite.

## MCP server (`anaplan-kit-mcp`)

`anaplan_kit.mcp_server` exposes the whole kit as [MCP](https://modelcontextprotocol.io) tools
over **stdio**, for use by AI agents (Claude Code, OpenClaw bots, any MCP client). Install the
extra and run the console script:

```bash
pip install -e ".[mcp]"
anaplan-kit-mcp
```

Two tool families (full tool table in the [root README](../README.md#mcp-server)):

- **Offline knowledge tools** — `search_kit`, `read_kit_doc`, `formula_reference`,
  `list_recipes`, `lint_blueprint`. Backed by `anaplan_kit/kitindex.py`: pure-stdlib ranked
  keyword search (term frequency + heading/title/filename boosts — no embeddings, no network)
  over the repo's Markdown, plus the *real* blueprint linter from `anaplan_kit.modeling`.
  The repo checkout is located via `ANAPLAN_KIT_ROOT`, falling back to walking up from the
  package (editable installs) or the working directory. `read_kit_doc` is sandboxed: relative
  paths only, resolved inside the repo, `.md` files only.
- **Live API tools** — `anaplan_connection_status`, `anaplan_list_workspaces`,
  `anaplan_list_models`, `anaplan_model_metadata`, `anaplan_run_action` /
  `anaplan_run_import` / `anaplan_run_export` / `anaplan_run_process` — thin wrappers over
  `AnaplanClient`, reading the same `ANAPLAN_*` environment variables as the examples
  (`ANAPLAN_AUTH_URL` / `ANAPLAN_API_BASE` override the endpoints, which is how the offline
  tests point them at mocked hosts).

> **Offline honesty invariant (load-bearing):** without `ANAPLAN_EMAIL` + `ANAPLAN_PASSWORD`,
> every live tool returns `{"mode": "offline", "error": "no Anaplan credentials configured"}`
> without raising and **without attempting any network I/O**. Nothing in the server touches the
> network at import/startup time either. Keep it that way — the public bot persona built on this
> server must never appear to have touched a tenant it couldn't reach.

The server is covered by the same offline test suite (`tests/test_mcp_server.py`,
`tests/test_kitindex.py`): knowledge tools read the repo's own Markdown, live happy paths mock
HTTP with `responses`, and the honesty invariant is asserted with zero registered mocks.
