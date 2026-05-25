# Step 4 — Input Modules (the DISCO "I")

> **Level:** L1 · **Area:** Tutorial · **DISCO:** Inputs · **PLANS:** Logical, Necessary

**Input modules** hold the numbers humans type — the planning assumptions. They are the *only*
modules most planners should edit. Keep them clean, dashboard-friendly, and minimally dimensioned.
See [DISCO](../docs/03-methodology/disco.md).

We need three, matching the blueprint: revenue assumptions (volume & price), the opex plan, and the
cost drivers (COGS %).

---

## 4.1 INP01 Revenue Assumptions

Revenue is driven by **volume × price**, planned per Product, per Cost Centre, per Month, per
Version. Prices are in each cost centre's **local currency** — conversion to USD happens in Step 5.

**Modules → New Module.** Name `INP01 Revenue Assumptions`.
**Applies To:** `L3 Cost Centre`, `L2 Product`. **Plus Time** (months) and **Versions**.

> In the module's **Applies To**, add the lists `L3 Cost Centre` and `L2 Product`. Time and Versions
> are added via the *Time* and *Versions* toggles. Dimension order: list dims, then Time, then
> Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Volume` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | *(input — units sold)* |
| `Price (local)` | Number (2 dp) | Average | L3 Cost Centre, L2 Product, Time, Versions | *(input — unit price in local currency)* |

Notes:

- **`Price (local)` summary = Average, not Sum.** A price shouldn't add up across months/products —
  summing it is meaningless. Choosing summary deliberately is a PLANS *Auditable* point.
- Enter a few values for the `Forecast` version, FY25 months (e.g. Sensor A in a UK cost centre:
  Volume 1,000/mo, Price (local) £25). Leave Budget/Actual blank for now.

> **Don't put `Revenue = Volume * Price (local)` here.** Inputs hold *typed* numbers only. The
> multiplication is a **calculation** (Step 5). Mixing input + calc in one module breaks DISCO and
> makes the cell editable-but-also-formula (impossible) — Anaplan forces you to pick. Keep them
> separate.

---

## 4.2 INP02 Opex Plan

Operating expenses planned per cost centre, in local currency. (In a fuller model, salaries here
would be **fed from a Workforce model** rather than typed — see the
[blueprint hand-offs](../blueprints/fpa-pl-planning/README.md).)

**Applies To:** `L3 Cost Centre`, plus Time and Versions. (Opex is planned at cost-centre level, not
per product, in this tutorial — fewer dimensions = smaller module = **Performance**.)

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Opex (local)` | Number | Sum | L3 Cost Centre, Time, Versions | *(input — expense in local currency)* |

Enter `Opex (local)` for the Forecast version (e.g. a UK cost centre £40,000/mo).

---

## 4.3 INP03 Cost Drivers

A product's **COGS %** — the direct cost as a percentage of revenue. Planners *do* tune this each
cycle, so it's an Input, not a System attribute. It's dimensioned by **Product only**.

**Applies To:** `L2 Product`.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `COGS %` | Number (%) | Average | L2 Product | *(input — e.g. Hardware 60%, Software 15%)* |

> **Why its own module at Product grain?** `COGS %` doesn't vary by cost centre, month or version, so
> dimensioning it by `L2 Product` only keeps it tiny. When the cost calc reads it inside a
> `Cost Centre × Product × Time × Versions` line, Anaplan broadcasts the product's value across the
> other dimensions automatically (PLANS *Performance, Necessary*).

---

## 4.4 A note on dimensionality (Performance)

| Module | Dimensions | Why |
| --- | --- | --- |
| `INP01 Revenue Assumptions` | L3 Cost Centre × L2 Product × Time × Versions | Revenue genuinely varies by product |
| `INP02 Opex Plan` | L3 Cost Centre × Time × Versions | Opex doesn't vary by product here |
| `INP03 Cost Drivers` | L2 Product | COGS % varies only by product |

Don't add `L2 Product` to `INP02` "to be safe" — that multiplies the cell count for no business
reason. Dimension a module only by the lists it **needs** (PLANS *Performance*, the single biggest
lever).

---

## 4.5 Sanity check

- [ ] `INP01` applies to L3 Cost Centre × L2 Product × Time × Versions; `Price (local)` summary =
      **Average**.
- [ ] `INP02 Opex Plan` applies to L3 Cost Centre × Time × Versions (no Product).
- [ ] `INP03 Cost Drivers` applies to L2 Product only and holds `COGS %`.
- [ ] All three contain **only input** line items — no formulas computing revenue/cost.
- [ ] You typed a few Forecast values so Step 5 has something to calculate.

> **DISCO check:** these are pure **Inputs**. Mappings/flags (`Region`, `Local Currency`, `Sign`)
> stayed in **System** (`SYS02`/`SYS03`). Good separation.

---

**Related:** [Modules](../docs/01-fundamentals/modules.md) ·
[Line items & formats](../docs/01-fundamentals/line-items-and-formats.md) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Performance](../docs/07-performance/)

**Next → [Step 5 — Calculation Modules](05-calculation-modules.md)**
