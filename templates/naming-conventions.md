# Naming Conventions

> **Level:** L1 · **Area:** Templates · **PLANS:** Sustainable, Auditable

A consistent naming scheme makes a model read itself. When every module, list and line item is named
predictably, any builder can open the model and immediately see *what kind of thing* each item is and
*where logic lives*. This is the standard the [methodology pages](../docs/03-methodology/disco.md),
[tutorials](../tutorials/) and [blueprints](../blueprints/) all follow.

---

## Module prefixes (DISCO)

Prefix every module with its [DISCO](../docs/03-methodology/disco.md) type, then a **two-digit
number**, then a clear name. The prefix tells you the module's role at a glance.

| Prefix | DISCO type | Holds | Example |
| --- | --- | --- | --- |
| `DAT` | **Data** | Imported source data, as-is (landing zone). | `DAT01 Actuals from GL` |
| `INP` | **Inputs** | Numbers humans type (assumptions, drivers, rates). | `INP01 Revenue Assumptions` |
| `SYS` | **System** | Time attributes, mappings, flags, hierarchy properties. | `SYS01 Time Settings` |
| `CAL` | **Calculations** | Formulas combining Inputs + Data + System. | `CAL01 Revenue` |
| `OUT` | **Outputs** | Reporting/export views — no new logic. | `OUT01 P&L Report` |

**Numbering (`SYS01`, `SYS02`, …):**
- Two digits, zero-padded, **per prefix** (`SYS01`, `SYS02`, `CAL01`, `CAL02`).
- Number roughly in **build/data-flow order** so a sorted module list reads top-to-bottom like the
  model: System first, then Inputs, then Calculations, then Outputs.
- Leave gaps if helpful (`CAL10`, `CAL20`) when you expect to insert related modules later.

**Module name after the prefix:**
- Title Case, a short noun phrase: `INP01 Revenue Assumptions`, not `INP01 rev_ass`.
- Describe *what it holds*, not how: `CAL02 Costs`, not `CAL02 Multiply Stuff`.

---

## List naming

| List kind | Convention | Example |
| --- | --- | --- |
| **Flat / standard** | Singular noun, Title Case. | `Product`, `Currency`, `Entity Type` |
| **Hierarchy levels** | Prefix each level `L1`, `L2`, `L3` (top → leaf) so the level is obvious. | `L1 Region`, `L2 Country`, `L3 Cost Centre/Entity` |
| **Numbered list** | Suffix to signal it's transactional/numbered. | `Transactions #`, `GL Lines #` |
| **Subset** | Reference the parent list + the slice. | `Active Products` (subset of `Product`) |

Notes:
- The **leaf** level of a hierarchy is what modules are usually dimensioned by; the `L1/L2/L3`
  prefixes make "which level?" unambiguous.
- A simpler tutorial/small model may use bare names (`Region`, `Entity`) — fine when the hierarchy
  is tiny and obvious. Use `L1/L2/L3` once a hierarchy has 3+ levels or is shared across models.
- **Top Level Item:** name it for the total it represents (`Total Org`, `All Products`).

---

## Line-item naming

- **Title Case noun phrases** that describe meaning: `Gross Revenue`, `EBITDA Margin %`,
  `Is Actual Month?`.
- **Booleans** read as a yes/no question and end with `?`: `Is Active?`, `Include in Plan?`,
  `Is Revenue?`.
- **Percentages / rates** carry a unit cue: `COGS %`, `Price Growth %`, `Rate to Group`.
- **Stepped calcs:** name each step for the value it produces (`Volume`, `Price`, `Gross Revenue`),
  not for the operation. A reader should trace the steps by name alone (*Auditable*).
- **Avoid** cryptic codes (`R1`, `X2`), abbreviations only you understand, and trailing
  spaces/odd characters.

---

## Time & version naming

| Item | Convention | Example |
| --- | --- | --- |
| **Versions** | Title Case, the standard trio. | `Actual`, `Budget`, `Forecast` |
| **Version formula** | Name the comparison. | `Variance` (= `Forecast − Budget`) |
| **Fiscal years** | Use the platform's `FY` label; don't rename per model. | `FY25`, `FY26`, `FY27` |
| **Time Ranges** | Name for the span + grain. | `FY26 Months`, `Plan Years` |

Notes:
- Configure Time and Versions **once** at the model level (see
  [Time & Versions tutorial](../tutorials/02-time-and-versions.md)); don't rebuild them as ordinary
  lists.
- Never bake a period into a name (`Revenue Jan26`) — drive time off the calendar and
  `SYS01 Time Settings` (*Sustainable*).

---

## Actions, views & pages

| Item | Convention | Example |
| --- | --- | --- |
| **Import action** | `Import — [what] to [target]` | `Import — Actuals to DAT01` |
| **Export action** | `Export — [what] from [source]` | `Export — P&L from OUT01` |
| **Process** | Verb phrase for the sequence. | `Monthly Actuals Load` |
| **Saved view** | `[Module] — [purpose]` | `DAT01 Actuals — for export` |
| **App / Page** | Business-readable, Title Case. | App `FP&A Planning`, page `P&L — Plan vs Actual` |

---

## Quick reference card

```
Modules:    PREFIX## Name        DAT01 Actuals · SYS01 Time Settings · CAL01 Revenue · OUT01 P&L Report
Lists:      Singular Title Case  Product · Currency
Hierarchy:  L1/L2/L3 levels      L1 Region › L2 Country › L3 Cost Centre/Entity
Numbered:   trailing #           Transactions #
Line items: Title Case phrase    Gross Revenue · EBITDA Margin %
Booleans:   question + ?         Is Actual Month? · Is Active?
Rates/%:    unit cue             COGS % · Rate to Group
Versions:   the trio             Actual · Budget · Forecast
Actions:    Import — X to Y       Import — Actuals to DAT01
```

---

**Related:** [DISCO](../docs/03-methodology/disco.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) ·
[Blueprint template](blueprint-template.md) ·
[Tutorials](../tutorials/) · [Blueprints](../blueprints/)
