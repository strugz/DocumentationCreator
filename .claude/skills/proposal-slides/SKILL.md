---
name: proposal-slides
description: MODES A AND B. Turn a finished Project Proposal (02-project-proposal.md in Mode A, 04-project-proposal.md in Mode B) into a PowerPoint deck for approvers with tools/md_to_pptx.js. It drafts a slide spec from the proposal, shortens the slide text while keeping every fact, figure and review marker, builds the .pptx, renders and checks every slide, and reports. Use when the user asks for the proposal as slides, a deck, a presentation, or PowerPoint, passes --format pptx to a proposal skill or suite, or asks to update the proposal slides. Mode C decks use /mod-suite instead.
argument-hint: <mode-a or mode-b project-slug> [--rebuild]
---

# Proposal Slides (PowerPoint)

> **Modes A and B.** For a Mode C modernization deck, use `/mod-suite` (Mode C Rule 40
> section 08).

> **Rules:** Before starting, read `rules/60-proposal-slides.md`. It is not preloaded.

Input: `$ARGUMENTS` (a slug, optionally `--rebuild` to start the slide spec again from the
proposal).

## Preconditions
1. Resolve the folder: `output/mode-a/<slug>/` holds `02-project-proposal.md`, or
   `output/mode-b/<slug>/` holds `04-project-proposal.md`. If neither exists, run
   `/doc-proposal` or `/new-proposal` first.
2. Run `python tools/lint_docs.py output/<mode>/<slug>` and fix every error in the
   proposal first. The slides only repeat the proposal.
3. If `tools/node_modules/` is missing, run `npm install` in `tools/` (it installs the
   pinned `pptxgenjs` and `docx`).

## Step 1 — Draft the slide spec
```bash
node tools/md_to_pptx.js output/<mode>/<slug> --draft
```
It writes `output/<mode>/<slug>/deck/proposal-slides.json`: the cover, one slide per
proposal section in the Rule 60 order (sections marked `Not applicable` are skipped), and
the ask, each with the section text as speaker notes. An existing spec is kept; pass
`--force` only with `--rebuild`, because the spec holds earlier slide edits.

## Step 2 — Edit the spec for approvers
Open the JSON and edit the slide text only. Rule 60 section 4 applies:
- Shorten bullets to one line where you can (the tool warns above 22 words) and keep at
  most 6 per slide. Move detail into `notes`.
- Keep every feature, figure, date, name, tag, and review marker exactly as the proposal
  writes it. Never add a fact the proposal does not contain.
- Keep tables to 8 rows and 5 columns; merge or drop columns that approvers do not need,
  and put the full table in `notes`.
- Mode B: features stay **Planned**. Mode A: keep the Existing / In progress / Planned tags.
- Names by role, and no word from the evidence base's Words to Avoid table (Rule 10).

Slide types: `cover` (title, subtitle, meta), `bullets` (eyebrow, title, lead, bullets),
`table` (columns, rows), `columns` (left and right, each with heading and bullets),
`timeline` (milestones with label and date, at most 6), `ask` (title, bullets). Every
slide has `notes`. `**bold**` and review markers in the text are rendered.

## Step 3 — Build and check
```bash
node tools/md_to_pptx.js output/<mode>/<slug> --strict
```
It writes `output/<mode>/<slug>/export/<Product>-Project-Proposal-Slides.pptx` and warns
about long titles, too many bullets or rows, missing notes, and markers or figures that
the proposal does not contain. Fix every warning in the spec and build again until there
are none.

## Step 4 — Render and look at every slide
On Windows with PowerPoint:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/pptx_to_png.ps1 `
  -Path output/<mode>/<slug>/export/<Product>-Project-Proposal-Slides.pptx
```

Without PowerPoint, use the `pptx` skill's LibreOffice conversion. Read each image and fix
overflow, overlaps, text cut off, and words split across lines in the spec; then build
and render the changed slides again.

## Step 5 — Report
Give the `.pptx` path, the slide count, the final check result, and the proposal's Open
Items that appear on the slides (the review markers).

## Later changes
When the proposal changes (Rule 55), update the matching slide text and notes in the
spec, then repeat Steps 3 and 4. Use `--rebuild` only when the proposal's structure
changed so much that the spec no longer matches it.
