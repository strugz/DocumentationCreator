# Rule 40 (Mode B) — Document-Specific Rules

> **Scope: Mode B only (new project, no code yet).** Mode A uses
> `mode-a-existing-project/rules/40-document-specific.md`.

## Suite and generation order
| # | Document | Skill | Built from |
|---|----------|-------|------------|
| 00 | Project Brief | `/new-brief` | User idea + interview |
| 01 | Requirements Specification | `/new-requirements` | Brief |
| 02 | System Design | `/new-design` | Brief + Requirements |
| 03 | Project Plan | `/new-plan` | Requirements + Design |
| 04 | Project Proposal | `/new-proposal` | Brief + Requirements + Plan |
| 05 | Test Plan | `/new-test-plan` | Requirements + Design |
| 06–08 | Draft User / Technical / Developer Manuals | `/new-manuals` | Requirements + Design |
| 09 | Gap Report (after code exists) | `/new-gap-check` | Mode B Requirements + Mode A Profile |

Later documents reuse earlier ones. Never contradict an earlier document. If a later
document reveals a problem, fix the earlier one first.

## 00. Project Brief
- It is the single source of truth for Mode B (like the Project Profile in Mode A).
- Record the user's words faithfully. Separate **what the user said** from **what Claude
  proposes**. Put proposals only in the "Proposed" column or section.
- Every feature gets an ID (`F-xx`), a MoSCoW priority, and a decision state.
- The interview asks all questions in **one round**. A second round is allowed only for
  blocking answers (product purpose, main users, core features).
- Increase the brief version (`v1`, `v2`…) every time the user changes a fact.

## 01. Requirements Specification
- Structure follows IEEE 29148 / SRS practice in a lighter form: purpose, scope,
  users, functional requirements, non-functional requirements, data, interfaces,
  constraints, acceptance, traceability.
- Every requirement is **atomic** (one "shall" per row), **testable**, and has an ID,
  priority, source (`F-xx` / `Brief §n`), and acceptance criteria.
- Write important flows as **user stories** ("As a <role>, I want <goal>, so that
  <benefit>") with **Given / When / Then** acceptance criteria.
- Non-functional requirements cover at least: performance, availability, security,
  privacy, usability and accessibility, compatibility, maintainability, backup, and
  logging. Numeric targets are **Proposed** unless the user gave them.
- Include an explicit **Out of Scope** list.

## 02. System Design
- Audience: the developers who will build it. Every design decision states its **reason**.
- Must cover: architecture style and diagram, components and responsibilities, tech stack
  with versions (all **Proposed** unless decided), data model (Mermaid `erDiagram`), API
  design (endpoint list), screen inventory and navigation map, roles and permission
  matrix, integrations, security design, deployment architecture and environments,
  proposed repository structure, and Architecture Decision Records (ADRs) for the major
  choices.
- Map every component and screen to the `FR` IDs it implements.
- Keep it buildable: prefer mainstream, well-supported technologies the team can hire for.
  If the user named a stack, use it.

## 03. Project Plan (build from zero)
- Same discipline as the Mode A Completion Plan, but there is no current state to assess.
  Replace it with a **Starting Point** section (team, tools, environments, approvals
  that must exist before work starts).
- WBS items are derived from the Design's components and the Requirements' `FR` IDs.
  Each has an ID, description, definition of done, dependencies, size (S/M/L/XL), and
  MoSCoW priority.
- Default phases: Phase 0 Mobilize and Setup → Phase 1 Foundation (auth, data model,
  CI/CD, skeleton) → Phase 2 Core Features (Must) → Phase 3 Additional Features (Should)
  → Phase 4 Testing and UAT → Phase 5 Deployment, Training, and Handover.
- Timelines come only from user dates or capacity; otherwise relative phases marked
  `[ASSUMPTION]`. If the deadline is shorter than the estimate, say so plainly and
  propose scope cuts.
- Always include risks, a Definition of Done, a quality plan (link the Test Plan), a
  go-live plan, and a handover checklist.

## 04. Project Proposal
- Same structure and rules as Mode A §2 (problem → solution → scope → approach →
  timeline → resources and cost → risks → benefits → recommendation).
- The proposal type is always **New system proposal**.
- All features are tagged **Planned**. Scope must equal the Requirements' in-scope list
  and the Plan's WBS.
- Cost: give a line-item structure. Amounts are `[TBD]` unless the user supplied rates.
  An effort estimate is allowed when it shows its method (from the Plan).

## 05. Test Plan
- Every Must and Should requirement has at least one test case. Every test case traces
  to an `FR`/`NFR` ID.
- Cover test levels (unit, integration, system, UAT, performance, security), environments,
  test data, entry and exit criteria, defect severity definitions, and the UAT sign-off.
- UAT scenarios are written in business language for the client's users.

## 06–08. Draft Manuals
- Use the Mode A templates (`mode-a-existing-project/templates/03`, `04`, `05`) so the
  final manuals keep the same structure once the system is built.
- Add the "planned system" banner (see Rule 30) under the Document Control block and set
  Status to **Draft — Pre-development**.
- User Manual: tasks come from the user stories; screen and button names come from the
  Design's screen inventory and are marked `[VERIFY: final label]`.
- Technical Manual: requirements, architecture, environments, and the proposed
  configuration keys from the Design. Exact install commands are `[TBD]` until the build
  exists.
- Developer Manual: stack, proposed repo structure, coding standards to adopt (labeled
  **Proposed**), branching and CI/CD plan. Use `Not applicable — code not yet written`
  for sections that need real code (e.g. module-by-module guide).

## 09. Gap Report
- Run only when code exists and a Mode A profile has been produced for it.
- For each `FR`/`NFR`: Implemented / Partial / Missing / Changed, with Mode A evidence
  (`path:line`). Also list features built that were **not** in the requirements.
