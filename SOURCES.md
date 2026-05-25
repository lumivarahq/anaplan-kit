# Sources & Validation

Content in this kit was validated against Anaplan's official documentation (**Anapedia**,
`help.anaplan.com`) and Anaplan's published best-practice materials. Anaplan is a SaaS platform
and its UI/behaviour change over time, so **always confirm against the live docs for your
platform version.** Where a specific Planual rule number could not be confirmed online, the rule is
stated by its PLANS principle and labelled as paraphrased rather than presented as an exact quote.

## How functions were validated

Anapedia blocks automated page fetches (HTTP 403), but its content is reachable via web search.
Each function reference page in [`docs/02-formulas/`](docs/02-formulas/) was cross-checked against
the Anapedia page for that function, and the per-function source URL is listed there.

## Key reference URLs

### Function reference (Anapedia)

- All functions index — https://help.anaplan.com/all-functions-160769b0-de37-4f08-87a0-cc3aa55525a3
- Formula usage tips — https://help.anaplan.com/formula-usage-tips-89bd50bd-dbbf-4465-b085-36163aa74450
- LOOKUP — https://help.anaplan.com/lookup-f8baa402-606d-4764-a349-d8003fa383be
- LOOKUP examples — https://help.anaplan.com/lookup-examples-18ec86e1-8e21-4d7b-a207-cf378a001d1d
- SELECT — https://help.anaplan.com/select-2ca3148d-466e-44bd-830e-7e5cf3ac8d08
- FINDITEM — https://help.anaplan.com/finditem-0668e215-a0d2-4ad1-b93f-3c2a56a9f5c2
- CUMULATE — https://help.anaplan.com/cumulate-1173a903-81bb-4838-a4d0-1c9f9c739aa3
- LAG — https://help.anaplan.com/lag-3064919f-964e-4b84-be56-15f0e127e371
- OFFSET — https://help.anaplan.com/offset-4f5a095c-0e7a-4f1a-b6ea-0ef8f88d6c3f
- YEARVALUE — https://help.anaplan.com/yearvalue-5df8cf5a-6609-4e14-832f-ddff9b29326b
- HALFYEARVALUE — https://help.anaplan.com/halfyearvalue-d78dd47b-5f5c-4e06-9788-7b1de7446b29
- QUARTERVALUE — https://help.anaplan.com/quartervalue-496d28ac-cf36-43bf-bc0e-06d4cc52c40e
- MONTHVALUE — https://help.anaplan.com/monthvalue-0f2e55c3-8808-4b37-9017-7ea57e6f0d37
- RANK — https://help.anaplan.com/rank-a5f5778e-5e88-48ad-96ad-715178cda9b2
- RANKCUMULATE — https://help.anaplan.com/1af75839-f426-43bf-b864-9027f1770161
- ITEM — https://help.anaplan.com/item-41298b7a-e877-40e8-8cfa-8d7009d8686f
- PARENT — https://help.anaplan.com/parent-1cdc486d-c4d7-42db-8b1a-d9e12c060999
- ISANCESTOR — https://help.anaplan.com/isancestor-2c35cf1b-9392-4726-8ebb-4291d1b24225
- ITEMLEVEL — https://help.anaplan.com/itemlevel-756d1428-5f1d-4d79-8274-d075a1bd312f
- FIND — https://help.anaplan.com/find-b4571668-130a-4de8-a7b2-57439714f344
- CURRENTPERIODSTART — https://help.anaplan.com/currentperiodstart-a7af7113-e1dc-478d-bbbe-ecb597092991
- START — https://help.anaplan.com/start-bc44fa0b-7af8-4a8f-ad8f-cbeaccf22003

> Note: `ANCESTOR` and `CHILDREN` are **not** Anaplan model formula functions (they exist only in
> Anaplan XL's MDX). For a higher ancestor level, chain `PARENT(PARENT(...))` or use a System
> mapping module; to aggregate children, use the Sum summary method or `SUM` with a mapping.

### Methodology & best practices

- Anapedia home — https://help.anaplan.com/
- The Planual (Anaplan's model-building rulebook) — published by Anaplan; see https://help.anaplan.com/ and the Anaplan Community.
- Anaplan Community / Academy best practices — https://community.anaplan.com/
- PLANS modeling standard & DISCO — Anaplan best-practice materials (Academy / Community).

### Calculation engines, performance diagnostics & ALM (field guide)

- Anaplan calculation engines (Classic vs Polaris) — https://help.anaplan.com/anaplan-calculation-engines-06c06ade-2807-4f3d-9a6e-d69ae0e257e5
- Polaris calculation engine — https://help.anaplan.com/polaris-calculation-engine-8b466778-42b2-4e35-b318-e5e4128b63b7
- Understand sparsity and density — https://help.anaplan.com/understand-sparsity-and-density-616ee341-8a5f-4718-8c90-c82e34eca86c
- How ALM supports the development lifecycle — https://help.anaplan.com/how-application-lifecycle-management-supports-the-development-lifecycle-aa369576-4135-4a3e-8636-1a942c28feaa
- Work with revision tags — https://help.anaplan.com/work-with-revision-tags-d9c92d0c-9b5b-4428-8c81-d023a0fe2d1c
- Considerations when you enable Deployed mode — https://help.anaplan.com/considerations-when-you-enable-deployed-mode-5dea12f4-57c4-4b57-a2cb-97bdfe5d007e
- Optimize time calculation performance — https://help.anaplan.com/5ebdaed1-bc59-45a8-a1f4-33f0c97518d7
- OEG Best Practice: Anaplan Performance Triangle (Community) — https://community.anaplan.com/discussion/140709/oeg-best-practice-anaplan-performance-triangle

### REST API & integration

- Anaplan REST API & integration docs — https://help.anaplan.com/ (Data Integrations section)
- Anaplan Connect — https://help.anaplan.com/ (Anaplan Connect section)
- CloudWorks — https://help.anaplan.com/ (CloudWorks section)

> If you spot anything out of date, check the live Anapedia page (linked above) — that is the source of truth.
