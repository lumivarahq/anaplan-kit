# Step 3 — System Modules (the DISCO "S")

> **Level:** L1→L2 · **Area:** Tutorial · **DISCO:** System · **PLANS:** Sustainable, Auditable

**System modules** are the quiet backbone. They hold time attributes, mappings between lists, and
Boolean flags — built **once**, referenced **everywhere**. Putting this logic here (not inside
calculations) is what makes a model *sustainable*: change a flag in one place and the whole model
follows. See [DISCO](../docs/03-methodology/disco.md).

We'll build three: a time-settings module and two attribute/mapping modules.

---

## 3.1 SYS01 Time Settings

A tiny module dimensioned **only by Time** that exposes useful per-period attributes so calc
modules don't recompute them. This is the standard Anaplan pattern.

**Modules → New Module.** Name `SYS01 Time Settings`. **Applies To:** *Time* (no lists, no
Versions).

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Month Start Date` | Date | None | Time | `START()` |
| `Is Actual Month?` | Boolean | None | Time | `Month Start Date < START()` evaluated vs current period — see note |
| `Period Name` | Text | None | Time | `NAME(ITEM(Time))` |

> **`Is Actual Month?` the sustainable way.** Don't hard-code `IF Time = Apr 26`. Compare the
> period to the **current period** so it self-updates every month:
>
> ```
> Is Actual Month?  =  START() < START(CURRENTPERIODSTART())
> ```
>
> If your platform exposes the current period differently, the robust idiom is to compare
> `START()` against a single-celled "Cut-off Date" input. Either way the date lives in **one place**
> (Sustainable, Planual). We'll reuse `Is Actual Month?` to blend actuals and forecast in Step 5.

---

## 3.2 SYS02 Product Details

Attributes of each product live here, not on the calc modules. **Applies To:** *Product*.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Product Type` | List: `Product Type` (or Text) | None | Product | *(input)* |
| `Is Active?` | Boolean | None | Product | *(input)* |
| `COGS %` | Number (%) | None | Product | *(input — default cost ratio)* |

Set `Is Active?` = TRUE for all three products and a sensible `COGS %` (e.g. Widget A/B 60%,
Service Plan 20%). These become drivers our cost calc reads.

> **Why a System module and not Inputs?** These are **structural attributes** of the product
> (rarely changed, set by the builder/admin), not planning assumptions planners tweak each cycle.
> The volume/price *assumptions* go in an **Inputs** module in [Step 4](04-input-modules.md).

---

## 3.3 SYS03 Org Details (a mapping module)

A **mapping module** translates one list to another or stores hierarchy attributes. Here we store
a reporting attribute and (illustratively) a currency per entity for later FX work.

**Applies To:** *Entity*.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Region` | List: `Region` | None | Entity | `PARENT(ITEM(Entity))` |
| `Local Currency` | List: `Currency` *(optional)* | None | Entity | *(input)* |
| `Is Reporting Entity?` | Boolean | None | Entity | *(input, default TRUE)* |

The `Region` line item is computed with `PARENT()` so it always matches the hierarchy — no manual
upkeep. This is a **mapping** you can `LOOKUP`/`SUM` against later instead of `SELECT`.

> If you skip Currency for now, that's fine — it's shown to illustrate where FX rates would map.
> Keep the module focused: don't add line items "just in case" (**Necessary**, PLANS).

---

## 3.4 Sanity check

- [ ] `SYS01 Time Settings` applies to **Time only** and has `Is Actual Month?` driven from the
      current period (no hard-coded date).
- [ ] `SYS02 Product Details` holds product attributes (`Is Active?`, `COGS %`).
- [ ] `SYS03 Org Details` derives `Region` via `PARENT()`.
- [ ] None of these modules contain business *calculations* — only attributes, flags, mappings.

> **DISCO check:** all three are pure **System**. If you ever feel tempted to put
> `Revenue = …` here, stop — that belongs in a **Calculations** module (Step 5).

---

**Related:** [DISCO](../docs/03-methodology/disco.md) ·
[Lookup & mapping](../docs/02-formulas/) ·
[Time](../docs/01-fundamentals/time.md) ·
[Naming conventions](../templates/naming-conventions.md)

**Next → [Step 4 — Input Modules](04-input-modules.md)**
