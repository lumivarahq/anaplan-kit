# User-Story Template (copy-paste)

> **Level:** L2 · **Area:** Templates · Part of **The Anaplan Way**

In **The Anaplan Way** (Anaplan's delivery methodology), requirements are captured as **user
stories** with **acceptance criteria** — small, testable slices of value. A model builder turns each
story into modules, line items and formulas. Capturing the story *before* building keeps you on
scope and gives you a clear "done" test.

Copy the block below into your backlog tool or ticket and fill the `[…]` placeholders.

---

## The template

```markdown
### Story: [short title]

**As a** [role — e.g. FP&A analyst]
**I want** [capability — e.g. to plan revenue by product and entity per month]
**so that** [business value — e.g. I can build a bottom-up annual budget].

**Context / background**
[1-3 sentences: why now, what's the current pain, any source systems involved.]

**Acceptance criteria** (Given / When / Then — each must be testable)
- [ ] Given [precondition], when [action], then [expected result].
- [ ] Given [precondition], when [action], then [expected result].
- [ ] Given [edge case — blanks / new member / year rollover], when [action], then [expected result].

**DISCO sketch** (where will this live?)
| Module (PREFIX##) | DISCO type | Why |
| --- | --- | --- |
| [INP## …] | Inputs | [what users type] |
| [CAL## …] | Calculations | [what's computed] |
| [OUT## …] | Outputs | [what's reported] |

**PLANS considerations**
- Performance: [dimensionality / time range concern]
- Sustainable: [no hard-coded dates? new members handled?]

**Out of scope**
- [explicitly list what this story does NOT cover, to prevent scope creep]

**Estimate:** [S / M / L]   **Depends on:** [other stories / data feeds]
```

---

## Worked example

```markdown
### Story: Plan revenue from volume and price

**As an** FP&A analyst
**I want** to enter monthly volume and price per product and entity
**so that** revenue is calculated automatically and rolls into the P&L.

**Context / background**
Today revenue is planned in a spreadsheet with no audit trail. We want a driver-based plan in
Anaplan so a change in volume ripples to EBITDA instantly.

**Acceptance criteria**
- [ ] Given a product/entity/month, when I enter Volume and Price, then Gross Revenue = Volume × Price.
- [ ] Given I change a Volume, when I view the P&L page, then Revenue and EBITDA update without a manual step.
- [ ] Given Price is left blank, when revenue calculates, then Gross Revenue is 0 (not an error).
- [ ] Given a new product is added to the list, when I open the input grid, then it appears with no formula change.

**DISCO sketch**
| Module | DISCO type | Why |
| --- | --- | --- |
| INP01 Revenue Assumptions | Inputs | analyst types Volume & Price |
| CAL01 Revenue | Calculations | Gross Revenue (local) = Volume × Price |
| OUT01 P&L Statement | Outputs | report card on the UX page |

**PLANS considerations**
- Performance: INP01 dimensioned only by L3 Cost Centre × L2 Product × Time × Versions; apply an FY26 Time Range.
- Sustainable: no period named in any formula; new products inherit structure automatically.

**Out of scope**
- Currency conversion (separate story).
- Loading actuals (separate story).

**Estimate:** M   **Depends on:** Lists & Time configured; SYS01 Time Settings built.
```

---

## Tips

- **One slice of value per story.** "Plan revenue" and "load actuals" are two stories, not one.
- **Acceptance criteria must be testable** — phrase as Given/When/Then so you (or QA) can verify in
  the model. Always include at least one **edge case** (blanks, new member, year rollover).
- The **DISCO sketch** forces you to decide where logic lives before you build — pair it with the
  [blueprint template](blueprint-template.md).
- At "done," run the [model-build checklist](model-build-checklist.md) against the story.

---

**Related:** [The Anaplan Way / methodology](../docs/03-methodology/) ·
[PLANS](../docs/03-methodology/plans-standard.md) · [DISCO](../docs/03-methodology/disco.md) ·
[Blueprint template](blueprint-template.md) · [Model-build checklist](model-build-checklist.md) ·
[Capstone exercise](../exercises/capstone-l3.md)
