---
name: mod-suite
description: MODE C (modernize an existing project). Generate the complete modernization documentation set from a Mode A Project Profile. It runs the modernization interview (target tech stack, strategy, scope), then the Current State Assessment, Target Requirements, Target System Design, Migration Plan, Modernization Proposal, and Migration Test Plan, followed by a traceability and consistency review. Use when the user says "modernize this project", "rebuild it on a new stack and create the documents", "plan the migration of the existing system", or gives a Mode A slug and asks for modernization documents.
argument-hint: <mode-a project-slug or code path> [--only assessment,requirements,design,plan,proposal,test] [--format md|docx|pdf]
---

# Full Modernization Documentation Suite

> **Mode C — Modernize an existing project.** For documenting the existing system as it
> is, use the Mode A `/doc-suite`. For a brand-new system with no code, use the Mode B
> `/new-suite`.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Step 1 — Brief
If `output/mode-c/<slug>/00-modernization-brief.md` does not exist, run the `mod-brief`
procedure, including finding or building the Mode A profile and its single interview
round. This is the **only pause** in the suite (skipped in non-interactive runs; see
`mod-brief` Step 3). After the user answers (or says "use defaults"), continue without
further questions. Any remaining unknowns become markers.

## Step 2 — Generate documents
Follow each skill's SKILL.md exactly, in this order (later documents reuse earlier ones):

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

## Step 3 — Traceability and consistency review
Read all generated documents and check the "Suite consistency" section of
`rules/50-review-checklist.md`, plus:
- Every `F-xx` in the brief's Feature Disposition table has the same disposition in the
  requirements (§3 headings and §8 Out of Scope), the design (Component Mapping), the
  plan (Scope), and the proposal (Key Features / Out of Scope).
- Every Keep and Improve feature has a parity requirement and a parity test (`TC-P-xx`).
- Every Critical and High finding (`D-xx`) is resolved by at least one requirement and
  addressed by a design component.
- Every Must and Should `FR` appears in the Design, the Plan (WBS item), and the Test
  Plan (test case). The Traceability Matrix has no `—` in those rows.
- The Stack Comparison in the design matches the brief §7 layer by layer; every changed
  layer has an ADR.
- The proposal's scope, strategy, timeline, and effort figures equal the plan's.
- No document describes the target system as already built; no document describes a
  current feature the profile does not list.
Start by running `python tools/lint_docs.py output/mode-c/<slug>`: it checks the
mechanical items (markers, structure, IDs, citations, traceability) for the whole folder.
Then review the judgment items above by reading the documents.
Fix any inconsistency in place, starting with the earliest document.

## Step 4 — Index and export
1. Write `output/mode-c/<slug>/INDEX.md`: a table of each document with its audience,
   status, and Open Items count. Then add a **Stack Summary** (layer, current, target,
   status), a consolidated **Decisions Needed** list (all `[DECISION]` items, with
   recommendations), and an **Open Items** list (deduplicated, grouped by who must
   answer: client, project manager, technical lead).
2. If `--format docx` or `pdf` was requested, convert each finished document into
   `output/mode-c/<slug>/export/` (for Word, run `node tools/md_to_docx.js
   output/mode-c/<slug>`; see Rule 20 Export).

## Step 5 — Report
Give a short summary: the files written (as links), the checklist pass/fail per document
(include the final lint result), the target stack per layer with its status, the
decisions the user should make first, and the reminder that once the new code exists,
`/doc-suite <new-code-path>` produces the final manuals and `/new-gap-check <slug>
<new-code-path>` compares the plan against the build.
