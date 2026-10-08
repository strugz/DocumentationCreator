---
name: mod-plan
description: MODE C (modernize an existing project). Write the Migration Plan for rebuilding an existing system on a new stack, with starting point, migration strategy and increments, WBS, phases from foundation through parity, data migration rehearsal, cutover with rollback, and decommission of the current system. Use when the user asks for a migration plan, modernization roadmap, cutover plan, rewrite schedule, or "how do we move from the old system to the new one".
argument-hint: <project-slug> [start date / cutover deadline / team size]
---

# Migration Plan

> **Mode C — Modernize an existing project.** For a brand-new system use the Mode B
> `/new-plan` skill; for finishing the existing system as it is, use the Mode A `/doc-plan`.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (slug, plus optional dates, deadline, and team size, which are
recorded in the brief §4 first).

## Preconditions
1. Resolve `<slug>`. The brief, assessment, and requirements must exist. If
   `03-target-system-design.md` is missing, run the `mod-design` procedure first.
2. Read the brief (§4, §6, §8, §9), the assessment, the requirements, the design,
   `mode-c-modernize-project/templates/04-migration-plan.md`, and
   `mode-c-modernize-project/rules/40-document-specific.md` §04.

## Procedure
1. **Starting point:** the current system's state (production or not, freeze policy,
   users and data volume `[TBD]` if unknown), open `[DECISION]` items, team, tools, and
   environments that must exist before work starts.
2. **Strategy and increments:** restate the brief's migration strategy. For an
   incremental strategy, define the increments: which features (`F-xx`) move in each,
   the routing change that exposes them, and the exit criteria. Order them so that
   low-risk, self-contained features go first and shared data stays consistent.
3. **Scope:** in-scope features with disposition and requirements (must equal the
   requirements' in-scope list); Drop features under out of scope.
4. **WBS:** derive items from the design's components and the requirements' `FR` IDs.
   Each has an ID, definition of done, dependencies, size (S/M/L/XL), and priority.
   Include items for data migration tooling, parity test automation, the interim router
   or facade (if incremental), cutover rehearsal, and decommission.
5. **Phases:** use the Rule 40 §04 default phases unless the strategy demands otherwise.
   Timelines come from the user's dates or stated capacity; otherwise relative durations
   marked `[ASSUMPTION]`. If the cutover deadline is shorter than the estimate, say so
   and propose scope cuts (Should features first).
6. **Team, RACI, estimate:** estimates only with the method shown (WBS size × capacity);
   otherwise `[TBD]` amounts. Include parallel-run and decommissioning lines.
7. **Risks:** at least the migration-specific ones: data loss or mismatch, feature
   regressions missed by parity tests, dual maintenance during parallel run, user
   resistance, vendor or hosting delays, and the assessment's Critical findings.
8. **Data migration, cutover, rollback, decommission:** fill §12–§14 of the template.
   The rollback plan names the trigger, the steps back to the current system, the owner,
   and a time limit (`[TBD]` if unknown).
9. **Traceability:** fill the "WBS item" column of the Target Requirements
   Specification's Traceability Matrix. This is the only edit to that document. Note it
   in its Revision History.

## Output
`output/mode-c/<slug>/04-migration-plan.md` (plus the traceability update in `02`)

Run the review checklist. Report the file path, the strategy and number of increments,
the WBS item count by phase, the estimate (with method) or `[TBD]`, the top risks, and
the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
