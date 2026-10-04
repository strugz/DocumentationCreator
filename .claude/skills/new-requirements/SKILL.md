---
name: new-requirements
description: MODE B (new project, no code yet). Write the Software Requirements Specification (SRS) for a planned project from its Project Brief, with functional and non-functional requirements, user stories, acceptance criteria, data, interfaces, and a traceability matrix. Use when the user asks for requirements, an SRS, a PRD, a functional specification, user stories, or acceptance criteria for a system that is not built yet.
argument-hint: <project-slug or idea>
---

# Software Requirements Specification

> **Mode B — New project.** For a project with existing code, requirements are derived by
> the Mode A skills instead.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Preconditions
1. Resolve `<slug>`. If `output/mode-b/<slug>/00-project-brief.md` is missing, run the
   `new-brief` procedure first (`.claude/skills/new-brief/SKILL.md`).
2. Read the brief, `mode-b-new-project/templates/01-requirements-specification.md`,
   `mode-b-new-project/rules/30-evidence-from-brief.md`, and
   `mode-b-new-project/rules/40-document-specific.md` §01.

## Procedure
1. **Scope and users:** take them from Brief §1–4. Copy role IDs (`R-xx`) unchanged.
2. **Functional requirements:** for each in-scope feature `F-xx` (Won't items go to Out of
   Scope), write one subsection. Break the feature into atomic "The system shall…"
   requirements (`FR-01`… numbered across the whole document). Each one has a priority,
   a source (`F-xx` or `Brief §n`), and a testable acceptance criterion.
   - Cover the obvious supporting behavior the user did not mention but the feature
     needs (validation, empty states, permissions, notifications). Mark it **Proposed**.
   - Every requirement needs a role allowed to perform it.
3. **User stories:** write one or more stories for each key workflow in Brief §6, with
   Given / When / Then acceptance criteria.
4. **Non-functional requirements:** fill every category in the template. Use the user's
   numbers from Brief §11. Otherwise suggest a reasonable target, labeled **Proposed**,
   e.g. "Pages load in under 3 seconds for 95% of requests — Proposed".
5. **Data:** list entities from Brief §7, plus any the requirements imply. Add validation
   rules and retention (`[TBD]` if legal retention is unknown). Fill Data Migration from
   Brief §5/§7, or mark it Not applicable.
6. **Interfaces and reports:** from Brief §9 and §12.
7. **Out of Scope:** copy Brief §13 and add things a reader might assume are included
   (mobile app, offline mode, multi-language, data migration) when the brief excludes them.
8. **Traceability Matrix:** fill the Feature → Requirement columns. Leave Design, WBS, and
   Test columns as `—`. Later skills fill them.
9. **Glossary:** copy from the brief and add new terms.

## Output
`output/mode-b/<slug>/01-requirements-specification.md`

Run `rules/50-review-checklist.md` (common + Mode B). Report the file path, the counts
(FR by priority, NFR, user stories), the Proposed items the user should confirm, and the
Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
