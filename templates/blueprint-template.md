# Blueprint Template (copy-paste)

> **Level:** L1 · **Area:** Templates

Blank templates for documenting a model **on paper before you build it** — the way every
[blueprint](../blueprints/) and [tutorial](../tutorials/) in this kit is written. Copy the table you
need, fill the `[…]` placeholders, delete the example row.

Designing on paper first is the cheapest place to catch a [PLANS](../docs/03-methodology/plans-standard.md)
or [DISCO](../docs/03-methodology/disco.md) problem — before it's cells in a tenant.

---

## 1. List-definition template

One row per list. For a hierarchy, list the levels top → leaf (`L1`, `L2`, `L3`).

```markdown
| List | Type | Parent | Top Level | Members (sample) | Notes |
| --- | --- | --- | --- | --- | --- |
| [List name] | [Standard / Numbered / Subset] | [parent list or —] | [Top Level Item or —] | [member1, member2, …] | [purpose / who owns it] |
```

**Example (filled):**

| List | Type | Parent | Top Level | Members (sample) | Notes |
| --- | --- | --- | --- | --- | --- |
| `L1 Region` | Standard | — | Total Org | EMEA, Americas, APAC | Top roll-up |
| `L2 Entity` | Standard | `L1 Region` | — | UK, Germany, USA | Planning grain |
| `Product` | Standard | — | All Products | Widget A, Widget B, Service Plan | Revenue grain |

---

## 2. Module blueprint table

One **blueprint table per module**. Head it with the module's name, its **DISCO type**, and its
**Applies To** (dimensionality). One row per line item — the same grid as Anaplan's Blueprint view.

```markdown
**Module:** [PREFIX## Module Name] · **DISCO:** [Data/Inputs/System/Calculations/Outputs] · **Applies To:** [dim1 × dim2 × Time × Versions]

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| [Line item name] | [Number / Number (%) / Boolean / Text / Date / List: X] | [Sum / Average / Min / Max / Formula / None] | [the dims this line item uses] | [Anaplan formula, or (input), or (import target)] |
```

**Example (filled):**

**Module:** `CAL01 Revenue` · **DISCO:** Calculations · **Applies To:** Entity × Product × Time × Versions

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Volume` | Number | Sum | Entity, Product, Time, Versions | `'INP01 Revenue Assumptions'.Volume` |
| `Price` | Number | Average | Entity, Product, Time, Versions | `'INP01 Revenue Assumptions'.Price` |
| `Gross Revenue` | Number | Sum | Entity, Product, Time, Versions | `Volume * Price` |

**Field cheat sheet:**

| Field | What to put |
| --- | --- |
| **Format** | `Number`, `Number (%)` for ratios, `Boolean` for flags (name them `Is …?`), `Text`, `Date`, or `List: [list name]` for a mapping. |
| **Summary** | How it aggregates up: `Sum` for amounts, `Average` for prices/rates/%, `None` for attributes/flags, `Formula` to repeat the line formula at the total. |
| **Applies To** | Only the dimensions this line *needs* — fewer dims = smaller module (*Performance*). Can be narrower than the module. |
| **Formula** | Anaplan syntax. `(input)` if humans type it; `(import target)` for a Data module line. |

---

## 3. Module summary line (for a module index)

When you list several modules together, one line each:

```markdown
| Module | DISCO | Applies To | Purpose |
| --- | --- | --- | --- |
| [PREFIX## Name] | [type] | [dimensions] | [one-line what it does] |
```

**Example:**

| Module | DISCO | Applies To | Purpose |
| --- | --- | --- | --- |
| `SYS01 Time Settings` | System | Time | Per-period flags & dates |
| `INP01 Revenue Assumptions` | Inputs | Entity × Product × Time × Versions | Volume & price planning |
| `CAL03 P&L` | Calculations | Entity × Time × Versions | Revenue → EBITDA roll-up |

---

## 4. Architecture sketch (optional)

A quick text diagram of how modules feed each other — paste at the top of a model doc:

```
INP01 Revenue Assumptions ─┐
                           ├─> CAL01 Revenue ─┐
SYS02 Product Details ─────┘                  ├─> CAL03 P&L ─> OUT01 P&L Report ─> UX page
INP02 Cost Drivers ───────────> CAL02 Costs ──┘        ▲
DAT01 Actuals ────────────────────────────────────────┘ (blended via SYS01.Is Actual Month?)
```

---

**Related:** [Naming conventions](naming-conventions.md) ·
[How to read a blueprint](../blueprints/README.md) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Line items & formats](../docs/01-fundamentals/line-items-and-formats.md) ·
[Tutorials](../tutorials/)
