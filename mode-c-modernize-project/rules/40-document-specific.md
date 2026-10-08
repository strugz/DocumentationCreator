# Rule 40 (Mode C) — Document-Specific Rules

> **Scope: Mode C only (modernize an existing project into a new one).** Mode A uses
> `mode-a-existing-project/rules/40-document-specific.md`; Mode B uses
> `mode-b-new-project/rules/40-document-specific.md`.

## Suite and generation order
| # | Document | Skill | Built from |
|---|----------|-------|------------|
| 00 | Modernization Brief | `/mod-brief` | Mode A Profile + modernization interview (tech stack, strategy, scope) |
| 01 | Current State Assessment | `/mod-assessment` | Mode A Profile and documents + source code |
| 02 | Target Requirements Specification | `/mod-requirements` | Brief + Assessment |
| 03 | Target System Design | `/mod-design` | Brief + Assessment + Requirements |
| 04 | Migration Plan | `/mod-plan` | Requirements + Design + Assessment |
| 05 | Modernization Proposal | `/mod-proposal` | Brief + Assessment + Requirements + Plan |
| 06 | Migration Test Plan | `/mod-test-plan` | Requirements + Design + Profile (parity) |

Later documents reuse earlier ones. Never contradict an earlier document. If a later
document reveals a problem, fix the earlier one first. If the problem is in the Mode A
profile, fix the profile, then the brief.

## 00. Modernization Brief
- It is the single source of truth for Mode C. It records three things, kept apart:
  **what exists** (copied from the profile), **what the user decided** (interview), and
  **what Claude proposes**.
- The interview is **one round**, at most about 12 questions, and always covers the
  **target tech stack** layer by layer (language, framework, database, UI, auth, hosting,
  CI/CD). For each layer record: current (from the profile), user preference, Proposed
  value if no preference, and the reason. A layer the user does not decide becomes a
  `[DECISION]` with Claude's recommendation.
- Record the **migration strategy** (big-bang rewrite / strangler fig / lift-and-shift
  then refactor / re-platform only) as a decision, with a recommendation based on the
  profile's maturity and status (a system in production favours incremental migration).
- The **Feature Disposition** table lists every `F-xx` from the profile with
  Keep / Improve / Replace / Drop / New, a priority, and a decision state. The user
  confirms dispositions; Claude's defaults are **Proposed**.
- Carry the profile's roles, data entities, integrations, and glossary into the brief so
  that later documents never need to open the profile for basic facts.
- Increase the brief version (`v1`, `v2`…) every time the user changes a decision.

## 01. Current State Assessment
- Audience: the tech lead and the sponsor. The reader must be able to say what is wrong
  with the current system, how severe it is, and what the modernization must fix.
- Every finding gets an ID (`D-01`…), a category (Technology / Architecture / Code quality /
  Security / Operations / Data / Process / Documentation), a severity (Critical / High /
  Medium / Low), evidence (`path:line` or `Profile §n`), and a consequence for the target
  system (what the modernization must do about it).
- Assess at least: stack currency (versions vs vendor support, `[VERIFY]` for dates),
  architecture fitness, test coverage and CI, security observations (Profile §16),
  operations (deployment, backup, monitoring), data model fitness, incomplete work
  (Profile §15), and documentation.
- Include a **Keep list**: what works well and should survive the modernization
  (patterns, data model parts, integrations). A modernization that discards good parts
  is a worse plan.
- Severity is a judgment; state the reasoning in one line. Never add numbers (outage
  counts, cost of downtime) that the evidence does not contain.

## 02. Target Requirements Specification
- Same discipline as Mode B §01 (atomic "shall", testable, IDs, priority, source,
  acceptance criteria), with two Mode C additions:
  - Every **Keep** and **Improve** feature produces at least one **parity requirement**
    whose acceptance criterion is "behaves as the current system does" with the current
    behaviour cited (`path:line` or Profile §7/§9). Parity requirements are Must unless
    the user says otherwise.
  - Every Critical and High assessment finding (`D-xx`) produces at least one requirement
    (functional or non-functional) that resolves it. The Source column names the `D-xx`.
- Include a **Data Migration** section: which entities move, which are transformed,
  which are archived, and how the migration is verified (counts, checksums, samples).
- Include an **Out of Scope** list that names every **Drop** feature with its reason.
- The Traceability Matrix has columns: Feature, Finding, Requirement, Design component,
  WBS item, Test case.

