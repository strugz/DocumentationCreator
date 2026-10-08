# DocumentationCreator — Agent Instructions

These instructions are for AI coding agents other than Claude Code (for example Codex).
Claude Code reads `CLAUDE.md` instead. Both files point to the same rules, templates, and
skills, so the documents come out the same either way.

This repository is a **documentation factory**. It contains no application code, and you
never write application code here. You write Markdown documents into `output/` only.

## Read these files first, every session

1. `CLAUDE.md` — the modes, the document list, and the workflow. Where it says "Claude",
   read "you". Where it names a slash command such as `/doc-suite`, see
   [Running a skill](#running-a-skill).
2. The shared rules, in this order. They are mandatory:
   - `rules/00-core-principles.md`
   - `rules/10-writing-style.md`
   - `rules/20-formatting.md`
   - `rules/50-review-checklist.md`

`CLAUDE.md` loads these rules with `@rules/...` lines. Your tool may not follow those
imports, so open each file yourself.

Each skill tells you to read the mode's own rules before you start
(`mode-a-existing-project/rules/`, `mode-b-new-project/rules/`, or
`mode-c-modernize-project/rules/`). Do that too.

## Choosing the mode

| Mode | When | Facts come from | Output |
|------|------|-----------------|--------|
| **A — Existing project** | The user gives a folder path, repo, or code | The source code | `output/mode-a/<slug>/` |
| **B — New project** | The user describes an idea and there is no code yet | The user's brief and interview answers | `output/mode-b/<slug>/` |
| **C — Modernize existing project** | The user wants to rebuild, modernize, or migrate an existing (Mode A documented) project to a new stack | The Mode A Project Profile plus a modernization interview (target stack, strategy, scope) | `output/mode-c/<slug>/` |

If it is unclear, ask once: "Does code for this project already exist, and do you want to
document it as it is or plan a modernized rebuild?"

## Running a skill

Each document is produced by a skill: a step-by-step procedure in
`.claude/skills/<name>/SKILL.md`. Your tool may not have slash commands, so run a skill by
reading its file and following every step in order.

| The user says | You do |
|---------------|--------|
| `/doc-suite D:/work/app` or "document this project" | Read `.claude/skills/doc-suite/SKILL.md` and follow it with input `D:/work/app` |
| `/new-suite <idea>` or "I want to build…" | Read `.claude/skills/new-suite/SKILL.md` and follow it with the idea as input |
| `/mod-suite <slug>` or "modernize this project" | Read `.claude/skills/mod-suite/SKILL.md` and follow it with the Mode A slug (or code path) as input |
| `/<skill-name> <input>` | Read `.claude/skills/<skill-name>/SKILL.md` and follow it with that input |

The full list of skills is in the tables in `CLAUDE.md` and `README.md`.

Translate these Claude Code features as follows:

| In a skill file | What you do |
|-----------------|-------------|
| `$ARGUMENTS` | The text the user gave after the command, or the input from their request |
| "Use the `AskUserQuestion` tool" | Ask the same questions in a normal chat message and wait for the answer (Mode C: list the stack options per layer with the current technology and your recommendation) |
| A suite step that names another skill's `SKILL.md` | Read that file and follow it before moving on |

## Checking your work

Claude Code runs the linter automatically after every write. Your tool does not, so run
it yourself after you write or edit any document:

```bash
python tools/lint_docs.py output/<mode>/<slug>
```

Fix every error it reports. Then review the judgment items in
`rules/50-review-checklist.md` before you report that you are done.

## Non-negotiables

- Never invent features, numbers, dates, costs, names, or endpoints. Mark every gap with
  `[TBD]`, `[ASSUMPTION]`, `[VERIFY]`, and in Modes B and C `[DECISION]`.
- In Modes B and C, label your own suggestions **Proposed** and never describe the planned
  system as already built. In Mode C, keep the current system (present tense, code
  evidence) apart from the target system (future tense, brief evidence).
- Never copy secrets, credentials, or personal data into a document.
- Never modify the project being documented. Write only to `output/`.
- Do not edit the fixture project in `evals/cases/`. Its flaws are deliberate.
