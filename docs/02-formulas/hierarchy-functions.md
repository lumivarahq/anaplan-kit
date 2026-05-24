# Hierarchy Functions

> **Level:** L2 · **Area:** Formulas

Hierarchy functions navigate **lists and their structure** — "which item am I?", "what's my
parent?", "is X above Y?", "what level am I at?". They return **list items** or **Booleans/numbers**
and are the backbone of building mappings and roll-up logic.

A mental model: every cell of a list-dimensioned module *knows which list item it sits on*.
`ITEM(List)` hands you that item, and the rest of these functions walk up/down the hierarchy from
there.

---

### ITEM

**Syntax**
```
ITEM(List)
```

**What it does**
Returns the **current list item** for the cell being calculated — the item on that row of the
dimension. The key to "am I this item?" tests and to building self-referential logic.

**Example**
```
Is HQ Cost Centre? = ITEM(Cost Centre) = Cost Centre.'HQ'
Own Name           = NAME(ITEM(Cost Centre))
```
The first asks, for each cost-centre row, "is this row the HQ item?"

**Watch out for**
- `ITEM(List)` only works if the module **is dimensioned by** that list.
- Comparing `ITEM(...)` to a hard-coded item name is acceptable for a one-off, but for recurring
  logic drive it from a System flag instead. *(Sustainable.)*

**Source:** https://help.anaplan.com/item-41298b7a-e877-40e8-8cfa-8d7009d8686f

---

### PARENT

**Syntax**
```
PARENT(Child item)
```

**What it does**
Returns the **immediate parent** of a list item (or time period) — one level up the hierarchy.
Returns a value of the same data type as the child, but at the parent's level.

**Example**
```
CC Region = PARENT(ITEM(Cost Centre))     -- if Region is the parent list of Cost Centre
```
Gives each cost centre its region item — a quick way to build a mapping when the hierarchy already
encodes the relationship.

**Watch out for**
- Result is **formatted as the parent list** — your line item must match that format.
- `PARENT` goes **exactly one** level up. For "two levels up" / a specific level, use `ANCESTOR`.

**Source:** https://help.anaplan.com/parent-1cdc486d-c4d7-42db-8b1a-d9e12c060999

---

### ANCESTOR

**Syntax**
```
ANCESTOR(Item, Level/Target)
```
*(Confirm exact arguments in Anapedia — see note below.)*

**What it does**
Returns an **ancestor** of an item at a chosen level of a composite hierarchy — like `PARENT`, but
able to jump **multiple** levels up to a named list level rather than just one.

**Example**
```
CC Division = ANCESTOR(ITEM(Cost Centre), Division)   -- jump from cost centre up to its division
```

**Watch out for**
- Use this when the level you want is **more than one step** above; `PARENT` handles a single step.
- ⚠️ **Validation note:** a dedicated Anapedia page URL for `ANCESTOR` could not be confirmed via
  search for this kit (related pages: `PARENT`, `ISANCESTOR`, `ITEMLEVEL`). **Confirm the exact
  argument list and a current source URL in Anapedia before relying on this signature.**

**Source:** Not separately confirmed — see the all-functions index
https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3 and confirm the
ANCESTOR page for your platform version.

---

### ISANCESTOR

**Syntax**
```
ISANCESTOR(Item1, Item2)
```

**What it does**
Returns a **Boolean**: TRUE if `Item1` is an ancestor of `Item2` (its parent, grandparent, and so
on). Great for "does this detail row belong under that node?" tests across composite hierarchies.

**Example**
```
Under Selected Node? = ISANCESTOR(Selected Region, ITEM(Cost Centre))
```
TRUE for every cost centre that sits beneath the chosen region.

**Watch out for**
- Returns a **Boolean** — use it directly, no `IF … THEN TRUE` wrapper.
- Order matters: `ISANCESTOR(ancestor, descendant)`. Swapping the arguments inverts the test.

