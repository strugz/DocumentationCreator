---
name: new-gap-check
description: Bridge from MODE B (or MODE C) to MODE A. Once code exists for a project that was planned with the Mode B or Mode C skills, compare the planned requirements and design with what was actually built, and write a Planned vs Built Gap Report. Use when the user asks "what did we build vs plan", "check the code against the requirements", "requirements coverage", or "gap analysis".
argument-hint: <mode-b or mode-c project-slug> <path-to-code>
---

# Planned vs Built Gap Report

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md`,
> `mode-b-new-project/rules/40-document-specific.md`, and (for the code side)
> `mode-a-existing-project/rules/30-evidence-and-accuracy.md`. They are not preloaded.

Input: `$ARGUMENTS`: the Mode B (or Mode C) slug and the path to the project's code. If
the path is missing, ask for it.

## Preconditions
1. The planned requirements must exist: `output/mode-b/<slug>/01-requirements-specification.md`
   (Mode B) or, if there is no Mode B folder for the slug,
   `output/mode-c/<slug>/02-target-requirements-specification.md` (Mode C, a modernized
   rebuild). If neither exists, stop and tell the user to run `/new-requirements` or
   `/mod-requirements` first. For a Mode C project, write the report to
   `output/mode-c/<slug>/09-gap-report.md`, compare the build against the Target System
   Design, and read `mode-c-modernize-project/rules/30-evidence-from-profile.md` as well.
2. A Mode A profile is needed for the code. If `output/mode-a/<slug>/00-project-profile.md`
   does not exist, run the `doc-intake` procedure on the code path, using the same slug.
   The source code is **read-only**.
3. Read `mode-b-new-project/templates/09-gap-report.md` and
   `mode-b-new-project/rules/40-document-specific.md` section 09.

## Procedure
1. For each `FR` and `NFR`, search the Mode A profile's features, endpoints, screens, and
   code for its implementation. Set a status:
   Implemented / Partial / Missing / Changed. Cite evidence as `path:line`.
2. Compare the design (stack, entities, endpoints, screens) with what was built. Record
   the differences as deviations, with their impact.
3. List Mode A features that match no requirement as **Unplanned features**.
4. Compute coverage = (Implemented + 0.5 × Partial) ÷ in-scope requirements, and show the
   formula.
5. Recommend actions: build the missing Must items, update the requirements for accepted
   changes, and remove or document unplanned features.

## Output
`output/mode-b/<slug>/09-gap-report.md`

Run the review checklist. Report the coverage, the missing Must requirements, and the
next step: generate the final manuals with the Mode A skills (`/doc-suite <code-path>`).

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
