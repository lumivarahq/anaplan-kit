# Step 1 — Set Up the Model & Lists

> **Level:** L1 · **Area:** Tutorial · **DISCO:** (foundations)

Before any module exists, a model needs the **things you plan by** — its lists. In this step you
create the model and the two dimensions our FP&A model is built on: an **Organization** hierarchy
and a flat **Product** list. (Time and Versions come in [Step 2](02-time-and-versions.md).)

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

> **Tip:** model and list names are forever-ish — renaming later is allowed but breaks nothing only
> because Anaplan tracks items by ID, not name. Still, name it right the first time.

---

## 1.2 Build the Organization hierarchy

We plan by region and entity. A **hierarchy** is two or more lists linked parent → child.

**Lists → New List**, create these two lists, in order (parents first):

| List | Parent | Purpose |
| --- | --- | --- |
| `Region` | (none — top) | EMEA, Americas, APAC |
| `Entity` | `Region` | Operating entities under each region |

Steps for each list:

1. **Lists → New List**, name it `Region`.
2. Open `Region`, click **+** and add members: `EMEA`, `Americas`, `APAC`.
3. **New List** → `Entity`. In the list's **Settings → General**, set **Parent** = `Region`.
4. Open `Entity`, add members and set each one's **Parent**:

| Entity | Parent (Region) |
| --- | --- |
| UK | EMEA |
| Germany | EMEA |
| USA | Americas |
| Canada | Americas |
| Japan | APAC |

You now have a 2-level hierarchy. Aggregations (e.g. revenue) will roll **Entity → Region → Top
Level** automatically once modules use it.

> **Top Level item:** in `Region` Settings, tick **Top Level Item** and name it `Total Org`. This
> gives you a single roll-up member for "the whole company" without a third list.

---

## 1.3 Build the Product list

Products are flat (no hierarchy) for this tutorial.

1. **Lists → New List** → `Product`.
2. Add members: `Widget A`, `Widget B`, `Service Plan`.
3. In `Product` Settings, tick **Top Level Item** → name it `All Products`.

**List definition** (the way we document a list in this kit — template in
[`templates/blueprint-template.md`](../templates/blueprint-template.md)):

| List | Type | Parent | Top Level | Members (sample) |
| --- | --- | --- | --- | --- |
| `Region` | Standard | — | Total Org | EMEA, Americas, APAC |
| `Entity` | Standard | Region | — | UK, Germany, USA, Canada, Japan |
| `Product` | Standard | — | All Products | Widget A, Widget B, Service Plan |

---

## 1.4 Sanity check

- [ ] `Entity` rolls up into `Region` (open `Entity`, the **Parent** column is filled in).
- [ ] `Region` has a Top Level Item `Total Org`.
- [ ] `Product` has a Top Level Item `All Products`.
- [ ] No data anywhere yet — that's correct. Lists are structure, not numbers.

> **Why standard (named) lists here, not numbered lists?** Region/Entity/Product are small, stable,
> human-meaningful sets — perfect for standard lists. Numbered lists are for large transactional
> data (you'll meet them in [Step 7](07-import-actuals.md) and the
> [exercises](../exercises/fundamentals-exercises.md)).

---

**Related:** [Lists & hierarchies](../docs/01-fundamentals/lists-and-hierarchies.md) ·
[Dimensions](../docs/01-fundamentals/dimensions.md) ·
[Naming conventions](../templates/naming-conventions.md) ·
[Blueprint: FP&A](../blueprints/fpa-pl-planning/)

**Next → [Step 2 — Time & Versions](02-time-and-versions.md)**
