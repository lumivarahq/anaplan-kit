# Step 1 — Set Up the Model & Lists

> **Level:** L1 · **Area:** Tutorial · **DISCO:** (foundations)

Before any module exists, a model needs the **things you plan by** — its lists. In this step you
create the model and the dimensional backbone the canonical
[FP&A P&L Planning blueprint](../blueprints/fpa-pl-planning/) is built on: the **Organization**
hierarchy, the **Product** hierarchy, the **P&L Account** chart of accounts, and a **Currency** list.
(Time and Versions come in [Step 2](02-time-and-versions.md).)

> **Same model as the blueprint.** Every name you create here matches
> [`blueprints/fpa-pl-planning/lists.md`](../blueprints/fpa-pl-planning/lists.md) and
> [`blueprints/_common/`](../blueprints/_common/) exactly, so your build and the reference never
> diverge.

---

## 1.1 Create the workspace & model

You build inside a **workspace** (a container with a memory allowance) that holds one or more
**models**.

1. From the Anaplan home page, open **Administration → Workspaces** (or use an existing workspace
   your admin gave you). Note the workspace name.
2. Go to the workspace and click **New Model**.
3. Name it `FP&A P&L Planning — Tutorial`. Choose **Create blank model**.
4. The model opens. You're now in **Blueprint** mode territory — the left rail shows *Modules*,
   *Lists*, *Actions*, etc.

> **Tip:** name it right the first time. Anaplan tracks items by internal ID, so renaming updates
> *formula* references automatically — but it does **not** fix every text-based reference:
> saved-view layouts, import/export column mappings and external integrations that match on **name**
> can break on a rename. Treat names as stable.

---

## 1.2 Build the Organization hierarchy

We plan by **cost centre**, which rolls up to **country** then **region**. A **hierarchy** (composite
list) is several lists linked parent → child. Build it **top-down**: `L1 Region` first, then
`L2 Country` (parent = Region), then `L3 Cost Centre` (parent = Country).

**Lists → New List**, create these three lists, in order (parents first):

| List | Parent | Purpose |
| --- | --- | --- |
| `L1 Region` | (none — top) | EMEA, Americas, APAC |
| `L2 Country` | `L1 Region` | Countries under each region; holds the local currency |
| `L3 Cost Centre` | `L2 Country` | The planning grain — where revenue, cost and headcount land |

Steps:

1. **Lists → New List**, name it `L1 Region`. Open it, click **+**, add `EMEA`, `Americas`, `APAC`.
2. **New List** → `L2 Country`. In **Settings → General**, set **Parent** = `L1 Region`. Add members
   and set each one's **Parent**:

   | L2 Country | Parent (L1 Region) |
   | --- | --- |
   | UK | EMEA |
   | Germany | EMEA |
   | USA | Americas |
   | India | APAC |

3. **New List** → `L3 Cost Centre`. Set **Parent** = `L2 Country`. Add members and parents:

   | L3 Cost Centre | Parent (L2 Country) |
   | --- | --- |
   | CC-1100 UK Sales | UK |
   | CC-1200 UK Ops | UK |
   | CC-3100 US Sales | USA |
   | CC-4100 India R&D | India |

You now have a 3-level hierarchy. Aggregations (e.g. revenue) roll **Cost Centre → Country → Region →
Top Level** automatically once modules use it — never sum them with formulas.

> **Top Level item:** in `L1 Region` Settings, tick **Top Level Item** and name it `Total Org`. This
> gives you a single roll-up member for "the whole company."

---

## 1.3 Build the Product hierarchy

Products roll up from a planning leaf (`L2 Product`) to a reporting family (`L1 Product Family`).

1. **Lists → New List** → `L1 Product Family`. Add members: `Hardware`, `Software`, `Services`. Tick
   **Top Level Item** → name it `All Products`.
