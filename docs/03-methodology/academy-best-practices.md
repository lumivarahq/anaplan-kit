# Academy & Community Best Practices

> **Level:** L2 · **Area:** Methodology · Field-tested advice from Anaplan's training and practitioner community.

The Planual gives you the *rules*; the **Anaplan Academy** (official training) and the **Anaplan
Community** (practitioner forums, best-practice articles, the Center of Excellence) give you the
*habits* that experienced builders use every day. This page distills the ones a new modeler should
adopt immediately.

## Design & structure

- **Design before you build.** Sketch the modules and the data flow (D→I→S→C→O) on paper first.
  Re-architecting a live model is far more expensive than a whiteboard rethink.
- **Use a Data Hub.** Centralise source data in one model and feed spokes from it. One place to
  load, validate and govern data. *(See [`docs/04-integration/`](../04-integration/).)*
- **System modules are your foundation.** Build `SYS` modules for Time attributes, list properties
  and mappings *first* — most calculations will lean on them.
- **Name consistently.** Adopt a prefix convention (`DAT/INP/SYS/CAL/OUT`, `SYS01`, etc.) and a
  line-item naming style on day one. See [`templates/naming-conventions.md`](../../templates/naming-conventions.md).

## Formulas & calculations

- **Stepped line items beat mega-formulas.** Easier to audit, faster to recalc, reusable.
- **Map, don't `SELECT`.** Put the relationship in a System mapping module and use `LOOKUP`/`SUM`.
- **Booleans over `IF` for filtering.** A `Boolean` flag line item is cheap and reusable; nested
  `IF`s on large modules are not.
- **Calculate at the right level.** Don't compute at leaf level then aggregate if you can compute on
  a small summary — and vice versa. Match the calc to where the data lives.

## Performance

- **Watch cell count.** It's the product of every dimension's size × number of line items. The
  cheapest performance win is removing an unnecessary dimension.
- **Time Ranges and subsets** keep modules lean — apply them as soon as a module only needs part of
  the calendar or list. *(See [`docs/07-performance/`](../07-performance/).)*
- **Avoid text and `IF` on huge modules**; both are comparatively expensive.

## Delivery & collaboration

- **Build to the user story, not beyond it.** Necessary (the N in PLANS) applies to features too.
- **Demo early and often** (The Anaplan Way) — feedback on a working module beats a perfect spec.
- **Use ALM from the start** for anything heading to production: build in DEV, promote to PROD via
  revisions. *(See [`docs/06-security-alm/alm.md`](../06-security-alm/alm.md).)*
- **Document assumptions** in the model (a notes module or line-item descriptions), so the next
  builder — often future-you — understands intent.

## Where to keep learning

- **Anapedia** — the reference docs: https://help.anaplan.com/
- **Anaplan Community** — best-practice articles, the model-builder forums, and the Planual:
  https://community.anaplan.com/
- **Anaplan Academy** — the official Level 1/2/3 courses behind [`LEARNING-PATH.md`](../../LEARNING-PATH.md).

**Related:** [PLANS](plans-standard.md) · [DISCO](disco.md) · [The Planual](planual.md) · [model-build-checklist.md](model-build-checklist.md)

> Source: Anaplan Academy & Anaplan Community best-practice materials. See [`SOURCES.md`](../../SOURCES.md).
