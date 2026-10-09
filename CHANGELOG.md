# Changelog

All notable changes to this project are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version
numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.0] - 2026-10-09

### Added
- `tools/md_to_pptx.js`: the repository's own PowerPoint exporter for the Mode A and B
  proposal, so slides no longer depend on an outside skill. `--draft` writes a slide
  spec (`deck/proposal-slides.json`) from the proposal in the Rule 60 order with the
  section text as speaker notes; the build lays it out with Rule 25 fonts and colours
  (cover and ask on a dark layout, tables, scope cards, a numbered timeline, highlighted
  review markers). `--strict` fails on long titles, crowded slides, missing notes, and
  markers or figures the proposal does not contain. `tools/pptx_to_png.ps1` renders every
  slide with PowerPoint for checking. New `/proposal-slides` skill runs draft, edit,
  build, render, and report; the proposal and suite skills hand `--format pptx` to it.
  `pptxgenjs` 3.12.0 is a pinned dependency in `tools/package.json`. Tests in
  `tests/test_md_to_pptx.py` (skipped without Node).
- Mode B and Mode C starter kits enable the `feature-dev` plugin (Mode B Rule 40 section 10
  and Mode C Rule 40 section 09, Plugins): a `.claude/settings.json` adds the official
  plugin marketplace and turns on `feature-dev@claude-plugins-official`, and the kit's
  `CLAUDE.md` and `README.md` say when to use `/feature-dev` (multi-layer features, started
  from requirement IDs and the `docs/design/` sections) versus the kit's own skills. In
  Mode C, a run for a Keep or Improve feature also names the parity requirement, its parity
  test, and the current code path (read only).
- Starter kits now go inside the project folder,
  `output/<mode>/<slug>/<repo-name>-repo-starter/`, instead of `output/`.
  `tools/lint_docs.py` and the lint hook skip `*-repo-starter` folders.
- Build repository starter kit for Mode B (Rule 40 section 10), like Mode C: `/new-suite`
  Step 4b writes `output/mode-b/<slug>/<repo-name>-repo-starter/` with `CLAUDE.md`, `README.md`, rule
  files (principles, architecture, backend, frontend, database, security, testing, an
  integration when the design has one, git and traceability), build skills, `.gitignore`,
  an ADR template, and a `docs/design/` copy of the suite. No application code; undecided
  stack layers keep their `[DECISION]` at the top of the rule file. The brief's
  Deliverables row and `/new-brief` group L offer it (default yes), `--only starter`
  builds it alone, and Rule 55 refreshes it after a change.
- Change-request mode for `/doc-suite` and `/new-suite` (Step 0), like `/mod-suite`: when
  the output folder already holds the documents, a change (answers, a decision, new
  commits in Mode A, scope, wording, names, readability) is applied instead of
  regenerating. New shared Rule 55 `rules/55-applying-changes.md` (not preloaded) sets
  the order (evidence base, then each document, INDEX, proposal slides, checks, exports),
  what to update in each document (Source revision, version, Revision History,
  readability layer, Open Items), a search for old values, the Mode B scope-addition
  chain with the capacity re-check, and when to ask one question.
- Shared Rule 45 `rules/45-estimation-and-release-gate.md` (not preloaded) gives Modes A
  and B one estimation method and one release gate: fixed sizes (S = 1, M = 3, L = 5,
  XL = 10 person-days, count × unit for repeated work; Mode A sizes remaining work only),
  an AI-assisted factor of 0.6 on code-heavy items only when the evidence base says so
  (both totals shown, checked at the first milestone), capacity = developers × 20 days ×
  75 % focus, a method table for the Effort and Cost Estimate section, a scope-change
  re-check, and a ready-to-deploy gate with testers by role that the plan, test plan, and
  proposal repeat word for word. `/doc-plan`, `/new-plan`, `/new-test-plan`, and both
  proposal skills apply it; the plan, test plan, and proposal templates carry the method
  table, the gate in the Go-Live Checklist and Definition of Done, and the gate in the
  exit criteria and approach.