2. **New List** → `L2 Product`. Set **Parent** = `L1 Product Family`. Add members and parents:

   | L2 Product | Parent (L1 Product Family) |
   | --- | --- |
   | Sensor A | Hardware |
   | Sensor B | Hardware |
   | Platform License | Software |
   | Support Plan | Services |

`L2 Product` is the **revenue planning grain** — modules dimension by it.

---

## 1.4 Build the P&L Account hierarchy and Currency

The **chart of accounts** is the spine the whole P&L rolls up to. Build it top-down:

1. **New List** → `L1 P&L Statement`. Add `Net Profit` (the statement total).
2. **New List** → `L2 P&L Group`. Parent = `L1 P&L Statement`. Add the subtotal groups: `Revenue`,
   `COGS`, `Gross Profit`, `Opex`, `EBITDA`.
3. **New List** → `L3 P&L Account`. Parent = `L2 P&L Group`. Add the leaf accounts postings land on:
   `Product Revenue`, `Services Revenue`, `Direct Materials`, `Salaries`, `Travel`, `Marketing`,
   `IT`. (Set each one's parent group, e.g. `Product Revenue → Revenue`, `Salaries → Opex`.)

Then a flat **Currency** list:

1. **New List** → `Currency`. Add `GBP`, `EUR`, `USD`, `INR`. The **group/reporting currency is USD**
   — every local amount converts to it in [Step 5](05-calculation-modules.md).

**List definition** (how we document lists in this kit — template in
[`templates/blueprint-template.md`](../templates/blueprint-template.md)):

| List | Type | Parent | Top Level | Members (sample) |
| --- | --- | --- | --- | --- |
| `L1 Region` | Standard (hierarchy) | — | Total Org | EMEA, Americas, APAC |
| `L2 Country` | Standard (hierarchy) | `L1 Region` | — | UK, Germany, USA, India |
| `L3 Cost Centre` | Standard (hierarchy) | `L2 Country` | — | CC-1100 UK Sales, CC-3100 US Sales |
| `L1 Product Family` | Standard (hierarchy) | — | All Products | Hardware, Software, Services |
| `L2 Product` | Standard (hierarchy) | `L1 Product Family` | — | Sensor A, Sensor B, Support Plan |
| `L1 P&L Statement` | Standard (hierarchy) | — | — | Net Profit |
| `L2 P&L Group` | Standard (hierarchy) | `L1 P&L Statement` | — | Revenue, COGS, Opex, EBITDA |
| `L3 P&L Account` | Standard (hierarchy) | `L2 P&L Group` | — | Product Revenue, Salaries, Travel |
| `Currency` | Standard (flat) | — | — | GBP, EUR, USD, INR |

---

## 1.5 Sanity check

- [ ] `L3 Cost Centre` rolls up via `L2 Country` to `L1 Region` (the **Parent** columns are filled).
- [ ] `L1 Region` has a Top Level Item `Total Org`; `L1 Product Family` has `All Products`.
- [ ] `L2 Product` rolls up to `L1 Product Family`.
- [ ] The P&L hierarchy is `L1 P&L Statement › L2 P&L Group › L3 P&L Account`.
- [ ] `Currency` lists USD as the group currency.
- [ ] No data anywhere yet — that's correct. Lists are structure, not numbers.

> **Why standard (named) lists here, not numbered lists?** Region/Country/Cost Centre, Product and
> the accounts are small, stable, human-meaningful sets — perfect for standard lists. Numbered lists
> are for large transactional data (you'll meet them in [Step 7](07-import-actuals.md) and the
> [exercises](../exercises/fundamentals-exercises.md)).

---

**Related:** [Lists & hierarchies](../docs/01-fundamentals/lists-and-hierarchies.md) ·
[Dimensions](../docs/01-fundamentals/dimensions.md) ·
[Naming conventions](../templates/naming-conventions.md) ·
[Blueprint: FP&A](../blueprints/fpa-pl-planning/)

**Next → [Step 2 — Time & Versions](02-time-and-versions.md)**
