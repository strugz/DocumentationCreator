# Changelog

All notable changes to this project are recorded in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Version
numbers follow [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Security policy (`SECURITY.md`) with private vulnerability reporting.
- Code of Conduct (Contributor Covenant 2.1).

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

[Unreleased]: https://github.com/strugz/DocumentationCreator/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/strugz/DocumentationCreator/releases/tag/v0.1.0
