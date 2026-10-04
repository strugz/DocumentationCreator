---
name: doc-repo-files
description: MODE A (existing code). Generate repository-level docs (README.md, ARCHITECTURE.md, API.md) for a fed-in project, following the templates in mode-a-existing-project/templates/repo/. Use when the user asks for a README, architecture doc, API reference, or GitHub repo docs.
argument-hint: <project-slug or path> [readme|architecture|api|all]
---

# Repository Docs: README / ARCHITECTURE / API

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

Input: `$ARGUMENTS`. Default target: `all`.

## Preconditions
1. Resolve `<slug>`. Run the `doc-intake` procedure if the profile is missing.
2. Read the profile, `mode-a-existing-project/templates/repo/*.md`, and `mode-a-existing-project/rules/40-document-specific.md` (Repo docs).

## Procedure
- **README.md:** overview and purpose, prerequisites (versions from manifests), quickstart
  (verified commands), core usage examples (CLI commands or function calls taken from
  tests or entry points), architecture summary table (Module → Responsibility), test
  command, and license.
- **ARCHITECTURE.md:** annotated directory map, key entry points, a Mermaid data-flow
  diagram plus a narrative, a component interaction table, and external dependencies.
- **API.md:** for each primary public function, class, or HTTP endpoint: `path:line`,
  signature (copied exactly), inputs, output, error conditions (thrown exceptions, HTTP
  status codes from handlers), and a usage snippet (prefer one adapted from an existing test).

These files use the GitHub repo style. They do not need the Document Control block or
Revision History, but the accuracy rules still apply.

## Output
`output/mode-a/<slug>/repo/README.md`, `output/mode-a/<slug>/repo/ARCHITECTURE.md`, `output/mode-a/<slug>/repo/API.md`

Do not write into the source project unless the user explicitly asks you to copy the files there.
