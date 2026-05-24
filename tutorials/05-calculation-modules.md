# Step 5 — Calculation Modules (the DISCO "C")

> **Level:** L1→L2 · **Area:** Tutorial · **DISCO:** Calculations · **PLANS:** Auditable, Performance

**Calculation modules** are the engine room — where **Inputs** (Step 4), **System** flags
(Step 3) and (later) **Data** meet to produce real numbers. The golden rule: **break logic into
stepped line items**, one per logical step. Stepped formulas are faster to recalc and far easier to
audit than one giant nested expression. See [DISCO](../docs/03-methodology/disco.md) and
[PLANS — Auditable](../docs/03-methodology/plans-standard.md).

We'll build four, matching the blueprint: revenue, cost, **currency conversion** (local → USD), and
the P&L build.

---

## 5.1 CAL01 Revenue

Revenue = `Volume × Price (local)`. Both drivers live in `INP01 Revenue Assumptions`; we only
*compute* here.

**Modules → New Module.** Name `CAL01 Revenue`.
**Applies To:** `L3 Cost Centre`, `L2 Product`, plus **Time** and **Versions** (same grain as
`INP01`).

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Volume` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `'INP01 Revenue Assumptions'.Volume` |
| `Price (local)` | Number | Average | L3 Cost Centre, L2 Product, Time, Versions | `'INP01 Revenue Assumptions'.Price (local)` |
| `Gross Revenue (local)` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `Volume * Price (local)` |

Notes:
- We pull `Volume` and `Price (local)` into local line items first, then multiply. That extra step is
  deliberate — it keeps `Gross Revenue (local)` a one-token-per-side formula that reads itself
  (*Auditable*). You could multiply the `INP01` references directly, but the stepped form is the
  house style.
- `Gross Revenue (local)` summary = **Sum** (revenue genuinely adds up across products, cost centres,
  months).
- `Price (local)` keeps summary = **Average** for the same reason as in `INP01`.

---

## 5.2 CAL02 Cost

Direct cost (COGS) derived from revenue × the product's `COGS %` (from `INP03 Cost Drivers`), then
gross profit.

**Applies To:** `L3 Cost Centre`, `L2 Product`, plus Time and Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `COGS %` | Number (%) | Average | L3 Cost Centre, L2 Product, Time, Versions | `'INP03 Cost Drivers'.COGS %` |
| `COGS (local)` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `'CAL01 Revenue'.Gross Revenue (local) * COGS %` |
| `Gross Profit (local)` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `'CAL01 Revenue'.Gross Revenue (local) - COGS (local)` |

Notes:
- `COGS %` is read from `INP03 Cost Drivers` (dimensioned by Product only); Anaplan broadcasts each
  product's value across Cost Centre, Time and Versions automatically — no mapping function needed.
- `COGS (local)` reads `Gross Revenue (local)` once; don't re-derive `Volume * Price * COGS %` here.
  Calculate once, reference many (*Necessary, Performance*).

---

## 5.3 CAL03 Currency Conversion (local → USD)

The blueprint's whole premise is a **USD** consolidated P&L: plans are entered in each cost centre's
local currency, then converted on the way up. We convert here, reading the FX rate from
`SYS04 Exchange Rates` by the cost centre's `Local Currency` — **never a hard-coded rate**.

**Applies To:** `L3 Cost Centre`, `L2 Product`, plus Time and Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `FX Rate` | Number (4 dp) | None | L3 Cost Centre, Time, Versions | `'SYS04 Exchange Rates'.Rate (filled)[LOOKUP: 'SYS02 Organization Details'.Local Currency]` |
| `Revenue (USD)` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `'CAL01 Revenue'.Gross Revenue (local) * FX Rate` |
| `COGS (USD)` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | `'CAL02 Cost'.COGS (local) * FX Rate` |
| `Opex (USD)` | Number | Sum | L3 Cost Centre, Time, Versions | `'INP02 Opex Plan'.Opex (local) * FX Rate` |

Notes:
- `LOOKUP` picks the `SYS04` row whose `Currency` equals the cost centre's `Local Currency`
  (from `SYS02`). `Rate (filled)` returns `1` for USD, so USD cost centres pass through unchanged.
- This is the **kit's signature currency pattern** — the same shape Sales and Workforce reuse. See
  the [blueprint formulas](../blueprints/fpa-pl-planning/formulas.md) and the
  [currency cookbook recipe](../cookbook/).

> **Sustainable:** because no rate is ever written into a formula, rolling to a new year just needs
> new months of rates imported into `SYS04`.

---

## 5.4 CAL04 P&L Build (the roll-up)

The P&L brings the USD amounts together into the lines a finance reader expects. To avoid mixing the
product-grain revenue/COGS with cost-centre-grain opex, this module sits at **L3 Cost Centre × Time ×
Versions** and pulls each USD measure at the right grain, summing over Product where needed.

**Applies To:** `L3 Cost Centre`, plus Time and Versions.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Revenue` | Number | Sum | L3 Cost Centre, Time, Versions | `'CAL03 Currency Conversion'.Revenue (USD)[SUM: L2 Product]` |
| `COGS` | Number | Sum | L3 Cost Centre, Time, Versions | `'CAL03 Currency Conversion'.COGS (USD)[SUM: L2 Product]` |
| `Gross Profit` | Number | Sum | L3 Cost Centre, Time, Versions | `Revenue - COGS` |
| `Opex` | Number | Sum | L3 Cost Centre, Time, Versions | `'CAL03 Currency Conversion'.Opex (USD)` |
| `EBITDA` | Number | Sum | L3 Cost Centre, Time, Versions | `Gross Profit - Opex` |

