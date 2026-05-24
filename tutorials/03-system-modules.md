# Step 3 — System Modules (the DISCO "S")

> **Level:** L1→L2 · **Area:** Tutorial · **DISCO:** System · **PLANS:** Sustainable, Auditable

**System modules** are the quiet backbone. They hold time attributes, mappings between lists, and
Boolean flags — built **once**, referenced **everywhere**. Putting this logic here (not inside
calculations) is what makes a model *sustainable*. See [DISCO](../docs/03-methodology/disco.md).

We'll build four, matching the blueprint's `SYS01`–`SYS04`: a time-settings module, the organization
and account attribute modules, and an exchange-rates module for currency conversion.

---

## 3.1 SYS01 Time Settings

A tiny module dimensioned **only by Time** that exposes useful per-period attributes so calc
modules don't recompute them. This is the standard Anaplan pattern.

**Modules → New Module.** Name `SYS01 Time Settings`. **Applies To:** *Time* (no lists, no
Versions).

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Period Index` | Number | None | Time | `CUMULATE(1)` *(a 1, 2, 3… counter for ordering / offsets)* |
| `Period Start Date` | Date | None | Time | `START()` |
| `Is Actual?` | Boolean | None | Time | `START() <= CURRENTPERIODSTART()` — see note |

> **`Is Actual?` the sustainable way.** Don't hard-code `IF Time = Mar 25`. Compare each period's
> **start date** to the current period so the flag self-updates every month:
>
> ```
> Is Actual?  =  START() <= CURRENTPERIODSTART()
> ```
>
> `CURRENTPERIODSTART()` returns the **date** the current period begins, and `START()` returns each
> period's start **date** — so both sides are dates and the comparison is valid. (Don't wrap it as
> `START(CURRENTPERIODSTART())` — `START()` takes a period, not a date.) The cut-over lives in
> **one place** (the model's Current Period), so a roll to a new year needs no edit. We'll reuse
> `Is Actual?` to blend actuals and forecast in Step 5.

---

## 3.2 SYS02 Organization Details (org attributes + mapping)

Each cost centre's attributes and mappings live here — its country, region and **local currency** —
so other modules read them instead of hard-coding. **Applies To:** *L3 Cost Centre*.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Country` | List: `L2 Country` | None | L3 Cost Centre | `PARENT(ITEM(L3 Cost Centre))` |
| `Region` | List: `L1 Region` | None | L3 Cost Centre | `PARENT(Country)` |
| `Local Currency` | List: `Currency` | None | L3 Cost Centre | *(input — e.g. UK cost centres → GBP, US → USD, India → INR)* |
| `Is Active?` | Boolean | None | L3 Cost Centre | *(input, default TRUE)* |

`Country`/`Region` are computed with `PARENT()` so they always match the hierarchy — no manual
upkeep. `Local Currency` is the key the FX conversion looks up in Step 5. These are **mappings** you
`LOOKUP`/`SUM` against later instead of `SELECT`.

> We climb the hierarchy with `PARENT()` (the leaf's parent, then its parent) — never `ANCESTOR()` or
> `CHILDREN()`. A `PARENT` chain is explicit and auditable.

---

## 3.3 SYS03 Account Details (account classification)

The chart of accounts needs a little classification so the P&L build (Step 5) can post and total
correctly. **Applies To:** *L3 P&L Account*.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Account Group` | List: `L2 P&L Group` | None | L3 P&L Account | `PARENT(ITEM(L3 P&L Account))` |
| `Sign` | Number | None | L3 P&L Account | *(input — `+1` revenue, `-1` cost)* |
| `Is Revenue?` | Boolean | None | L3 P&L Account | `Account Group = L2 P&L Group.Revenue` |

---

## 3.4 SYS04 Exchange Rates (FX)

A System module holding the rate from each currency **to the group currency (USD)**, by month and
version (rates differ Actual vs Budget vs Forecast). Conversions read this — never a hard-coded rate.

**Applies To:** *Currency × Time × Versions*.

**Blueprint:**

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| `Rate to USD` | Number (4 dp) | None | Currency × Time × Versions | *(input — units of USD per 1 unit local)* |
| `Is Group Currency?` | Boolean | None | Currency | `ITEM(Currency) = Currency.USD` |
| `Rate (filled)` | Number (4 dp) | None | Currency × Time × Versions | `IF Is Group Currency? THEN 1 ELSE Rate to USD` |

Enter a couple of rates (e.g. `GBP → 1.27`, `INR → 0.012`). `Rate (filled)` returns `1` for USD so
USD cost centres pass through unchanged. Step 5's CAL03 looks this up by each cost centre's
`Local Currency`.

> **Where's COGS %?** It is **not** here. A product's cost ratio is a driver planners tune each cycle,
> so it lives in an **Inputs** module (`INP03 Cost Drivers`) in [Step 4](04-input-modules.md), not
> in System. System is for stable mappings/flags only.

---

## 3.5 Sanity check

- [ ] `SYS01 Time Settings` applies to **Time only** and has `Is Actual?` driven from the current
      period (no hard-coded date; both sides of the comparison are dates).
- [ ] `SYS02 Organization Details` derives `Country`/`Region` via `PARENT()` and holds
      `Local Currency`.
- [ ] `SYS03 Account Details` derives `Account Group` via `PARENT()` and holds `Sign`.
- [ ] `SYS04 Exchange Rates` holds `Rate to USD` with a `Rate (filled)` that returns 1 for USD.
- [ ] None of these modules contain business *calculations* — only attributes, flags, mappings.

> **DISCO check:** all four are pure **System**. If you ever feel tempted to put
> `Revenue = …` here, stop — that belongs in a **Calculations** module (Step 5).

---

**Related:** [DISCO](../docs/03-methodology/disco.md) ·
[Lookup & mapping](../docs/02-formulas/) ·
[Time](../docs/01-fundamentals/time.md) ·
[Naming conventions](../templates/naming-conventions.md)

**Next → [Step 4 — Input Modules](04-input-modules.md)**
