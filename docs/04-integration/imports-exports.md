# Imports & Exports

> **Level:** L1 · **Area:** Integration · **PLANS:** Sustainable, Necessary · **DISCO:** Data

An **import** loads data from a source (a file or another Anaplan view) into a target in
your model. An **export** writes data out of a view to a file. You build them once in the
browser, Anaplan saves the **mapping**, and from then on the import is a reusable
**action** you (or a script) can re-run against a fresh source of the same shape.

## The two kinds of import

This is the distinction that trips up every beginner. Imports do *two different jobs*:

| Import type | What it changes | Example |
| --- | --- | --- |
| **Data import** | The numbers/values inside a **module** | Load this month's actuals into `DAT01 Actuals` |
| **Structural (list) import** | The **members** of a **list** | Add new products/cost centres to a list; update their properties |

A data import never adds list members on its own *unless you ask it to* (see
[auto-create](#auto-create-list-members)). A list import never fills a module with numbers
— it builds the dimension first. A typical "new product launch" load is therefore **two
actions**: first import the product into the **list**, then import its numbers into the
**module**. Grouping them is exactly what a [process](actions-and-processes.md) is for.

> **Rule of thumb:** lists first, data second. You cannot load a number against a product
> that doesn't exist yet.

## Sources you can import from

- **A flat file** — CSV, TXT or a fixed-width text file you upload. Anaplan stores the
  uploaded file so the action can be re-run by replacing the file with one of the same
  layout.
- **A saved view of another module** — the basis of **model-to-model** imports and the
  heart of a [Data Hub](README.md). The "file" is really a live view in another model.

A **saved view** is just a module view (rows/columns/filters/selected line items) that you
named and saved. It can be the **source** of an import *and* the thing you point an
**export** at. Shaping a clean `OUT`-type output view for export is far better than
exporting a raw calc module.

## Mapping: matching source columns to your model

When you build an import, Anaplan shows a **mapping** screen. You tell it how each source
column lines up with the target's **dimensions** and **line items**:

| Source column | Maps to | Notes |
| --- | --- | --- |
| `Cost Centre Code` | the **Cost Centre** list dimension | match on code or name |
| `Month` | the **Time** dimension | source format must be parseable |
| `Account` | another list dimension | |
| `Amount` | a **line item** | the actual value |

Key mapping ideas for a beginner:

- **Match on code, not name, where you can.** Codes are stable; names get retyped.
- Columns that identify *where* a number sits map to **dimensions**; the column holding the
  *value* maps to a **line item**.
- Anaplan tries to auto-match by header name. Always check it — a silent mis-map is the
  classic "the totals look wrong" bug.
- Map a **Version** explicitly if your module is versioned (e.g. load into `Actual`).

## Updating data vs updating lists

Say it out loud before every import: *am I updating data or updating the list?*

- **Updating data** overwrites/loads values in a module. It does **not** remove list
  members that are missing from the file — it just doesn't update them.
- **Updating a list** changes the dimension itself: adding members, updating their
  properties/parents, or (if configured) removing members not present in the source.

Mixing these up is how people accidentally wipe planning numbers or, worse, delete list
members. Keep them in separate actions and you keep them straight.

## Auto-create list members

A data import can be told to **create list members on the fly**: if the source has a
product code the target list doesn't contain yet, Anaplan adds it. This is convenient but
**use it deliberately** — it's the most common cause of a list quietly bloating with junk
members (typos, blanks, retired codes) that inflate cell count forever.

Preferred pattern: **import the list cleanly first** (its own structural action, often into
a Data Hub), validated, *then* import data with auto-create **off**. Reserve auto-create
for genuinely dynamic transactional lists where the hub is the gatekeeper.

## Common import pitfalls

| Pitfall | Symptom | Fix |
| --- | --- | --- |
| Matching on **name** not **code** | rows silently skipped when a name changed | map on a stable code |
| **Auto-create** left on | list fills with typo'd / blank members | clean list import first, auto-create off |
| Wrong **Version** mapped | numbers land in `Forecast` instead of `Actual` | map the Version column explicitly |
| **Time** format mismatch | dates won't parse, rows ignored | match source date format to the model calendar |
| Importing into a **calc** line item | values won't stick (formula overwrites them) | import into input line items / `DAT` modules only |
| Exporting a raw calc module | messy, fragile file | export a purpose-built `OUT` saved view |
| Ignoring the **import log** | think it worked; half the rows failed | always read the "rows successful / ignored / failed" summary |

> **Always read the import results dialog.** It tells you how many rows succeeded, were
> ignored, or failed, and why. Treat ignored rows as a bug until proven otherwise.

## Where this fits in DISCO and PLANS

- Land raw imports in a flat **D (Data)** module, faithful to the source. Don't calculate
  in it. *(Logical)*
- Don't import the same file into many models — load it once into a **Data Hub** and feed
  spokes from there. *(Necessary, Sustainable)*
- Keep import mappings driven by stable codes and saved views, not ad-hoc layouts, so the
  load survives next month's file. *(Sustainable)*

**Related:** [Actions & Processes](actions-and-processes.md) ·
[Integration overview / Data Hub](README.md) ·
[DISCO](../03-methodology/disco.md) ·
[Lists & hierarchies](../01-fundamentals/lists-and-hierarchies.md) ·
[REST API](rest-api.md)

> Source: Anaplan import/export & data integration docs (`help.anaplan.com`, Data
> Integrations section). See [`SOURCES.md`](../../SOURCES.md).
