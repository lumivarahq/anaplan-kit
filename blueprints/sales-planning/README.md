# Sales Planning — Blueprint

> **Level:** L2 · **Area:** Blueprint (Sales) · **DISCO:** mixed

Plans **sales targets by rep and product**, sets **quotas** from a top-down number, and tracks a
**pipeline** to see whether coverage is sufficient. Its product **Target $** is the revenue signal
that should reconcile with the FP&A model's `CAL01 Gross Revenue`.

---

## What this model does

1. Reps are organised into **territories**; each rep maps to a **Cost Centre** in the shared org.
2. Leadership sets a **top-down target** per territory × product (Inputs).
3. The engine **allocates** the target down to reps by a weight (e.g. prior attainment), producing a
   per-rep **quota**.
4. A **pipeline** of open opportunities is loaded (Data) and weighted by probability.
5. **Coverage** = weighted pipeline ÷ quota tells each rep how exposed they are.
6. Targets convert to **USD** and roll up the org so Sales reconciles with the FP&A P&L Revenue.

---

## Which `_common` lists it reuses

| Shared structure | From | Used as |
| --- | --- | --- |
| **Time** + `SYS01 Time Settings` | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | monthly target / pipeline phasing; `Is Actual?` for attainment-to-date |
| **Versions** | [`_common/time-and-versions.md`](../_common/time-and-versions.md) | Budget (quota) vs Forecast (latest call) |
| **L3 Cost Centre/Entity** + `SYS02 Organization Details` | [`_common/organization-hierarchy.md`](../_common/organization-hierarchy.md) | each rep's home cost centre → Country/Region roll-up |
| **Currency** + `SYS04 Exchange Rates` | [`_common/common-lists.md`](../_common/common-lists.md) | local targets → USD |
| **L2 Product** | [`_common/common-lists.md`](../_common/common-lists.md) | the product axis of targets & pipeline |
| **L3 P&L Account** | [`_common/common-lists.md`](../_common/common-lists.md) | `Target $` feeds the `Product Revenue` line |

Domain-specific lists (Sales Rep, Territory, Opportunity, Sales Stage) live in [`lists.md`](lists.md).

---

## Architecture sketch (data flow)

```
  Inputs               System                Data            Calculations         Outputs
  ------               ------                ----            ------------         -------
  INP01 Top-Down ┐     SYS01 Time     ┐
  Target          │    SYS02 Org       │     DAT01
  INP02 Rep        ├──► SYS10 Rep       ├──►  Pipeline ──►  CAL01 Quota      ┐
  Weight          │    Details          │    (numbered)    Allocation        ├─► OUT01 Rep
                  ┘    SYS04 FX         ┘                   CAL02 Weighted    │   Scorecard
                       SYS11 Stage Prob                     Pipeline          │
                                                            CAL03 Coverage    ┘
                                                            CAL04 Target USD ──► (feeds FP&A Revenue)
```

- One direction: Inputs/Data + System → Calculations → Outputs. *(Logical)*
- The numbered **Opportunity** list keeps the large, churning pipeline out of the planning grids.
  *(Performance)*

### Hand-off to FP&A

`CAL04 Target (USD)` summed by Cost Centre × Product × Time is the **same shape** as FP&A
`CAL01 Gross Revenue (USD)` — the two should reconcile. Sales is the *bottom-up* revenue view; FP&A
is the *driver-based* view. See [fpa-pl-planning/formulas.md](../fpa-pl-planning/formulas.md).

---

**Related:** [`lists.md`](lists.md) · [`modules.md`](modules.md) · [`formulas.md`](formulas.md) ·
[`_common` backbone](../_common/README.md) · [FP&A blueprint](../fpa-pl-planning/README.md) ·
[DISCO](../../docs/03-methodology/disco.md)
