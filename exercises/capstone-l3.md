# Capstone (L3) — Build From Requirements

> **Level:** L3 · **Area:** Exercises · Solution: [`solutions/capstone-l3-solution.md`](solutions/capstone-l3-solution.md)

This is an **L3-style brief**: a small but *complete* planning scenario described in business
language, with **acceptance criteria** and **hints** — but no step-by-step. Your job is to do what a
consultant does on day one: turn written requirements into a model design (lists, DISCO modules,
blueprint tables, key formulas), review it against PLANS, and state your assumptions.

Work it as a paper design first. Then compare with the
[worked solution](solutions/capstone-l3-solution.md) — there are several valid designs; the
solution explains *why* its choices satisfy PLANS.

> Prereq: finish the [tutorials](../tutorials/) and the L1/L2 exercises. Use the
> [user-story](../templates/user-story-template.md) and
> [blueprint](../templates/blueprint-template.md) templates, and run the
> [model-build checklist](../templates/model-build-checklist.md) at the end.

---

## The business brief — "Northwind Devices: FY27 Operating Plan"

Northwind Devices sells hardware and services across three regions. Finance wants a connected
**operating plan** in Anaplan to replace the current spreadsheet. You're the model builder.

### Background

- They sell **products** (`Sensor A`, `Sensor B`, `Platform License`, `Support Plan`) grouped into
  families (`Hardware`, `Software`, `Services`).
- They operate through **cost centres** under **countries** under **regions** (e.g.
  `EMEA › UK › CC-1100 UK Sales`). Each country has a **local currency**; the group reports in
  **USD**.
- Planning grain is **monthly**; the plan covers **FY27**, with **FY26 actuals** loaded for
  comparison. "Today" is **Mar FY26**.
- Versions: **Actual**, **Budget**, **Forecast**.

### What the business wants (requirements)

**RQ1 — Revenue plan.** Planners enter **Volume** and **Price** per product, per cost centre, per
month, for the Forecast version. Revenue = Volume × Price.

**RQ2 — Price uplift.** Instead of typing every month's price, planners enter a **base price** (per
product) and an **annual price-increase %** (per product, per year); the model derives the monthly
price. Planners can still override a specific month.

**RQ3 — Cost plan.** Two cost streams:
- **Variable COGS** = revenue × a per-product `COGS %` (a structural attribute, not a planner input).
- **Fixed OpEx** typed per cost centre per month.

**RQ4 — P&L.** Roll up to a P&L per cost centre (and therefore per country/region):
`Revenue → COGS → Gross Profit → Fixed OpEx → EBITDA`, with `EBITDA Margin %`.

**RQ5 — Currency.** Plans are entered in **local currency** but the consolidated P&L must report in
**USD**, using a **monthly rate** per currency per version. No rate may be hard-coded.

**RQ6 — Actuals & forecast blend.** Load FY26 actuals; the **Forecast** P&L must show **actuals for
past months** and **plan for future months**, splitting at "today" automatically as the period
advances.

**RQ7 — Reporting.** A UX page: P&L grid (rows = P&L lines, columns = months) with **Region**,
**Version** and **Currency view (Local/USD)** selectors, plus a **top-products** view ranking
products by revenue.

### Constraints (PLANS)

- **Performance:** assumptions and actuals must use **Time Ranges** (not the full calendar where
  unnecessary); don't dimension a module by lists it doesn't need.
- **Sustainable:** no hard-coded dates, periods, currencies or list members in any formula. Rolling
  to FY28 must need **no formula changes**.
- **Auditable:** stepped line items; a reviewer can trace EBITDA back to Volume × Price.
- **Necessary:** no duplicate calculations or unused line items.

---

## Acceptance criteria (your design must satisfy these)

- [ ] **AC1** Lists model the product family→product and region→country→cost-centre hierarchies;
      modules are dimensioned by the correct **leaf** lists.
- [ ] **AC2** Every module is exactly one DISCO type and named with the right prefix.
- [ ] **AC3** Monthly price is derived from base price + annual uplift, with a per-month override
      path; no period is named in the formula.
- [ ] **AC4** COGS % lives in a **System** module; planners cannot edit it on the input page.
- [ ] **AC5** Local→USD conversion reads a System FX module by the cost centre's local currency and
      the month/version; no rate is hard-coded.
- [ ] **AC6** The Forecast P&L blends actuals/forecast via a **System Boolean** keyed to the current
      period; advancing the period re-splits with no edits.
- [ ] **AC7** A product-revenue **ranking** is available for the top-products view.
- [ ] **AC8** Time Ranges and dimensionality choices are stated and justified per module.
- [ ] **AC9** You list your **assumptions** and any **out-of-scope** items.

---

## Hints

- **Lists:** reuse the `_common` backbone pattern — `L1 Product Family › L2 Product`,
  `L1 Region › L2 Country › L3 Cost Centre/Entity`, `Currency`, and the `L1/L2/L3 P&L Account`
  hierarchy (see [`blueprints/_common/`](../blueprints/_common/)).
- **RQ2 price uplift:** think *base price (Product)* × *cumulative uplift factor (Product × Year)*,
  then `IF override exists THEN override ELSE derived`. Where do base/uplift/override each live
  (System vs Inputs)? How do you compound the uplift year over year without naming a year?
- **RQ5 currency:** one System FX module `SYS04 Exchange Rates` (Currency × Time × Versions) +
  `Local Currency` per cost centre in `SYS Org Details`. Convert *on the way up*. A `Currency view`
  selector can switch the page between Local and USD line items.
- **RQ6 blend:** `SYS01 Time Settings.Is Actual Month?` keyed to the current period; the same idiom
  as [Tutorial Step 7](../tutorials/07-import-actuals.md).
- **RQ7 ranking:** `RANK( … , DESCENDING)` within month — see the
  [formula exercises](formula-exercises.md) section 6.
- **DISCO order:** sketch D → I → S → C → O and draw the arrows before writing any formula.

---

## Deliverables (what to produce)

1. A **list-definition table** (all lists, types, parents).
2. A **module map** (each module: name · DISCO · Applies To · purpose) with an architecture sketch.
3. **Blueprint tables** for the key modules (at least the price-derivation, revenue, currency
   conversion, P&L, blend and ranking).
4. The **key formulas** in Anaplan syntax, stepped.
5. A short **PLANS review** (one line per principle) + your **assumptions / out-of-scope** list.

---

**Related:** [Blueprints `_common`](../blueprints/_common/) ·
[FP&A blueprint](../blueprints/fpa-pl-planning/) · [DISCO](../docs/03-methodology/disco.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) · [Templates](../templates/) ·
[Cookbook (FX, allocation, rolling forecast)](../cookbook/) ·
[Solution →](solutions/capstone-l3-solution.md)
