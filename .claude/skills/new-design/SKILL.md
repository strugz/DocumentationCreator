---
name: new-design
description: MODE B (new project, no code yet). Write the System Design Document for a planned project, covering architecture, proposed tech stack, data model (ERD), API design, screen inventory, roles and permissions, security, deployment, repository structure, and ADRs. Use when the user asks for a system design, software design document, technical design, architecture design, database design, or solution design for a system that is not built yet.
argument-hint: <project-slug> [preferred stack / hosting]
---

# System Design Document

> **Mode B — New project.** For existing code, architecture is documented by the Mode A
> Technical and Developer Manuals.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (slug, plus an optional stack or hosting preference that overrides
the brief).

## Preconditions
1. Resolve `<slug>`. The brief must exist (run `new-brief` if not). If
   `01-requirements-specification.md` is missing, run the `new-requirements` procedure first.
2. Read the brief, the requirements, `mode-b-new-project/templates/02-system-design.md`,
   and `mode-b-new-project/rules/40-document-specific.md` §02.

## Procedure
1. **Design goals:** pick the 3–5 NFRs that shape the design most (e.g. security,
   offline support, low hosting cost) and state them.
2. **Architecture:** choose the simplest style that meets the requirements. A modular
   monolith is the default for small and medium teams. Draw a context diagram and a
   component diagram. Map every component to the `FR` IDs it implements.
3. **Tech stack:** use the user's stack if given. Otherwise propose a mainstream stack with
   current LTS versions, labeled **Proposed**, each with a reason (team skills, hosting
   preference, licensing cost). Record big choices as ADRs. If an unresolved
   `[DECISION]` blocks a choice, design for the recommended option and say so.
4. **Data design:** build a Mermaid `erDiagram` from the requirements' entities. List
   attributes with types and required flags. Keep it under about 20 entities per diagram.
5. **API design:** list the proposed endpoints (REST by default) with method, path, roles,
   and the `FR` they implement. State conventions: versioning, error format, pagination, auth.
6. **UI design:** build a screen inventory (`S-01`…) covering every user-facing `FR`, a
   navigation map, and short descriptions of key screens (fields, actions, validation).
   Wireframes are `[TBD]` unless the user supplied some.
7. **Roles and permissions:** build a matrix from the brief's roles and the requirements.
8. **Processes:** draw sequence diagrams for the 2–4 most important workflows.
9. **Security, error handling, logging:** design to meet the security and logging NFRs.
   Follow OWASP practice (hashed passwords, least privilege, input validation, secrets
   outside the code).
10. **Deployment:** define environments, a deployment diagram, and the backup design.
11. **Configuration (planned):** list the configuration keys the design implies
    (database URL, mail server, storage). Use placeholders and never real values.
12. **Repository structure:** propose a folder tree that matches the stack's conventions.
13. **Traceability:** fill the "Design component" column of the Requirements
    Specification's Traceability Matrix. This is the only edit to that document. Note
    it in its Revision History.

## Output
`output/mode-b/<slug>/02-system-design.md` (plus the traceability update in `01`)

Run the review checklist. Report the file path, the stack chosen (Proposed vs Agreed),
the counts (components, entities, endpoints, screens), the ADRs, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
