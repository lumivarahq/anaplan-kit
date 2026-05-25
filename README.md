# Anaplan Data Modeler Kit

A comprehensive, beginner-friendly **learning + reference kit for a new Anaplan model builder / consultant.**

It is four things at once:

1. **A course** — structured docs that follow Anaplan's official **Level 1 → Level 2 → Level 3** model-building progression. See [`LEARNING-PATH.md`](LEARNING-PATH.md).
2. **A reference** — function-by-function formula docs (validated against [Anapedia](https://help.anaplan.com/)), plus the methodology that holds it all together: **The Anaplan Way, PLANS, DISCO, and The Planual.**
3. **A cookbook** — the [`cookbook/`](cookbook/) is the centerpiece: ready-to-use "cheat code" recipes for the scenarios you actually get handed at work (rolling forecast, currency conversion, top-down allocation, data hub, DCA-driven approval, …).
4. **A toolkit** — a small Python package ([`tooling/`](tooling/)) that wraps the **Anaplan REST API v2** for imports/exports/processes.

> **Who this is for:** someone new to Anaplan model building who wants one place to learn the platform *and* keep open while doing real work.

---

## How to use this repo

| If you want to… | Go to |
| --- | --- |
| Learn Anaplan from scratch, in order | [`LEARNING-PATH.md`](LEARNING-PATH.md) → [`docs/00-getting-started/`](docs/00-getting-started/) |
| Look up a function's syntax | [`docs/02-formulas/`](docs/02-formulas/) and the [cheat sheet](docs/02-formulas/cheatsheet.md) |
| Solve a specific task *right now* | [`cookbook/`](cookbook/) (browse the [recipe index](cookbook/README.md)) |
| Understand the "right way" to build | [`docs/03-methodology/`](docs/03-methodology/) |
| See a complete worked model | [`blueprints/`](blueprints/) |
| Follow a build-along tutorial | [`tutorials/`](tutorials/) |
| Practice | [`exercises/`](exercises/) |
| Integrate via API | [`tooling/`](tooling/) |

### Reading conventions used everywhere

Every doc page and every cookbook recipe starts with a one-line badge so you always know where it sits:

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Sustainable · **DISCO:** Calculations

- **Level** — L1 / L2 / L3, mapped to the Anaplan model-building certification track.
- **PLANS** — which principle of the Anaplan modeling standard it serves (Performance, Logical, Auditable, Necessary, Sustainable).
- **DISCO** — module classification where relevant (Data, System, Inputs, Calculations, Outputs).
- **Planual** — referenced rule(s) where a specific rule applies. The Planual is Anaplan's official rulebook; rule numbers are cited where confirmable, otherwise stated by principle. See [`docs/03-methodology/planual.md`](docs/03-methodology/planual.md).

Formula examples are written in **Anaplan formula syntax**. Module/list designs are shown as **blueprint tables** — the same Line Item / Format / Summary / Formula grid you see in the Anaplan Blueprint view.

> ⚠️ **Important:** Anaplan is a SaaS platform you build in a browser — there is no "compile and run" outside a real tenant. The docs/blueprints/recipes therefore *describe and illustrate*; they are verified against Anaplan's published syntax rules (see [`SOURCES.md`](SOURCES.md)), not by executing them. The Python tooling is the only runnable code and needs a real Anaplan tenant + credentials.

---

## Repository map

```
anaplan-kit/
├── LEARNING-PATH.md        L1 → L2 → L3 reading order, every topic mapped to a level
├── cookbook/               ★ real-world recipes (the "cheat codes")
├── docs/
│   ├── 00-getting-started/ platform architecture, glossary, orientation
│   ├── 01-fundamentals/    lists, modules, line items, dimensions, time, versions
│   ├── 02-formulas/        function reference by category + cheat sheet (Anapedia-validated)
│   ├── 03-methodology/     The Anaplan Way · PLANS · DISCO · The Planual · Academy best practices
│   ├── 04-integration/     imports/exports, actions, Anaplan Connect, CloudWorks, REST API
│   ├── 05-ux/              New UX (Pages/Boards/Worksheets) & classic dashboards
│   ├── 06-security-alm/    roles, selective access, DCA, ALM (dev/test/prod)
│   ├── 07-performance/     sparsity, time ranges, subsets, optimization checklist
│   ├── 08-advanced-features/ data hub architecture, Optimizer, PlanIQ, Workflow, Excel/PPT add-ins
│   ├── 09-troubleshooting/ common errors & fixes, reconciliation/control totals, testing & UAT, model size
│   └── 10-field-guide/     real-world anti-patterns → fixes, engineering discipline, platform-aware decisions
├── blueprints/             worked models — shared _common backbone + FP&A / Sales / Supply Chain / Workforce
├── tutorials/              build the FP&A model end-to-end, step by step
├── exercises/              practice problems + solutions (incl. an L3 capstone)
├── tooling/                Python package: Anaplan REST API v2 client + offline modeling tools
├── templates/              naming conventions, checklists, blueprint CSV templates
├── tools/                  repo dev scripts (relative-link checker, blueprint conventions linter)
├── .github/workflows/      CI: ruff + pytest, markdownlint, link & conventions checks
└── SOURCES.md              reference URLs used to validate content
```

---

## What is Anaplan? (30-second version)

Anaplan is a cloud **connected-planning** platform. You model a business problem as a set of
**modules** (multi-dimensional grids) built from **lists** (the things you plan by — products,
cost centres, months) and **line items** (the measures and calculations). Formulas connect
modules so a change in an assumption ripples through the whole plan instantly, in memory.

A model builder's job is to turn business requirements into modules, line items and formulas that
are **fast, logical, auditable, necessary and sustainable** (that's **PLANS**) — and this kit
teaches you exactly that. Start at [`docs/00-getting-started/`](docs/00-getting-started/README.md).

---

## Quality, linting & CI

The repo lints itself with the same standards it teaches:

- **Anaplan conventions linter** — `python tools/lint_blueprints.py` runs `anaplan-model lint` over
  `blueprints/` (flags `ANCESTOR`/`CHILDREN`, single-keyword multi-mappings, non-canonical naming,
  missing summaries, nested-`IF`, …). See [`tooling/`](tooling/README.md).
- **Relative-link check** — `python tools/check_links.py .` (every Markdown link must resolve).
- **Markdown lint** — `npx markdownlint-cli2 "**/*.md"` (config in [`.markdownlint.json`](.markdownlint.json)).
- **Python** — `ruff check tooling` + `ruff format --check tooling`, and `cd tooling && python -m pytest` (offline, mocked HTTP).

Run them locally with **pre-commit**: `pip install pre-commit && pre-commit install`
([`.pre-commit-config.yaml`](.pre-commit-config.yaml)). The same checks run in **GitHub Actions** on
every push and PR ([`.github/workflows/ci.yml`](.github/workflows/ci.yml)).

---

## Disclaimer

This is an independent educational resource. "Anaplan", "Anapedia", "The Planual", "PLANS",
"DISCO" and related marks belong to Anaplan, Inc. Always confirm syntax and behaviour against the
official docs at [help.anaplan.com](https://help.anaplan.com/) for your platform version.
