# Rolling forecast (n-month window)

> **Level:** L2 · **Area:** Time & Forecasting · **PLANS:** Sustainable, Logical · **DISCO:** System / Calculations

## The ask
"We run an 18-month rolling forecast. Every month-end the window should shuffle forward one month automatically — I'm tired of re-pointing the dashboard each cycle."

## When you'll see this
- Rolling 12/18/24-month forecasts that advance each close.
- A "current month" that moves and a window that follows it.
- Reports that should always show "next N months" without manual edits.

## Approach
Never hard-code the current month. Store it **once** as a setting and derive the window with **Boolean flags per period** in a `SYS00 Time Settings` module. Everything (forecast logic, filters, dashboards) reads those flags. When the cycle rolls, you change **one** input (the current period) and the whole model follows — pure PLANS *Sustainable*.

```
In Forecast Window? = period is after the cutoff AND within N months of it
```

Drive "current period" from a single input cell. Compare each period's index to the current period's index using a period-number line item.

Why idiomatic:
- **Sustainable (PLANS):** the window is data-driven; rolling forward is a one-cell change, no formula edits.
- **Logical:** one source of truth (`SYS00`) for "where are we now".

## Blueprint
**`SYS00 Time Settings`** — period scaffolding, `Applies To` Time:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Period Index | Number | None | Time | `CUMULATE(1)` *(1,2,3… across the timescale)* |
| Current Period? | Boolean | None | Time | `Period Index = SYS90 Settings.Current Index` |
| In Forecast Window? | Boolean | None | Time | see formula |

**`SYS90 Settings`** — one cell, the only thing you change each cycle:

| Line Item | Format | Summary | Applies To | Formula |
| --- | --- | --- | --- | --- |
| Current Month | Time period (or Date) | None | *(none)* | *(input each close)* |
| Current Index | Number | None | *(none)* | `LOOKUP/derived index of Current Month` |
| Window Length (months) | Number | None | *(none)* | *(input, e.g. 18)* |

## Formula(s)
Give every period a sequential index using `CUMULATE(1)`:

```
// SYS00 Time Settings -> Period Index
CUMULATE(1)
```

The rolling window: periods strictly after the current month, up to N months ahead:

```
// SYS00 Time Settings -> In Forecast Window?
Period Index > SYS90 Settings.Current Index
AND Period Index <= SYS90 Settings.Current Index + SYS90 Settings.Window Length
```

Use the flag wherever the window matters — e.g. only forecast forward periods:

```
// CAL60 Forecast -> Value
IF SYS00 Time Settings.In Forecast Window? THEN Forecast Driver ELSE 0
```

(For "actuals before, forecast after" see [actual-forecast-switchover](actual-forecast-switchover.md).)

## Pitfalls / gotchas
- **Don't hard-code `IF Time = Jan 25`** anywhere — that's the cardinal rolling-forecast sin. Drive everything from `Current Month`.
- Size your model's **Time scale / Time Range** to actually contain the rolling window plus history — the window can't show periods the model doesn't have. See [shrink-with-subsets-and-time-ranges](../performance/shrink-with-subsets-and-time-ranges.md).
- Decide whether the current month is *inside* or *outside* the forecast window (is it actual or forecast?). Be explicit with `>` vs `>=`.
- If `Current Index` is set wrong (off-by-one), the whole window shifts. Show `Current Period?` on an admin board to sanity-check.
- `CUMULATE(1)` indexes across the **whole** timescale; if you use Time Ranges, confirm indices still align as intended.

## Performance & PLANS notes
- One input cell drives the entire roll — the textbook **Sustainable** win.
- Boolean flags are cheap and reusable across forecast, filters, and DCA (lock past, open future).
- Combine with a **dynamic time filter** so dashboards show exactly the window (see [dynamic-time-filter](../ux-and-workflow/dynamic-time-filter.md)).

## Related
- [`docs/02-formulas/time-functions.md`](../../docs/02-formulas/time-functions.md)
- [`docs/07-performance/time-ranges.md`](../../docs/07-performance/time-ranges.md)
- Recipes: [actual-forecast-switchover](actual-forecast-switchover.md) · [dynamic-time-filter](../ux-and-workflow/dynamic-time-filter.md) · [ytd-mtd-qtd](ytd-mtd-qtd.md)
