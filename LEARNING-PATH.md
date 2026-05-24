# Learning Path — Level 1 → Level 2 → Level 3

This kit follows the same progression as Anaplan's official **model-building certification track**.
You don't have to follow it in order, but if you're new, this is the fastest route from zero to
"trusted to build in a client model."

Each level below lists **what to learn**, **where it lives in this repo**, and **what you should be
able to do** before moving on. Every doc page and cookbook recipe carries a `Level:` badge so you
can always tell where something sits.

> **How the levels map to Anaplan's courses**
> - **Level 1 — Model Building** = the foundations: navigate the platform and build a small,
>   correct model end-to-end.
> - **Level 2 — Model Building** = build *well*: DISCO structure, numbered lists, subsets, time
>   ranges, data hubs, real imports, better UX.
> - **Level 3 — Model Building** = build *at scale*: architecture, performance, ALM, advanced
>   calculation patterns, and a capstone built from written requirements.

---

## Level 1 — Foundations

**Goal:** understand the building blocks and build a simple, working model.

| Learn | Where |
| --- | --- |
| What Anaplan is; tenant → workspace → model; the calc engine | [`docs/00-getting-started/`](docs/00-getting-started/) |
| Lists & simple hierarchies | [`docs/01-fundamentals/lists-and-hierarchies.md`](docs/01-fundamentals/lists-and-hierarchies.md) |
| Modules, line items & **formats**, summary methods | [`docs/01-fundamentals/modules.md`](docs/01-fundamentals/modules.md), [`line-items-and-formats.md`](docs/01-fundamentals/line-items-and-formats.md) |
| Dimensions, Time, Versions | [`docs/01-fundamentals/dimensions.md`](docs/01-fundamentals/dimensions.md), [`time.md`](docs/01-fundamentals/time.md), [`versions.md`](docs/01-fundamentals/versions.md) |
| Core formulas: aggregation, `IF`, simple time, basic `LOOKUP` | [`docs/02-formulas/`](docs/02-formulas/) |
| Basic dashboards / UX | [`docs/05-ux/`](docs/05-ux/) |
| Simple imports & exports | [`docs/04-integration/imports-exports.md`](docs/04-integration/imports-exports.md) |
| **Build along:** the FP&A model | [`tutorials/`](tutorials/) |

**You can move on when you can:** create a hierarchy, build input and calculation modules with the
right formats and summaries, write `SUM`/`LOOKUP`/`IF`/time formulas, and put it on a dashboard.

---

## Level 2 — Intermediate / real builds

**Goal:** build the *sanctioned* way — structured, reusable, importable.

| Learn | Where |
| --- | --- |
| **DISCO** module pattern | [`docs/03-methodology/disco.md`](docs/03-methodology/disco.md) |
| **PLANS** standard & **The Planual** | [`docs/03-methodology/plans-standard.md`](docs/03-methodology/plans-standard.md), [`planual.md`](docs/03-methodology/planual.md) |
| Numbered lists & properties | [`docs/01-fundamentals/numbered-lists-and-subsets.md`](docs/01-fundamentals/numbered-lists-and-subsets.md) |
| Subsets & line item subsets | same page + [`docs/07-performance/`](docs/07-performance/) |
| Time Ranges | [`docs/07-performance/time-ranges.md`](docs/07-performance/time-ranges.md) |
| Mapping with `SUM` / `LOOKUP`; subsidiary views | [`docs/02-formulas/lookup-and-mapping.md`](docs/02-formulas/lookup-and-mapping.md) |
| **Data Hubs** & multi-step imports / processes | [`docs/04-integration/`](docs/04-integration/) |
| Selective access (intro) | [`docs/06-security-alm/`](docs/06-security-alm/) |
| **Most of the [cookbook](cookbook/)** lives here | [`cookbook/`](cookbook/) |

**You can move on when you can:** classify every module by DISCO, build a data hub that feeds a
spoke model, design with subsets/time ranges to control size, and explain why each choice satisfies PLANS.

---

## Level 3 — Advanced / architecture

**Goal:** build at scale and operate it safely.

| Learn | Where |
| --- | --- |
| Data hub & multi-model **architecture** | [`docs/04-integration/`](docs/04-integration/), [`blueprints/`](blueprints/) |
| **Performance** & sparsity | [`docs/07-performance/`](docs/07-performance/) |
| Advanced calc patterns (allocation, FX, depreciation, ranking) | [`cookbook/`](cookbook/) |
| **ALM**: dev / test / prod, revisions, deployed mode | [`docs/06-security-alm/alm.md`](docs/06-security-alm/alm.md) |
| Advanced security & **DCA** | [`docs/06-security-alm/dynamic-cell-access.md`](docs/06-security-alm/dynamic-cell-access.md) |
| Integration at scale: CloudWorks, REST API | [`docs/04-integration/`](docs/04-integration/), [`tooling/`](tooling/) |
| Data hub **architecture** (hub-and-spoke) | [`docs/08-advanced-features/data-hub-architecture.md`](docs/08-advanced-features/data-hub-architecture.md) |
| Specialised features: Optimizer, PlanIQ, Workflow, Office add-ins | [`docs/08-advanced-features/`](docs/08-advanced-features/) |
| Troubleshooting, reconciliation, testing & model size | [`docs/09-troubleshooting/`](docs/09-troubleshooting/) |
| **Capstone:** build from requirements | [`exercises/`](exercises/) |

**You're "L3-ready" when you can:** take a written requirement, design a multi-model architecture
that performs, deploy it through ALM, secure it, and integrate it with source systems.

---

## Cross-cutting: the Cookbook

The [`cookbook/`](cookbook/) is usable at **any** level — it's organised by *task*, not by level,
though each recipe is tagged. When a real request lands ("spread the annual budget to months",
"convert to USD", "let managers edit only their own cost centre"), start there.

## Where this leads: Anaplan certifications

This track mirrors Anaplan's official **model-building** levels. The certifications you'll hear
about, in rough order:

1. **Level 1 / 2 / 3 Model Building** — the courses this path follows.
2. **Anaplan Certified Model Builder** — validates you can build production models well (PLANS).
3. **Anaplan Solution Architect** — designs multi-model architectures and data flows.
4. **Anaplan Master Anaplanner** — the senior practitioner credential.

Certifications evolve — check the current catalogue in the **Anaplan Academy / Community**
(see [`docs/03-methodology/academy-best-practices.md`](docs/03-methodology/academy-best-practices.md)).
