---
name: doc-developer-manual
description: MODE A (existing code). Write the Developer Manual for a fed-in project. It covers the tech stack, repo structure, local setup, architecture, module guide, data model, API reference, coding standards, testing, CI/CD, git workflow, how-to guides, and tech debt. Use when the user asks for a developer manual, developer guide, onboarding guide for engineers, contributor guide, or code documentation.
argument-hint: <project-slug or path>
---

# Developer Manual

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Preconditions
1. Resolve `<slug>`. Run the `doc-intake` procedure if the profile is missing.
2. Read the profile, `mode-a-existing-project/templates/05-developer-manual.md`, and `mode-a-existing-project/rules/40-document-specific.md` section 5.
3. If `output/mode-a/<slug>/04-technical-manual.md` exists, link to its configuration reference
   instead of duplicating it.

## Procedure
1. **Stack and structure:** take versions from manifests and lock files. Annotate the tree
   with one line per folder.
2. **Local setup:** list verified commands only (from scripts, Makefile, CI, README).
   Cover install, env setup, DB setup and seed, run, and test. Add a "Common Setup
   Problems" table from known pitfalls (native deps, ports, env vars without defaults).
3. **Architecture:** identify the patterns actually used (layering, DI container,
   repository/service pattern, state management, middleware) and cite where each one
   lives. Draw one high-level flowchart and one sequence diagram of the main request path.
4. **Module guide:** for each module in the profile, give location, responsibility, key
   symbols with `path:line`, dependencies (imports) and dependents, and gotchas (global
   state, side effects, TODOs).
5. **Data model:** build a Mermaid `erDiagram` from models and migrations. List them,
   and explain how to create a new migration using the project's tool.
6. **API reference:** summarize endpoints in a table. If there are more than about 15
   endpoints or public functions, also run the `doc-repo-files` procedure for `API.md`
   and link to it.
7. **Coding standards:** read the lint, format, and type configs (`.eslintrc*`,
   `.prettierrc*`, `ruff.toml`, `.editorconfig`, `tsconfig.json`, `stylecop`, etc.).
   Document what is enforced. Put observed but unenforced conventions under
   "Recommendations".
8. **Testing:** cover the frameworks, layout, commands, fixtures and mocks, and an example
   modeled on an existing test file.
9. **CI/CD and git:** document pipeline stages from workflow files. Infer the branching and
   commit conventions from `git log --oneline -50` and branch names, and mark them
   `[ASSUMPTION]` unless documented.
10. **How-to guides:** write a worked example for adding a feature end to end, following
    an existing feature's file trail (route → controller → service → model → test → UI).
11. **Tech debt:** list it from the TODO/FIXME scan, dead code, outdated dependencies,
    missing tests, and duplicated logic.

## Output
`output/mode-a/<slug>/05-developer-manual.md` (plus `output/mode-a/<slug>/API.md` if generated)

Run the review checklist. Report the file paths, the module count, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-a/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
