---
name: doc-suite
description: MODE A (existing code). Generate the complete documentation suite for a fed-in project. It runs intake, then the Completion Plan, Proposal, User Manual, Technical Manual, Developer Manual (and optionally repo docs), followed by a cross-document consistency review. Also applies later changes (answers to open questions, decisions, new code, scope, wording, names) to every document and the proposal slides without regenerating. Use when the user says "document this project", "create all the documents", "full documentation", or gives a project path without naming a specific document, or asks to update the existing Mode A documents.
argument-hint: <path-to-project or slug> [change request] [--only plan,proposal,user,technical,developer,repo] [--format md|docx|pdf|pptx]
---

# Full Documentation Suite

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Step 0 — New suite or change to an existing one?
- If `output/mode-a/<slug>/` already holds the documents and the input describes a change
  (answers to open questions, a decision, new commits, a feature to add, a rejected word,
  names to replace, "hard to read"), do **not** regenerate. Read
  `rules/55-applying-changes.md` (not preloaded) and apply the change in its order: the
  profile first, then 01 → 02 → 03 → 04 → 05 → repo docs, INDEX, proposal slides; then
  the Step 3 checks and the Step 4 exports.
- If the replacement for a name or term is unclear, ask one question with options;
  otherwise do not ask.
- Otherwise continue with Step 1.

## Step 1 — Intake
If `output/mode-a/<slug>/00-project-profile.md` does not exist, run the `doc-intake` procedure.
Then show the user the Open Questions **once**. Ask them to answer what they can, or to
reply "continue" to proceed with `[TBD]` markers. Wait for that reply. It is the only
pause in the suite. In a non-interactive or evaluation run, do not pause: continue with
`[TBD]` markers.
Before Step 2, write the answers into the profile: section 2 for approvers, testers,
pain points, names, and deliverables; section 17.1 for words to avoid. Every document
then follows them (Rule 10). If the deliverables include proposal slides, treat it as
`--format pptx`.

## Step 2 — Generate documents
Follow each skill's SKILL.md exactly. Default order (later documents reuse earlier ones):

| Order | Skill file | Output |
|-------|-----------|--------|
| 1 | `.claude/skills/doc-plan/SKILL.md` | `01-project-completion-plan.md` |
| 2 | `.claude/skills/doc-proposal/SKILL.md` | `02-project-proposal.md` |
| 3 | `.claude/skills/doc-user-manual/SKILL.md` | `03-user-manual.md` |
| 4 | `.claude/skills/doc-technical-manual/SKILL.md` | `04-technical-manual.md` |
| 5 | `.claude/skills/doc-developer-manual/SKILL.md` | `05-developer-manual.md` |
| 6 (optional) | `.claude/skills/doc-repo-files/SKILL.md` | `repo/*` |

Respect `--only` if it is given.

**Parallelism:** documents 1→2 are sequential (the Proposal reuses the Plan). Documents
3, 4, and 5 depend only on the profile, so you may delegate them to parallel
`general-purpose` agents. Give each agent the slug, the skill file path to follow, and the
instruction to obey `CLAUDE.md`, `rules/`, and `mode-a-existing-project/rules/`.

## Step 3 — Cross-document consistency review
Read all generated documents and check the "Suite consistency" section of
`rules/50-review-checklist.md`:
- Product name, version, and terminology are identical (use the profile Glossary).
- Feature IDs (F-xx) are consistent between Plan, Proposal, and User Manual.
- Every document has the Rule 35 readability layer, and a flow that appears in several
  documents uses the identical Mermaid source.
- Proposal scope = Plan WBS scope.
- Config keys in the Developer Manual setup ⊆ the Technical Manual config reference.
Start by running `python tools/lint_docs.py output/mode-a/<slug>`: it checks the
mechanical items (markers, structure, IDs, citations, traceability) for the whole folder.
Then review the judgment items above by reading the documents.
Fix any inconsistency in place.

## Step 4 — Index and export
1. Write `output/mode-a/<slug>/INDEX.md`: a table of each document with its audience, status,
   and Open Items count, followed by a consolidated **Open Items** list (deduplicated,
   grouped by who must answer).
2. If `--format docx` or `pdf` was requested, convert each finished Markdown document with
   the `docx` / `pdf` skill into `output/mode-a/<slug>/export/` (for Word, run
   `node tools/md_to_docx.js output/mode-a/<slug>`; see Rule 20 Export).
3. If `--format pptx` was requested (alone or with another format, for example
   `--format docx,pptx`), build the proposal slides from `02-project-proposal.md` into
   `output/mode-a/<slug>/export/` by following `.claude/skills/proposal-slides/SKILL.md`
   (`tools/md_to_pptx.js`, Rule 60). Only the proposal becomes slides.

## Step 5 — Report
Give a short summary: the files written (as links), the checklist pass/fail per document (include the final lint result),
and the top Open Items the user should resolve first.
