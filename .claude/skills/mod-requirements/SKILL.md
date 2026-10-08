---
name: mod-requirements
description: MODE C (modernize an existing project). Write the Target Requirements Specification for the modernized system from the Modernization Brief and the Current State Assessment, with parity requirements for every kept feature, requirements that resolve each serious finding, data migration requirements, and a traceability matrix. Use when the user asks for requirements, an SRS, a PRD, or acceptance criteria for a rebuilt or modernized system.
argument-hint: <project-slug>
---

# Target Requirements Specification

> **Mode C — Modernize an existing project.** For a brand-new system with no current
> code, use the Mode B `/new-requirements` skill.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (slug).

## Preconditions
1. Resolve `<slug>`. The brief must exist (run `mod-brief` if not). If
   `01-current-state-assessment.md` is missing, run the `mod-assessment` procedure first.
2. Read the brief, the assessment, the Mode A profile (for current behaviour to cite),
   `mode-c-modernize-project/templates/02-target-requirements-specification.md`, and
   `mode-c-modernize-project/rules/40-document-specific.md` §02.

## Procedure
1. **Scope and perspective:** state what the target system replaces, the goals it serves
   (Brief §3), and, for an incremental strategy, how it coexists with the current system.
2. **Users:** carry the roles (`R-xx`) from the brief with any changes noted there.
3. **Functional requirements, by feature and disposition:**
   - **Keep:** at least one **parity** requirement. Acceptance criterion: "matches the
     current behaviour" with the evidence cited (`path:line` or Profile §7/§9). Priority
     Must unless the brief says otherwise.
   - **Improve:** a parity requirement for what stays the same plus one requirement per
     stated change.
   - **Replace:** requirements for the need being served, not the old mechanism; note
     the current mechanism in "Current behaviour".
   - **New:** requirements from the brief's description, acceptance criteria proposed
     and labeled.
   - **Drop:** no requirements; list the feature in §8 Out of Scope with the reason.
   One "shall" per row. Type column: Parity / Improvement / New / Finding.
4. **Findings:** every Critical and High `D-xx` from the assessment gets at least one
   requirement (functional or non-functional) that resolves it; its Source names the
   `D-xx`. Medium findings get one where the brief's goals justify it.
5. **Non-functional requirements:** fill every category. The "Current" column cites the
   assessment or profile; the "Target" is the user's figure or a **Proposed** value.
6. **Data:** entities from the brief §9; a Data Migration table (migrate / transform /
   archive / drop, with verification). If no data migrates, write
   `Not applicable — <reason from the brief>`.
7. **Interfaces and reports:** from the brief §10 and the profile §9 and §12, each with
   its disposition.
8. **Traceability Matrix:** one row per requirement with Feature and Finding filled.
   Leave Design component, WBS item, and Test case as `{{filled by /mod-design}}` etc.
   only while those documents do not exist; the later skills fill them.

## Output
`output/mode-c/<slug>/02-target-requirements-specification.md`

Run the review checklist. Report the file path, the requirement counts by type and
priority, how many findings are resolved by a requirement (and which are not), and the
Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
