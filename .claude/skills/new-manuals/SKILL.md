---
name: new-manuals
description: MODE B (new project, no code yet). Write draft User, Technical, and Developer Manuals for a planned system from its requirements and design, using the Mode A manual templates so they can be finalized once the system is built. Use when the user asks for a draft user manual, early training material, a planned admin guide, or developer onboarding for a system that is not built yet.
argument-hint: <project-slug> [user|technical|developer|all]
---

# Draft Manuals (pre-development)

> **Mode B — New project.** Once code exists, regenerate the final manuals with the Mode A
> skills (`/doc-user-manual`, `/doc-technical-manual`, `/doc-developer-manual`).

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`. Default target: `all`.

## Preconditions
1. Resolve `<slug>`. Requires the brief, `01-requirements-specification.md`, and
   `02-system-design.md` (run the missing procedures first).
2. Read `mode-b-new-project/rules/40-document-specific.md` §06–08 and the Mode A templates:
   - `mode-a-existing-project/templates/03-user-manual.md`
   - `mode-a-existing-project/templates/04-technical-manual.md`
   - `mode-a-existing-project/templates/05-developer-manual.md`

## Common rules for all three
- Keep every template heading so that the final Mode A manual can replace the draft
  section by section.
- Set **Status** to `Draft — Pre-development` and **Source revision** to `Brief v<n>, <date>`.
- Directly under the Document Control block, add:
  ```markdown
  > [!IMPORTANT]
  > This manual describes the planned system. Screens, labels, and commands will change
  > during development. Final version: regenerate with the Mode A skills after the build.
  ```
- Write in the future tense where the text describes behavior ("You will be able to…"),
  or in the normal imperative for procedures, with `[VERIFY: final label]` on every
  screen label and button name.
- A section that needs real code gets `Not applicable — code not yet written; complete
  after development.`

## User Manual → `06-user-manual-draft.md`
1. Tasks come from the user stories and key workflows, grouped by user goal, one section
   per role (`R-xx`).
2. Screen names and fields come from the design's screen inventory (`S-xx`).
3. Troubleshooting: list the validation and permission failures from the requirements.
   Messages are `[TBD: final message text]`.
4. No code, no file paths.

## Technical Manual → `07-technical-manual-draft.md`
1. Architecture, components, ports, and environments come from the design.
2. Requirements come from the design's stack and the NFRs. Hardware sizing is `[TBD]`.
3. Configuration reference: the design's planned keys (§13), with `[VERIFY]` on each.
4. Installation commands: write the expected sequence for the proposed stack, marked
   `[VERIFY: confirm after build]`. Never present them as tested.
5. Security, backup, monitoring: from the design and NFRs.

## Developer Manual → `08-developer-manual-draft.md`
1. Stack and versions, the proposed repository structure, and the architecture come from
   the design.
2. Coding standards, branching, and CI/CD: propose them, labeled **Proposed**, under the
   template's Recommendations subsection.
3. Data model and API: link to the design. Do not duplicate it.
4. Module guide, tech debt, and worked examples: Not applicable until code exists.

## Output
`output/mode-b/<slug>/06-user-manual-draft.md`, `07-technical-manual-draft.md`,
`08-developer-manual-draft.md` (only those requested)

Run the review checklist for each. Report the file paths, the task count per role, and the
Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
