# Step 4 — Input Modules (the DISCO "I")

> **Level:** L1 · **Area:** Tutorial · **DISCO:** Inputs · **PLANS:** Logical, Necessary

**Input modules** hold the numbers humans type — the planning assumptions. They are the *only*
modules most planners should edit. Keep them clean, dashboard-friendly, and minimally dimensioned.
See [DISCO](../docs/03-methodology/disco.md).

We need two: revenue assumptions (volume & price) and cost drivers.

---

## 4.1 INP01 Revenue Assumptions

Revenue is driven by **volume × price**, planned per Product, per Entity, per Month, per Version.

**Modules → New Module.** Name `INP01 Revenue Assumptions`.
**Applies To:** `Entity`, `Product`. **Plus Time** (months) and **Versions**.

> In the module's **Applies To**, add the lists `Entity` and `Product`. Time and Versions are added
> via the *Time* and *Versions* toggles. Dimension order: list dims, then Time, then Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Volume` | Number | Sum | Entity, Product, Time, Versions | *(input)* |
| `Price` | Number | Average | Entity, Product, Time, Versions | *(input)* |
| `Price Growth %` | Number (%) | Average | Entity, Product, Time, Versions | *(input — optional)* |

Notes:
- **`Price` summary = Average, not Sum.** A price shouldn't add up across months/products — summing
  it is meaningless. Choosing summary deliberately is a PLANS *Auditable* point.
- Enter a few values for `Forecast` version, FY26 months (e.g. Widget A: Volume 1,000/mo, Price
  £25). Leave Budget/Actual blank for now.

> **Don't put `Revenue = Volume * Price` here.** Inputs hold *typed* numbers only. The
> multiplication is a **calculation** (Step 5). Mixing input + calc in one module breaks DISCO and
> makes the cell editable-but-also-formula (impossible) — Anaplan forces you to pick. Keep them
> separate.

---

## 4.2 INP02 Cost Drivers

Costs in this model come from two places: a variable **COGS %** (already a product attribute in
`SYS02`) applied to revenue, and planned **fixed operating costs** per entity. The *planned* part
goes here.

**Applies To:** `Entity`, plus Time and Versions. (Costs are planned at entity level, not per
product, in this tutorial — fewer dimensions = smaller module = **Performance**.)

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Fixed OpEx` | Number | Sum | Entity, Time, Versions | *(input)* |
| `Headcount` | Number | Sum | Entity, Time, Versions | *(input — optional driver)* |
| `Cost per Head` | Number | Average | Entity, Time, Versions | *(input — optional)* |

Enter `Fixed OpEx` for the Forecast version (e.g. UK £40,000/mo). The optional `Headcount` /
`Cost per Head` show how you'd drive a personnel cost — keep them only if you'll use them
(**Necessary**).

---

## 4.3 A note on dimensionality (Performance)

| Module | Dimensions | Why |
| --- | --- | --- |
| `INP01 Revenue Assumptions` | Entity × Product × Time × Versions | Revenue genuinely varies by product |
| `INP02 Cost Drivers` | Entity × Time × Versions | Fixed costs don't vary by product here |

Don't add `Product` to `INP02` "to be safe" — that multiplies the cell count for no business
reason. Dimension a module only by the lists it **needs** (PLANS *Performance*, the single biggest
lever).

---

## 4.4 Sanity check

- [ ] `INP01` applies to Entity × Product × Time × Versions; `Price` summary = **Average**.
- [ ] `INP02` applies to Entity × Time × Versions (no Product).
- [ ] Both contain **only input** line items — no formulas computing revenue/cost.
- [ ] You typed a few Forecast values so Step 5 has something to calculate.

> **DISCO check:** these are pure **Inputs**. Attributes (COGS %, Is Active?) stayed in **System**
> (`SYS02`). Good separation.

---

**Related:** [Modules](../docs/01-fundamentals/modules.md) ·
[Line items & formats](../docs/01-fundamentals/line-items-and-formats.md) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Performance](../docs/07-performance/)

**Next → [Step 5 — Calculation Modules](05-calculation-modules.md)**
