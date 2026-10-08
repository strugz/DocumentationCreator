---
name: mod-design
description: MODE C (modernize an existing project). Write the Target System Design Document for a modernized system, with a current-vs-target stack comparison and ADRs for every changed layer, old-to-new component and data mappings, an interim architecture for incremental migration, data model, API, screens, security, deployment, and repository structure. Use when the user asks for the target architecture, modernization design, migration architecture, or "how should the new version be built".
argument-hint: <project-slug> [stack / hosting override]
---

# Target System Design Document

> **Mode C — Modernize an existing project.** For a brand-new system with no current
> code, use the Mode B `/new-design` skill.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (slug, plus an optional stack or hosting preference that overrides
the brief; if it does, update the brief §7 first and bump its version).

## Preconditions
1. Resolve `<slug>`. The brief and the assessment must exist. If
   `02-target-requirements-specification.md` is missing, run the `mod-requirements`
   procedure first.
2. Read the brief, the assessment, the requirements, the Mode A profile (§3, §6, §9, §10,
   §11, §12), `mode-c-modernize-project/templates/03-target-system-design.md`, and
   `mode-c-modernize-project/rules/40-document-specific.md` §03.

## Procedure
1. **Design goals:** the 3–5 NFRs and findings (`D-xx`) that shape the design most.
2. **Architecture:** summarize the current architecture (present tense, from the
   assessment), then choose the target style and say what it fixes. Draw context and
   component diagrams. Map every component to the `FR` IDs it implements and the `D-xx`
   it resolves. For an incremental strategy, draw the **Interim Architecture** (router or
   facade, shared data, sync); otherwise mark that section `Not applicable — big-bang
   strategy`.
3. **Stack comparison:** one row per layer from Brief §7: current (Profile §3), target,
   version, status (Agreed / Proposed), reason, ADR. Every changed layer gets an ADR with
   options considered. Every kept layer states why it stays. Versions are current LTS or
   stable releases, **Proposed** unless the user decided; end-of-support dates `[VERIFY]`.
   If a `[DECISION]` on a layer is still open, design for the recommended option and say so.
4. **Component mapping:** every current module (Profile §6) → target component with its
   disposition and what changes. Dropped modules say "Drop" and why.
5. **Data design:** target `erDiagram` and entity table; a **Data Mapping** table from
   every current entity (Profile §10) with the transformation and whether data migrates.
6. **API and UI:** endpoint list and screen inventory (`S-01`…) with "Replaces" columns
   pointing at the current routes and endpoints (Profile §9). Map every user-facing `FR`.
7. **Roles, integrations, processes:** permission matrix; integration table with current
   and target methods; sequence diagrams for the 2–4 key workflows.
8. **Security, logging, observability:** design to resolve the security and operations
   findings and the matching NFRs. Follow OWASP practice; secrets outside the code.
9. **Deployment and configuration:** environments, deployment diagram, backup design,
   planned configuration keys with placeholders and their current equivalents
   (Profile §11). Never real values.
10. **Repository structure:** propose a tree that matches the target stack's conventions.
11. **Traceability:** fill the "Design component" column of the Target Requirements
    Specification's Traceability Matrix. This is the only edit to that document. Note it
    in its Revision History.

## Output
`output/mode-c/<slug>/03-target-system-design.md` (plus the traceability update in `02`)

Run the review checklist. Report the file path, the stack per layer (Agreed vs Proposed),
the number of changed layers and ADRs, the counts (components, entities, endpoints,
screens), and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
