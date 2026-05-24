# Formula Exercises — Write the Formula

> **Level:** L1–L2 · **Area:** Exercises · Solutions: [`solutions/formula-solutions.md`](solutions/formula-solutions.md)

Given a requirement, write the **Anaplan-syntax formula** (and say which line item / module it lives
in, with the right Format and Summary). Use the FP&A model's lists and modules from the
[tutorials](../tutorials/). Check the [formula docs](../docs/02-formulas/) if you're stuck. Try
before peeking at [solutions](solutions/formula-solutions.md).

> Reminder of the model (the canonical FP&A P&L model — see
> [`blueprints/fpa-pl-planning/`](../blueprints/fpa-pl-planning/)): lists
> `L1 Region › L2 Country › L3 Cost Centre`, `L1 Product Family › L2 Product`, the
> `L1/L2/L3 P&L Account` hierarchy, `Currency`; native `Time` (FY24–FY26 months) and `Versions`
> (`Actual`/`Budget`/`Forecast`); modules `SYS01 Time Settings`, `SYS02 Organization Details`
> (`Region`, `Local Currency`), `SYS03 Account Details`, `SYS04 Exchange Rates` (`Rate to USD`),
> `INP01 Revenue Assumptions` (`Volume`, `Price (local)`), `INP02 Opex Plan` (`Opex (local)`),
> `INP03 Cost Drivers` (`COGS %`), `CAL01 Revenue`–`CAL04 P&L Build`, `DAT01 Actuals`,
> `OUT01 P&L Statement`.

---

## 1. Core / aggregation

**1.1 (L1).** In `CAL01 Revenue`, write `Gross Revenue (local)` from the assumptions module.

**1.2 (L1).** Write `Gross Profit` in `CAL04 P&L Build` from `Revenue` and `COGS`.

**1.3 (L1).** Write `EBITDA Margin %` (a display ratio) in `OUT01 P&L Statement`, guarding against
divide-by-zero when `Revenue` is 0.

---

## 2. YTD / time

**2.1 (L1).** Add `Revenue YTD` to `OUT01 P&L Statement` — cumulative revenue from the start of the
fiscal year to the current month.

**2.2 (L2).** Add `Revenue Prior Year` — the same month last year — so you can show YoY growth.
Then write `Revenue YoY %`.

**2.3 (L2).** Write `Avg Monthly Revenue (Last 3 Months)` — a 3-month trailing average.

---

## 3. Mapping (LOOKUP / SUM)

**3.1 (L1).** In `SYS02 Organization Details`, derive each cost centre's `Region` from the hierarchy
(no typing).

**3.2 (L2).** `CAL02 Cost` needs each row's `COGS %` from `INP03 Cost Drivers`. Write it. (It's a
property of Product only — how does it apply across the Cost Centre/Time/Versions dims?)

**3.3 (L2).** You have revenue by `L3 Cost Centre × L2 Product × Time` (in `CAL01 Revenue`) and want
**Revenue by Region × Time** (collapsing Cost Centre to Region and summing Product). The Cost
Centre→Region mapping is in `SYS02 Organization Details.Region`. Write the `SUM` formula.

---

## 4. Allocation

**4.1 (L2).** `INP02 Opex Plan.Opex (local)` is planned at **cost-centre level**. You want to
**allocate** it down to products in proportion to each product's `Gross Revenue (local)`. Write the
allocated `Opex by Product` line (L3 Cost Centre × L2 Product × Time × Versions). Handle the case
where a cost centre's total revenue is 0.

**4.2 (L2).** An annual marketing budget of `Marketing Budget (Annual)` per cost centre must be
**spread evenly across the 12 months** of the year. Write the monthly line.

---

## 5. Switchover (Actual vs Forecast blend)

**5.1 (L2).** Using `SYS01 Time Settings.Is Actual?`, write `Reported Revenue` in `CAL04 P&L Build`:
show `DAT01 Actuals` revenue for actual months, the forecast `Revenue` for future months. (Actuals
are L3 Cost Centre × L2 Product × Time; the P&L is L3 Cost Centre × Time.)

**5.2 (L2).** Why must this blend key off the **System Boolean** rather than `IF Time <= Mar 2026`?
Name the PLANS principle.

---

## 6. Ranking & conditional

**6.1 (L2).** In an Outputs module dimensioned by `L2 Product × Time`, write `Product Revenue Rank` —
rank products by `Gross Revenue (local)` within each month, largest = 1.

**6.2 (L2).** Write `Top 2 Product?` — a Boolean that is `TRUE` for the two highest-revenue products
in each month (reuse the rank from 6.1).

**6.3 (L1).** Write `Revenue Band` (Text): `"High"` if `Gross Revenue (local) >= 50000`, `"Medium"`
if `>= 20000`, else `"Low"`.

---

**Related:** [Formula reference](../docs/02-formulas/) ·
[Cheat sheet](../docs/02-formulas/cheatsheet.md) ·
[Lookup & mapping](../docs/02-formulas/lookup-and-mapping.md) ·
[Time tutorial](../tutorials/02-time-and-versions.md) ·
[Solutions →](solutions/formula-solutions.md)
