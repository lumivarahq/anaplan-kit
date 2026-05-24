# Formula Exercises — Write the Formula

> **Level:** L1–L2 · **Area:** Exercises · Solutions: [`solutions/formula-solutions.md`](solutions/formula-solutions.md)

Given a requirement, write the **Anaplan-syntax formula** (and say which line item / module it lives
in, with the right Format and Summary). Use the FP&A model's lists and modules from the
[tutorials](../tutorials/). Check the [formula docs](../docs/02-formulas/) if you're stuck. Try
before peeking at [solutions](solutions/formula-solutions.md).

> Reminder of the model: lists `Region › Entity`, `Product`; native `Time` (FY25–FY27 months) and
> `Versions` (`Actual`/`Budget`/`Forecast`); modules `SYS01 Time Settings`, `SYS02 Product Details`
> (`COGS %`), `SYS03 Org Details` (`Region`), `INP01 Revenue Assumptions` (`Volume`, `Price`),
> `INP02 Cost Drivers` (`Fixed OpEx`), `CAL01–03`, `DAT01 Actuals`, `OUT01 P&L Report`.

---

## 1. Core / aggregation

**1.1 (L1).** In `CAL01 Revenue`, write `Gross Revenue` from the assumptions module.

**1.2 (L1).** Write `Gross Profit` in `CAL03 P&L` from `Revenue` and `COGS`.

**1.3 (L1).** Write `EBITDA Margin %` (a display ratio) in `OUT01 P&L Report`, guarding against
divide-by-zero when `Revenue` is 0.

---

## 2. YTD / time

**2.1 (L1).** Add `Revenue YTD` to `OUT01` — cumulative revenue from the start of the fiscal year to
the current month.

**2.2 (L2).** Add `Revenue Prior Year` — the same month last year — so you can show YoY growth.
Then write `Revenue YoY %`.

**2.3 (L2).** Write `Avg Monthly Revenue (Last 3 Months)` — a 3-month trailing average.

---

## 3. Mapping (LOOKUP / SUM)

**3.1 (L1).** In `SYS03 Org Details`, derive each entity's `Region` from the hierarchy (no typing).

**3.2 (L2).** `CAL02 Costs` needs each row's `COGS %` from `SYS02 Product Details`. Write it. (It's a
property of Product only — how does it apply across the Entity/Time/Versions dims?)

**3.3 (L2).** You have a module `Revenue by Entity × Product × Time` and want **Revenue by Region ×
Time** (collapsing Entity to Region and summing Product). The Entity→Region mapping is in
`SYS03 Org Details.Region`. Write the `SUM` formula.

---

## 4. Allocation

**4.1 (L2).** `INP02 Cost Drivers.Fixed OpEx` is planned at **entity level**. You want to **allocate**
it down to products in proportion to each product's `Gross Revenue`. Write the allocated
`OpEx by Product` line (Entity × Product × Time × Versions). Handle the case where an entity's total
revenue is 0.

**4.2 (L2).** An annual marketing budget of `Marketing Budget (Annual)` per entity must be **spread
evenly across the 12 months** of the year. Write the monthly line.

---

## 5. Switchover (Actual vs Forecast blend)

**5.1 (L2).** Using `SYS01 Time Settings.Is Actual Month?`, write `Reported Revenue` in `CAL03 P&L`:
show `DAT01 Actuals` revenue for actual months, the forecast `Revenue` for future months. (Actuals
are Entity × Product × Time; the P&L is Entity × Time.)

**5.2 (L2).** Why must this blend key off the **System Boolean** rather than `IF Time <= Mar 2026`?
Name the PLANS principle.

---

## 6. Ranking & conditional

**6.1 (L2).** In an Outputs module dimensioned by `Product × Time`, write `Product Revenue Rank` —
rank products by `Gross Revenue` within each month, largest = 1.

**6.2 (L2).** Write `Top 2 Product?` — a Boolean that is `TRUE` for the two highest-revenue products
in each month (reuse the rank from 6.1).

**6.3 (L1).** Write `Revenue Band` (Text): `"High"` if `Gross Revenue >= 50000`, `"Medium"` if
`>= 20000`, else `"Low"`.

---

**Related:** [Formula reference](../docs/02-formulas/) ·
[Cheat sheet](../docs/02-formulas/cheatsheet.md) ·
[Lookup & mapping](../docs/02-formulas/lookup-and-mapping.md) ·
[Time tutorial](../tutorials/02-time-and-versions.md) ·
[Solutions →](solutions/formula-solutions.md)
