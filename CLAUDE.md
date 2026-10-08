# DocumentationCreator — Project Instructions

This repository is a **documentation factory** with three modes. This repository itself
contains no application code, and Claude never writes application code here.

| Mode | When | Input | Facts come from | Folder | Output |
|------|------|-------|-----------------|--------|--------|
| **A — Existing project** | Code already exists | A folder path, repo, or pasted code | The source code | `mode-a-existing-project/` | `output/mode-a/<slug>/` |
| **B — New project** | Only an idea, no code yet | A description of what to build | The user's brief and interview answers | `mode-b-new-project/` | `output/mode-b/<slug>/` |
| **C — Modernize existing project** | Code exists and is documented by Mode A; the user wants to rebuild, modernize, or optimize it as a new project | A Mode A slug (or a code path, which runs intake first) | The Mode A Project Profile (current system) plus a modernization interview (target stack, strategy, scope) | `mode-c-modernize-project/` | `output/mode-c/<slug>/` |

**Choosing the mode:** a code path or repo → Mode A. "I want to build…", "create a project
like…", or an idea with no path → Mode B. "Modernize / rebuild / migrate / optimize this
project to a new stack", or a Mode A slug with a request for a new version → Mode C. If
unclear, ask once: "Does code for this project already exist, and do you want to document
it as it is or plan a modernized rebuild?"

## Mode A — Document an existing project

| # | Document | Skill | Template (`mode-a-existing-project/templates/`) | Primary audience |
|---|----------|-------|-----------------------------------------------|------------------|
| 0 | Project Profile (evidence base) | `/doc-intake` | `00-project-profile.md` | Internal — feeds all others |
| 1 | Project Completion Plan ("planning to finish") | `/doc-plan` | `01-project-completion-plan.md` | PM, team lead, stakeholders |
| 2 | Project Proposal | `/doc-proposal` | `02-project-proposal.md` | Client, management, approvers |
| 3 | User Manual | `/doc-user-manual` | `03-user-manual.md` | End users, operators |
| 4 | Technical Manual | `/doc-technical-manual` | `04-technical-manual.md` | IT ops, sysadmins, support |
| 5 | Developer Manual | `/doc-developer-manual` | `05-developer-manual.md` | Developers, maintainers |
| + | Repo docs (README / ARCHITECTURE / API) | `/doc-repo-files` | `repo/` | Contributors on GitHub |
| ★ | Everything above, in order | `/doc-suite` | — | — |

## Mode B — Document a new project (before it is built)

| # | Document | Skill | Template (`mode-b-new-project/templates/`) | Primary audience |
|---|----------|-------|------------------------------------------|------------------|
| 0 | Project Brief (evidence base, from interview) | `/new-brief` | `00-project-brief.md` | Internal — feeds all others |
| 1 | Software Requirements Specification | `/new-requirements` | `01-requirements-specification.md` | Client, PM, developers, QA |
| 2 | System Design Document | `/new-design` | `02-system-design.md` | Developers, tech lead |
| 3 | Project Plan (build from zero) | `/new-plan` | `03-project-plan.md` | PM, team lead, stakeholders |
| 4 | Project Proposal (new system) | `/new-proposal` | `04-project-proposal.md` | Client, management, approvers |
| 5 | Test Plan | `/new-test-plan` | `05-test-plan.md` | QA, client UAT users |
| 6–8 | Draft User / Technical / Developer Manuals | `/new-manuals` | Mode A templates `03`–`05` | Same as Mode A |
| 9 | Planned vs Built Gap Report (after code exists) | `/new-gap-check` | `09-gap-report.md` | PM, tech lead |
| ★ | Everything above (0–8), in order | `/new-suite` | — | — |

## Mode C — Modernize an existing project into a new one

| # | Document | Skill | Template (`mode-c-modernize-project/templates/`) | Primary audience |
|---|----------|-------|------------------------------------------------|------------------|
| 0 | Modernization Brief (evidence base: profile + interview) | `/mod-brief` | `00-modernization-brief.md` | Internal — feeds all others |
| 1 | Current State Assessment | `/mod-assessment` | `01-current-state-assessment.md` | Tech lead, sponsor |
| 2 | Target Requirements Specification | `/mod-requirements` | `02-target-requirements-specification.md` | Client, PM, developers, QA |
| 3 | Target System Design | `/mod-design` | `03-target-system-design.md` | Developers, tech lead |
| 4 | Migration Plan | `/mod-plan` | `04-migration-plan.md` | PM, team lead, stakeholders |
| 5 | Modernization Proposal | `/mod-proposal` | `05-modernization-proposal.md` | Client, management, approvers |
| 6 | Migration Test Plan | `/mod-test-plan` | `06-migration-test-plan.md` | QA, client UAT users |
| ★ | Everything above, in order | `/mod-suite` | — | — |

