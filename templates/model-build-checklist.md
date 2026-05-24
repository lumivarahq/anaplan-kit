# Model-Build Checklist (copy-paste)

> **Level:** L2 · **Area:** Templates · Run before you call a build "done" or review someone else's.

A clean, standalone, copy-paste version of the methodology checklist
([`docs/03-methodology/model-build-checklist.md`](../docs/03-methodology/model-build-checklist.md)).
Copy the block below into your ticket, PR description or review doc and tick as you go. It's phrased
as **DISCO + PLANS + delivery** checks.

---

```markdown
## Model-Build Checklist — [model / module name]
Reviewer: [name]   Date: [date]

### Structure (DISCO)
- [ ] Every module is clearly ONE DISCO type (Data / Inputs / System / Calculations / Outputs).
- [ ] Mappings and attributes live in System modules, not scattered in calcs.
- [ ] Data flows one way: D/I -> S -> C -> O. No circular references.
- [ ] Modules follow the naming convention (DAT/INP/SYS/CAL/OUT prefixes + numbering).

### Performance (P)
- [ ] No module is dimensioned by a list it doesn't need.
- [ ] Time Ranges applied where a module doesn't need the full calendar.
- [ ] Subsets used where a module only needs part of a list.
- [ ] No IF/text formulas over very large cell counts where a Boolean/lookup would do.
- [ ] Sub-expressions used many times are calculated once in their own line item.

### Logical & Auditable (L, A)
- [ ] Complex logic is split into stepped line items, each readable.
- [ ] Names describe meaning (Gross Revenue, not R1).
- [ ] Summary methods set deliberately (Sum vs Average vs Formula vs None).
- [ ] A reviewer can trace any output number back to its inputs.

### Necessary (N)
- [ ] No duplicate calculations (same logic in two places).
- [ ] No unused / experimental line items or modules left behind.
- [ ] Nothing stored that could be cheaply derived (and vice-versa).

### Sustainable (S)
- [ ] No hard-coded dates, periods or list items in any formula.
- [ ] No SELECT on specific list items - mapped via System modules instead.
- [ ] Adding a new product / period / entity needs no formula changes.
- [ ] Shared source data comes from a Data Hub, not re-imported per model.

### Delivery
- [ ] Built to the user story (no scope creep).
- [ ] Tested with realistic data; edge cases checked (blanks, new members, year rollover).
- [ ] Production-bound work is under ALM (built in DEV, promotable via revision).
- [ ] Key assumptions documented (notes module / line-item descriptions).

### Sign-off
- [ ] Builder self-review complete.
- [ ] Peer review complete.
- [ ] Approved to promote.
```

---

## How to use it

- Run it **on yourself first** (builder self-review), then hand to a peer.
- A failed check isn't a fail-the-build — it's a **refactor item**. Log each one. See the worked
  example in [tutorial Step 8](../tutorials/08-review-against-plans.md), which walks this exact list
  against the FP&A model and produces a refactor table.
- The five PLANS letters in order (**P**erformance, **L**ogical, **A**uditable, **N**ecessary,
  **S**ustainable) catch most beginner mistakes before they reach a client model.

---

**Related:** [Methodology checklist](../docs/03-methodology/model-build-checklist.md) ·
[PLANS](../docs/03-methodology/plans-standard.md) · [DISCO](../docs/03-methodology/disco.md) ·
[Naming conventions](naming-conventions.md) ·
[Tutorial Step 8 — Review](../tutorials/08-review-against-plans.md)
