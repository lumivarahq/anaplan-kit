# Fundamentals Exercises — Lists, Modules, Formats, Dimensions

> **Level:** L1 · **Area:** Exercises · Solutions: [`solutions/fundamentals-solutions.md`](solutions/fundamentals-solutions.md)

Practice the building blocks. Attempt each on paper using the
[blueprint template](../templates/blueprint-template.md) and
[naming conventions](../templates/naming-conventions.md) before checking the solution. These map to
[Tutorial Steps 1–4](../tutorials/) and [fundamentals docs](../docs/01-fundamentals/).

---

## A. Lists & hierarchies

**A1 (L1).** You must plan by **Region › Country › Cost Centre**. Write the list-definition table:
name each list, its type, its parent, and a sample of members. Which list will modules normally be
*dimensioned by*, and why?

**A2 (L1).** A colleague built `Region`, `Country` and `Cost Centre` as **three separate flat
lists** and a `Cost Centre` line item "Region" that they type in by hand. What's wrong with this,
and what should they do instead?

**A3 (L2).** Your model must hold **2 million GL transaction rows**. Should `Transactions` be a
standard list or a **numbered list**? Give two reasons.

**A4 (L1).** What is a **Top Level Item** on a list, and why add one to `Product`? Give the member
name you'd use.

---

## B. Modules & dimensions

**B1 (L1).** You're building `INP01 Revenue Assumptions` to plan **Volume** and **Price** by
product, by entity, by month, by version. State the module's **Applies To** (its dimensionality).

**B2 (L1).** `INP02 Cost Drivers` plans **Fixed OpEx** by entity and month — costs do **not** vary
by product here. A teammate says "add `Product` to its Applies To, just in case." Why is that a bad
idea? Name the PLANS principle.

**B3 (L2).** A module is dimensioned `Entity (5) × Product (3) × Time (36 months) × Versions (3)`
and has **4 line items**. Roughly how many cells is that? Why does this number matter?

---

## C. Formats

**C1 (L1).** Give the correct **Format** for each line item:
1. `Gross Revenue`
2. `COGS %`
3. `Is Active?`
4. `Cost Centre Manager`
5. `Period Start Date`
6. `Region` (a mapping that points each Entity to its parent region)

**C2 (L1).** Why should a flag be a **Boolean** line item rather than a Text line item holding
`"Yes"`/`"No"`? Give a performance reason and a usability reason.

---

## D. Summary methods

**D1 (L1).** For each line item, choose the right **Summary** method (Sum / Average / None /
Formula) and say why:
1. `Gross Revenue`
2. `Price`
3. `COGS %`
4. `Is Actual Month?`
5. `EBITDA Margin %`

**D2 (L2).** You have `Price` (Average summary) and `Volume` (Sum summary) and a line
`Gross Revenue = Volume * Price`. At the **Year** total, will `Gross Revenue` equal
`(sum of Volume) × (average Price)`? Explain what actually happens and how to make the annual total
correct.

---

## E. DISCO classification

**E1 (L1).** Classify each module by DISCO type (D/I/S/C/O) and give its prefix:
1. A module holding imported actuals from the GL.
2. A module where planners type next year's headcount.
3. A module computing `Revenue − COGS = Gross Profit`.
4. A module of Boolean time flags dimensioned only by Time.
5. A module shaped exactly for a dashboard P&L card.

**E2 (L2).** In which DISCO module type does each of these belong?
1. The mapping `Entity → Region`.
2. A product's default `COGS %`.
3. A planner's monthly `Volume` assumption.
4. `Gross Revenue = Volume × Price`.

---

**Related:** [Lists & hierarchies](../docs/01-fundamentals/lists-and-hierarchies.md) ·
[Modules](../docs/01-fundamentals/modules.md) ·
[Line items & formats](../docs/01-fundamentals/line-items-and-formats.md) ·
[DISCO](../docs/03-methodology/disco.md) ·
[Solutions →](solutions/fundamentals-solutions.md)
