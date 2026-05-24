# Modeling & Design Exercises — Solutions

> **Level:** L2 · **Area:** Exercises (solutions) · Exercise: [`../modeling-design-exercises.md`](../modeling-design-exercises.md)

Worked designs and PLANS critiques. Several designs can be valid — the reasoning is graded, not the
exact names.

---

## Part 1 — Design from a requirement

**D1 — Price increase % → price → revenue.**

| Module | DISCO | Applies To | Key line items |
| --- | --- | --- | --- |
| `INP01 Revenue Assumptions` | Inputs | Entity × Product × Time × Versions | `Volume`, `Base Price` |
| `INP02 Price Increase` | Inputs | Product × Year × Versions | `Price Increase %` |
| `CAL01 Revenue` | Calculations | Entity × Product × Time × Versions | `Price` (derived), `Gross Revenue` |

- The **%** lives in an **Inputs** module at `Product × Year` grain (it's typed, and it doesn't vary
  by month or entity — *Performance*: don't over-dimension it).
- The **derivation and multiplication** live in **Calculations**:
  `Price = Base Price * (1 + 'INP02 Price Increase'.Price Increase %)` and
  `Gross Revenue = Volume * Price`. Math never lives in Inputs.
- Why: planners edit only Inputs; the engine recomputes in CAL. Clean DISCO separation
  (*Logical, Auditable*).

**D2 — Daily FX → monthly average → USD.**

| Module | DISCO | Applies To | Role |
| --- | --- | --- | --- |
| `DAT01 FX Daily` | **Data** | Currency × Date | landing zone for imported daily rates, as-is |
| `SYS04 Exchange Rates` | **System** | Currency × Time(month) × Versions | `Monthly Avg Rate` = average of the month's daily rates |
| `CAL0x Revenue (USD)` | **Calculations** | Entity × Product × Time × Versions | `Revenue USD = Revenue Local * rate (looked up by Local Currency)` |
| `OUT01 …` | **Outputs** | … | report card |

Raw daily rates → **Data**. The monthly average the model plans on → **System** (a derived attribute
referenced everywhere). Conversion math → **Calculations**, reading the rate by the entity's
`Local Currency` (from `SYS Org Details`) × month × version. No rate hard-coded (*Sustainable*).

**D3 — Managers edit only their own cost centre.**

- **Editable:** `INP02 Cost Drivers` (OpEx) — an **Inputs** module. Restrict *write* access to a
  manager's own cost centre via **selective access** on the Entity list and/or **Dynamic Cell
  Access** (a Boolean from a System module gating editability). See
  [security/DCA](../../docs/06-security-alm/dynamic-cell-access.md).
- **Read-only:** `CAL03 P&L` / `OUT01 P&L Report` — everyone views the consolidated result.
- **Why DISCO helps:** because inputs are *already* separated from calcs and outputs, you secure the
  one small **Inputs** module without touching the engine or the report. If input + calc + report
  were one module, you couldn't make "edit my OpEx but view everything" clean.

---

## Part 2 — Spot the PLANS violation

**V1.** Hard-coded date `Apr 2026`. Breaks **Sustainable** (wrong next month / next year). Fix:
drive the uplift from a System/Input driver and time logic that references the calendar, never a
literal month.

**V2.** One module mixing all five DISCO types. Breaks **Logical** and **Auditable** (can't tell
where data enters / where humans input / where math happens) and hurts **Performance** (typing one
input recalculates the whole grid). Fix: split into `DAT`/`INP`/`SYS`/`CAL`/`OUT` modules.

**V3.** `Volume * Price` and the gross-profit expression are repeated. Breaks **Necessary** (and
**Performance** — recomputed several times; **Auditable** — long nested formulas). Fix: compute
`Gross Revenue = Volume * Price` and `COGS = Gross Revenue * COGS %` **once** as stepped line items,
then `Gross Profit = Gross Revenue - COGS`, `Net Margin % = Gross Profit / Gross Revenue`
(Formula summary, with a zero guard).

**V4.** Over-dimensioned and over-lined for what it reports. Breaks **Performance** (huge cell count)
and **Necessary** (40 line items, daily/customer/SKU grain unused). Fix: an **Outputs** module
dimensioned `Region × Time(month)` with only the lines the report shows; apply a **Time Range**.

**V5.** `SELECT: Entity.UK` hard-codes a member. Breaks **Sustainable** (adding Germany = copy-paste
edits) and **Necessary** (duplicated logic). Fix: dimension by Entity and use **mappings/`SUM`** so
all entities flow through one formula; no member named.

**V6.** Leftover experimental line items. Breaks **Necessary** (dead cells, confusion) and
**Auditable** (which one feeds the dashboard?). Fix: confirm the live one, **delete** `Revenue v2`
and `Revenue_OLD`, rename the survivor clearly.

---

## Part 3 — Refactor

**R1.** Issues in the draft:
1. `region` (typed Text) is a **mapping/attribute** → belongs in **System**, derived with `PARENT()`.
2. `cogs pct` typed every month is a **structural attribute** → belongs in **System** (`Product`
   grain), not retyped per period.
3. `Vol`/`Prc` are **inputs** → belong in an **Inputs** module, not the calc.
4. `profit` repeats `Vol*Prc` three times → **not Necessary/Auditable**; step it.
5. `Prc` summary = Sum is wrong → **Average**; `cogs pct` summary = Sum is wrong → Average.
6. Cryptic names (`Vol`, `Prc`, `rev`) → use meaningful names.

Corrected design:

**`SYS02 Product Details`** · System · Product

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| `COGS %` | Number (%) | Average | *(input)* |

**`SYS03 Org Details`** · System · Entity

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| `Region` | List: Region | None | `PARENT(ITEM(Entity))` |

**`INP01 Revenue Assumptions`** · Inputs · Entity × Product × Time × Versions

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| `Volume` | Number | Sum | *(input)* |
| `Price` | Number | Average | *(input)* |

**`CAL01 Revenue`** · Calculations · Entity × Product × Time × Versions

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| `Gross Revenue` | Number | Sum | `'INP01 Revenue Assumptions'.Volume * 'INP01 Revenue Assumptions'.Price` |
| `COGS` | Number | Sum | `Gross Revenue * 'SYS02 Product Details'.COGS %` |
| `Gross Profit` | Number | Sum | `Gross Revenue - COGS` |
| `Net Margin %` | Number (%) | Formula | `IF Gross Revenue = 0 THEN 0 ELSE Gross Profit / Gross Revenue` |

**Moved out:** `region` → `SYS03` (derived); `cogs pct` → `SYS02` (Product grain);
`Vol`/`Prc` → `INP01`. Result: one DISCO type per module, stepped/auditable, correct summaries, no
repeated sub-expressions.

---

**Related:** [DISCO](../../docs/03-methodology/disco.md) ·
[PLANS](../../docs/03-methodology/plans-standard.md) ·
[Model-build checklist](../../templates/model-build-checklist.md) ·
[Back to exercise](../modeling-design-exercises.md)
