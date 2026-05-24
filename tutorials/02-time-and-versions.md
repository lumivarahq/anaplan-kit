# Step 2 — Time & Versions

> **Level:** L1 · **Area:** Tutorial · **DISCO:** (foundations)

Two dimensions in Anaplan are **native** — you don't build them as lists, you configure them on the
model: **Time** and **Versions**. Almost every module in our FP&A model uses both.

---

## 2.1 Configure the model calendar (Time)

1. Open **Model Settings → Time** (the calendar icon / "Time" in the model settings menu).
2. Set:
   - **Calendar type:** *Calendar Months/Quarters/Years*.
   - **Current Period:** `Apr 2026` (our "today" for this build — it drives forecast switchover later).
   - **Fiscal year start month:** January (keep it simple).
3. Set the **range of years**:
   - **Past:** 1 year (gives us `FY25` for actuals).
   - **Future:** 1 year (gives us `FY27`).
   - This yields **FY25, FY26, FY27** with months and quarters under each.
4. Click **OK**. Anaplan generates the Time hierarchy: Year → Quarter → Month.

> **Time summary levels** matter later: a module dimensioned by Time can be viewed at Month, then
> rolled to Quarter/Year automatically. You don't make separate "quarter" line items.

> **Performance heads-up (L2):** the full calendar is more periods than most modules need. In
> [Step 8](08-review-against-plans.md) we discuss applying a **Time Range** so, e.g., the
> assumptions module only spans `FY26`. For now, the model calendar is fine.

---

## 2.2 Understand Versions

**Versions** is a native list used to hold parallel copies of a plan: `Actual`, `Budget`,
`Forecast`, etc. You compare them side by side.

1. Open **Model Settings → Versions**.
2. You'll see one default version. Configure these three:

| Version | Is Actual? | Notes |
| --- | --- | --- |
| `Actual` | ✓ (tick the *Actual* column) | Holds loaded actuals (Step 7) |
| `Budget` | — | The locked annual plan |
| `Forecast` | — | The living re-plan; default *current* version |

3. Set **Forecast** as the **Current** version (the dot/radio in the Current column) — it's the one
   users land on.
4. The **Actual** version's "Is Actual?" flag is special: combined with a **switchover** date it
   lets a module show actuals for past months and forecast for future months automatically (you'll
   use this in [Step 5](05-calculation-modules.md)).

> **Switchover** (Versions settings): set the Actual version's switchover to the **start of the
> current period** (`Apr 2026`). Then any line item with *Time Range = model calendar* and the
> right setup reads Actual ≤ Mar 2026 and Forecast from Apr 2026 on. We'll wire the logic
> explicitly in CAL so it's auditable.

---

## 2.3 Sanity check

- [ ] Time shows **FY25 / FY26 / FY27**, each with 4 quarters and 12 months.
- [ ] Current Period = `Apr 2026`.
- [ ] Versions list = `Actual` (Is Actual ✓), `Budget`, `Forecast` (Current).
- [ ] Still no modules — Time and Versions are model-level settings, ready to dimension modules with.

---

**Related:** [Time](../docs/01-fundamentals/time.md) ·
[Versions](../docs/01-fundamentals/versions.md) ·
[Time Ranges (L2 performance)](../docs/07-performance/time-ranges.md) ·
[Naming conventions](../templates/naming-conventions.md)

**Next → [Step 3 — System Modules](03-system-modules.md)**
