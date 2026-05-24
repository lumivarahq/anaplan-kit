# Step 8 — Review Against PLANS

> **Level:** L2 · **Area:** Tutorial · **PLANS:** all five · **DISCO:** all

You have a working model. A *good* model builder doesn't stop there — they **review against the
standard** before calling it done. This step walks the
[model-build checklist](../docs/03-methodology/model-build-checklist.md) against everything you
built in Steps 1–7 and lists the refactors that take this from "works" to "sanctioned."

Use the copyable version: [`templates/model-build-checklist.md`](../templates/model-build-checklist.md).

---

## 8.1 Walk the checklist

### Structure (DISCO)
- [x] Every module is **one** DISCO type — `DAT01` (Data), `INP01/02` (Inputs),
      `SYS01/02/03` (System), `CAL01/02/03` (Calculations), `OUT01` (Outputs).
- [x] Mappings/attributes live in System (`SYS02 COGS %`, `SYS03 Region`), not in calcs.
- [x] Data flows one way: `DAT/INP → SYS → CAL → OUT`. No circular references.
- [x] Naming follows `DAT/INP/SYS/CAL/OUT` + numbering (see
      [naming conventions](../templates/naming-conventions.md)).

### Performance (P)
- [ ] **Apply Time Ranges.** `INP01/INP02` only need the plan years — give them a Time Range of
      `FY26` (or `FY26–FY27`) instead of the full `FY25–FY27` calendar. `DAT01` only needs actual
      months. This is the single biggest size lever. See
      [time ranges](../docs/07-performance/time-ranges.md).
- [x] No module is dimensioned by a list it doesn't need (`INP02` deliberately has no Product).
- [ ] **Subsets:** if only some products are ever planned, give `INP01` a Product *subset* rather
      than the whole list.
- [x] No heavy `IF` over huge cell counts — the actual/forecast switch keys off a **Boolean**
      (`SYS01.Is Actual Month?`), not a text/date comparison repeated everywhere.
- [x] Sub-expressions computed once (`Gross Revenue` is referenced, not re-derived in COGS).

### Logical & Auditable (L, A)
- [x] Logic is **stepped**: `Volume → Price → Gross Revenue`; `Revenue → COGS → Gross Profit →
      EBITDA`. Each line readable.
- [x] Names describe meaning (`Gross Revenue`, `EBITDA Margin %` — not `R1`, `X2`).
- [x] Summaries set deliberately — `Price`/`COGS %`/`Margin %` = **Average**, amounts = **Sum**.
- [x] A reviewer can trace `EBITDA` back to `Volume × Price`.

### Necessary (N)
- [ ] **Prune optional drivers.** Did you keep `Price Growth %`, `Headcount`, `Cost per Head` from
      Steps 3–4 without using them? If nothing references them, **delete them** — unused line items
      still cost memory and confuse readers.
- [x] No duplicate calculations (COGS % defined once in SYS02).
- [x] `OUT01` adds no new logic beyond display ratios.

### Sustainable (S)
- [x] **No hard-coded** dates/periods — the switchover reads `SYS01.Is Actual Month?` and the
      current period, so a roll to FY27 needs no formula edits.
- [x] No `SELECT` on specific list items — `PARENT()`/mappings used instead (`SYS03.Region`).
- [x] Adding a new product/entity/month needs **no formula changes** (they inherit structure).
- [ ] **Data Hub (L2/L3):** in a real landscape, actuals would come from a shared **data hub**, not
      a per-model CSV. Note this as the next architectural step. See
      [integration docs](../docs/04-integration/).

### Delivery
- [x] Built to the brief (revenue → P&L, actuals blend, a report page) — no scope creep.
- [ ] **Test edge cases:** blank Volume/Price (does `COGS` go blank or zero?), a new entity with no
      data, the **year rollover** (advance Current Period and confirm the blend re-splits).
- [ ] **ALM:** production-bound work should be built in a DEV model and promoted via a revision.
      This tutorial model is a sandbox; note ALM as the path to production. See
      [ALM](../docs/06-security-alm/alm.md).
- [ ] **Document assumptions:** add line-item descriptions / a notes module for the COGS % logic and
      the switchover rule.

---

## 8.2 The refactor list (do these next)

| # | Refactor | PLANS | Effort |
| --- | --- | --- | --- |
| 1 | Apply **Time Ranges** to `INP01`, `INP02`, `DAT01`. | Performance | Low |
| 2 | **Delete unused** optional line items (`Price Growth %`, `Headcount`…) if not wired in. | Necessary | Low |
| 3 | Add **line-item descriptions** for COGS %, switchover, margin. | Auditable | Low |
| 4 | Add a **Product subset** to `INP01` if only some products are planned. | Performance | Med |
| 5 | Move actuals to a **data hub** feed (saved view import) for a real landscape. | Sustainable | High |
| 6 | Put the model under **ALM** (DEV → TEST → PROD via revisions). | Sustainable | High |

> Items 1–3 are quick wins that every reviewer expects. 4–6 are the L2/L3 maturity steps — they're
> exactly what the [Learning Path](../LEARNING-PATH.md) Level 2/3 sections and the
> [cookbook](../cookbook/) cover.

---

## 8.3 You're done — what you built

A complete FP&A model: an Organization hierarchy and Product list, a model calendar with three
versions, the System backbone, planning inputs, a stepped calculation engine producing a P&L,
loaded actuals blended with forecast, and a UX page reporting Plan vs Actual — all following
**DISCO** and reviewable against **PLANS**.

Compare your build to the finished reference:
[`blueprints/fpa-pl-planning/`](../blueprints/fpa-pl-planning/). Then test yourself with the
[exercises](../exercises/) and the [L3 capstone](../exercises/capstone-l3.md).

---

**Related:** [Model-build checklist](../docs/03-methodology/model-build-checklist.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) · [DISCO](../docs/03-methodology/disco.md) ·
[Performance](../docs/07-performance/) · [ALM](../docs/06-security-alm/alm.md) ·
[Exercises](../exercises/) · [Capstone](../exercises/capstone-l3.md)

**Next → [Practice with the exercises](../exercises/README.md)**
