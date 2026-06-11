# anaplan-kit

Beginner-friendly **learning + reference kit** for new Anaplan model builders/consultants:
a course (L1→L3), formula reference (Anapedia-validated), cookbook recipes, blueprints, and a
small runnable Python client for the Anaplan REST API v2. Public educational repo.

- **Lumivara product line:** Learn.
- **Mostly Markdown docs** — Anaplan is browser-only SaaS; docs/blueprints/recipes *describe & illustrate*, verified against published syntax (`SOURCES.md`), NOT executed. Only runnable code is `tooling/`.

## Toolchain & commands (authoritative — from README + CI)

Python tooling uses **pip + venv** (repo's own convention; NOT uv). Python 3.10+ (CI uses 3.11).

```bash
cd tooling && python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev,mcp]"      # runtime + test deps (pytest, responses) + MCP server (mcp)
# from repo ROOT:
ruff check tooling && ruff format --check tooling   # lint + format check
cd tooling && python -m pytest -q                   # tests: OFFLINE, HTTP mocked, no tenant
# docs gates (repo ROOT):
python tools/check_links.py .                       # every relative MD link must resolve
python tools/lint_blueprints.py                     # anaplan-model lint over blueprints/
npx --yes markdownlint-cli2 "**/*.md" "#**/node_modules/**"
```

Run all gates locally via pre-commit: `pip install pre-commit && pre-commit install` (`.pre-commit-config.yaml`).
CI (`.github/workflows/ci.yml`) runs the same on every push/PR: `python` job (ruff+pytest) + `docs` job.

## Key directories

- `docs/` — 00-getting-started … 10-field-guide (fundamentals, formulas, methodology, integration, UX, security/ALM, perf, advanced, troubleshooting).
- `cookbook/` — ★ centerpiece: real-world "cheat code" recipes.
- `blueprints/` — worked models (`_common` backbone + FP&A / Sales / Supply Chain / Workforce).
- `tutorials/` · `exercises/` — build-along + practice (incl. L3 capstone).
- `tooling/` — `anaplan_kit` pkg (auth, client, metadata, imports_exports, actions) + `modeling/` CLI (`anaplan-model`) + MCP server (`anaplan-kit-mcp` stdio; `mcp_server.py`/`kitindex.py`; tests via the same pytest run) + offline tests.
- `tools/` — repo dev scripts (link checker, blueprint conventions linter). `templates/` · `LEARNING-PATH.md` · `SOURCES.md`.

## Gotchas / invariants

- No deploy target — this is a docs+code repo, not a deployed app. No Vercel.
- `tooling/` reads Anaplan creds from **env vars only** (`ANAPLAN_EMAIL/PASSWORD/WORKSPACE_ID/MODEL_ID`); never hard-code/commit `.env`.
- Tests mock HTTP (`responses`) — never make live calls in tests. MCP live tools without creds must return `{"mode": "offline"}` (no raise, no network) — never fake tenant access.
- Every doc/recipe opens with a badge: **Level · Area · PLANS · DISCO · Planual** — keep that convention when adding content.
- ruff config (line-length 100, py310, select E/F/W/I/UP/B) lives in `tooling/pyproject.toml`.
