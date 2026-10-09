---
name: new-test-plan
description: MODE B (new project, no code yet). Write the Test Plan for a planned system, covering test strategy, environments, test data, entry and exit criteria, test cases traced to requirements, non-functional tests, UAT scenarios, defect severity, coverage, and UAT sign-off. Use when the user asks for a test plan, QA plan, test cases, UAT plan, or acceptance test plan for a system that is not built yet.
argument-hint: <project-slug>
---

# Test Plan

> **Mode B — New project.**

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Preconditions
1. Resolve `<slug>`. Requires the brief and `01-requirements-specification.md` (run the
   missing procedures first). Read `02-system-design.md` and `03-project-plan.md` if they
   exist.
2. Read `mode-b-new-project/templates/05-test-plan.md` and
   `mode-b-new-project/rules/40-document-specific.md` section 05, and
   `rules/45-estimation-and-release-gate.md` section 5 (the release gate).

## Procedure
1. **Strategy:** fill the test-level table. Tooling follows the design's stack (e.g. the
   stack's standard unit-test framework, Playwright for end-to-end tests). Label it
   **Proposed** unless agreed.
2. **Environments and test data:** take the environments from the design. Test data must
   be synthetic or anonymized, never real personal data.
3. **Functional test cases:** for every Must and Should `FR`, write at least one test case
   (`TC-01`…) from its acceptance criteria. Add a negative case (invalid input, missing
   permission) for every requirement that has validation or role restrictions.
4. **Non-functional test cases:** one per NFR with a measurable target (`TC-NF-01`…).
5. **UAT scenarios:** one per key workflow in Brief section 6, in business language, each
   listing the requirements it covers.
6. **Defects:** define severities with examples from this product.
7. **Coverage:** build the requirements coverage table. Every Must must be covered.
   Report any gaps.
8. **Schedule:** align with the Plan's Phase 4 (or relative phases if there is no plan).
9. **Release gate:** the exit criteria of the last level and the UAT Sign-Off use the
   Rule 45 section 5 gate word for word, with the testers named by role from Brief
   section 3. If the Plan exists, its gate wording must be identical.
10. **Traceability:** fill the "Test case" column of the Requirements' Traceability Matrix
   and note it in that document's Revision History.

## Output
`output/mode-b/<slug>/05-test-plan.md`

Run the review checklist. Report the file path, the test case counts (functional,
non-functional, UAT), the coverage of Must and Should requirements, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
