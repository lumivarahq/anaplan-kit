# Step 7 — Import Actuals (the DISCO "D")

> **Level:** L1→L2 · **Area:** Tutorial · **DISCO:** Data · **PLANS:** Logical, Auditable

So far every number is planned. Real FP&A also needs **actuals** — last period's results from the
GL. They arrive by **import** and land in a **Data** module: a flat, faithful landing zone, no
calculation. From there the P&L blends Actuals (past) with Forecast (future). See
[DISCO — Data](../docs/03-methodology/disco.md) and
[Imports & exports](../docs/04-integration/imports-exports.md).

---

## 7.1 DAT01 Actuals — the landing zone

A **Data** module holds imported data exactly as it arrives. Ours receives actual revenue and cost
by cost centre, product and month, into the **Actual** version. (Actuals are loaded already in USD
from the GL, so no FX conversion is needed on this module.)

**Modules → New Module.** Name `DAT01 Actuals`.
**Applies To:** `L3 Cost Centre`, `L2 Product`, plus **Time** and **Versions**.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Revenue` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | *(import target — no formula)* |
| `COGS` | Number | Sum | L3 Cost Centre, L2 Product, Time, Versions | *(import target — no formula)* |
| `Opex` | Number | Sum | L3 Cost Centre, Time, Versions | *(import target — no formula)* |

> **No formulas in a Data module.** It must stay flat and faithful to the source so you can always
> reconcile "what we loaded" against the GL (*Auditable*). Calculations read from it; they don't
> live in it.

---

## 7.2 Prepare the source file

Imports map a flat file (CSV) to a module. Your file's columns become the things Anaplan maps to
**dimensions** and **line items**. A simple actuals file:

```
Cost Centre,      Product,          Month,    Revenue, COGS,  Opex
CC-1100 UK Sales, Sensor A,         Jan 2025, 26000,   15600, 40000
CC-1100 UK Sales, Sensor B,         Jan 2025, 18000,   10800,
CC-3100 US Sales, Sensor A,         Jan 2025, 31000,   18600, 55000
...
```

Tips:

- Use list member names that **exactly match** your lists (`CC-1100 UK Sales`, `Sensor A`) — or map
  them.
- Month format must match what Anaplan expects (`Jan 2025` / `Jan 25` depending on calendar
  display). Anaplan shows a preview so you can confirm the parse.

---

## 7.3 Create the import action

1. With `DAT01 Actuals` open, **File → Import** (or **Actions → New Action → Import** from a file).
2. Upload the CSV. Anaplan parses it and shows the **mapping** screen.
3. **Map columns to dimensions:**

   | File column | Maps to | How |
   | --- | --- | --- |
   | `Cost Centre` | `L3 Cost Centre` list | match by **Name** |
   | `Product` | `L2 Product` list | match by **Name** |
   | `Month` | `Time` | match by **period name** |
   | (fixed) | `Versions` | set to **Actual** (a constant — the file is all actuals) |

4. **Map columns to line items:** `Revenue → Revenue`, `COGS → COGS`, `Opex → Opex`.
5. Name the action clearly, e.g. **`Import — Actuals to DAT01`**. Run it.
6. Check the **import log**: it reports rows loaded, ignored, and any **unmapped members** (e.g. a
   product spelled differently). Fix the file or add the member, re-run.

> **Save it as a reusable action.** A named import action can be re-run every period and chained
> into a **process** (Anaplan Connect / CloudWorks / the [Python tooling](../tooling/)). Don't do a
> throwaway manual paste — make the action so next month is one click (*Sustainable*).

---

## 7.4 Importing *from* a module: saved views

You won't always import from a file — often you import **from another module** (model-to-model, or
within a model). The source is a **saved view**:

1. Open the source module, arrange it exactly as the target expects (right line items on rows,
   dimensions on the page/columns), apply any filter.
2. **Save as View** with a clear name, e.g. `DAT01 Actuals — for export`.
3. The import action then reads that **view**, not the raw module — so if the module changes, the
   view (and the mapping) stays stable. This is the standard pattern for **data hubs** feeding spoke
   models (L2/L3). See [imports & exports](../docs/04-integration/imports-exports.md).

> **Numbered lists for transactions:** a real GL feed is millions of rows. You'd land them in a
> module dimensioned by a **numbered list** (one member per transaction), then aggregate up via a
> mapping into `DAT01`. See [numbered lists](../docs/01-fundamentals/numbered-lists-and-subsets.md)
> and the [fundamentals exercises](../exercises/fundamentals-exercises.md). For this tutorial, the
> cost centre × product × month grain is enough.

---

## 7.5 Wire the blend (Actuals + Forecast)

Now connect Data to the report. Add a blended line to `CAL04 P&L Build` (or a new `Reported` line
set) keyed off the **System** flag from Step 3 — never a hard-coded month:

```
Reported Revenue =
  IF 'SYS01 Time Settings'.Is Actual?
  THEN 'DAT01 Actuals'.Revenue[SUM: L2 Product]
  ELSE Revenue
```

Do the same for COGS / Opex. Past months now show loaded actuals; future months show the plan —
and it self-adjusts as the current period advances (*Sustainable*). Point `OUT01 P&L Statement` at
the `Reported` lines for the live view.

---

## 7.6 Sanity check

- [ ] `DAT01 Actuals` contains **only** import-target line items — no formulas.
- [ ] The import action maps Cost Centre/Product by Name, Month to Time, Versions = **Actual**.
- [ ] The import log shows zero unmapped members (or you've reconciled them).
- [ ] The blended `Reported` lines key off `SYS01.Is Actual?`, not a typed date.
- [ ] Data flows the DISCO way: **D**ATA (DAT01) → **C**ALC (blend) → **O**UTPUT (OUT01).

---

**Related:** [Imports & exports](../docs/04-integration/imports-exports.md) ·
[Numbered lists](../docs/01-fundamentals/numbered-lists-and-subsets.md) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Python tooling (API imports)](../tooling/) ·
[Blueprint: FP&A](../blueprints/fpa-pl-planning/)

**Next → [Step 8 — Review Against PLANS](08-review-against-plans.md)**
