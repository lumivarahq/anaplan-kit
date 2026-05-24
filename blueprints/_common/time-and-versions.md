# `_common` — Time & Versions

> **Level:** L2 · **Area:** Blueprint (shared backbone) · **DISCO:** System

The shared calendar and the shared scenario axis. Configured **once** for the connected-planning
landscape; every domain ticks "Applies to Time" / "Applies to Versions" to inherit them. Native Time
and Versions are *not* ordinary lists — don't rebuild them by hand. See
[Time](../../docs/01-fundamentals/time.md).

---

## Time Settings (the standard)

| Setting | Value | Why |
| --- | --- | --- |
| Calendar type | Calendar Months / Quarters / Years | Standard 12-month planning grain. |
| Fiscal year start | **January** (FY = calendar year here) | Keeps the example simple; change in one place if your FY starts Apr/Jul/Oct. |
| Model span | **FY2024 → FY2026** (3 years) | One actual-ish year + plan years. |
| Period types shown | Month, Quarter, Year | Months are the input grain; Q/Y roll up automatically. |
| Current Period | **Mar FY2025** | The "today" marker that splits Actual from Forecast (set in Model Settings). |

> Months are the **input grain**. Quarters and Years are roll-ups Anaplan gives you for free — never
> create line items to sum months into quarters. *(Necessary, Performance)*

---

## Versions (the scenario axis)

| Version | Role | Editable? |
| --- | --- | --- |
| **Actual** | Loaded / historic results. | No (import only). |
| **Budget** | The locked annual plan (the baseline you measure against). | Once, then locked. |
| **Forecast** | The living view: Actuals to date + latest plan for the rest. | Yes (planners). |

A formula version (`Variance = Forecast − Budget`) can be added as a **Version formula** so it shows
across the version axis without a separate line item. *(Necessary)*

---

## `SYS01 Time Settings` — the time flags module

The backbone of all time intelligence. A tiny **System** module dimensioned **by Time only** (one
column per month) holding Boolean and attribute line items that every other module reads instead of
hard-coding dates. Built once, referenced everywhere. *(Sustainable, Performance — Booleans beat `IF`.)*

**Module:** `SYS01 Time Settings` · **DISCO: System** · **Applies To:** Time

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Is Actual? | Boolean | — | Time | `ITEM(Time) <= 'SYS01 Time Settings'.Current Period` *(set against the current-period marker)* |
| Is Forecast? | Boolean | — | Time | `NOT Is Actual?` |
| Is Current Year? | Boolean | — | Time | `YEARVALUE(Current Period flag) = ITEM(Time.Year)` *(true for all months of the open FY)* |
| Is Current Month? | Boolean | — | Time | `Is Actual? AND NOT Is Actual?[NEXT: 1]` *(last actual month)* |
| Is First Month of Year? | Boolean | — | Time | `MONTH(START()) = MONTH(START(YEAR))` |
| Is Last Month of Year? | Boolean | — | Time | `Is First Month of Year?[NEXT: 1]` |
| Period Start Date | Date | — | Time | `START()` |
| Period End Date | Date | — | Time | `END()` |
| Days in Period | Number | Sum | Time | `END() - START() + 1` |
| Year Label | Text | — | Time | `NAME(ITEM(Time.Year))` |

> `Is Actual?` is the master switch a rolling forecast keys off: *"use Actuals where `Is Actual?`,
> else use the plan."* Every domain reuses it — see each `formulas.md`.

---

## How domains reuse Time & Versions

- **FP&A, Sales, Supply Chain, Workforce** all dimension their time-phased modules by this Time and
  this Versions axis — so Actual/Budget/Forecast and the calendar mean the same thing everywhere.
- Rolling-forecast blends (`IF 'SYS01 Time Settings'.Is Actual? THEN Actuals ELSE Plan`) reference
  `SYS01` rather than naming any month. Roll the model to FY2027 and nothing breaks. *(Sustainable)*

---

**Related:** [`organization-hierarchy.md`](organization-hierarchy.md) · [`common-lists.md`](common-lists.md) ·
[Time fundamentals](../../docs/01-fundamentals/time.md) ·
[Versions](../../docs/01-fundamentals/) · [FP&A formulas](../fpa-pl-planning/formulas.md)
