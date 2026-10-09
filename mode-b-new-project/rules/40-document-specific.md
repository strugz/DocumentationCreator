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
| 10 | Build repository starter kit (not a document) | `/new-suite` Step 4b | The finished suite |

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
- Section 2.2 holds the pain points in the users' own words; the proposal and plan state
  problems from it. Section 3 records approvers, testers, rollout, naming, and
  deliverables. Section 16.1 Words to Avoid is binding for every document (Rule 10).

## 01. Requirements Specification
- Structure follows IEEE 29148 / SRS practice in a lighter form: purpose, scope,
  users, functional requirements, non-functional requirements, data, interfaces,
  constraints, acceptance, traceability.
- Every requirement is **atomic** (one "shall" per row), **testable**, and has an ID,
  priority, source (`F-xx` / `Brief section n`), and acceptance criteria.
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
- Estimate and gate with `rules/45-estimation-and-release-gate.md`: fixed sizes, the
  AI-assisted factor when the brief says so, capacity, and one ready-to-deploy gate that
  the Test Plan and the Proposal repeat word for word.

## 04. Project Proposal
- Same structure and rules as Mode A section 2 (problem → solution → scope → approach →
  timeline → resources and cost → risks → benefits → recommendation).
- The proposal type is always **New system proposal**.
- All features are tagged **Planned**. Scope must equal the Requirements' in-scope list
  and the Plan's WBS.
- Cost: give a line-item structure. Amounts are `[TBD]` unless the user supplied rates.
  An effort estimate is allowed when it shows its method (from the Plan).
- PowerPoint slides of the proposal, when requested, follow `rules/60-proposal-slides.md`
  and carry exactly the proposal's facts and markers.

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

## 10. Build repository starter kit
Written last, by `/new-suite`, when Brief section 3 Deliverables lists it (or with
`--only starter`). It prepares the new code repository so the build starts with the
agreed decisions. It contains **no application code**.

- **Location:** `output/mode-b/<slug>/<repo-name>-repo-starter/`, inside the project's
  folder so the suite and its kit stay together. `tools/lint_docs.py` and the lint hook skip
  every `*-repo-starter` folder, because the kit is not a suite document. `<repo-name>`
  comes from Design section 14 Proposed Repository Structure, or is the slug.
- **Source:** the finished suite only. Every rule file cites the design section,
  requirement, or ADR it comes from. Examples use real IDs from the suite; check that a
  cited test case really covers the cited requirement.
- **Undecided layers:** write a stack-specific rule file only for a layer that is Agreed
  or **Proposed** in Design section 3. For a `[DECISION]` layer, write the file with the
  open decision at the top and only the stack-neutral rules below it.
- **Tense:** the kit describes the system the team will build. Planned commands are
  marked "planned" until the build exists.

| File | Content, from the suite |
|------|-------------------------|
| `CLAUDE.md` | The product; a table of the design documents and what each gives a developer; the stack (Agreed or Proposed); the repository layout (Design section 14); planned build and test commands; `@rules/...` imports; the skills and plugins table (`/feature-dev` included, see below); a working agreement (start from a requirement ID, layer order, tests with every change, no secrets or personal names, small reviewed changes) |
| `README.md` | For people: what the product does, how it is built, layout, prerequisites, planned commands (one per code block), how to use the skills and the `/feature-dev` plugin, how the team works, links to `docs/design/` |
| `.claude/settings.json` | Enables the `feature-dev` plugin for everyone who opens the repository (block below) |
| `rules/00-project-principles.md` | Goals (`G-xx`), the users and roles (`R-xx`), the ready-to-deploy gate (Rule 45 section 5), glossary terms, Words to Avoid, roles instead of names |
| `rules/10-architecture.md` | Parts and layer dependencies (Design section 2), fixed ADRs (section 15), how to add an ADR |
| `rules/20-backend-<language>.md`, `rules/30-frontend-<framework>.md` | API conventions, errors, logging (Design sections 5 and 11); screens and navigation (section 6) |
| `rules/40-database.md` | Data model, migrations, backups, test data (Design section 4; synthetic data only) |
| `rules/50-security.md` | Design section 10 and every security NFR as a "never" rule |
| `rules/60-testing.md` | Test levels and tools from the Test Plan, test names with `FR` and `TC` IDs, the Definition of Done |
| `rules/70-<integration>.md` | Only when Design section 8 has an integration: the riskiest one and how it is tested and released |
| `rules/80-git-and-traceability.md` | Branches, commits, and PRs with requirement IDs; `docs/traceability.md` from the Traceability Matrix; new ADRs |
| `.claude/skills/<name>/SKILL.md` | `implement-requirement`, `add-api-endpoint`, `add-<ui>-screen`, `add-<db>-migration`, `write-tests`, `review-change`, `release-readiness` (and `new-<integration>` when section 8 has one); each reads the design and test plan first, builds in layer order, adds tests, and reports |
| `.gitignore`, `docs/adr/README.md` | Stack ignores including local secrets; an ADR template numbered after the design's last ADR |
| `docs/design/` | A copy of the suite's Markdown files and INDEX, unchanged |

### Plugins: `/feature-dev`
The kit enables the `feature-dev` plugin from the official Claude Code plugin marketplace.
`/feature-dev` guides one feature at a time: explore the code, ask clarifying questions,
compare architecture options, implement after approval, then review. Write
`.claude/settings.json` exactly as follows:

```json
{
  "extraKnownMarketplaces": {
    "claude-plugins-official": {
      "source": { "source": "github", "repo": "anthropics/claude-plugins-official" }
    }
  },
  "enabledPlugins": {
    "feature-dev@claude-plugins-official": true
  }
}
```

Claude Code asks each developer to trust the marketplace and install the plugin the first
time they open the repository. In the kit's `CLAUDE.md` and `README.md`, state when to use
each tool:

| Use | When |
|-----|------|
| `/feature-dev <FR-xx …> <short goal>` | A feature that spans several layers or needs an architecture choice. Name the requirement IDs and point it to the design sections in `docs/design/`, because its exploration reads only the code. |
| `implement-requirement` and the other kit skills | A focused change that follows a pattern already in the design (one endpoint, one screen, one migration) |
| `review-change`, `release-readiness` | Before every merge and every release, also after `/feature-dev` |

Add this to the working agreement: a `/feature-dev` run starts from a requirement ID,
follows the `rules/` files over its own proposals, and records any new architecture choice
as an ADR in `docs/adr/`.

Zip the folder when the user wants one file to copy. After any later change to the suite
(Rule 55), refresh `docs/design/` and every rule file that cites a changed section.
