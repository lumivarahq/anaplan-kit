# FP&A P&L Planning — Blueprint

> **Level:** L2 · **Area:** Blueprint (FP&A) · **DISCO:** mixed

The **canonical** model of the kit — the one the [tutorials](../../tutorials/) build step by step. It
plans **revenue (volume × price)** and **cost**, converts local amounts to the group currency, and
rolls everything up to a **P&L** on the shared chart of accounts. It is the *master plan*: Sales,
Workforce and Supply Chain feed numbers **into** it.

---

## What this model does

1. Planners enter **volume** and **price** assumptions by Cost Centre × Product × Time (Inputs).
2. A calc engine derives **gross revenue**, applies **COGS %**, and computes **gross profit**.
3. **Opex** (salaries, travel, marketing, IT) is planned per Cost Centre.
4. Local amounts convert to **group currency (USD)** via the shared FX rates.
5. Every line maps to a **P&L Account**, so the result is a real Profit & Loss with subtotals
   (Revenue → Gross Profit → EBITDA → Net Profit).
6. A rolling **Forecast** blends Actuals-to-date with the plan using `SYS01.Is Actual?`.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | every module is monthly; `Is Actual?` drives the rolling forecast |
| **Versions** (Actual / Budget / Forecast) | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | the scenario axis on all plan modules |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | the entity each P&L line belongs to; supplies `Local Currency` |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](../_common/common-lists.md) | local → USD conversion |
| **L3 P&L Account** + `SYS03 Account Details` | [`_common/common-lists.md`](../_common/common-lists.md) | the chart of accounts the P&L rolls up to; this model **owns** it |
| **L2 Product** | [`_common/common-lists.md`](../_common/common-lists.md) | revenue planning grain |

Domain-specific lists added on top live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Inputs                System                 Calculations              Outputs
  ------                ------                 ------------              -------
  INP01 Volume &  ┐     SYS01 Time      ┐
  Price            │    SYS02 Org        │
  INP02 Opex Plan  ├──► SYS03 Account    ├──►  CAL01 Revenue      ┐
  INP03 COGS %     │    SYS04 FX Rates   │     CAL02 Cost / COGS   ├──► OUT01 P&L
                   ┘                     ┘     CAL03 FX Convert    │    Statement
                                               CAL04 P&L Build     ┘    OUT02 Variance
        ▲                                            ▲
        │                                            │
   feeds from ───────── Sales (revenue), Workforce (salaries), Supply Chain (COGS)
```

- **One direction**: Inputs + System → Calculations → Outputs. No circular references. *(Logical)*
- Each calc step is its **own line item** so a number can be traced from the P&L back to an
  assumption. *(Auditable)*

### How the other domains hand off into this model

| Number | Produced in | Lands in (here) | P&L Account |
| --- | --- | --- | --- |
| Product revenue target | Sales `CAL Target $` | a Revenue feed (sense-check vs `CAL01`) | `Product Revenue` |
| Labour cost | Workforce `CAL Fully-Loaded Cost` | `INP02 Opex Plan` (Salaries) | `Salaries` |
| Direct materials | Supply Chain `CAL Supply Cost` | `CAL02 Cost` (COGS) | `Direct Materials` |

See each domain's `formulas.md` for the exact hand-off line items.

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [Tutorials](../../tutorials/) ·
[DISCO](../../docs/03-methodology/disco.md)
