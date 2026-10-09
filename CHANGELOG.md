# Changelog

All notable changes to this project are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version
numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/strugz/DocumentationCreator/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/strugz/DocumentationCreator/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/strugz/DocumentationCreator/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/strugz/DocumentationCreator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/strugz/DocumentationCreator/releases/tag/v0.1.0
