# Modeling & Design Exercises — DISCO and PLANS

> **Level:** L2 · **Area:** Exercises · Solutions: [`solutions/modeling-design-solutions.md`](solutions/modeling-design-solutions.md)

Move beyond single formulas to **design**: given a requirement, lay out the right modules with
[DISCO](../docs/03-methodology/disco.md); given a bad design, spot the
[PLANS](../docs/03-methodology/plans-standard.md) violations. Answer with blueprint sketches and
short reasoning. [Solutions →](solutions/modeling-design-solutions.md)

---

## Part 1 — Design from a requirement (DISCO)

**D1 (L2).** *Requirement:* "Planners enter a **price increase %** per product per year; the model
applies it to last year's price to get next year's price, then revenue = volume × price."
Design the modules: list each as **module name · DISCO type · Applies To · key line items**. Where
does the % live, where does the multiplication live, and why?

**D2 (L2).** *Requirement:* "We import **daily FX rates**, but planning uses a **monthly average
rate**. Convert local-currency revenue to USD for reporting."
Sketch the modules (Data, System, Calculations, Outputs) and the data flow. Which DISCO type holds
the raw daily rates, and which holds the monthly average the calc reads?

**D3 (L2).** *Requirement:* "Managers should be able to edit **only their own cost centre's** OpEx
assumptions; everyone can view the consolidated P&L."
You don't need the security syntax — describe the **module design** that makes this clean: which
module is editable, which is read-only, and how DISCO separation helps.

---

## Part 2 — Spot the PLANS violation

For each bad design below, name **which PLANS principle(s)** it breaks and give the fix.

**V1 (L2).** A calc line item:
```
Revenue = IF Time = Apr 2026 THEN Volume * Price * 1.05 ELSE Volume * Price
```

**V2 (L2).** A single module `Everything` holds: imported actuals, planners' typed volume, the
Cost Centre→Region mapping, `Revenue = Volume × Price`, **and** the dashboard view — all in one grid.

**V3 (L2).** `CAL` module:
```
Gross Profit = (Volume * Price) - (Volume * Price * COGS %)
Net Margin %  = ((Volume * Price) - (Volume * Price * COGS %)) / (Volume * Price)
```
(`Volume * Price` and the gross-profit expression are each written out multiple times.)

**V4 (L2).** A reporting module is dimensioned `L3 Cost Centre × L2 Product × Customer × SKU × Day ×
Versions` with 40 line items, even though the report only ever shows monthly revenue by Region.

**V5 (L2).** To pull UK numbers, a formula uses `SELECT: L2 Country.UK` in several places; to add
Germany next quarter someone will copy-paste and edit each one.

**V6 (L2).** There are three line items — `Rev`, `Revenue v2`, `Revenue_OLD` — two left over from
experiments; nobody's sure which the dashboard uses.

---

## Part 3 — Refactor a module

**R1 (L2).** Below is a draft `CAL Revenue` module. Rewrite it as a **clean stepped blueprint
table** (correct DISCO placement, formats, summaries, stepped line items), and list what you moved
out and where.

Draft (as given by a junior builder):

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| Vol | Number | Sum | *(planners type here)* |
| Prc | Number | Sum | *(planners type here)* |
| cogs pct | Number | Sum | *(typed per row, repeated every month)* |
| rev | Number | Sum | `Vol * Prc` |
| profit | Number | Sum | `(Vol*Prc) - (Vol*Prc*cogs pct)` |
| region | Text | None | *(typed: "EMEA", "Americas"…)* |

Identify every issue and produce the corrected design across the right DISCO modules.

---

**Related:** [DISCO](../docs/03-methodology/disco.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) ·
[Model-build checklist](../templates/model-build-checklist.md) ·
[Blueprint template](../templates/blueprint-template.md) ·
[Solutions →](solutions/modeling-design-solutions.md)
