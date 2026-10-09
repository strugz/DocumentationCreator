---
name: new-plan
description: MODE B (new project, no code yet). Write the Project Plan for building a new system from zero, covering the starting point, WBS, phases, Gantt timeline, team and RACI, effort estimate, risks, QA, go-live, training, and handover. Use when the user asks for a project plan, build plan, implementation plan, roadmap, or schedule for a system that is not built yet.
argument-hint: <project-slug> [start date / deadline / team / sprint length]
---

# Project Plan (new build)

> **Mode B — New project.** For a project that already has code, use the Mode A
> `/doc-plan` (Completion Plan) instead.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (slug, plus optional start date, deadline, team size, sprint length).

## Preconditions
1. Resolve `<slug>`. Requires the brief and `01-requirements-specification.md`. Run the
   missing procedures first. If `02-system-design.md` is missing, run `new-design` first,
   because the WBS is built from its components.
2. Read the brief, requirements, design, `mode-b-new-project/templates/03-project-plan.md`,
   `mode-b-new-project/rules/40-document-specific.md` section 03, and
   `rules/45-estimation-and-release-gate.md` (not preloaded).
3. Merge any new context from `$ARGUMENTS` or chat into the brief section 3 first (increase the
   brief version).

## Procedure
1. **Starting point:** list what must exist before development begins: signed-off
   requirements, resolved `[DECISION]` items, team, repository, environments, and access
   to integrations.
2. **WBS:** build it from the design and requirements:
   - Phase 0 Mobilize and Setup: repo, CI/CD, environments, project tools, kickoff.
   - Phase 1 Foundation: project skeleton, authentication and roles, data model and
     migrations, base layout and navigation, logging.
   - Phase 2 Core Features: one or more items per Must feature, each listing its `FR` IDs.
   - Phase 3 Additional Features: Should items (Could items are listed as optional).
   - Phase 4 Testing and UAT: test automation, performance and security testing, UAT
     rounds, and bug fixing (link the Test Plan).
   - Phase 5 Deployment, Training, and Handover: production setup, data migration, go-live,
     final manuals, training, and the support period.
   Every item has an ID, a Definition of Done, dependencies, a size, and a MoSCoW priority.
3. **Sizing:** use the fixed sizes of Rule 45 section 1 (S = 1, M = 3, L = 5, XL = 10
   person-days). Apply the AI-assisted factor (Rule 45 section 2) only when Brief section 3
   says the team uses AI-assisted coding, and then show both totals.
4. **Timeline:** compute capacity and duration as Rule 45 section 3 describes, and fill
   section 8 with its method table. Use real dates only if the user gave a start date or
   deadline plus the team size; otherwise use relative durations marked `[ASSUMPTION]`.
   If the deadline is shorter than the estimate, say so plainly in the Executive Summary
   and name the Should and Could items that move out of the first release.
5. **Release gate:** write the Rule 45 section 5 gate with the testers from Brief section 3.
   Name the release milestone "Release 1.0 tested and ready to deploy" (with a pilot,
   "<Site> pilot live" first), and use the gate in the Go-Live Checklist and the
   Definition of Done. Client rollouts that depend on a later agreement are described,
   not scheduled.
6. **Team and RACI:** list the roles the work needs (project manager, developers, QA,
   designer, client product owner). Names are `[TBD]` unless given.
7. **Risks:** cover unclear requirements, unresolved decisions, integration access, team
   availability, scope creep, data migration quality, user adoption, and the timeline.
8. **Traceability:** fill the "WBS item" column of the Requirements' Traceability Matrix
   and note it in that document's Revision History.
9. Fill every remaining template section. Use `[TBD]` for names, owners, and costs.

## Output
`output/mode-b/<slug>/03-project-plan.md`

Run the review checklist. Report the file path, the headline (WBS item count, estimated
effort with method, duration, phases), the scope-versus-deadline verdict, and the Open
Items.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
