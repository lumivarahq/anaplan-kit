# Top-down allocation by ratio

> **Level:** L2 · **Area:** Mapping & Allocation · **PLANS:** Logical, Auditable · **DISCO:** Calculations

## The ask
"Marketing have a £5m brand budget at the total-company level. Push it down to each region in proportion to last year's revenue."

## When you'll see this
- A number is planned at a parent level and must land on the children.
- The split follows a **driver ratio** (revenue, headcount, prior spend), not an even share.
- You need each child's slice to sum exactly back to the parent.

## Approach
Compute each child's **share of a driver**, then multiply the parent total by that share. The pattern is three stepped line items (PLANS *Auditable*): the driver, the child's ratio of the driver, and the allocated amount. Pull the parent total down to children with `PARENT` (or a `SUM`/`LOOKUP` over a mapping when the parent isn't a hierarchy ancestor).

```
child allocation = parent total × (child driver ÷ total driver)
```

Why idiomatic:
- **Auditable (PLANS):** one line item per step — you can see the ratio and the result separately.
- **Logical:** ratios sum to 1, so allocations sum back to the parent automatically — no rounding plug needed (usually).

## Blueprint
**`INP01 Brand Budget`** — total typed at the parent, `Applies To` Company (top of Region hierarchy):

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Budget | Number | Sum | Company, Time | *(input)* |

**`CAL20 Allocation`** — `Applies To` Region × Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Driver (PY Revenue) | Number | Sum | Region, Time | `OUT_PY.Revenue` |
| Total Driver | Number | Sum | Region, Time | `Driver (PY Revenue)[SUM: SYS Region.Parent]` *(or via ancestor)* |
| Share | Number | None | Region, Time | `IF Total Driver = 0 THEN 0 ELSE Driver (PY Revenue) / Total Driver` |
| Allocated Budget | Number | Sum | Region, Time | `Parent Budget × Share` |
| Parent Budget | Number | Sum | Region, Time | `INP01 Brand Budget.Budget[LOOKUP: SYS Region.Company]` |

## Formula(s)
Each child's share of the driver, guarding the divide-by-zero:

```
// CAL20 Allocation -> Share
IF Total Driver = 0 THEN 0 ELSE Driver (PY Revenue) / Total Driver
```

Bring the parent total to each child (here the parent is the `Company` an `Applies To` Region maps to):

```
// CAL20 Allocation -> Parent Budget
INP01 Brand Budget.Budget[LOOKUP: SYS Region.Company]
```

Allocate:

```
// CAL20 Allocation -> Allocated Budget
Parent Budget * Share
```

`Total Driver` is the sum of the driver across the children sharing one parent — compute it with a `SUM` back up to the parent, then pull it down again, so every child divides by the *same* total.

## Pitfalls / gotchas
- **Divide-by-zero:** if `Total Driver` is 0 the whole allocation is `1/0`. Always guard with `IF Total Driver = 0 THEN 0`.
- **Ratios must share a common denominator.** Each child must divide by the *parent's* total driver, not its own — get the total to the parent and back down.
- **Rounding:** shares are fractions; allocated amounts may not sum to the penny. If exactness matters, allocate all-but-one child and plug the last (or use a rounding-residual line item).
- Don't hard-code the split percentages — drive them from the live driver so they self-adjust (*Sustainable*).
- Make sure the driver line item has `Sum` summary, or `Total Driver` rolls up wrong.

## Performance & PLANS notes
- Stepped line items (driver → share → allocation) are both **Auditable** and faster to recalc than one nested formula.
- This pattern is reused everywhere — cost allocation, target setting, phasing — so build it cleanly once.
- For driver-based *cost* allocation specifically, see [allocate-by-driver](allocate-by-driver.md); for letting users type the total and auto-split, see [breakback-ratio-input](breakback-ratio-input.md).

## Related
- [`docs/02-formulas/lookup-and-mapping.md`](../../docs/02-formulas/lookup-and-mapping.md)
- Recipes: [allocate-by-driver](allocate-by-driver.md) · [breakback-ratio-input](breakback-ratio-input.md) · [seasonality-phasing](../time-and-forecasting/seasonality-phasing.md) · [item-parent-ancestor-rollup](../hierarchies-and-lists/item-parent-ancestor-rollup.md)
