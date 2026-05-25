# Capstone (L3) — Worked Solution

> **Level:** L3 · **Area:** Exercises (solutions) · Brief: [`../capstone-l3.md`](../capstone-l3.md)

One valid, PLANS-clean design for **Northwind Devices: FY27 Operating Plan**. Other designs work —
what's graded is DISCO discipline, no hard-coding, stepped/auditable calcs, and controlled
dimensionality. This reuses the [`_common`](../../blueprints/_common/) backbone pattern.

---

## 1. List-definition table

| List | Type | Parent | Top Level | Members (sample) |
| --- | --- | --- | --- | --- |
| `L1 Product Family` | hierarchy top | — | All Products | Hardware, Software, Services |
| `L2 Product` | hierarchy leaf | `L1 Product Family` | — | Sensor A, Sensor B, Platform License, Support Plan |
| `L1 Region` | hierarchy top | — | Total Org | EMEA, Americas, APAC |
| `L2 Country` | hierarchy | `L1 Region` | — | UK, USA, India |
| `L3 Cost Centre` | hierarchy leaf | `L2 Country` | — | CC-1100 UK Sales, … |
| `Currency` | flat | — | — | GBP, USD, INR (group = USD) |
| `L1 P&L Statement` | hierarchy top | — | — | Net Profit |
| `L2 P&L Group` | hierarchy | `L1 P&L Statement` | — | Revenue, COGS, Gross Profit, Opex, EBITDA |
| `L3 P&L Account` | hierarchy leaf | `L2 P&L Group` | — | Product Revenue, Direct Materials, Salaries… |

Planning grain (leaf lists): **`L2 Product`** and **`L3 Cost Centre`**. *(AC1)*

---

## 2. Module map + architecture

| Module | DISCO | Applies To | Purpose |
| --- | --- | --- | --- |
| `SYS01 Time Settings` | System | Time | `Is Actual?`, `Period Index`, `Period Start Date`, year flags |
| `SYS02 Organization Details` | System | L3 Cost Centre | `Country`, `Region`, `Local Currency`, `Is Active?` |
| `SYS03 Account Details` | System | L3 P&L Account | `Account Group`, `Sign`, `Is Revenue?` |
| `SYS04 Exchange Rates` | System | Currency × Time × Versions | `Rate to USD` (filled), `Is Group Currency?` |
| `INP01 Revenue Assumptions` | Inputs | L3 CC × L2 Product × Time × Versions | `Volume`, `Price Override` |
| `INP02 Price Setup` | Inputs | L2 Product × Versions (+ Year via Time Range) | `Base Price`, `Annual Increase %` |
| `INP03 Cost Drivers` | Inputs | L2 Product (+ L3 CC × Time × Versions for opex) | `COGS %`, `Fixed Opex (Local)` |
| `CAL01 Price` | Calculations | L2 Product × Time × Versions | derived monthly `Price (local)` |
| `CAL02 Revenue` | Calculations | L3 CC × L2 Product × Time × Versions | `Gross Revenue (local)` |
| `CAL03 Cost` | Calculations | L3 CC × L2 Product × Time × Versions | `COGS (local)` |
| `CAL04 P&L (Local)` | Calculations | L3 CC × Time × Versions | Revenue→EBITDA in local |
| `CAL05 P&L (USD)` | Calculations | L3 CC × Time × Versions | converted to USD |
| `CAL06 Reported P&L` | Calculations | L3 CC × Time × Versions | actuals/forecast blend |
| `DAT01 Actuals` | Data | L3 CC × L2 Product × Time × Versions | imported FY26 actuals |
| `OUT01 P&L Statement` | Outputs | L3 CC × Time × Versions | report (Local/USD selectable) |
| `OUT02 Top Products` | Outputs | L2 Product × Time | revenue + rank |

```
INP02 Price Setup ─> CAL01 Price ─┐
INP01 (Volume,override) ──────────┼─> CAL02 Revenue ─┐
INP03 (COGS %) ───────────────────┘                  ├─> CAL04 P&L (Local) ─> CAL05 P&L (USD) ─┐
INP03 (Fixed Opex) ──────────────> CAL03 Cost ───────┘            ▲                            ├─> CAL06 Reported ─> OUT01
SYS04 (FX) + SYS02 (Local Currency) ─────────────────────────────┘                            │
DAT01 Actuals ────────────────────────────────────────────────────────────────────────────────┘ (blend via SYS01.Is Actual?)
```

*(AC2 — each module is exactly one DISCO type, correctly prefixed.)*

---

## 3–4. Key blueprint tables & formulas

### RQ2 — Price derivation *(AC3)*

**`CAL01 Price`** · Calculations · L2 Product × Time × Versions

| Line Item | Format | Summary | Formula |
| --- | --- | --- | --- |
| `Years From Base` | Number | None | `YEARVALUE(ITEM(Time.Year)) - YEARVALUE(START of model)` (count of years since the base year, derived from the calendar — no year named) |
| `Uplift Factor` | Number | None | `(1 + 'INP02 Price Setup'.Annual Increase %) ^ Years From Base` |
| `Derived Price` | Number | Average | `'INP02 Price Setup'.Base Price * Uplift Factor` |
| `Price (local)` | Number | Average | `IF ISNOTBLANK('INP01 Revenue Assumptions'.Price Override) THEN 'INP01 Revenue Assumptions'.Price Override ELSE Derived Price` |

