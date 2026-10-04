---
name: new-suite
description: MODE B (new project, no code yet). Generate the complete pre-development documentation set from a project idea. It runs the brief interview, then the Requirements Specification, System Design, Project Plan, Proposal, Test Plan, and optional draft manuals, followed by a traceability and consistency review. Use when the user says "create a project like…", "I want to build…, create the documents", "plan and document a new system", or describes an idea without giving a code path.
argument-hint: <project idea or slug> [--only requirements,design,plan,proposal,test,manuals] [--no-manuals] [--format md|docx|pdf]
---

# Full New-Project Documentation Suite

> **Mode B — New project.** For a project that already has code, use the Mode A
> `/doc-suite` instead.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Step 1 — Brief
If `output/mode-b/<slug>/00-project-brief.md` does not exist, run the `new-brief`
procedure, including its single interview round. This is the **only pause** in the suite (skipped in non-interactive runs; see `new-brief` Step 3).
After the user answers (or says "use defaults"), continue without further questions.
Any remaining unknowns become markers.

## Step 2 — Generate documents
Follow each skill's SKILL.md exactly, in this order (later documents reuse earlier ones):

| Order | Skill file | Output |
|-------|-----------|--------|
| 1 | `.claude/skills/new-requirements/SKILL.md` | `01-requirements-specification.md` |
| 2 | `.claude/skills/new-design/SKILL.md` | `02-system-design.md` |
| 3 | `.claude/skills/new-plan/SKILL.md` | `03-project-plan.md` |
| 4 | `.claude/skills/new-proposal/SKILL.md` | `04-project-proposal.md` |
| 5 | `.claude/skills/new-test-plan/SKILL.md` | `05-test-plan.md` |
| 6 | `.claude/skills/new-manuals/SKILL.md` | `06`–`08` draft manuals (skip with `--no-manuals`) |

Respect `--only` if it is given (still create the prerequisites each skill requires).

**Parallelism:** 1 → 2 → 3 → 4 are sequential. Once 3 is done, 5 (Test Plan) and 6
(manuals) may run as parallel `general-purpose` agents. Give each agent the slug, the
skill file path to follow, and the instruction to obey `CLAUDE.md`, `rules/`, and
`mode-b-new-project/rules/`. Agents must not edit `01-requirements-specification.md`. The
main agent fills the Traceability Matrix "Test case" column after the Test Plan returns.

## Step 3 — Traceability and consistency review
Read all generated documents and check the "Suite consistency" section of
`rules/50-review-checklist.md`, plus:
- Every Must and Should `FR` appears in the Design (component or screen), in the Plan
  (WBS item), and in the Test Plan (test case). The Traceability Matrix has no `—` in
  those rows.
- Feature IDs (`F-xx`), role IDs (`R-xx`), and terms match the brief's Glossary everywhere.
- Proposal scope = Requirements in-scope = Plan WBS scope.
- Timeline and effort figures in the Proposal equal the Plan's.
- No document describes the system as already built.
Start by running `python tools/lint_docs.py output/mode-b/<slug>`: it checks the
mechanical items (markers, structure, IDs, citations, traceability) for the whole folder.
Then review the judgment items above by reading the documents.
Fix any inconsistency in place, starting with the earliest document.

## Step 4 — Index and export
1. Write `output/mode-b/<slug>/INDEX.md`: a table of each document with its audience,
   status, and Open Items count. Then add a consolidated **Decisions Needed** list
   (all `[DECISION]` items, with recommendations) and **Open Items** list (deduplicated,
   grouped by who must answer: client, project manager, technical lead).
2. If `--format docx` or `pdf` was requested, convert each finished document with the
   `docx` / `pdf` skill into `output/mode-b/<slug>/export/`.

## Step 5 — Report
Give a short summary: the files written (as links), the checklist pass/fail per document (include the final lint result),
the decisions the user should make first, and the reminder that once code exists,
`/new-gap-check` compares plan against build and the Mode A skills produce the final manuals.
