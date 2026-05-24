# Formula Exercises — Solutions

> **Level:** L1–L2 · **Area:** Exercises (solutions) · Exercise: [`../formula-exercises.md`](../formula-exercises.md)

Worked formulas in Anaplan syntax, with the line item's Format/Summary and a short rationale. Syntax
idioms (`TIMESUM`, `LAG`, `RANK`, `SUM`) follow [Anapedia](https://help.anaplan.com/); confirm
against your platform version (see [`SOURCES.md`](../../SOURCES.md)).

---

## 1. Core / aggregation

**1.1** `CAL01 Revenue.Gross Revenue (local)` — Number, Sum:
```
Volume * Price (local)
```
where `Volume` and `Price (local)` are pulled from `INP01` into local steps first (house style).
Direct form: `'INP01 Revenue Assumptions'.Volume * 'INP01 Revenue Assumptions'.Price (local)`.

**1.2** `CAL04 P&L Build.Gross Profit` — Number, Sum:
```
Revenue - COGS
```

**1.3** `OUT01 P&L Statement.EBITDA Margin %` — Number (%), Summary = **Formula**:
```
IF Revenue = 0 THEN 0 ELSE EBITDA / Revenue
```
The `IF Revenue = 0` guard prevents divide-by-zero; Summary = Formula recomputes the ratio at every
roll-up level (don't average monthly percentages).

---

## 2. YTD / time

**2.1** `Revenue YTD` — Number, Sum:
```
YTD(Revenue)
```
`YTD()` accumulates from the start of the fiscal year to the current period. (Equivalent:
`TIMESUM(Revenue, START OF YEAR, PERIOD)` style on platforms without `YTD()`.)

**2.2** `Revenue Prior Year` — Number, Sum:
```
LAG(Revenue, 12, 0)
```
(or `Revenue[PREVIOUS: 12]` / `LAG(Revenue, 1, 0, YEAR)` for a year offset depending on your
calendar). Then `Revenue YoY %` — Number (%), Formula:
```
IF Revenue Prior Year = 0 THEN 0 ELSE (Revenue - Revenue Prior Year) / Revenue Prior Year
```

**2.3** `Avg Monthly Revenue (Last 3 Months)` — Number, Average:
```
(Revenue + LAG(Revenue, 1, 0) + LAG(Revenue, 2, 0)) / 3
```
(Cleaner with `MOVINGSUM(Revenue, -2, 0)/3` if available.)

---

## 3. Mapping

**3.1** `SYS02 Organization Details.Region` — List: L1 Region, None:
```
PARENT(Country)
```
Derived up the hierarchy from `Country` (itself `PARENT(ITEM(L3 Cost Centre))`), so it never drifts
(*Sustainable*).

**3.2** `CAL02 Cost.COGS %` — Number (%), Average:
```
'INP03 Cost Drivers'.COGS %
```
`INP03` is dimensioned by **L2 Product only**; when referenced inside an `L3 Cost Centre × L2 Product
× Time × Versions` line, Anaplan **repeats** the product's value across the other dimensions
automatically — no mapping function needed because Product is a shared dimension.

**3.3** Revenue by Region × Time, in a module dimensioned `L1 Region × Time`:
```
'CAL01 Revenue'.Gross Revenue (local)[SUM: 'SYS02 Organization Details'.Region]
```
`SUM` reads the **Cost Centre→Region** mapping and totals; Product collapses automatically because
the target isn't dimensioned by Product. (Equivalently aggregate Product first, then `SUM` Region.)

---

## 4. Allocation

**4.1** `Opex by Product` — Number, Sum, Applies To L3 Cost Centre × L2 Product × Time × Versions:
```
IF 'CAL01 Revenue'.Gross Revenue (local)[SUM: L2 Product] = 0
THEN 0
ELSE 'INP02 Opex Plan'.Opex (local)
     * 'CAL01 Revenue'.Gross Revenue (local)
     / 'CAL01 Revenue'.Gross Revenue (local)[SUM: L2 Product]
```
Each product gets opex in proportion to its share of the cost centre's revenue (`product revenue ÷
cost-centre total revenue`). The `IF … = 0` guard avoids divide-by-zero when a cost centre has no
revenue. Compute the cost-centre total once if reused.

**4.2** `Marketing Monthly` — Number, Sum:
```
'INP… '.Marketing Budget (Annual) / 12
```
Even spread. (To spread by working days instead, divide by `SYS01.Days in Period[SUM: TIME = YEAR]`
and multiply by `SYS01.Days in Period` — driver-based, no hard-coded 12.)

---

## 5. Switchover

**5.1** `CAL04 P&L Build.Reported Revenue` — Number, Sum:
```
IF 'SYS01 Time Settings'.Is Actual?
THEN 'DAT01 Actuals'.Revenue[SUM: L2 Product]
ELSE Revenue
```
`[SUM: L2 Product]` collapses the actuals' Product dimension to match the P&L's L3 Cost Centre × Time
grain.

**5.2** Because `IF Time <= Mar 2026` **hard-codes a date** — next month it's wrong, and rolling to
FY28 silently breaks. Keying off `SYS01.Is Actual?` (driven by the current period) means the split
moves itself. Principle: **Sustainable** (and it's a single source of truth — *Auditable*).

---

## 6. Ranking & conditional

**6.1** `Product Revenue Rank` — Number, None (in an Outputs module dimensioned `L2 Product × Time`
that holds a `Revenue` line = `'CAL01 Revenue'.Gross Revenue (local)[SUM: L3 Cost Centre]`):
```
RANK(Revenue, DESCENDING, ANY, , L2 Product)
```
`RANK(values, Direction, Equal-handling, Include-value, Groups)`: the **Groups** slot (5th argument)
takes `L2 Product`, so the rank is computed **within each month** (over the Product dimension; Time
stays on the axis). The Include-value (tie-break) slot is left empty here. Largest revenue = rank 1.
The line-item reference `Revenue` is **not** quoted — quotes are only for module/list names with
spaces. (Confirm argument order in [Anapedia](https://help.anaplan.com/rank-a5f5778e-5e88-48ad-96ad-715178cda9b2).)

**6.2** `Top 2 Product?` — Boolean, None:
```
Product Revenue Rank <= 2
```

**6.3** `Revenue Band` — Text, None:
```
IF Gross Revenue (local) >= 50000 THEN "High"
ELSE IF Gross Revenue (local) >= 20000 THEN "Medium"
ELSE "Low"
```
(For a large module, prefer Booleans + a small text-mapping module over big nested `IF`/text — but
for a thin Outputs module this is fine.)

---

**Related:** [Formula reference](../../docs/02-formulas/) ·
[Lookup & mapping](../../docs/02-formulas/lookup-and-mapping.md) ·
[Cheat sheet](../../docs/02-formulas/cheatsheet.md) ·
[PLANS](../../docs/03-methodology/plans-standard.md) ·
[Back to exercise](../formula-exercises.md)
