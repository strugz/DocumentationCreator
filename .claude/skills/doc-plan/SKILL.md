---
name: doc-plan
description: MODE A (existing code). Write the Project Completion Plan ("planning to finish") for a fed-in project. It assesses current state from code evidence, then gives a work breakdown, milestones, risks, QA, go-live, and handover. Use when the user asks for a project plan, completion plan, roadmap to finish, remaining work, or "how do we finish this project".
argument-hint: <project-slug or path> [deadline / team / constraints]
---

# Project Completion Plan

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

Input: `$ARGUMENTS` (project slug or path, plus any context such as deadline, team size,
or sprint length).

## Preconditions
1. Resolve `<slug>`. If `output/mode-a/<slug>/00-project-profile.md` is missing, run the
   `doc-intake` procedure first (`.claude/skills/doc-intake/SKILL.md`).
2. Read the profile, `mode-a-existing-project/templates/01-project-completion-plan.md`, and
   `mode-a-existing-project/rules/40-document-specific.md` §1.
3. Merge any context the user gave in `$ARGUMENTS` or in chat into the profile §2 first.

## Procedure
1. **Current state:** build §3.2 from the profile's Features Inventory. Re-open the
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
4. **Sizing:** S ≈ ≤1 day, M ≈ 2–3 days, L ≈ 1 week, XL ≈ more than 1 week (split XL items
   if possible). Label these as estimates.
5. **Timeline:** use dates only if the user gave a start date or deadline and capacity.
   Otherwise use relative durations in the Gantt chart and mark them `[ASSUMPTION]`.
   If the user's deadline is shorter than the estimate, say so plainly in the Executive
   Summary and propose scope cuts (Could → Won't).
6. **Risks:** derive them from evidence (single points of failure, no tests, outdated
   dependencies, unclear requirements, missing environments) plus timeline risk.
7. Fill every remaining template section. Use `[TBD]` for names, owners, and costs.

## Output
`output/mode-a/<slug>/01-project-completion-plan.md`

Run the `rules/50-review-checklist.md` checks. Then report the file path, the headline
(completion %, number of WBS items, estimated phases), and the Open Items.
