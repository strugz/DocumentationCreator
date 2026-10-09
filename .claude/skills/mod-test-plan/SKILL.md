---
name: mod-test-plan
description: MODE C (modernize an existing project). Write the Migration Test Plan for a modernized system, covering functional tests per requirement, parity tests against the current system for every kept feature, data migration tests, cutover and rollback rehearsals, non-functional tests, UAT with side-by-side comparison, defect severity, coverage, and sign-off. Use when the user asks for a test plan, regression plan, parity testing, migration verification, or UAT plan for a rebuilt system.
argument-hint: <project-slug>
---

# Migration Test Plan

> **Mode C — Modernize an existing project.** For a brand-new system use the Mode B
> `/new-test-plan` skill.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

> **Also read** `mode-c-modernize-project/rules/50-readability-and-refinement.md`, and
> follow the brief section 4 answers on rollout, testers, release gate, names and wording.

Input: `$ARGUMENTS` (slug).

## Preconditions
1. Resolve `<slug>`. The brief and requirements must exist. If
   `03-target-system-design.md` is missing, run the `mod-design` procedure first. Read
   `04-migration-plan.md` if it exists (phases, cutover, rollback).
2. Read the brief (section 6 dispositions), the requirements, the design, the plan, the Mode A
   profile (sections 7 and 9 for current behaviour),
   `mode-c-modernize-project/templates/06-migration-test-plan.md`, and
   `mode-c-modernize-project/rules/40-document-specific.md` section 06.

## Procedure
1. **Strategy and environments:** fill every level, including Parity, Data migration,
   and Cutover rehearsal. Environments include the current system as a reference and a
   target staging environment with migrated data.
2. **Test data:** a copy of production data for rehearsal, anonymized if it holds
   personal data; synthetic data for new features. Never real personal data in the plan.
3. **Functional test cases (`TC-xx`):** at least one per Must and Should requirement,
   traced to its `FR`.
4. **Parity test cases (`TC-P-xx`):** one per Keep and Improve feature, traced to the
   parity `FR` and citing the current behaviour (`path:line` or Profile section 7/section 9). Expected
   result: same as current (Keep) or the stated change (Improve).
5. **Data migration test cases (`TC-D-xx`):** record counts per entity, referential
   integrity, spot checks, transformed fields, and a full rehearsal, each traced to the
   data migration requirements.
6. **Cutover and rollback test cases (`TC-C-xx`):** the plan's go/no-go checklist and a
   rollback rehearsal with the time limit, traced to the availability or recovery NFRs.
7. **Non-functional test cases (`TC-NF-xx`):** one per NFR with method and pass condition.
8. **UAT scenarios (`UAT-xx`):** business language, one per key workflow; state whether
   each is compared side by side with the current system.
9. **Defects, coverage, schedule, sign-off:** severity definitions (Medium "must fix
   before cutover?" is a `[DECISION]` unless the user decided), a coverage table with
   every `FR`/`NFR`, a schedule aligned with the plan's phases, and the sign-off table.
10. **Traceability:** fill the "Test case" column of the Target Requirements
    Specification's Traceability Matrix. This is the only edit to that document. Note it
    in its Revision History.

## Readability layer
Write the `Read This First` section (Rule 50 section 1): who tests what (role, what they test,
when), the testing flow step by step, the integration or driver release flow, the defect
flow, and the ready-to-deploy gate (same Mermaid source as the plan). Add an "In short"
note under every numbered section. Add the transmission or integration test level run by
the testers the brief names, with criteria, schedule and sign-off rows (Rule 40 section 06).

## Output
`output/mode-c/<slug>/06-migration-test-plan.md` (plus the traceability update in `02`)

Run the review checklist. Report the file path, the test case counts per group
(functional, parity, data, cutover, non-functional, UAT), any Must or Should requirement
without a test, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
