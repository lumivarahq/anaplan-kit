# Tutorials — Build the FP&A Revenue → P&L Model

> **Level:** L1 · **Area:** Tutorial

This is a **build-along**: you'll construct one complete model from an empty workspace to a
working dashboard, step by step. It builds the canonical model documented in
[`blueprints/fpa-pl-planning/`](../blueprints/fpa-pl-planning/), using the **same list and module
names** — the tutorial *builds* it; the blueprint is the *finished reference*. Where the blueprint
goes further (the full `L3 P&L Account` roll-up), the tutorial says so and builds the core.

By the end you'll have a small but real **FP&A planning model**: plan revenue from volume × price,
plan cost, convert local amounts to USD, roll them into a P&L, load actuals, and report Plan vs
Actual on a UX page.

---

## What you'll build

```
Lists:        L1 Region › L2 Country › L3 Cost Centre  ·  L1 Product Family › L2 Product
              L1/L2/L3 P&L Account  ·  Currency  ·  Versions  ·  Time
SYS modules:  SYS01 Time Settings · SYS02 Organization Details · SYS03 Account Details · SYS04 Exchange Rates
INP modules:  INP01 Revenue Assumptions  ·  INP02 Opex Plan  ·  INP03 Cost Drivers
CAL modules:  CAL01 Revenue · CAL02 Cost · CAL03 Currency Conversion · CAL04 P&L Build
DAT module:   DAT01 Actuals (import landing zone)
OUT module:   OUT01 P&L Statement  →  UX page "P&L — Plan vs Actual"
```

This is the **DISCO** pattern end-to-end (Data → Inputs → System → Calculations → Outputs).
See [`docs/03-methodology/disco.md`](../docs/03-methodology/disco.md).

---

## Prerequisites

- A login to an Anaplan tenant where you have **Workspace Administrator** rights (or follow along
  conceptually — every step shows the clicks and the blueprint tables).
- You've skimmed Level 1 of the [Learning Path](../LEARNING-PATH.md) and the fundamentals:
  [lists](../docs/01-fundamentals/lists-and-hierarchies.md),
  [modules](../docs/01-fundamentals/modules.md),
  [line items & formats](../docs/01-fundamentals/line-items-and-formats.md).
- You understand the four conventions used throughout: **blueprint tables**, **Anaplan formula
  syntax**, the **DAT/INP/SYS/CAL/OUT** naming, and the badge blockquote at the top of each page.

> New to a term? Keep [`docs/00-getting-started/`](../docs/00-getting-started/README.md) open in a
> second tab.

---

## The steps

| # | Step | DISCO focus | You'll learn |
| --- | --- | --- | --- |
| 1 | [Set up the model & lists](01-set-up-model-and-lists.md) | — | Workspace, model, Organization hierarchy, Product list |
| 2 | [Time & Versions](02-time-and-versions.md) | — | Model calendar, the native Versions list |
| 3 | [System modules](03-system-modules.md) | **S** | Time settings, org/account mappings, FX rates |
| 4 | [Input modules](04-input-modules.md) | **I** | Volume, price, opex, cost-driver assumptions |
| 5 | [Calculation modules](05-calculation-modules.md) | **C** | Revenue = volume × price, cost, local→USD, P&L build |
| 6 | [Outputs & dashboard](06-outputs-and-dashboard.md) | **O** | An Outputs module + a UX page |
| 7 | [Import actuals](07-import-actuals.md) | **D** | A saved view, an import action, mapping |
| 8 | [Review against PLANS](08-review-against-plans.md) | all | Walk the model-build checklist; refactor |

Start at **[Step 1 →](01-set-up-model-and-lists.md)**.

---

**Related:** [Blueprint: FP&A P&L Planning](../blueprints/fpa-pl-planning/) ·
[DISCO](../docs/03-methodology/disco.md) · [PLANS](../docs/03-methodology/plans-standard.md) ·
[Naming conventions](../templates/naming-conventions.md) · [Exercises](../exercises/)