Notes:
- `[SUM: L2 Product]` collapses the Product dimension — it sums each product's USD revenue/COGS up to
  the cost centre. `Opex (USD)` is already at cost-centre grain, so it's pulled once here — **not**
  double-counted across products.
- Each P&L line is **one stepped formula**. `Gross Profit` and `EBITDA` reference the lines above — a
  reviewer can trace `EBITDA → Gross Profit → Revenue/COGS → Volume/Price` without leaving the
  module. That traceability *is* the Auditable principle.

> **Tutorial vs blueprint — be honest about the difference.** Here we build the **core** P&L by
> stepped line items (Revenue → EBITDA) at cost-centre grain. The
> [blueprint's CAL04 P&L Build](../blueprints/fpa-pl-planning/modules.md) goes one step further: it
> maps each USD amount onto an `L3 P&L Account` (using `SYS03 Account Details` and an opex→account
> map) so the **account hierarchy roll-up** *is* the P&L, and subtotals like Gross Profit and EBITDA
> come free from the `L1/L2/L3 P&L Account` structure. That's the production-grade build — see the
> [blueprint reference](../blueprints/fpa-pl-planning/formulas.md) for the full account-hierarchy
> version. The model you build here is a faithful, simpler subset, not an identical copy.

> **The actuals-vs-forecast blend comes next.** Right now every line is Forecast-driven. Once
> actuals are loaded in [Step 7](07-import-actuals.md), you'll add a blended line such as:
>
> ```
> Reported Revenue = IF 'SYS01 Time Settings'.Is Actual?
>                    THEN 'DAT01 Actuals'.Revenue[SUM: L2 Product]
>                    ELSE Revenue
> ```
>
> Note it keys off the **System** flag from Step 3 — never a hard-coded month (*Sustainable*).

---

## 5.5 Sanity check

- [ ] `CAL01 Revenue` computes `Gross Revenue (local) = Volume * Price (local)`; values appear for
      the months you entered in `INP01`.
- [ ] `CAL02 Cost` reads `COGS %` from `INP03` and computes `COGS (local)` / `Gross Profit (local)`.
- [ ] `CAL03 Currency Conversion` looks up `FX Rate` by `Local Currency` and produces `Revenue (USD)`
      etc. — no rate typed in a formula.
- [ ] `CAL04 P&L Build` shows `Revenue → COGS → Gross Profit → Opex → EBITDA` in USD, stepped.
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
