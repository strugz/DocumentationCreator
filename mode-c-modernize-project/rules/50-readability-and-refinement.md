# Rule 50 (Mode C) — Readability and Refinement

> **Scope: Mode C only.** These lessons come from a real modernization suite reviewed by
> management and laboratory staff. Apply them in the **first** generation, so the suite
> does not need rounds of corrections, and again whenever the suite is changed after
> review (`/mod-suite` with the change follows section 5).

## 1. Readability layer (every document)
Shared Rule 35 (`rules/35-readability.md`) applies the same layer to Modes A and B. This
section and section 3 remain the Mode C version, with the Mode C flows.

Technical completeness is not enough: readers said the documents were "complex and hard
to read" until they had a plain-language entry point. Every Mode C document therefore has:

1. **A `## Read This First` section** after the Table of Contents (and in the ToC), with:
   - a **one-page table** of the questions the reader asks, each answered in one line
     with a section reference (for example "When is it ready to deploy?");
   - **at least one picture**: a Mermaid flow from section 3 below;
   - a **"Where to Find What"** table (`I want to know…` → section) for long documents.
2. **An "In short" note** at the start of every numbered `##` section:
   `> [!NOTE]` / `> **In short:** <one or two plain sentences>`.
3. **An executive summary in bullets** (What / How / Testing / When / Effort / Risks /
   Needed to start) in the plan and proposal, not a dense paragraph.

The detail stays in the numbered sections; the readability layer only summarizes it and
never adds facts that the sections do not contain.

## 2. Audience and wording
- **Problems from the user's point of view.** For management decks and proposals, state
  each problem as the people who use the system feel it (for a laboratory: "missing lab
  modules", "no archiving", "cannot keep up", "limited formulas", "hard to install", "not
  flexible"), then confirm it with assessment findings. Technical findings (VB6, secrets,
  SQL injection) go below the table or into the assessment.