The Mode C interview always asks which **target tech stack** to use, layer by layer, with
the current technology shown next to each. Undecided layers become `[DECISION]` items.

## Workflow (always follow)

1. **Evidence base first.** Mode A depends on `output/mode-a/<slug>/00-project-profile.md`
   (`/doc-intake`). Mode B depends on `output/mode-b/<slug>/00-project-brief.md`
   (`/new-brief`). Mode C depends on `output/mode-c/<slug>/00-modernization-brief.md`
   (`/mod-brief`), which in turn needs the Mode A profile. If it does not exist, create it
   before writing anything else.
2. **Generate from the template.** Copy the matching template's structure. Keep every
   section heading; if a section does not apply, keep the heading and write
   `Not applicable — <one-line reason>.`
3. **Ground every claim.** Mode A: `mode-a-existing-project/rules/30-evidence-and-accuracy.md`.
   Mode B: `mode-b-new-project/rules/30-evidence-from-brief.md`. Mode C:
   `mode-c-modernize-project/rules/30-evidence-from-profile.md`. Never invent features,
   numbers, dates, costs, names, or endpoints. In Modes B and C, label Claude's
   suggestions **Proposed**. In Mode C, keep the current system (present tense, code
   evidence) apart from the target system (future tense, brief evidence).
4. **Self-review.** Run `python tools/lint_docs.py output/<mode>/<slug>` (the mechanical
   checks) and fix every error, then review the judgment items in
   `rules/50-review-checklist.md` before reporting done.
5. **Report.** Tell the user which files were written, and list every `[TBD]`,
   `[ASSUMPTION]`, `[VERIFY]`, and (Modes B and C) `[DECISION]` marker that needs their input.

## Rules (mandatory)

Shared by both modes (always loaded):

@rules/00-core-principles.md
@rules/10-writing-style.md
@rules/20-formatting.md
@rules/50-review-checklist.md

Mode-specific rules are **not** loaded up front; the skills read them when they run.
Before writing or editing any document outside a skill, read the active mode's rules first:

| Mode | Evidence rule | Document rules |
|------|---------------|----------------|
| A | `mode-a-existing-project/rules/30-evidence-and-accuracy.md` | `mode-a-existing-project/rules/40-document-specific.md` |
| B | `mode-b-new-project/rules/30-evidence-from-brief.md` | `mode-b-new-project/rules/40-document-specific.md` |
| C | `mode-c-modernize-project/rules/30-evidence-from-profile.md` | `mode-c-modernize-project/rules/40-document-specific.md` |

The non-negotiables from those rules, in short: never invent features, numbers, dates,
costs, or names; mark every gap with `[TBD]`, `[ASSUMPTION]`, `[VERIFY]` (and in Modes B
and C, `[DECISION]`); in Modes B and C label Claude's own suggestions **Proposed** and
never describe the planned system as already built; in Mode C never describe a current
feature that the profile does not list.

## Automated checks

`tools/lint_docs.py` performs the mechanical part of Rule 50 (structure, markers in Open
Items, placeholders, code-block tags, Mermaid, anchors, secrets, Mode A and C `path:line`
citations, Mode B and C requirement traceability). A project hook (`.claude/settings.json`)
runs it automatically after every Write/Edit under `output/mode-*/` and reports errors
back. Fix every reported error before moving on. Run it on the whole folder at the end:

```bash
python tools/lint_docs.py output/<mode>/<slug>
```

Rule 50's judgment items (audience, tone, accuracy against evidence) remain a manual
review.

## Directory Conventions

- `rules/` — writing and review rules shared by both modes.
- `mode-a-existing-project/` — Mode A templates and rules.
- `mode-b-new-project/` — Mode B templates and rules.
- `mode-c-modernize-project/` — Mode C templates and rules.
- `.claude/skills/` — the slash-command skills (`doc-*` = Mode A, `new-*` = Mode B,
  `mod-*` = Mode C).
- `projects/` — optional drop zone for Mode A input projects (read-only).
- `output/mode-a/<slug>/`, `output/mode-b/<slug>/`, and `output/mode-c/<slug>/` —
  generated documents.

Never modify files inside a project being documented. Write only to `output/`.
