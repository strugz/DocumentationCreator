---
name: doc-user-manual
description: MODE A (existing code). Write the end-user User Manual for a fed-in project. It is task-based, organized per role, non-technical, and includes step-by-step procedures, troubleshooting with exact error messages, FAQ, and glossary. Use when the user asks for a user manual, user guide, end-user documentation, help guide, or training material.
argument-hint: <project-slug or path> [target roles]
---

# User Manual

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`.

## Preconditions
1. Resolve `<slug>`. Run the `doc-intake` procedure if the profile is missing.
2. Read the profile, `mode-a-existing-project/templates/03-user-manual.md`, `rules/10-writing-style.md`, and
   `mode-a-existing-project/rules/40-document-specific.md` §3.

## Procedure
1. **Inventory the UI.** For each user-facing feature in the profile, open its screen,
   page, component, or CLI command. Extract:
   - exact labels of buttons, menus, fields, and page titles (from JSX/templates/i18n files);
   - form fields with their validation rules (required, length, format) from validators/schemas;
   - success and error messages, verbatim;
   - role or permission guards around the screen or action.
   If an i18n/locale file exists (`en.json`, `messages.properties`, `*.resx`), use it as
   the source of UI text.
2. **Map features to user goals.** Group tasks the way a user thinks
   ("Manage orders", "Run reports"), not by code module. Order them by typical workflow:
   first login → daily tasks → occasional tasks → admin tasks.
3. **Roles.** If roles exist, add §3 User Roles and mark "Who can do this" on every task.
   Put admin-only tasks in their own section.
4. **Write each task** using the task block in the template: purpose, who, prerequisites,
   numbered steps (one action each, labels in **bold**), result, tips, errors.
5. **Navigation paths:** derive them from router/menu definitions, e.g.
   **Settings** › **Users** › **Add User**.
6. **Screenshots:** you cannot capture them. Insert placeholders where a screen is first
   introduced: `![Screenshot: <screen>](assets/TBD.png)` + `[TBD: capture screenshot]`.
   If the user approves running the app and a browser is available, you may capture real
   screenshots into `output/mode-a/<slug>/assets/`.
7. **Troubleshooting:** build the table from the error strings you collected. Explain each
   one in plain language and give the fix.
8. **FAQ:** 5–10 questions inferred from validation rules, permissions, and common flows.
9. **Language check:** remove code, file paths, and technical jargon (unless the product is a CLI).

## Output
`output/mode-a/<slug>/03-user-manual.md`

Run the review checklist. Report the file path, the number of tasks documented per role,
the screenshot placeholders, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-a/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
