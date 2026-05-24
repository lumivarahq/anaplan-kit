# Step 6 — Outputs & Dashboard (the DISCO "O")

> **Level:** L1 · **Area:** Tutorial · **DISCO:** Outputs · **PLANS:** Necessary, Logical

**Output modules** are the presentation layer — a module shaped *exactly* for a dashboard card or an
export file. The rule: **no new business logic** here. Outputs select, format and arrange numbers
that **Calculations** already produced. See [DISCO](../docs/03-methodology/disco.md).

We'll build one Outputs module and put it on a New UX page.

---

## 6.1 OUT01 P&L Report

A clean, reporting-shaped view of the P&L: the lines a finance reader wants, ready to drop on a page.
It mirrors `CAL03 P&L` but adds the comparison lines a report needs (Plan vs Actual, Variance).

**Modules → New Module.** Name `OUT01 P&L Report`.
**Applies To:** `Entity`, plus **Time** and **Versions**.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Revenue` | Number | Sum | Entity, Time, Versions | `'CAL03 P&L'.Revenue` |
| `COGS` | Number | Sum | Entity, Time, Versions | `'CAL03 P&L'.COGS` |
| `Gross Profit` | Number | Sum | Entity, Time, Versions | `'CAL03 P&L'.Gross Profit` |
| `Fixed OpEx` | Number | Sum | Entity, Time, Versions | `'CAL03 P&L'.Fixed OpEx` |
| `EBITDA` | Number | Sum | Entity, Time, Versions | `'CAL03 P&L'.EBITDA` |
| `EBITDA Margin %` | Number (%) | Average | Entity, Time, Versions | `EBITDA / Revenue` |

Notes:
- Every line is a **straight reference** to `CAL03` — no recomputation. `EBITDA Margin %` looks like
  a calculation, but it's a *display ratio* derived from already-final numbers, which belongs with
  the report. (If a margin were a planning driver, it would live in CAL.) Use judgement; when in
  doubt, push logic up into CAL and keep OUT thin (*Necessary*).
- Summary on `EBITDA Margin %` = **Average** (a ratio shouldn't sum).

> **Variance across versions.** Rather than add `Variance` line items, use a **Version formula**
> (Step 2): `Forecast − Budget`, evaluated across the Versions axis. It shows in the report without
> bloating the module (*Necessary*). If your tenant doesn't use version formulas, add explicit
> `Var vs Budget = Forecast value − Budget value` lines here — that's the one place a small amount
> of "report math" is acceptable.

---

## 6.2 Build the UX page

Anaplan's **New UX** organises pages into **Apps**. We'll add a page that shows the P&L and lets a
planner switch entity and version.

1. Top-left app menu → **Apps** → **New App** (or open an existing app). Name it `FP&A Planning`.
2. Inside the app, **+ → New Page → Board**. Name the page `P&L — Plan vs Actual`.
3. **Add a card → Grid.** Source: module `OUT01 P&L Report`.
   - **Rows:** the line items (`Revenue … EBITDA Margin %`).
   - **Columns:** `Time` (show Months, with Quarter/Year roll-ups available).
   - **Page selectors (top of page):** `Entity` and `Versions`.
4. Add a second card → **Chart (Column)** from the same module: plot `Revenue` and `EBITDA` over
   Time so the trend is visible at a glance.
5. *(Optional)* Add a **KPI card** showing `EBITDA Margin %` for the selected entity/period.

> **Page selectors vs filters:** put `Entity` and `Versions` as **page selectors** so the whole page
> re-points together (pick `Forecast`, pick `UK`, everything updates). Use filters only to hide rows
> within a card.

---

## 6.3 Let planners edit assumptions from the page (optional)

A planning page usually lets users *input*, not just read. Add an **input card** sourced from
`INP01 Revenue Assumptions` (Volume, Price) on the same or a linked page — that's the one card that
should be editable. `OUT01` and the `CAL` modules stay read-only.

> **DISCO on a page:** the editable card points at **Inputs**; the report cards point at
> **Outputs**. A user types a new Volume → `CAL01` recomputes → `CAL03` rolls up → `OUT01` and the
> chart refresh, instantly. That live ripple is the whole point of Anaplan.

---

## 6.4 Sanity check

- [ ] `OUT01 P&L Report` contains only references to `CAL03` (+ a display ratio) — no business logic.
- [ ] The page shows the P&L grid with `Entity` and `Versions` as page selectors and `Time` on
      columns.
- [ ] Changing the `Entity` selector re-points the whole page.
- [ ] (If added) editing a Volume on the input card flows through to the report instantly.

> **DISCO check:** Outputs are thin and read-only. If you found yourself writing real logic in
> `OUT01`, move it back into a `CAL` module — that's the classic "fat output module" smell we'll
> hunt for in [Step 8](08-review-against-plans.md).

---

**Related:** [UX docs](../docs/05-ux/) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Blueprint: FP&A modules](../blueprints/fpa-pl-planning/modules.md) ·
[Naming conventions](../templates/naming-conventions.md)

**Next → [Step 7 — Import Actuals](07-import-actuals.md)**
