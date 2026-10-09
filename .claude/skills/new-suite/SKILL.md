---
name: new-suite
description: MODE B (new project, no code yet). Generate the complete pre-development documentation set from a project idea. It runs the brief interview, then the Requirements Specification, System Design, Project Plan, Proposal, Test Plan, and optional draft manuals, followed by a traceability and consistency review and an optional starter kit for the new code repository. Also applies later changes (answers, decisions, scope, wording, names) to every document and the proposal slides without regenerating. Use when the user says "create a project like…", "I want to build…, create the documents", "plan and document a new system", or describes an idea without giving a code path, or asks to update the existing Mode B documents.
argument-hint: <project idea or slug> [change request] [--only requirements,design,plan,proposal,test,manuals,starter] [--no-manuals] [--format md|docx|pdf|pptx]
---

# Full New-Project Documentation Suite

> **Mode B — New project.** For a project that already has code, use the Mode A
> `/doc-suite` instead.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Step 0 — New suite or change to an existing one?
- If `output/mode-b/<slug>/` already holds the documents and the input describes a change
  (answers, a decision, a new or dropped feature, a rejected word, names to
  replace, "hard to read"), do **not** regenerate. Read `rules/55-applying-changes.md`
  (not preloaded) and apply the change in its order: the brief (new version) first, then
  01 → 02 → 03 → 04 → 05 → 06–08 → 09, INDEX, proposal slides, starter kit; then the
  Step 3 checks
  and the Step 4 exports.
- If the replacement for a name or term is unclear, ask one question with options;
  otherwise do not ask.
- Otherwise continue with Step 1.

## Step 1 — Brief
If `output/mode-b/<slug>/00-project-brief.md` does not exist, run the `new-brief`
procedure, including its single interview round. This is the **only pause** in the suite (skipped in non-interactive runs; see `new-brief` Step 3).
After the user answers (or says "use defaults"), continue without further questions.
Any remaining unknowns become markers.
Every document follows the brief's naming choice and section 16.1 Words to Avoid
(Rule 10). If the brief's deliverables include proposal slides, treat it as
`--format pptx`.

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
- Every document has the Rule 35 readability layer, and a flow that appears in several
  documents uses the identical Mermaid source.
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
   `docx` / `pdf` skill into `output/mode-b/<slug>/export/` (for Word, run
   `node tools/md_to_docx.js output/mode-b/<slug>`; see Rule 20 Export).
3. If `--format pptx` was requested (alone or with another format, for example
   `--format docx,pptx`), build the proposal slides from `04-project-proposal.md` into
   `output/mode-b/<slug>/export/` by following `.claude/skills/proposal-slides/SKILL.md`
   (`tools/md_to_pptx.js`, Rule 60). Only the proposal becomes slides.

## Step 4b — Build repository starter kit
When Brief section 3 Deliverables lists it, or with `--only starter`, write the kit per
`mode-b-new-project/rules/40-document-specific.md` section 10 to
`output/mode-b/<slug>/<repo-name>-repo-starter/`, with `docs/design/` copied from the finished suite
and `.claude/settings.json` enabling the `feature-dev` plugin (section 10, Plugins).
Write it after the Step 3 review, so it copies the final documents. Zip it when the user
asks for one file.

## Step 5 — Report
Give a short summary: the files written (as links), the checklist pass/fail per document (include the final lint result),
the decisions the user should make first, where the starter kit is (if built), and the
reminder that once code exists,
`/new-gap-check` compares plan against build and the Mode A skills produce the final manuals.
