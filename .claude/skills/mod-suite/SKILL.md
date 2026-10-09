---
name: mod-suite
description: MODE C (modernize an existing project). Generate the complete modernization set from a Mode A Project Profile in one run — interview (stack, strategy, scope, rollout, testers, audience, wording, deliverables), a Tech Stack Questionnaire for stakeholders and developers, Current State Assessment, Target Requirements, Target System Design, Migration Plan, Modernization Proposal, Migration Test Plan, each with a plain-language Read This First page and process flows, then INDEX, Word files, a presentation deck and a starter kit for the new code repository. Also applies later review feedback (decisions, scope, wording, names) and returned questionnaire answers to every document and slide. Use when the user says "modernize this project", "rebuild it on a new stack and create the documents", "plan the migration of the existing system", gives a Mode A slug, asks for a tech stack questionnaire or survey for stakeholders or developers, brings back questionnaire answers, or asks to update the modernization documents or slides.
argument-hint: <mode-a project-slug or code path> [change request] [--only questionnaire,assessment,requirements,design,plan,proposal,test,deck,starter] [--format md|docx|pdf]
---

# Full Modernization Documentation Suite

> **Mode C — Modernize an existing project.** For documenting the existing system as it
> is, use the Mode A `/doc-suite`. For a brand-new system with no code, use the Mode B
> `/new-suite`.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`,
> `mode-c-modernize-project/rules/40-document-specific.md`, and
> `mode-c-modernize-project/rules/50-readability-and-refinement.md`. They are not preloaded.

Input: `$ARGUMENTS`.

The goal is a suite that management can read and approve **without rounds of
corrections**: decisions about rollout, testers, naming, wording and deliverables are
asked up front, and every document is written in the plain, readable form of Rule 50
from the first draft.

## Step 0 — New suite or change to an existing one?
- If `output/mode-c/<slug>/` already holds the documents and the input describes a change
  (a decision, new features, a stack choice, testers, a rejected word, names to replace,
  "hard to read", "update all slides"), do **not** regenerate. Apply the change with Rule
  50 section 5: brief first (new version), then 01 → 02 → 03 → 04 → 06 → 05, INDEX, deck,
  PowerPoint copy, starter kit `docs/design/` copy; then Step 3 checks and Step 4 exports.
  If names must be replaced and the replacement for each is unclear, ask one question with
  options; otherwise do not ask.
- If the input holds filled-in tech stack questionnaires (files or pasted answers),
  consolidate them per Rule 40 section 07 ("Consolidating answers"), then carry the
  brief changes through the suite the same way.
- Otherwise continue with Step 1.

## Step 1 — Brief
If `output/mode-c/<slug>/00-modernization-brief.md` does not exist, run the `mod-brief`
procedure, including finding or building the Mode A profile and its single interview
round (stack, strategy, scope, rollout, testers, audience and wording, deliverables). This
is the **only pause** in the suite (skipped in non-interactive runs; see `mod-brief` Step 3).
After the user answers (or says "use defaults"), continue without further questions. Any
remaining unknowns become markers.

## Step 1b — Tech Stack Questionnaire
Always write `output/mode-c/<slug>/07-tech-stack-questionnaire.md` from
`mode-c-modernize-project/templates/07-tech-stack-questionnaire.md`, following Rule 40
section 07 ("Writing it"). It needs only the profile and the brief, so write it before
Step 2. Skip it only when `--only` is given without `questionnaire`.

## Step 2 — Generate documents
Follow each skill's SKILL.md exactly, in this order (later documents reuse earlier ones).
Every document includes the readability layer (Rule 50 section 1) and its standard flows
(Rule 50 section 3), and follows the brief section 4 naming and wording rules.

| Order | Skill file | Output |
|-------|-----------|--------|
| 1 | `.claude/skills/mod-assessment/SKILL.md` | `01-current-state-assessment.md` |
| 2 | `.claude/skills/mod-requirements/SKILL.md` | `02-target-requirements-specification.md` |
| 3 | `.claude/skills/mod-design/SKILL.md` | `03-target-system-design.md` |
| 4 | `.claude/skills/mod-plan/SKILL.md` | `04-migration-plan.md` |
| 5 | `.claude/skills/mod-proposal/SKILL.md` | `05-modernization-proposal.md` |
| 6 | `.claude/skills/mod-test-plan/SKILL.md` | `06-migration-test-plan.md` |

Respect `--only` if it is given (still create the prerequisites each skill requires).

**Parallelism:** 1 → 2 → 3 → 4 are sequential. Once 4 is done, 5 (Proposal) and 6 (Test
Plan) may run as parallel `general-purpose` agents. Give each agent the slug, the skill
file path to follow, and the instruction to obey `CLAUDE.md`, `rules/`, and
`mode-c-modernize-project/rules/`. Agents must not edit
`02-target-requirements-specification.md`. The main agent fills the Traceability Matrix
"Test case" column after the Test Plan returns.

## Step 3 — Traceability, consistency and readability review
Read all generated documents and check the "Suite consistency" section of
`rules/50-review-checklist.md`, plus:
- Every `F-xx` in the brief's Feature Disposition table has the same disposition in the
  requirements (section 3 headings and section 8 Out of Scope), the design (Component Mapping), the
  plan (Scope), and the proposal (Key Features / Out of Scope).
- Every Keep and Improve feature has a parity requirement and a parity test (`TC-P-xx`).
- Every Critical and High finding (`D-xx`) is resolved by at least one requirement and
  addressed by a design component.
- Every Must and Should `FR` appears in the Design, the Plan (WBS item), and the Test
  Plan (test case). The Traceability Matrix has no `—` in those rows.
- The Stack Comparison in the design matches the brief section 7 layer by layer; every changed
  layer has an ADR.
- The proposal's scope, strategy, timeline, and effort figures equal the plan's.
- The questionnaire's Current and Proposed values per layer equal the brief section 7
  table, and its "(decision needed)" layers equal the brief's open stack decisions.
- No document describes the target system as already built; no document describes a
  current feature the profile does not list.
- Every document has its `Read This First` section and an "In short" note under every
  numbered section (Rule 50 section 1); shared flows use identical Mermaid source and no label
  starts with `1.` (Rule 50 section 3).
- The named testers, the release gate wording and the milestone names are the same in
  the plan, test plan, proposal and deck (Rule 50 section 4).
- No personal name the brief says to replace, and no word the brief says to avoid,
  appears outside Revision History rows (search all documents and deck files).
Start by running `python tools/lint_docs.py output/mode-c/<slug>`: it checks the
mechanical items (markers, structure, IDs, citations, traceability) for the whole folder.
Then review the judgment items above by reading the documents.
Fix any inconsistency in place, starting with the earliest document.

## Step 4 — Index and Word files
1. Write `output/mode-c/<slug>/INDEX.md`. Start with **How to Use These Documents**: a
   reader guide (role → documents → what they decide) and the document map flow. Then a
   table of each document with its audience, status, and Open Items count (count the rows
   of each Open Items table), a **Stack Summary** (layer, current, target, status), a
   consolidated **Decisions Needed** list (all `[DECISION]` items, with recommendations),
   and an **Open Items** list (deduplicated, grouped by who must answer).
2. Word files, when the brief's deliverables or `--format docx` ask for them: run
   `python tools/render_mermaid.py output/mode-c/<slug>` and open the URL it prints in a
   browser so diagrams become images, then `node tools/md_to_docx.js output/mode-c/<slug>`
   (Rule 20 Export). Then make the questionnaire's two audience copies (Rule 40
   section 07, item 7): `07-tech-stack-questionnaire-stakeholders.docx` and
   `07-tech-stack-questionnaire-developers.docx`. If a file is locked (`EBUSY`), export it to `export/updated/` and
   say so. For PDF, see Rule 20.

## Step 5 — Presentation deck
When the brief's deliverables include a deck (or `--only deck`), build it per Rule 40 section 08:
an online deck with the session's slide-deck artifact type when one exists, and a
PowerPoint file in `output/mode-c/<slug>/export/` when the brief lists PowerPoint (Rule 50
Section 8: `pptx` skill, same content and notes as the online deck, Rule 25 fonts and sizes, every
slide rendered and checked before it is reported). Use the
proposal's and plan's figures exactly; put detail in speaker notes; number the footers.

## Step 6 — Build repository starter kit
When the brief's deliverables include it (default) or `--only starter`, write the kit per
Rule 40 section 09 to `output/mode-c/<slug>/<repo-name>-repo-starter/`, with `docs/design/` copied from the
finished suite and `.claude/settings.json` enabling the `feature-dev` plugin (section 09,
Plugins). Zip it when the user asks for one file.

In non-interactive or evaluation runs, skip Steps 5 and 6 unless the input asks for them.

## Step 7 — Report
Give a short summary: the files written (as links), the checklist pass/fail per document
(include the final lint result), the target stack per layer with its status, the
decisions the user should make first, where the deck and starter kit are, and the reminder
that once the new code exists, `/doc-suite <new-code-path>` produces the final manuals and
`/new-gap-check <slug> <new-code-path>` compares the plan against the build. Do not attach
or send files unless the user asks for them.
