# Rule 60 — Proposal Slides (PowerPoint)

> **Scope: Modes A and B.** Mode C builds its presentation deck with
> `mode-c-modernize-project/rules/40-document-specific.md` section 08 and
> `mode-c-modernize-project/rules/50-readability-and-refinement.md` section 8 instead.
> This rule is not preloaded: `/doc-proposal`, `/new-proposal`, `/doc-suite`, and
> `/new-suite` read it when slides are requested.

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

`<Product>` is the product name with spaces replaced by hyphens. Never write slide source
files as Markdown under `output/<mode>/<slug>/`, because the linter treats every Markdown
file there as a document.

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
1. Use the `pptx` skill with a `pptxgenjs` script. Write the script and its
   `node_modules` in the session scratchpad, never in this repository.
2. Use the 16:9 wide layout. Use a dark layout for the cover and the ask, and a light
   content layout with an eyebrow, a one-line title, and the slide number.
3. Apply Rule 25 section 5 for families and sizes, and Rule 25 section 7 for colours
   (`#1F3864` and `#2F5496` for titles and accents, `#595959` for muted text).
4. Use native tables for scope, team, budget, and risks; a timeline or milestone row for
   the timeline; and large figures only for numbers the proposal states.
5. Keep each slide title on one line. Shorten the title rather than shrink the font.
6. Add the speaker notes to every slide.

## 6. Check before reporting
1. Render every slide to an image. Where PowerPoint is installed, use its COM export from
   PowerShell; otherwise use the `pptx` skill's LibreOffice conversion.
2. Look at each image. Fix overflow, overlaps, uneven card tops, text below the Rule 25
   minimum sizes, and words split across lines.
3. Render the changed slides again until none has a problem.
4. Compare the slide figures with the proposal one last time.
5. Report the `.pptx` path with the proposal's Open Items.
