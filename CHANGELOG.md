# Changelog

All notable changes to this project are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version
numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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

[Unreleased]: https://github.com/strugz/DocumentationCreator/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/strugz/DocumentationCreator/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/strugz/DocumentationCreator/releases/tag/v0.1.0