## 03. Target System Design
- Same content as Mode B §02 (architecture, stack, data model, API, screens, roles,
  security, deployment, repository structure, ADRs), plus:
  - A **Stack Comparison** table: layer, current technology and version (Profile §3),
    target technology and version, status (Agreed / Proposed), reason, and the ADR that
    records the choice. Every changed layer has an ADR. Every kept layer says why it stays.
  - A **Component Mapping** table: current module (Profile §6) → target component, with
    the disposition (Keep / Improve / Replace / Drop) and what changes.
  - A **Data Mapping** table: current entity or table (Profile §10) → target entity, with
    the transformation and whether existing data is migrated.
  - An **Interim Architecture** diagram when the migration strategy is incremental:
    how old and new run side by side, where the routing or facade sits, and which data
    is shared.
- Versions in the target stack are current LTS or stable releases labeled **Proposed**
  unless the user decided them. Mark end-of-support dates `[VERIFY]`.

## 04. Migration Plan
- Same discipline as Mode B §03 (WBS with IDs, definition of done, dependencies, size,
  priority; phases; risks; RACI; DoD), with these Mode C changes:
  - The **Starting Point** section records the current system's state (production or
    not, users, data volume `[TBD]` if unknown, freeze or no-freeze policy).
  - Default phases: Phase 0 Mobilize and Decide (`[DECISION]` items closed, environments)
    → Phase 1 Foundation (target skeleton, CI/CD, auth, data model) → Phase 2 Parity
    (Keep and Improve features, Must) → Phase 3 Resolve Findings and New Features
    (Should) → Phase 4 Data Migration Rehearsal and Testing → Phase 5 Cutover and
    Stabilization → Phase 6 Decommission and Handover.
  - For an incremental strategy, Phase 2 is split into **increments**, each naming the
    features that move and the routing change that exposes them.
  - A **Cutover Plan** with a go/no-go checklist, a parallel-run or freeze window
    (`[TBD]` dates), a verification step, and a **rollback plan** that names the trigger
    and the steps back to the current system.
  - A **Decommission** checklist for the current system (data archive, DNS, licences,
    repositories, documentation).
- Timelines come only from user dates or stated capacity; otherwise relative phases
  marked `[ASSUMPTION]`.

## 05. Modernization Proposal
- Same structure as Mode B §04 (problem → solution → scope → approach → timeline →
  resources and cost → risks → benefits → recommendation), with the proposal type
  **Modernization proposal**.
- The **Problem Statement** is built from the assessment's Critical and High findings,
  stated for a non-technical reader, each with its business consequence. Do not quote
  numbers the evidence does not contain.
- Include an **Options Considered** table: Do nothing / Upgrade in place / Partial
  modernization / Full rebuild, each with what it addresses and what it does not. Mark
  the recommended option and tie it to the brief's migration strategy decision.
- Features are tagged with their disposition (Keep / Improve / Replace / New). Dropped
  features appear under Scope → Out of Scope with the reason.
- Cost: a line-item structure that includes **decommissioning** and **parallel-run**
  costs. Amounts are `[TBD]` unless the user supplied rates.

## 06. Migration Test Plan
- Same discipline as Mode B §05 (levels, environments, data, entry and exit criteria,
  defect severity, UAT sign-off), plus three Mode C test groups:
  - **Parity tests** (`TC-P-xx`): one per Keep and Improve feature, traced to its parity
    `FR` and to the current behaviour (Profile §7/§9). The expected result is the current
    system's result unless the feature is Improve, in which case the changed behaviour
    is stated.
  - **Data migration tests** (`TC-D-xx`): record counts, referential integrity, spot
    checks, and a rehearsal on a copy of production data (anonymized if it contains
    personal data).
  - **Cutover and rollback tests** (`TC-C-xx`): the go/no-go checks and a rollback
    rehearsal.
- Every Must and Should requirement has at least one test case. Every test case traces
  to an `FR`/`NFR` ID.
- UAT scenarios compare old and new side by side where the strategy allows it.

## After the build
When code for the target system exists, run the Mode A skills on it (`/doc-suite
<new-code-path>`) for the final manuals. To compare the plan against the build, run
`/new-gap-check` with the Mode C slug; it reads the Mode C requirements when no Mode B
folder exists for that slug.