- Audience and wording rules for every mode (Rule 10 "Audience and wording"): problems from
  the users' point of view, approvers read only what helps them decide, roles instead of
  personal names, and binding Words to Avoid with a search after every change. The Mode B
  brief adds who asked, pain points in the users' words, development approach, pilot and
  rollout, testers, user acceptance, naming, deliverables (section 3), and a section 16.1
  Words to Avoid table. The Mode A profile adds the same context rows to section 2 and a
  section 17.1 Words to Avoid table. `/new-brief` asks groups J to L (rollout and testing,
  audience and wording, deliverables) and up to about 15 questions; `/doc-intake` always
  adds the audience and wording questions to Open Questions, and `/doc-suite` writes the
  answers into the profile before generating. Both proposal templates start the problem
  statement from the users' pain points. `tools/lint_docs.py` has a `wording` check that
  reports any Words to Avoid entry used outside Revision History.
- Shared Rule 35 `rules/35-readability.md` brings the Mode C readability layer to Modes A
  and B: a `Read This First` section (questions table, at least one flow, "Where to Find
  What" for long documents), an "In short" note under every numbered section, and bullet
  executive summaries in plans and proposals. It lists standard process flows per
  document and the Mermaid pitfalls. Every Mode A and B document template (Completion
  Plan, Proposal, the three manuals, Requirements, System Design, Project Plan, Test Plan,
  Gap Report) has the new section. CLAUDE.md and AGENTS.md load the rule; the review
  checklist and both suite reviews check it.
- `tools/lint_docs.py`: a `readability` check warns when a document has no `Read This
  First` section or a numbered section has no "In short" note (summary sections are
  exempt), and the `mermaid` check reports a label that starts with "1." as an error,
  because Mermaid renders it blank.
- PowerPoint export of the proposal in Modes A and B. New Rule 60
  `rules/60-proposal-slides.md` (not preloaded) sets when to build the slides, the output
  path `output/<mode>/<slug>/export/<Product>-Project-Proposal-Slides.pptx`, a 12-slide
  order that mirrors the proposal sections, content rules (same facts and visible review
  markers as the proposal, Mode B features stay Planned, detail in speaker notes, no
  code), the `pptx` skill build with Rule 25 fonts and colours, and a render-and-check
  step for every slide. `/doc-proposal` and `/new-proposal` take `--format pptx`, and
  `/doc-suite` and `/new-suite` accept `pptx` in `--format`. Rule 20 Export, Rule 25
  section 9, the review checklist, both Rule 40 files, CLAUDE.md, AGENTS.md, and the
  README point to it.

### Changed
- Mode A and B WBS sizes are fixed values (S = 1, M = 3, L = 5, XL = 10 person-days)
  instead of ranges (S up to 1 day, M 2 to 3 days, L 1 week, XL more than 1 week), so
  effort totals are the same in every run.

## [0.4.0] - 2026-10-09

### Added
- Shared Rule 15 `rules/15-response-and-code-output.md`: direct openings with no filler,
  complete runnable code blocks (only secret and reader-supplied placeholders allowed),
  tables for comparisons of 3 or more items, numbered lists for sequences, and concise,
  specific explanations. It applies to chat replies and to code blocks in documents.
- Shared Rule 25 `rules/25-typography.md`: one type system for every output. It sets
  font families with CSS font-stack fallbacks (Calibri, Cambria, Consolas, plus
  metric-compatible and system fonts), the print scale in pt for the Word export, the screen
  scale in rem/px with weights, line heights, letter spacing and margins (H1–H4, body,
  captions, UI elements, code), slide sizes, line-length limits, and WCAG 2.2 contrast pairs.
  CLAUDE.md, AGENTS.md, Rule 20, the review checklist, and the Mode C deck rules point to it.
- Mode C Tech Stack Questionnaire (template `07-tech-stack-questionnaire.md`, Rule 40
  section 07), written by `/mod-suite` in every run right after the brief: Part A for
  stakeholders (goals, users, hosting, compliance, budget, support, timeline), Parts B
  and C for developers (stack layer by layer with current and Proposed values, team
  skills, tools, risks), and a Response Summary. `tools/split_questionnaire.py` makes a
  stakeholder copy and a developer copy for separate Word files; `tools/md_to_docx.js`
  finds the suite's rendered diagrams for those copies. Running `/mod-suite <slug>` with the
  returned answers consolidates them into the brief and the rest of the suite. The deck
  and starter kit sections of Rule 40 are now sections 08 and 09.
- Mode C rule `50-readability-and-refinement.md`: the readability layer (Read This First
  page, In short notes, bullet executive summaries), standard process flows (case flow,
  SDLC, sprint, release gate, testing and defect flows) with Mermaid pitfalls, audience
  and professional-naming guidance, binding wording rules, the order for propagating a
  change across documents and slides, and export notes.

### Changed
- LMS 4 PowerPoint deck follows Rule 25: the orange accent is `9B540E` (was `C46A12`,
  3.1–3.9:1, now 4.6–5.7:1), card and flow-step text is 14 pt (was 13 pt), and the slide 6
  cards are 0.12" taller so the Verify step fits. Rule 25 section 5 adds sizes for card
  text, card headings, and number badges, and requires accent text to meet 4.5:1.
- Word export (`tools/md_to_docx.js`) follows Rule 25: body text uses 1.15 line spacing
  (headings and code stay at 1.0), and the footer and note text is `#595959` instead of
  `#808080`, which failed the 4.5:1 contrast minimum.
- Mode C produces the refined result in one run, based on a full review cycle of a real
  suite:
  - The `/mod-brief` interview also asks for the request's origin, the users' own pain
    points, team and AI-assisted development, pilot site, when clients receive the new
    version, data migration, who tests and the release gate, how approvers are named,
    words to avoid, and the deliverables. Brief §4 records the answers.
  - Every Mode C template starts with a `Read This First` section, and every document
    skill writes it with its standard flows and an "In short" note per section.
  - Rule 40 adds the estimation method (sizes, AI-assisted factor, capacity), pilot and
    release milestones, named testers and a transmission test level, user-view problems
    and a short options paragraph in the proposal, case flows in the design, and two new
    outputs: the presentation deck (§07) and the build repository starter kit (§08).
  - `/mod-suite` checks readability, names and wording, writes a reader guide in
    INDEX.md, renders diagrams before the Word export, builds the deck and the starter
    kit, and applies later review changes in order when run with a change request.
  - The review checklist has a Mode C readability item.
- Documents never use the section sign: Rule 10 says to write "section 4", templates,
  rules and skills follow it, and `tools/lint_docs.py` reports a section sign as an error.

### Fixed
- `tools/render_mermaid.py` rendered Gantt charts as empty files, because Mermaid sized
  them to a 0-pixel-wide container. It now sets a fixed Gantt width and reports an empty
  image as a failure. `tools/md_to_docx.js` no longer crashes on an empty or invalid PNG;
  it shows the diagram source instead and prints a warning.
- Word asked "This document contains fields that may refer to other files" every time an
  exported `.docx` opened. `tools/md_to_docx.js` no longer sets the update-fields flag. It
  now builds the Table of Contents itself as a linked list of the `##` and `###` headings,
  so the TOC is filled in on open without the prompt (it has no page numbers).

## [0.3.0] - 2026-10-08

### Added
- `tools/render_mermaid.py`: renders every Mermaid diagram of an output folder to PNG in
  `assets/diagrams/`, through a local page opened in any browser. `tools/md_to_docx.js`
  embeds a rendered image in place of the diagram source when one matches the block.
- Eval case `c-tasktrack-modernize` for Mode C: reuses the `a-tasktrack` fixture project
  with scripted modernization interview answers (NestJS/React/PostgreSQL target stack,
  strangler-fig migration, feature dispositions, no budget or dates) and checks for
  planted secrets, feature carry-over from the profile, parity requirements and tests,
  `[DECISION]` for undecided hosting, and invented costs, dates, or organization names.
  No baseline score is recorded yet; it needs a real generation run.
- Eval runner and grader support for prerequisite output: a case may declare a
  `prerequisite` (Mode C: the Mode A profile) that the prompt reuses or builds, `collect`
  stores next to `output/` as `prerequisite/`, and checks address with the
  `prerequisite/` prefix. New `ids_covered` check type (every ID in one file appears in
  another). Mode C citations are verified against the case's `input` project.

## [0.2.0] - 2026-10-08

### Added
- Security policy (`SECURITY.md`) with private vulnerability reporting.
- Code of Conduct (Contributor Covenant 2.1).
- Dependabot security updates for the Word export and GitHub Actions dependencies.
- `AGENTS.md` so other AI agents (for example Codex) can use the repository, and a README
  section on using other AI tools.
- **Mode C (modernize an existing project):** skills, templates, and rules that plan the
  rebuild of a Mode A documented project on a new tech stack: Modernization Brief (with a
  layer-by-layer target stack interview), Current State Assessment, Target Requirements
  Specification (parity requirements), Target System Design (stack comparison, ADRs,
  component and data mappings), Migration Plan (cutover, rollback, decommission),
  Modernization Proposal, Migration Test Plan, and the `/mod-suite` command.
- Linter support for `output/mode-c/`: the modernization brief defines feature IDs,
  `02-target-requirements-specification.md` holds the traceability matrix, and
  `path:line` citations are verified against the brief's source location.

## [0.1.0] - 2026-10-07

### Added
- **Mode A (existing project):** skills, templates, and rules that document an existing
  code base: Project Profile, Completion Plan, Proposal, User / Technical / Developer
  Manuals, repo docs (README, ARCHITECTURE, API), and the `/doc-suite` command that runs
  them all.
- **Mode B (new project):** skills, templates, and rules that document a project before it
  is built: Project Brief interview, Requirements Specification, System Design, Project
  Plan, Proposal, Test Plan, draft manuals, Planned vs Built Gap Report, and the
  `/new-suite` command.
- Shared rules for core principles, writing style, formatting, and the review checklist.
- Document linter (`tools/lint_docs.py`) that checks structure, review markers,
  placeholders, code blocks, Mermaid diagrams, anchors, secrets, Mode A `path:line`
  citations, and Mode B requirement traceability.
- Project hook that lints each document automatically after Claude writes or edits it.
- Eval set with two cases (`a-tasktrack`, `b-clinic-booking`), a grader, a runner, an LLM
  judge rubric, and a recorded baseline (a-tasktrack 100, b-clinic-booking 91.7).
- Word export (`tools/md_to_docx.js`) that converts finished Markdown to `.docx`.
- MIT License, contributing guide, issue forms, and pull request template.
- GitHub Actions workflow that runs the unit tests on Ubuntu and Windows (Python 3.9 and
  3.13) and smoke-tests the Word export.

### Changed
- Mode rules load on demand when a skill runs, instead of at session start.
- Word and PDF export use `tools/md_to_docx.js` instead of the `docx` / `pdf` skill.
- README covers installation, Word export, evals, and status badges.

### Security
- Generated documents under `output/mode-a/` and `output/mode-b/` are ignored by git, so
  client and project details stay out of the repository.

[Unreleased]: https://github.com/strugz/DocumentationCreator/compare/v0.5.0...HEAD
[0.5.0]: https://github.com/strugz/DocumentationCreator/compare/v0.4.0...v0.5.0
[0.4.0]: https://github.com/strugz/DocumentationCreator/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/strugz/DocumentationCreator/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/strugz/DocumentationCreator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/strugz/DocumentationCreator/releases/tag/v0.1.0
