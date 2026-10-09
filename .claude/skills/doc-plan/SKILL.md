---
name: doc-plan
description: MODE A (existing code). Write the Project Completion Plan ("planning to finish") for a fed-in project. It assesses current state from code evidence, then gives a work breakdown, milestones, risks, QA, go-live, and handover. Use when the user asks for a project plan, completion plan, roadmap to finish, remaining work, or "how do we finish this project".
argument-hint: <project-slug or path> [deadline / team / constraints]
---

# Project Completion Plan

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (project slug or path, plus any context such as deadline, team size,
or sprint length).

## Preconditions
1. Resolve `<slug>`. If `output/mode-a/<slug>/00-project-profile.md` is missing, run the
   `doc-intake` procedure first (`.claude/skills/doc-intake/SKILL.md`).
2. Read the profile, `mode-a-existing-project/templates/01-project-completion-plan.md`, and
   `mode-a-existing-project/rules/40-document-specific.md` section 1, and
   `rules/45-estimation-and-release-gate.md` (not preloaded).
3. Merge any context the user gave in `$ARGUMENTS` or in chat into the profile section 2 first.

## Procedure
1. **Current state:** build section 3.2 from the profile's Features Inventory. Re-open the
   evidence for any feature marked Partial or Broken. Note exactly what is missing
   (e.g. "form exists, `onSubmit` is empty at `src/pages/Order.tsx:88`").
2. **Completion %:** compute it as `(Done + 0.5 × Partial) / total in-scope features`.
   State the formula in the table.
3. **Gaps → WBS:** turn every Partial / Not started / Broken feature, every significant
   TODO/FIXME, missing tests, missing CI, security gaps, and documentation gaps into WBS
   items. Group them by phase:
   - Phase 1 Stabilize: broken items, blockers, build and CI fixes.
   - Phase 2 Complete core features: Must items.
   - Phase 3 Hardening and QA: tests, security, performance, Should items.
   - Phase 4 Deployment and Handover: environments, go-live, docs, training.
4. **Sizing:** use the fixed sizes of Rule 45 section 1 (S = 1, M = 3, L = 5, XL = 10
   person-days), for remaining work only. Apply the AI-assisted factor (Rule 45 section 2)
   only when Profile section 2 says the team uses AI-assisted coding.
5. **Timeline:** compute capacity and duration as Rule 45 section 3 describes, and fill
   section 8 with its method table. Use dates only if the user gave a start date or
   deadline and the team size. Otherwise use relative durations in the Gantt chart and
   mark them `[ASSUMPTION]`.
   If the user's deadline is shorter than the estimate, say so plainly in the Executive
   Summary and propose scope cuts (Could → Won't).
6. **Release gate:** write the Rule 45 section 5 gate with the testers from Profile
   section 2, and use it in the release milestone, the Go-Live Checklist, and the
   Definition of Done.
7. **Risks:** derive them from evidence (single points of failure, no tests, outdated
   dependencies, unclear requirements, missing environments) plus timeline risk.
8. Fill every remaining template section. Use `[TBD]` for names, owners, and costs.

## Output
`output/mode-a/<slug>/01-project-completion-plan.md`

Run the `rules/50-review-checklist.md` checks. Then report the file path, the headline
(completion %, number of WBS items, estimated phases), and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-a/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
