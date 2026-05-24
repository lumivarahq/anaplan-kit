# Fundamentals Exercises — Solutions

> **Level:** L1 · **Area:** Exercises (solutions) · Exercise: [`../fundamentals-exercises.md`](../fundamentals-exercises.md)

Worked answers with the *why*. There's often more than one acceptable answer — the reasoning is what
matters.

---

## A. Lists & hierarchies

**A1.** Build a composite hierarchy (parents first):

| List | Type | Parent | Members (sample) |
| --- | --- | --- | --- |
| `L1 Region` | Standard (hierarchy top) | — | EMEA, Americas, APAC |
| `L2 Country` | Standard (hierarchy) | `L1 Region` | UK, Germany, USA |
| `L3 Cost Centre` | Standard (hierarchy leaf) | `L2 Country` | CC-1100 UK Sales, … |

Modules are normally dimensioned by the **leaf** (`L3 Cost Centre`). Roll-ups to Country and Region
are then **automatic** — you never sum them with formulas (*Necessary, Performance*).

**A2.** Wrong because: (a) the hierarchy isn't real, so totals don't roll up automatically — they'd
have to sum Region manually; (b) the typed "Region" can get out of sync with reality (a Country
re-parented won't update). **Fix:** make them a proper **composite hierarchy** (Country's parent =
Region, etc.) and derive any "Region" attribute with `PARENT(ITEM(...))` in a System module
(*Sustainable, Auditable*).

**A3.** A **numbered list**. Reasons: (1) transactional rows have no natural unique name — numbered
lists key by an internal ID, so duplicates/blank names aren't a problem; (2) they're built for large
volumes and let you store row properties efficiently, and you aggregate up via a mapping. (Standard
lists are for small, stable, human-meaningful sets like Region/Product.)

**A4.** A **Top Level Item** is a single roll-up member that sits *above* all the list's members,
giving you a "grand total" line without creating another list level. On `Product` you'd name it
`All Products`. (On a hierarchy you usually put it on the top list, e.g. `Total Org` on `Region`.)

---

## B. Modules & dimensions

**B1.** **Applies To:** `Entity × Product × Time × Versions`. (List dims first, then Time, then
Versions — see [naming conventions](../../templates/naming-conventions.md).)

**B2.** Adding `Product` multiplies the cell count by the number of products **for no business
reason** — Fixed OpEx doesn't vary by product, so you'd store identical/empty values across a whole
dimension. Dimension a module only by lists it **needs**. Principle: **Performance** (the single
biggest lever — cell count = product of all dimension sizes × line items).

**B3.** `5 × 3 × 36 × 3 = 1,620` combinations × **4 line items ≈ 6,480 cells**. It matters because
**cell count drives model size and recalculation time** — the core of the *Performance* principle.
Multiply that mistake across many modules and a model becomes slow or won't open.

---

## C. Formats

**C1.**
1. `Gross Revenue` → **Number**
2. `COGS %` → **Number** formatted as a **percentage** (`Number (%)`)
3. `Is Active?` → **Boolean**
4. `Cost Centre Manager` → **Text**
5. `Period Start Date` → **Date**
6. `Region` (mapping) → **List: Region** (a list-formatted line item is how you map one list to
   another)

**C2.** **Performance:** a Boolean is the cheapest format and lets you use it directly in formulas
(`IF Is Active? THEN …`) and as a fast filter, instead of a text comparison `= "Yes"` over a large
cell count. **Usability:** a checkbox can't be mistyped (`"yes"`, `"Y"`, `" Yes"`), so the data stays
clean and filters/aggregations behave.

---

## D. Summary methods

**D1.**
1. `Gross Revenue` → **Sum** (money adds up across products/entities/months).
2. `Price` → **Average** (a price shouldn't add up; the average across the grain is meaningful-ish).
3. `COGS %` → **Average** (a ratio shouldn't sum).
4. `Is Actual Month?` → **None** (a flag has no meaningful aggregate; or Formula if you want a
   rule).
5. `EBITDA Margin %` → **Average** (a ratio; ideally recomputed at the total — see D2).

**D2.** **No** — Anaplan applies each line item's *own* summary up the dimension, so the Year
`Gross Revenue` is the **Sum of the 12 monthly** `Gross Revenue` values (each = that month's
Volume × Price), which is the correct annual revenue. The trap is `Margin %`/ratio lines: a summed
or averaged ratio is usually wrong at the total. **Fix for ratios:** set Summary = **Formula** so
`Margin % = EBITDA / Revenue` is recomputed at every level (using the already-correct summed EBITDA
and Revenue), rather than averaging the monthly percentages.

---

## E. DISCO classification

**E1.**
1. Imported GL actuals → **Data** → `DAT01`
2. Typed headcount plan → **Inputs** → `INP0x`
3. `Gross Profit = Revenue − COGS` → **Calculations** → `CAL0x`
4. Boolean time flags by Time → **System** → `SYS01`
5. Dashboard-shaped P&L card → **Outputs** → `OUT0x`

**E2.**
1. `Entity → Region` mapping → **System**
2. Default `COGS %` (a structural attribute) → **System**
3. Monthly `Volume` assumption → **Inputs**
4. `Gross Revenue = Volume × Price` → **Calculations**

> The recurring lesson: **attributes/mappings/flags = System; typed plan numbers = Inputs; math =
> Calculations.** Keeping them separate is exactly what [DISCO](../../docs/03-methodology/disco.md)
> enforces.

---

**Related:** [DISCO](../../docs/03-methodology/disco.md) ·
[Line items & formats](../../docs/01-fundamentals/line-items-and-formats.md) ·
[Naming conventions](../../templates/naming-conventions.md) ·
[Back to exercise](../fundamentals-exercises.md)
