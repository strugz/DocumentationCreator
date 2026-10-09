# Rule 60 — Proposal Slides (PowerPoint)

> **Scope: Modes A and B.** Mode C builds its presentation deck with
> `mode-c-modernize-project/rules/40-document-specific.md` section 08 and
> `mode-c-modernize-project/rules/50-readability-and-refinement.md` section 8 instead.
> This rule is not preloaded: the `/proposal-slides` skill reads it, and `/doc-proposal`,
> `/new-proposal`, `/doc-suite`, and `/new-suite` hand slide requests to that skill.
> The repository's own exporter `tools/md_to_pptx.js` builds the file; no outside skill
> is needed.

## 1. When to build
- Build the slides when the user passes `--format pptx` or asks for the proposal as
  slides, a deck, a presentation, or PowerPoint.
- Write the Markdown proposal first and finish its self-review (Rule 50). The slides are
  an export of the proposal, like the Word file (Rule 20 Export). Never author slide
  content that the proposal does not contain.

## 2. Output
| Mode | Source | Output |
|------|--------|--------|
| A | `output/mode-a/<slug>/02-project-proposal.md` | `output/mode-a/<slug>/export/<Product>-Project-Proposal-Slides.pptx` |
| B | `output/mode-b/<slug>/04-project-proposal.md` | `output/mode-b/<slug>/export/<Product>-Project-Proposal-Slides.pptx` |

`<Product>` is the product name with spaces replaced by hyphens. The slide text lives in
`output/<mode>/<slug>/deck/proposal-slides.json` (the slide spec), so later edits survive
a rebuild. Never write slide source files as Markdown under `output/<mode>/<slug>/`,
because the linter treats every Markdown file there as a document.

## 3. Slide order
One message per slide, for the approvers. The order mirrors the proposal sections.

| # | Slide | From proposal section |
|---|-------|-----------------------|
| 1 | Cover: product name, "Project Proposal", proposal type, date, prepared by | Document Control, section 1 |
| 2 | The problem | 2. Background and Problem Statement |
| 3 | What we want to achieve | 3. Objectives |
| 4 | What we propose: key features with their tags | 4. Proposed Solution |
| 5 | What is in and out of scope | 5. Scope |
| 6 | How we deliver it | 6. Approach and Methodology |
| 7 | Timeline and milestones | 7. Timeline and Milestones |
| 8 | Team and resources | 8. Team and Resources |
| 9 | Budget | 9. Budget and Cost Breakdown |
| 10 | Benefits, each with the feature that enables it | 10. Benefits and Expected Outcomes |
| 11 | Main risks and how we handle them | 11. Risks and Mitigation |
| 12 | The ask: the approval request and next steps | 14. Recommendation and Next Steps, 15. Approval |

- Leave out a slide whose section is `Not applicable`. Renumber the footers.
- No slide for assumptions, maintenance, the appendices, or Open Items. Those stay in the
  document; mention the open items count in the speaker notes of the ask slide.

## 4. Content
- **Same facts as the proposal.** Every feature, figure, date, name, and tag equals the
  proposal word for word. If the proposal changes, rebuild the slides from it.
- **Markers stay visible.** A `[TBD]`, `[ASSUMPTION]`, `[VERIFY]`, or `[DECISION]` value
  appears on the slide as written, with the Rule 25 review-marker highlight. Never replace
  a marker with an invented value or hide it in the notes.
- **Mode A:** features keep their Existing / In progress / Planned tag.
- **Mode B:** every feature is **Planned**; nothing is described as built or working.
- **Few words.** Short bullets on the slide; the detail and reasoning from the proposal go
  in the speaker notes of the same slide.
- **No code.** No file paths, code references, or stack detail beyond one line on slide 4
  (the proposal body rule in Rule 20).
- **No secrets or personal data** (Rule 00, item 6). Use role names where the proposal
  does.

## 5. Build
Follow `.claude/skills/proposal-slides/SKILL.md`:

1. Draft the slide spec from the proposal:
   `node tools/md_to_pptx.js output/<mode>/<slug> --draft`.
2. Edit the spec's slide text for approvers (section 4). Keep the facts; move detail into
   the notes.
3. Build: `node tools/md_to_pptx.js output/<mode>/<slug> --strict`.

The exporter applies the layout, so every deck looks the same:
- 16:9 wide layout; a dark layout for the cover and the ask, and a light content layout
  with an eyebrow, a one-line title, a footer, and the slide number.
- Rule 25 section 5 families and sizes (Cambria titles, Calibri text, nothing below
  14 pt) and Rule 25 section 7 colours; review markers on a yellow highlight.
- Native tables, two cards for scope, and a numbered timeline for up to 6 milestones.
- Speaker notes on every slide.

## 6. Check before reporting
1. Fix every warning of `--strict`: long titles, too many bullets or rows, missing notes,
   and review markers or figures that the proposal does not contain.
2. Render every slide to an image with
   `powershell -NoProfile -ExecutionPolicy Bypass -File tools/pptx_to_png.ps1 -Path <deck>`
   (needs PowerPoint), or the `pptx` skill's LibreOffice conversion without it.
3. Look at each image. Fix overflow, overlaps, cut-off text, and words split across lines
   in the spec, then build and render again until no slide has a problem.
4. Report the `.pptx` path with the proposal's Open Items.
