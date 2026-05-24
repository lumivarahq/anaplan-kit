# Ranking Functions

> **Level:** L2 · **Area:** Formulas

Ranking functions order items by value — "who's #1?", "top 10 products", "running cumulative by
rank". They return a **number** (the rank), which you then use to filter or label.

---

### RANK

**Syntax**
```
RANK(Source values [, Direction, Equal handling, Tie-break value, Groups])
```

**What it does**
Returns the **rank position** of each value within its set (1 = first). You control the direction
(ascending/descending), how ties are handled, an explicit tie-break, and an optional grouping so
ranking restarts within each group.

**Example**
```
Sales Rank = RANK(Total Sales, DESCENDING)
```
Ranks products so the highest seller is `1`. Add a `Groups` argument (e.g. region) to rank within
each region independently.

**Watch out for**
- **Direction matters** — without it you may rank smallest-first when you wanted largest-first.
- **Ties:** decide deliberately how equal values are handled and supply a tie-break value, or two
  items can share a rank (and a rank can be skipped).
- The result is a **Number**; the line item must be Number-formatted.

**Source:** https://help.anaplan.com/rank-a5f5778e-5e88-48ad-96ad-715178cda9b2

---

### RANKCUMULATE

**Syntax**
```
RANKCUMULATE(Cumulation values, Ranking values [, Direction] [, Include value] [, Ranking groups])
```

**What it does**
Walks items **in rank order** and returns a **running cumulative total** of one line item as it
goes. Perfect for "cumulative share by rank" / Pareto / ABC analysis: sort by sales, accumulate
sales down the ranking.

**Example**
```
Cumulative Sales by Rank = RANKCUMULATE(Total Sales, Total Sales, DESCENDING)
```
Accumulates `Total Sales` from the top seller downward — the first item shows its own sales, the
second shows the top two combined, and so on.

**Watch out for**
- The **first** argument is *what you accumulate*; the **second** is *what you rank by* — they are
  often the same line item but need not be.
- Use `Ranking groups` to accumulate within each group (e.g. cumulative within region).
- Confirm the exact optional-argument order in Anapedia.

**Source:** https://help.anaplan.com/1af75839-f426-43bf-b864-9027f1770161

---

## Worked example: Top-N products

Goal: flag the **top 5** products by sales, and show each product's cumulative share so you can do
80/20 analysis. Module dimensioned by `Product`.

| Line Item | Format | Formula | Notes |
| --- | --- | --- | --- |
| `Total Sales` | Number | *(from sales module)* | the measure |
| `Sales Rank` | Number | `RANK(Total Sales, DESCENDING)` | 1 = biggest |
| `In Top 5?` | Boolean | `Sales Rank <= 5` | the Top-N flag |
| `Cumul Sales` | Number | `RANKCUMULATE(Total Sales, Total Sales, DESCENDING)` | running total down the ranking |
| `Cumul Share %` | Number | `Cumul Sales / Total Sales[SUM: SYS Product.All]` | each rank's cumulative % of the grand total |

```
Sales Rank    = RANK(Total Sales, DESCENDING)
In Top 5?     = Sales Rank <= 5
Cumul Sales   = RANKCUMULATE(Total Sales, Total Sales, DESCENDING)
Cumul Share % = Cumul Sales / Grand Total Sales
```

Now `In Top 5?` is a clean Boolean you can filter a dashboard on, and `Cumul Share %` tells you how
many products make up (say) 80% of revenue — all driven by data, recomputing automatically as sales
change. To switch from Top-5 to Top-10, change `5` once (or, even better, point `<=` at an input
line item so planners control N without touching the formula). *(Sustainable.)*

> The grand total `Total Sales[SUM: SYS Product.All]` uses the mapping-aggregation pattern from
> [aggregation-functions.md](aggregation-functions.md) / [lookup-and-mapping.md](lookup-and-mapping.md).

**Related:** [aggregation-functions.md](aggregation-functions.md) ·
[logical-functions.md](logical-functions.md) (the Top-N Boolean) · [cheatsheet.md](cheatsheet.md)