**Source:** https://help.anaplan.com/isancestor-2c35cf1b-9392-4726-8ebb-4291d1b24225

---

### ITEMLEVEL

**Syntax**
```
ITEMLEVEL(Item [, LEAF])
```

**What it does**
Returns the **level** of an item within its hierarchy as text/number, letting you treat leaf items
differently from parents. The optional `LEAF` keyword tests for bottom-level items.

**Example**
```
Is Leaf? = ITEMLEVEL(ITEM(Cost Centre), LEAF)
```
Flags the lowest-level cost centres (those with no children) — useful so input only happens at
leaf level.

**Watch out for**
- Handy to **prevent double counting**: calculate only at leaves and let Summary roll the rest up.
- Confirm the exact return type/keywords for your platform.

**Source:** https://help.anaplan.com/itemlevel-756d1428-5f1d-4d79-8274-d075a1bd312f

---

### CHILDREN

**Syntax**
```
Source.Line Item[SUM: CHILDREN(Parent)]    -- used inside an aggregation as a mapping
```
*(Confirm exact usage/arguments in Anapedia — see note below.)*

**What it does**
References the **direct children** of a parent item, typically inside an aggregation to total just
one level down (rather than rolling the whole subtree).

**Example**
```
Sum of Children = Amount[SUM: CHILDREN(ITEM(Region))]
```
Totals only the immediate children of each region.

**Watch out for**
- Often you **don't need** `CHILDREN` at all — a line item's **Summary = Sum** already rolls
  children up its own hierarchy automatically. Reach for it only when you need explicit one-level
  control.
- ⚠️ **Validation note:** a dedicated Anapedia page URL for `CHILDREN` could not be confirmed via
  search for this kit. **Confirm the exact syntax and a current source URL in Anapedia before use.**

**Source:** Not separately confirmed — see the all-functions index
https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3 and confirm the
CHILDREN page for your platform version.

---

### FIRSTNONBLANK

**Syntax**
```
Values to search[FIRSTNONBLANK: Mapping]
```

**What it does**
An **aggregation** function: returns the **first non-blank** value found for each target item
(across the mapped source, in list/time order). The natural way to grab "the first value that
exists" — e.g. the first month a product had sales. Returns a value matching the source's type.

**Example**
```
First Active Region = SYS Cost Centre.Region[FIRSTNONBLANK: SYS Cost Centre.Division]
```
For each division, the first non-blank region among its cost centres.

**Watch out for**
- The containing line item must be **dimensioned by all of the mapping's dimensions**.
- "First" follows the **order of the list/time dimension** — make sure that order means what you
  think.
- It is the default aggregation method for text/date/list line items in `MOVINGSUM`/`TIMESUM`.

**Source:** https://help.anaplan.com/firstnonblank-125738aa-c067-4602-b5bb-da6f4dfe940c

---

## The "am I this item?" pattern (and why ITEM beats SELECT)

A recurring need: do something only for a particular item, or build a mapping from the hierarchy.

```
-- Build a Cost Centre -> Region mapping straight from the hierarchy (no manual table):
CC Region        = PARENT(ITEM(Cost Centre))

-- Treat one item specially, sustainably (compare ITEM, don't SELECT a value):
Apply HQ Overhead? = ITEM(Cost Centre) = Cost Centre.'HQ'
```

Using `ITEM`/`PARENT`/`ANCESTOR` keeps the logic **driven by structure**, so adding members or
re-parenting the hierarchy needs no formula change — far more sustainable than `SELECT`ing a
specific item (see [lookup-and-mapping.md](lookup-and-mapping.md)).

**Related:** [lookup-and-mapping.md](lookup-and-mapping.md) (hierarchy-built mappings feed
LOOKUP/SUM) · [aggregation-functions.md](aggregation-functions.md) (ANY/ALL/FIRSTNONBLANK) ·
[DISCO — System modules](../03-methodology/disco.md) · [cheatsheet.md](cheatsheet.md)