Base price compounds by the annual % via a power of "years since base" — derived from the calendar,
**no year hard-coded**. A per-month `Price Override` in Inputs wins when present. *(Sustainable)*

### RQ1/RQ3 — Revenue & costs

**`CAL02 Revenue`** · L3 CC × L2 Product × Time × Versions:

```
Gross Revenue (local) = 'INP01 Revenue Assumptions'.Volume * 'CAL01 Price'.Price (local)
```

**`CAL03 Cost`** · same grain:

```
COGS (local) = 'CAL02 Revenue'.Gross Revenue (local) * 'INP03 Cost Drivers'.COGS %
```

`COGS %` is a per-product driver in `INP03 Cost Drivers` (Product grain); it broadcasts across Cost
Centre/Time/Versions automatically. *(AC4)*

### RQ4 — P&L (local)

**`CAL04 P&L (Local)`** · L3 CC × Time × Versions (Product collapsed):

| Line Item | Summary | Formula |
| --- | --- | --- |
| `Revenue` | Sum | `'CAL02 Revenue'.Gross Revenue (local)[SUM: L2 Product]` |
| `COGS` | Sum | `'CAL03 Cost'.COGS (local)[SUM: L2 Product]` |
| `Gross Profit` | Sum | `Revenue - COGS` |
| `Fixed Opex` | Sum | `'INP03 Cost Drivers'.Fixed Opex (Local)` |
| `EBITDA` | Sum | `Gross Profit - Fixed Opex` |
| `EBITDA Margin %` | Formula | `IF Revenue = 0 THEN 0 ELSE EBITDA / Revenue` |

### RQ5 — Currency conversion *(AC5)*

**`SYS04 Exchange Rates`** holds `Rate to USD` per Currency × Time × Versions (filled to 1 for
USD). **`CAL05 P&L (USD)`** converts each line, looking up the rate by the cost centre's local
currency:

```
Revenue USD = 'CAL04 P&L (Local)'.Revenue
            * 'SYS04 Exchange Rates'.Rate (filled)[LOOKUP: 'SYS02 Organization Details'.Local Currency]
```

(Same pattern for COGS, Opex; Gross Profit/EBITDA recompute from the USD lines.) No rate
hard-coded; roll to FY28 and new months' rates simply get imported. *(Sustainable)*

### RQ6 — Actuals/forecast blend *(AC6)*

**`CAL06 Reported P&L`** · L3 CC × Time × Versions:

```
Reported Revenue =
  IF 'SYS01 Time Settings'.Is Actual?
  THEN 'DAT01 Actuals'.Revenue[SUM: L2 Product]
  ELSE 'CAL05 P&L (USD)'.Revenue USD
```

(Repeat per line.) Keyed to `Is Actual?` (driven by the current period) — advancing the period
re-splits automatically, **no edits**. *(Sustainable, Auditable)*

### RQ7 — Ranking *(AC7)*

**`OUT02 Top Products`** · L2 Product × Time:

```
Revenue           = 'CAL02 Revenue'.Gross Revenue (local)[SUM: L3 Cost Centre]
Product Rev Rank  = RANK(Revenue, DESCENDING, ANY, , L2 Product)   // within each month: Groups slot = L2 Product
Top 3 Product?    = Product Rev Rank <= 3
```

---

## 5. PLANS review + assumptions *(AC8, AC9)*

| Principle | How the design satisfies it |
| --- | --- |
| **Performance** | Time Ranges: `INP02 Price Setup`/`SYS04` need only plan years; `DAT01` only FY26 actual months; `INP01` FY27. No module dimensioned by a list it doesn't need (price has no CC/Entity dim; OpEx has no Product dim). |
| **Logical** | Strict D→I→S→C→O flow; one direction; mappings in System. |
| **Auditable** | Every P&L line stepped; EBITDA traces to Volume × Price; ratios use Formula summary with zero-guards. |
| **Necessary** | Each sub-expression (price, revenue, COGS) computed once and referenced; no duplicate or experimental line items. |
| **Sustainable** | No date/period/currency/member named in any formula; price uplift, FX and blend all driven by System/calendar; rolling to FY28 needs no formula change. |

**Assumptions:** FY = calendar year; one currency per country; daily→monthly FX handled upstream (or
rates imported monthly); Budget locked, Forecast editable; revenue posts to the `Product Revenue`
account. **Out of scope:** balance sheet/cash flow; allocations of shared-service OpEx across cost
centres; multi-tenant ALM promotion (note as the production path); workforce-level salary detail
(would feed `Fixed Opex` from a Workforce model in a real landscape).

**Time Ranges per module (AC8):** `INP01`/`CAL01–06`/`OUT*` → FY27 (+ FY26 for comparison where
shown); `DAT01` → FY26; `INP02`/`SYS04` → plan years only; `SYS01` → full model calendar (it defines
the flags).

---

**Related:** [Blueprints `_common`](../../blueprints/_common/) ·
[FP&A blueprint](../../blueprints/fpa-pl-planning/) · [DISCO](../../docs/03-methodology/disco.md) ·
[PLANS](../../docs/03-methodology/plans-standard.md) ·
[Cookbook (FX, allocation, rolling forecast)](../../cookbook/) ·
[Model-build checklist](../../templates/model-build-checklist.md) ·
[Back to brief](../capstone-l3.md)
