# Formula Exercises — Solutions

> **Level:** L1–L2 · **Area:** Exercises (solutions) · Exercise: [`../formula-exercises.md`](../formula-exercises.md)

Worked formulas in Anaplan syntax, with the line item's Format/Summary and a short rationale. Syntax
idioms (`TIMESUM`, `LAG`, `RANK`, `SUM`) follow [Anapedia](https://help.anaplan.com/); confirm
against your platform version (see [`SOURCES.md`](../../SOURCES.md)).

---

## 1. Core / aggregation

**1.1** `CAL01 Revenue.Gross Revenue` — Number, Sum:
```
Volume * Price
```
where `Volume` and `Price` are pulled from `INP01` into local steps first (house style). Direct
form: `'INP01 Revenue Assumptions'.Volume * 'INP01 Revenue Assumptions'.Price`.

**1.2** `CAL03 P&L.Gross Profit` — Number, Sum:
```
Revenue - COGS
```

**1.3** `OUT01 P&L Report.EBITDA Margin %` — Number (%), Summary = **Formula**:
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

**3.1** `SYS03 Org Details.Region` — List: Region, None:
```
PARENT(ITEM(Entity))
```
Derived from the hierarchy, so it never drifts (*Sustainable*).

**3.2** `CAL02 Costs.COGS %` — Number (%), Average:
```
'SYS02 Product Details'.COGS %
```
`SYS02` is dimensioned by **Product only**; when referenced inside a `Entity × Product × Time ×
Versions` line, Anaplan **repeats** the product's value across the other dimensions automatically —
no mapping function needed because Product is a shared dimension.

**3.3** Revenue by Region × Time, in a module dimensioned `Region × Time`:
```
'Revenue by Entity x Product x Time'.Revenue[SUM: 'SYS03 Org Details'.Region]
```
`SUM` reads the **Entity→Region** mapping and totals; Product collapses automatically because the
target isn't dimensioned by Product. (Equivalently aggregate Product first, then `SUM` Region.)

---

## 4. Allocation

**4.1** `OpEx by Product` — Number, Sum, Applies To Entity × Product × Time × Versions:
```
IF 'CAL01 Revenue'.Gross Revenue[SUM: Product] = 0
THEN 0
ELSE 'INP02 Cost Drivers'.Fixed OpEx
     * 'CAL01 Revenue'.Gross Revenue
     / 'CAL01 Revenue'.Gross Revenue[SUM: Product]
```
Each product gets OpEx in proportion to its share of the entity's revenue (`product revenue ÷ entity
total revenue`). The `IF … = 0` guard avoids divide-by-zero when an entity has no revenue. Compute
the entity total once if reused.

**4.2** `Marketing Monthly` — Number, Sum:
```
'INP… '.Marketing Budget (Annual) / 12
```
Even spread. (To spread by working days instead, divide by `SYS01.Days in Period[SUM: TIME = YEAR]`
and multiply by `SYS01.Days in Period` — driver-based, no hard-coded 12.)

---

## 5. Switchover

**5.1** `CAL03 P&L.Reported Revenue` — Number, Sum:
```
IF 'SYS01 Time Settings'.Is Actual Month?
THEN 'DAT01 Actuals'.Revenue[SUM: Product]
ELSE Revenue
```
`[SUM: Product]` collapses the actuals' Product dimension to match the P&L's Entity × Time grain.

**5.2** Because `IF Time <= Mar 2026` **hard-codes a date** — next month it's wrong, and rolling to
FY28 silently breaks. Keying off `SYS01.Is Actual Month?` (driven by the current period) means the
split moves itself. Principle: **Sustainable** (and it's a single source of truth — *Auditable*).

---

## 6. Ranking & conditional

**6.1** `Product Revenue Rank` — Number, None:
```
RANK('Gross Revenue', DESCENDING, ANY, Product)
```
Ranks products by revenue **within each month** (the rank is over the Product dimension; Time stays
on the axis). Largest revenue = rank 1. (Exact `RANK` argument order varies by platform — confirm in
Anapedia.)

**6.2** `Top 2 Product?` — Boolean, None:
```
Product Revenue Rank <= 2
```

**6.3** `Revenue Band` — Text, None:
```
IF Gross Revenue >= 50000 THEN "High"
ELSE IF Gross Revenue >= 20000 THEN "Medium"
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
