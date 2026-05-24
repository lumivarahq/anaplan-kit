# Step 5 — Calculation Modules (the DISCO "C")

> **Level:** L1→L2 · **Area:** Tutorial · **DISCO:** Calculations · **PLANS:** Auditable, Performance

**Calculation modules** are the engine room — where **Inputs** (Step 4), **System** flags
(Step 3) and (later) **Data** meet to produce real numbers. The golden rule: **break logic into
stepped line items**, one per logical step. Stepped formulas are faster to recalc and far easier to
audit than one giant nested expression. See [DISCO](../docs/03-methodology/disco.md) and
[PLANS — Auditable](../docs/03-methodology/plans-standard.md).

We'll build three: revenue, costs, and the P&L roll-up.

---

## 5.1 CAL01 Revenue

Revenue = `Volume × Price`. Both drivers live in `INP01 Revenue Assumptions`; we only *compute*
here.

**Modules → New Module.** Name `CAL01 Revenue`.
**Applies To:** `Entity`, `Product`, plus **Time** and **Versions** (same grain as `INP01`).

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Volume` | Number | Sum | Entity, Product, Time, Versions | `'INP01 Revenue Assumptions'.Volume` |
| `Price` | Number | Average | Entity, Product, Time, Versions | `'INP01 Revenue Assumptions'.Price` |
| `Gross Revenue` | Number | Sum | Entity, Product, Time, Versions | `Volume * Price` |

Notes:
- We pull `Volume` and `Price` into local line items first, then multiply. That one extra step is
  deliberate — it keeps `Gross Revenue` a one-token-per-side formula that reads itself
  (*Auditable*). You could write `'INP01…'.Volume * 'INP01…'.Price` directly, but the stepped form
  is the house style.
- `Gross Revenue` summary = **Sum** (revenue genuinely adds up across products, entities, months).
- `Price` keeps summary = **Average** for the same reason as in `INP01`.

---

## 5.2 CAL02 Costs

Two cost streams: **variable COGS** (revenue × the product's `COGS %` from `SYS02`) and **fixed
OpEx** (typed in `INP02`). We compute each, then total.

**Applies To:** `Entity`, `Product`, plus Time and Versions.

> Why `Product` here when `INP02 Cost Drivers` had none? COGS is product-driven (it reads
> `CAL01.Gross Revenue`, which is per product). Fixed OpEx isn't — we bring it in at entity level
> and it simply repeats/aggregates across the Product dimension. Keep reading.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `COGS %` | Number (%) | Average | Entity, Product, Time, Versions | `'SYS02 Product Details'.COGS %` |
| `COGS` | Number | Sum | Entity, Product, Time, Versions | `'CAL01 Revenue'.Gross Revenue * COGS %` |
| `Fixed OpEx` | Number | Sum | Entity, Time, Versions | `'INP02 Cost Drivers'.Fixed OpEx` |
| `Total Cost` | Number | Sum | Entity, Product, Time, Versions | `COGS + Fixed OpEx` |

Notes:
- `COGS %` is read from the **System** module — never typed here. Change a product's cost ratio in
  one place (`SYS02`) and every period follows (*Sustainable*).
- `Fixed OpEx` is dimensioned **Entity × Time × Versions** (no Product) — it matches its source.
  When it's used inside the Product-dimensioned `Total Cost`, Anaplan repeats the entity value
  across products; if you'd rather it sit on one product line, allocate it (see the
  [allocation recipe](../cookbook/README.md) and the
  [allocation exercise](../exercises/formula-exercises.md)). For this tutorial, totalling at the
  entity level (Section 5.3) avoids double-counting — see the note there.

> **Performance:** `COGS` reads `Gross Revenue` once. Don't re-derive `Volume * Price * COGS %` here
> — reference the existing line item. Calculate once, reference many (*Necessary, Performance*).

---

## 5.3 CAL03 P&L (the roll-up)

The P&L brings revenue and cost together into the lines a finance reader expects. To avoid mixing
the product-grain revenue/COGS with entity-grain fixed OpEx, this module sits at **Entity × Time ×
Versions** and pulls each input at the right grain with `SUM` over Product where needed.

**Applies To:** `Entity`, plus Time and Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Revenue` | Number | Sum | Entity, Time, Versions | `'CAL01 Revenue'.Gross Revenue[SUM: Product]` *(see note)* |
| `COGS` | Number | Sum | Entity, Time, Versions | `'CAL02 Costs'.COGS[SUM: Product]` |
| `Gross Profit` | Number | Sum | Entity, Time, Versions | `Revenue - COGS` |
| `Fixed OpEx` | Number | Sum | Entity, Time, Versions | `'INP02 Cost Drivers'.Fixed OpEx` |
| `EBITDA` | Number | Sum | Entity, Time, Versions | `Gross Profit - Fixed OpEx` |

Notes:
- `[SUM: Product]` collapses the Product dimension — it sums each product's revenue/COGS up to the
  entity. (If your model dimensions `CAL01`/`CAL02` so that aggregation is automatic, you can
  reference them directly; the explicit `SUM` is shown so the roll-up is visible and *auditable*.)
- `Fixed OpEx` comes straight from `INP02` at entity grain — pulled once, here, so it's **not**
  double-counted across products.
- Each P&L line is **one stepped formula**. `Gross Profit` and `EBITDA` reference the lines above —
  a reviewer can trace `EBITDA → Gross Profit → Revenue/COGS → Volume/Price` without leaving the
  module. That traceability *is* the Auditable principle.

> **The actuals-vs-forecast blend comes next.** Right now every line is Forecast-driven. Once
> actuals are loaded in [Step 7](07-import-actuals.md), you'll add a blended line such as:
>
> ```
> Reported Revenue = IF 'SYS01 Time Settings'.Is Actual Month?
>                    THEN 'DAT01 Actuals'.Revenue
>                    ELSE Revenue
> ```
>
> Note it keys off the **System** flag from Step 3 — never a hard-coded month (*Sustainable*).

---

## 5.4 Sanity check

- [ ] `CAL01 Revenue` computes `Gross Revenue = Volume * Price`; values appear for the months you
      entered in `INP01`.
- [ ] `CAL02 Costs` reads `COGS %` from **System** and `Fixed OpEx` from **Inputs** — no typed
      numbers here.
- [ ] `CAL03 P&L` shows `Revenue → COGS → Gross Profit → Fixed OpEx → EBITDA`, stepped.
- [ ] Every formula references existing line items rather than re-deriving them.
- [ ] No inputs and no mappings live in these modules — they're pure **Calculations**.

> **DISCO check:** Inputs (Step 4) feed Calculations (here) via System attributes (Step 3). Data
> (Step 7) and Outputs (Step 6) complete the D → I → S → C → O flow.

---

**Related:** [DISCO](../docs/03-methodology/disco.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) ·
[Formulas reference](../docs/02-formulas/) ·
[Lookup & mapping (`SUM`)](../docs/02-formulas/lookup-and-mapping.md) ·
[Blueprint: FP&A formulas](../blueprints/fpa-pl-planning/formulas.md)

**Next → [Step 6 — Outputs & Dashboard](06-outputs-and-dashboard.md)**