- **Executives read only what helps them decide.** Drop slides or sections the approvers
  will not use (an options comparison was removed because "management will only go over
  their head"); keep a one-paragraph options summary in the proposal.
- **Professional naming.** Do not put personal names or internal department nicknames in
  documents or slides. Use roles: "Management" for approvers and sponsors, "the
  development team" (in tables: Technical lead / Developer, or Developer 1 / Developer 2)
  for builders, and named functions such as "QA and IMS personnel" when the user wants
  testers named. Ask the user once which names to replace, then apply it everywhere.
- **Wording rules from the user are binding.** When the user rejects a phrase (for
  example "won bid", "in-house"), record the rule in the brief's Interview Log and
  Decisions, replace it in **every** document, the INDEX and the slides, and paraphrase
  earlier interview quotes that contain it (mark them "user, paraphrased"). Prefer
  neutral, quality-focused wording: "thoroughly tested before it is ready to deploy",
  "MDMPI pilot" instead of "in-house pilot".
- After every wording change, search all documents and slides for the old terms,
  excluding Revision History rows, and fix every hit:
  `grep -rn -i -E "<old term 1>|<old term 2>" output/mode-c/<slug> --include=*.md --include=*.html`.

## 3. Standard process flows
Use Mermaid flowcharts (under about 20 nodes, quoted labels). Reuse the **identical**
source block when the same flow appears in several documents, so it reads the same and
renders once.

| Flow | Shows | Put it in |
|------|-------|-----------|
| System in one picture | Users, the main parts, database, printers, outside systems | Design, Proposal, Brief |
| Case flow (domain workflow) | A real case from start to end in the users' terms, with the key decision (for a laboratory: order → check-in → analyzer → verify, hold critical → release → print, HIS, portal, monthly reports → archive) | Design, Requirements, Proposal |
| Module case flows | One flow per special module (for example QC, microbiology, blood bank), with the safety check as a decision | Design |
| SDLC process flow | Plan → requirements → design → build in sprints → developer tests → QA testing → user acceptance → pilot → ready to deploy → handover; failed tests loop back to build | Plan, Proposal |
| Sprint flow | Pick items → code with Claude → review → CI → QA check → demo | Plan |
| Integration or driver release flow | Capture real traffic → write → replay test → QA sign-off → released | Plan, Test Plan |
| Ready-to-deploy gate | All Must tests → QA sign-off → UAT signed → pilot stable → ready | Plan, Proposal, Test Plan |
| Testing flow | Unit → replay → QA transmission → system → parity → UAT → rehearsal | Test Plan |
| Defect flow | New → Triaged → In progress → Fixed → retest → Verified → Closed | Test Plan |
| Problem to fix | Finding → requirement → design → work item → test | Assessment |
| Requirement to acceptance | Requirement → design → work item → test → QA → UAT | Requirements |
| Questionnaire flow | Profile → questionnaire sent → stakeholders and developers answer → summary → brief updated → stack decided | Questionnaire |
| Document map | How the suite's documents feed each other | INDEX |

**Mermaid gotchas**
- A label that starts with a number and a period (`["1. Plan"]`) is parsed as a Markdown
  list and renders **blank**. Write `["Step 1: Plan"]`.
- Quote every label that contains punctuation or parentheses.
- Split a flow that needs more than about 20 nodes.

## 4. Who tests, and the release gate
- Name the testing roles the user names (for example QA and IMS personnel for analyzer
  transmission and system tests; medical technologists for UAT) in the test strategy,
  environments, entry and exit criteria, roles, schedule, sign-off, the plan's team and
  RACI, the go-live checklist, the Definition of Done, and the proposal's approach.
- Define one **ready-to-deploy gate** and use the same wording everywhere: all Must tests
  pass, the testers sign off, user acceptance is signed, the pilot runs stable for a set
  period. Milestone names use it ("Release 1.0 tested and ready to deploy").

## 5. Propagating a change
Shared Rule 55 (`rules/55-applying-changes.md`) gives Modes A and B the same procedure.

A change to a decision, scope, wording or name always flows in this order:

1. **Brief** — record the decision (Decisions, Interview Log, Feature Disposition), bump
   the brief version (`v7` → `v8`), and update every document's Source revision.
   Update the tech stack questionnaire's Proposed values and "(decision needed)"
   headings too, unless its Status is already "Consolidated".
2. **Assessment → Requirements → Design → Plan → Test Plan → Proposal** — update each,
   adding a Revision History row that says what changed and why.
3. **INDEX** — headline numbers, Decisions Needed, Open Items and their **counts**.
4. **Slides** — text, speaker notes, page numbers, and any PowerPoint copy.
5. **Checks** — `python tools/lint_docs.py output/mode-c/<slug>`, the banned-terms search
   (section 2), and a read-through of the readability layer.
6. **Exports** — `python tools/render_mermaid.py output/mode-c/<slug>` (open the printed
   URL), then `node tools/md_to_docx.js output/mode-c/<slug>`.

For a **scope addition**: add the feature to the brief (disposition New, priority), then
requirements with acceptance criteria and traceability, design components and screens,
WBS items with sizes, a capacity and schedule check (say plainly when slack is gone and
add a risk), test cases, proposal scope and support items, and the slides.

Keep current-system facts (present tense, LMS 3.1) apart from target facts (future tense)
during every edit; a sweeping replace must not change statements about the current
system (for example "SQL Server" is correct for the current system only).

## 6. Exports and files
- Render diagrams before the Word export; otherwise Word shows Mermaid source.
- If an export fails with `EBUSY`, the `.docx` is open in Word. Export that file to
  `export/updated/` and tell the user, or ask them to close it.
- Edit long documents with small scripted, asserted replacements (each old string must
  match exactly once) rather than rewriting whole files, and re-run the linter after each
  batch.
- Scratch scripts never go under `output/mode-c/<slug>/`, because the linter treats every
  Markdown file there as a document. The one exception is the repository starter kit in
  `<repo-name>-repo-starter/`, which the linter skips (Rule 40 section 09).

## 7. Slides
- One message per slide, few words, for the approvers. Mirror the proposal: today →
  problems → what changes → proposal → case flow → approach → SDLC → timeline → effort →
  support → risks → ask.
- After adding or removing a slide, renumber every footer and update the deck order.
- Keep speaker notes in step with the slide text; they carry the detail.
- When a PowerPoint copy exists, rebuild it after slide changes so the two stay equal.

## 8. PowerPoint (.pptx) deck
The online deck cannot export a `.pptx` from the session, so build the PowerPoint file
directly when the brief lists it (or the user asks "send the slides as pptx").

- **Tool:** the `pptx` skill with a `pptxgenjs` script. Write the script and its
  `node_modules` in the session scratchpad, never in this repository. If `pptxgenjs` is
  missing, install it there (`npm install pptxgenjs@<pinned version>`); if the skill's
  `apply_theme.js` cannot find it, run node with `NODE_PATH` set to that `node_modules`.
- **Output:** `output/mode-c/<slug>/export/<Product>-Modernization-Proposal-Slides.pptx`,
  next to the Word files.
- **Same content as the online deck:** same slide order, text, figures and speaker notes.
  Read each speaker note from the deck's HTML (`<aside>`) so the two cannot drift.
- **Structured deck:** 16:9 wide layout; a theme with the deck palette; a dark layout for
  the cover and the ask, a light content layout with eyebrow, title, source line and slide
  number; one section per deck section; every element named.
- **Fonts:** Rule 25 section 5 (Cambria for titles, Calibri for text, minimum sizes), so the
  file looks the same on every PC.
- **Visual style:** cards with a soft shadow, numbered circles for steps and arrows
  between flow steps, native tables for comparisons, support and risks, large numbers for
  effort. No accent bars or stripes along card edges. Highlight the gate steps (testing,
  ready to deploy) and key milestones in the accent colour.
- **Fit:** a slide title must fit on one line. Shorten it rather than shrink it, and keep
  the online deck's title the same. Use a non-breaking space inside product names
  (`LMS 4`) so they never split across lines.
- **Check before sending:** render every slide to an image and look at each one. Where
  PowerPoint is installed, use its COM export
  (`$p.Slides.Item(n).Export(path, "PNG", 1600, 900)` from PowerShell); otherwise use the
  skill's LibreOffice conversion. Fix overflow, overlaps, uneven card tops and words split
  across lines, then render the changed slides again.
- **After any slide change:** rebuild the `.pptx` from the script and check the changed
  slides again.
