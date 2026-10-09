# DocumentationCreator

[![Tests](https://github.com/strugz/DocumentationCreator/actions/workflows/tests.yml/badge.svg)](https://github.com/strugz/DocumentationCreator/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

A Claude Code workspace that produces professional, evidence-based software documentation
in three modes:

| Mode | You have | You give Claude | You get |
|------|----------|-----------------|---------|
| **A — Existing project** | Working or partial code | A project folder path | Completion Plan, Proposal, User / Technical / Developer Manuals, repo docs, all grounded in the code |
| **B — New project** | Only an idea | A description of what you want to build | Project Brief, Requirements Specification, System Design, Project Plan, Proposal, Test Plan, draft manuals |
| **C — Modernize existing project** | Code documented with Mode A, and the wish to rebuild it on a new stack | The Mode A slug, then answers about the target tech stack and what to keep, improve, replace, or drop | Modernization Brief, Current State Assessment, Target Requirements, Target System Design, Migration Plan, Modernization Proposal, Migration Test Plan |

Nothing is invented. Anything the evidence cannot tell you (budget, deadline, client,
names) is marked `[TBD]`. In Modes B and C, Claude's own suggestions are labeled
**Proposed**, and choices you must make are marked `[DECISION]`.

## Prerequisites
| Tool | Needed for | Required? |
|------|------------|-----------|
| [Claude Code](https://claude.com/claude-code) (CLI, desktop app, or IDE extension) | Running the skills. Other AI agents work too; see [Using Other AI Tools](#using-other-ai-tools) | Yes, or another agent |
| Python 3.9 or later | The document linter and its auto-lint hook (`tools/lint_docs.py`) | Yes |
| `git` | Recording the source revision in Mode A documents | Optional |
| Node.js 18 or later | Exporting documents to Word (`tools/md_to_docx.js`) and the proposal to PowerPoint (`tools/md_to_pptx.js`) | Optional |

Mode A also needs read access to the project you want to document.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/strugz/DocumentationCreator.git
   ```
2. Optional: install the Word export dependency:
   ```bash
   cd DocumentationCreator/tools && npm install
   ```
3. Open the `DocumentationCreator` folder in Claude Code. The skills in `.claude/skills/`
   and the lint hook in `.claude/settings.json` load automatically. The first time, Claude
   Code asks you to trust the folder and approve the project hook.

The linter uses only the Python standard library, so there is nothing to `pip install`.

## Quickstart
1. Open this folder in Claude Code (or open it in the desktop app):
   ```bash
   cd DocumentationCreator
   claude
   ```
2. Pick your mode:
   ```text
   /doc-suite D:/path/to/your-project
   ```
   ```text
   /new-suite An online ordering system for a bakery with customer accounts, order tracking, and a daily production report
   ```
   ```text
   /mod-suite your-project
   ```
3. Answer the questions Claude asks (one round), or reply `continue` / `use defaults`.
   In Mode C the questions always include the target tech stack, layer by layer.
4. Collect the results from `output/mode-a/<slug>/`, `output/mode-b/<slug>/`, or
   `output/mode-c/<slug>/`.

> [!NOTE]
> Generated documents are ignored by git (see `.gitignore`), so your project and client
> documents stay on your machine. Only the empty `output/mode-a/`, `output/mode-b/`, and
> `output/mode-c/` folders are tracked. To keep your documents in version control, store
> them in a separate private repository.

You can also ask in plain language, for example "Create a user manual for the project in
D:/work/inventory-system" (Mode A), "I want to build a leave request system for our HR
team, create the documents" (Mode B), or "Modernize the inventory system on a new stack
and plan the migration" (Mode C). The matching skills trigger automatically.

## Commands

### Mode A — Existing project (`doc-*`)
| Command | What it does | Output |
|---------|--------------|--------|
| `/doc-intake <path> [name]` | Analyzes the code and builds the evidence base | `00-project-profile.md` |
| `/doc-plan <slug> [deadline/team]` | Project Completion Plan | `01-project-completion-plan.md` |
| `/doc-proposal <slug> [client/budget] [--format pptx]` | Project Proposal, optionally as PowerPoint slides | `02-project-proposal.md`, `export/*-Slides.pptx` |
| `/doc-user-manual <slug> [roles]` | User Manual | `03-user-manual.md` |
| `/doc-technical-manual <slug> [env]` | Technical Manual | `04-technical-manual.md` |
| `/doc-developer-manual <slug>` | Developer Manual | `05-developer-manual.md` |
| `/doc-repo-files <slug> [readme\|architecture\|api\|all]` | GitHub-style repo docs | `repo/*.md` |
| `/doc-suite <path> [change] [--only ...] [--format docx\|pdf\|pptx]` | All of the above, plus a consistency review. Run it again with a change (answers, decision, new code, scope, wording, names) to update every document | everything + `INDEX.md` |

### Mode B — New project (`new-*`)
| Command | What it does | Output |
|---------|--------------|--------|
| `/new-brief <idea> [name]` | Interviews you once and records the idea | `00-project-brief.md` |
| `/new-requirements <slug>` | Software Requirements Specification | `01-requirements-specification.md` |
| `/new-design <slug> [stack/hosting]` | System Design Document | `02-system-design.md` |
| `/new-plan <slug> [start/deadline/team]` | Project Plan (build from zero) | `03-project-plan.md` |
| `/new-proposal <slug> [client/budget/rates] [--format pptx]` | Project Proposal (new system), optionally as PowerPoint slides | `04-project-proposal.md`, `export/*-Slides.pptx` |
| `/new-test-plan <slug>` | Test Plan with UAT scenarios | `05-test-plan.md` |
| `/new-manuals <slug> [user\|technical\|developer\|all]` | Draft manuals for the planned system | `06`–`08` |
| `/new-suite <idea> [change] [--only ...] [--no-manuals] [--format docx\|pdf\|pptx]` | All of the above, plus a traceability review. Builds a starter kit for the new code repository when the brief lists it. Run it again with a change (answers, decision, scope, wording, names) to update every document | everything + `INDEX.md` |
| `/new-gap-check <slug> <code-path>` | After the build: planned vs built (Mode B or C slug) | `09-gap-report.md` |

### Mode C — Modernize an existing project (`mod-*`)
| Command | What it does | Output |
|---------|--------------|--------|
| `/mod-brief <mode-a slug or path> [name]` | Reads the Mode A profile and interviews you about the target stack, migration strategy, and feature dispositions | `00-modernization-brief.md` |
| `/mod-assessment <slug>` | Current State Assessment with severity-rated findings and a keep list | `01-current-state-assessment.md` |
| `/mod-requirements <slug>` | Target Requirements Specification with parity requirements | `02-target-requirements-specification.md` |
| `/mod-design <slug> [stack/hosting]` | Target System Design with stack comparison, ADRs, and old-to-new mappings | `03-target-system-design.md` |
| `/mod-plan <slug> [start/deadline/team]` | Migration Plan with cutover, rollback, and decommission | `04-migration-plan.md` |
| `/mod-proposal <slug> [client/budget/rates]` | Modernization Proposal with options considered | `05-modernization-proposal.md` |
| `/mod-test-plan <slug>` | Migration Test Plan with parity, data migration, and cutover tests | `06-migration-test-plan.md` |
| `/mod-suite <mode-a slug or path> [change] [--only ...] [--format docx\|pdf]` | All of the above, plus a Tech Stack Questionnaire for stakeholders and developers (`07-tech-stack-questionnaire.md`), in plain, readable form (Read This First pages, case and SDLC flows), plus a traceability review, Word files, a presentation deck and a starter kit for the new code repository. Run it again with a change (decision, scope, wording, names) or the returned questionnaire answers to update every document and slide | everything + `INDEX.md`, `deck/`, `<repo>-repo-starter/` |

### Examples
```text
/doc-intake D:/work/inventory-system "Inventory Management System"
/doc-plan inventory-management-system deadline 2026-12-15, 2 developers, 2-week sprints
/doc-suite D:/work/inventory-system --only user,technical --format docx

/new-brief A mobile-friendly web app for field technicians to log site visits with photos
/new-plan field-visit-tracker start 2026-11-02, 3 developers, deadline 2027-03-31
/new-suite A leave request and approval system for 150 employees --format docx
/new-gap-check field-visit-tracker D:/work/field-visit-tracker

/mod-brief inventory-management-system target: .NET 8 backend, React frontend, keep SQL Server
/mod-suite inventory-management-system --format docx
```

## How It Works

```mermaid
flowchart LR
    subgraph A["Mode A — existing project"]
        C[Your code<br/>read-only] --> AI["/doc-intake"] --> PF[(Project Profile)]
        PF --> AD[Plan · Proposal · Manuals · Repo docs]
    end
    subgraph B["Mode B — new project"]
        ID[Your idea] --> BI["/new-brief<br/>interview"] --> BR[(Project Brief)]
        BR --> BD[Requirements · Design · Plan · Proposal · Test Plan · Draft manuals]
    end
    subgraph C["Mode C — modernize existing project"]
        PF --> CI["/mod-brief<br/>stack interview"] --> MB[(Modernization Brief)]
        MB --> CD[Assessment · Target Requirements · Target Design · Migration Plan · Proposal · Test Plan]
    end
    BD -. "code gets built" .-> GC["/new-gap-check"]
    CD -. "new code gets built" .-> GC
    GC -.-> AI
```

1. **Evidence base:** Mode A scans the code into a **Project Profile**. Mode B interviews
   you into a **Project Brief**. Mode C copies the profile and interviews you into a
   **Modernization Brief**. Every other document reuses these facts.
2. **Documents:** each skill fills its template. Mode A cites code (`path:line`). Modes B
   and C trace everything to requirement IDs (`FR-01`, `NFR-01`); Mode C also keeps the
   profile's feature IDs and adds assessment findings (`D-01`).
3. **Review:** every document passes `rules/50-review-checklist.md`. The suites also check
   cross-document consistency (and, in Modes B and C, requirement traceability).

### Markers
| Marker | Meaning |
|--------|---------|
| `[TBD: ...]` | Not in the evidence. A human must supply it (budget, dates, names). |
| `[ASSUMPTION: ...]` | Inferred, so please confirm. |
| `[VERIFY: ...]` | Sources conflict, may be stale, or must be confirmed after the build. |
| `[DECISION: ...]` | Modes B and C: you must choose between options. A recommendation is given. |
| **Proposed** | Modes B and C: Claude's suggestion, with a reason. |
| **Keep / Improve / Replace / Drop / New** | Mode C: what happens to each current feature in the target system. |

Each document ends with an **Open Items** table. `INDEX.md` consolidates them all.

## Automated Checks

`tools/lint_docs.py` checks the mechanical parts of the review checklist so the model
does not have to grade itself on them:

| Check | What it catches |
|-------|-----------------|
| structure | Missing Document Control fields, H1 count, skipped heading levels, Table of Contents gaps, missing Open Items / Revision History |
| markers | `[TBD]` / `[ASSUMPTION]` / `[VERIFY]` / `[DECISION]` markers that are not listed in Open Items |
| placeholders | Unfilled `{{...}}` template placeholders, leftover template comments, the section sign (write "section N") |
| code / mermaid | Code blocks without a language tag, unclosed fences, invalid or oversized Mermaid diagrams |
| links | `#anchors` that match no heading |
| secrets | Passwords, keys, tokens, connection strings with credentials |
| citations (Modes A and C) | `path:line` references to files or lines that do not exist in the source |
| ids / trace (Modes B and C) | Undefined `F-xx` / `FR-xx` references; Must/Should requirements missing from the Design, Plan, Test Plan, or Traceability Matrix |

It runs automatically after every document write (hook in `.claude/settings.json`). You
can also run it yourself:

```bash
python tools/lint_docs.py output/mode-b/my-app
```

```bash
python -m unittest discover -s tests
```

## Exporting to Word
Markdown is the master format. To produce `.docx` files from a finished output folder:

```bash
node tools/md_to_docx.js output/mode-b/my-app
```

The files are written to `output/<mode>/<slug>/export/`. Review markers are highlighted.
Mermaid diagrams appear as source with a note, unless you render them first:

```bash
python tools/render_mermaid.py output/mode-b/my-app
```

The script prints a local URL; open it in any browser and it renders every diagram (with
Mermaid from the jsDelivr CDN) to `output/<mode>/<slug>/assets/diagrams/`. The Word export
then embeds those images. Re-run it after a diagram changes. For PDF, open the `.docx` in Word and save
as PDF. The suites do this for you when you pass `--format docx` or `--format pdf`.

## Exporting the Proposal to PowerPoint
In Modes A and B, pass `--format pptx` to `/doc-proposal`, `/new-proposal`, or a suite, or
ask for the proposal as slides, or run `/proposal-slides <slug>` on a finished proposal.
The repository's own exporter builds the deck in three steps:

```bash
node tools/md_to_pptx.js output/mode-b/my-app --draft
```

```bash
node tools/md_to_pptx.js output/mode-b/my-app --strict
```

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File tools/pptx_to_png.ps1 `
  -Path output/mode-b/my-app/export/My-App-Project-Proposal-Slides.pptx
```

1. `--draft` writes the slide spec `deck/proposal-slides.json` from the proposal: about 12
   slides in the proposal's order, with the section text as speaker notes. Claude then
   shortens the slide text for approvers and keeps every fact and review marker.
2. The build writes `export/<Product>-Project-Proposal-Slides.pptx` with Rule 25 fonts and
   colours. `--strict` fails on long titles, crowded slides, missing notes, and markers or
   figures the proposal does not contain.
3. `tools/pptx_to_png.ps1` renders every slide with PowerPoint so each one can be checked.

The rules are in [`rules/60-proposal-slides.md`](rules/60-proposal-slides.md). Mode C builds
its own presentation deck in `/mod-suite`.

## Measuring Quality (Evals)
If you change a rule, template, or skill, run the eval set before and after the change
and compare the scores. Two fixture cases (one per mode) test that Claude does not invent
features, copy secrets, or fill in budgets it was never given.

```bash
python evals/run_evals.py run all
```

See [`evals/README.md`](evals/README.md) for the scoring layers and the baseline.

> [!NOTE]
> `evals/cases/a-tasktrack/project/.env` contains **fake, deliberately planted** secrets.
> The eval checks that they never appear in generated documents. They are not real
> credentials.

## Repository Structure

```text
DocumentationCreator/
├── CLAUDE.md                     # Master instructions (both modes, imports all rules)
├── AGENTS.md                     # Same instructions for other AI agents (Codex and others)
├── README.md                     # This file
├── rules/                        # Shared rules (both modes)
│   ├── 00-core-principles.md
│   ├── 10-writing-style.md
│   ├── 15-response-and-code-output.md
│   ├── 20-formatting.md
│   ├── 25-typography.md
│   ├── 35-readability.md         # Read This First, In short notes, process flows
│   ├── 45-estimation-and-release-gate.md  # Modes A and B: sizes, AI factor, gate
│   ├── 50-review-checklist.md
│   ├── 55-applying-changes.md    # Modes A and B: update an existing suite
│   └── 60-proposal-slides.md     # Modes A and B: proposal as PowerPoint (not preloaded)
├── mode-a-existing-project/      # MODE A — document existing code
│   ├── README.md
│   ├── rules/                    #   30 evidence (code), 40 document rules
│   └── templates/                #   00-profile … 05-developer-manual, repo/
├── mode-b-new-project/           # MODE B — document a project before it is built
│   ├── README.md
│   ├── rules/                    #   30 evidence (brief), 40 document rules
│   └── templates/                #   00-brief … 05-test-plan, 09-gap-report
├── mode-c-modernize-project/     # MODE C — plan the modernized rebuild of a Mode A project
│   ├── README.md
│   ├── rules/                    #   30 evidence (profile + brief), 40 document rules
│   └── templates/                #   00-modernization-brief … 06-migration-test-plan
├── .claude/skills/
│   ├── doc-*/                    #   Mode A skills (intake, plan, proposal, manuals, repo, suite)
│   ├── new-*/                    #   Mode B skills (brief, requirements, design, plan, proposal,
│   │                             #   test-plan, manuals, suite, gap-check)
│   └── mod-*/                    #   Mode C skills (brief, assessment, requirements, design, plan,
│                                 #   proposal, test-plan, suite)
├── tools/
│   ├── lint_docs.py              # Automated Rule 50 checks (run on any output folder)
│   ├── md_to_docx.js             # Markdown → Word export (needs `npm install` in tools/)
│   ├── md_to_pptx.js             # Proposal → PowerPoint slides (Modes A and B)
│   ├── pptx_to_png.ps1           # Renders slides to PNG with PowerPoint for checking
│   ├── render_mermaid.py         # Renders Mermaid diagrams to PNG for the Word export
│   └── hooks/lint_on_write.py    # Hook: lints each document as Claude writes it
├── evals/                        # Eval cases, grader, and baseline scores
├── tests/                        # Unit tests for the linter and grader
├── .claude/settings.json         # Registers the lint hook (shared with the team)
├── projects/                     # (optional) drop Mode A projects here
└── output/                       # Generated documents (git-ignored)
    ├── mode-a/<project-slug>/    # Generated Mode A documentation
    ├── mode-b/<project-slug>/    # Generated Mode B documentation
    └── mode-c/<project-slug>/    # Generated Mode C documentation
```

## Architecture Summary

| Module | Responsibility |
|--------|----------------|
| `CLAUDE.md` | Entry point. Defines the three modes and the workflow, and imports the rules |
| `rules/` | Shared standards: principles, style, response and code output, formatting, typography, QA checklist |
| `mode-a-existing-project/` | Mode A templates and evidence rules (code is the source of truth) |
| `mode-b-new-project/` | Mode B templates and evidence rules (the brief is the source of truth) |
| `mode-c-modernize-project/` | Mode C templates and evidence rules (the Mode A profile for the current system, the modernization brief for the target) |
| `.claude/skills/` | Step-by-step procedures Claude runs for each document |
| `projects/` | Mode A input staging area (read-only to Claude) |
| `output/` | Generated documents, assets, and exports, separated by mode |
| `tools/` | Deterministic checks (`lint_docs.py`) and the hook that runs them |

## Customizing
- **Change the house style or sections:** edit the templates in
  `mode-a-existing-project/templates/`, `mode-b-new-project/templates/`, or
  `mode-c-modernize-project/templates/`.
- **Change writing standards:** edit `rules/` (shared) or the mode's own `rules/` folder.
  They load automatically through `CLAUDE.md`.
- **Add a new document type:** add a template to the mode's `templates/`, add
  `.claude/skills/<name>/SKILL.md` (copy an existing skill of the same mode), add a
  section to that mode's `rules/40-document-specific.md`, and register it in `CLAUDE.md`
  and in the mode's suite skill (`doc-suite`, `new-suite`, or `mod-suite`).
- **PowerPoint proposal:** pass `--format pptx` to a proposal skill or suite in Mode A or
  B, or ask "export the proposal to PowerPoint". See
  [Exporting the Proposal to PowerPoint](#exporting-the-proposal-to-powerpoint).
- **Word/PDF output:** pass `--format docx` or `--format pdf` to either suite, or ask
  "export the proposal to Word". See [Exporting to Word](#exporting-to-word).

## Tips for Best Results
- Give business context up front (client, purpose, deadline, team size, budget). It
  turns most `[TBD]`s in the Plan and Proposal into real content.
- Mode B: the more detail in your idea (users, must-have features, platform), the fewer
  interview questions. Attach existing forms or spreadsheets. They are good evidence.
- Mode A: permission to run the app lets Claude capture real screenshots for the User Manual.
- From B to A: when development is done, run `/new-gap-check`, then `/doc-suite` on the
  code for the final manuals.
- From A to C: run `/doc-suite` (or at least `/doc-intake`) on the current code first.
  The better the profile, the better the assessment and the parity requirements. Tell
  Claude your team's skills and any must-use or must-avoid technologies; it turns most
  stack `[DECISION]`s into agreed choices.

## Using Other AI Tools
The repository is built for Claude Code, but the templates, rules, skills, and tools are
plain Markdown and scripts that any AI coding agent can follow. `AGENTS.md` gives other
agents (for example Codex) the same instructions that `CLAUDE.md` gives Claude Code.

| Feature | Claude Code | Other agents |
|---------|-------------|--------------|
| Project instructions | `CLAUDE.md` loads automatically | Agents that read `AGENTS.md` load it automatically. Otherwise, tell the agent to read `AGENTS.md` first |
| Rules | Imported by `CLAUDE.md` | `AGENTS.md` tells the agent to open each rule file |
| Commands | `/doc-suite <path>`, `/new-suite <idea>`, `/mod-suite <slug>`, … | Ask in words, for example "Follow `.claude/skills/doc-suite/SKILL.md` for `D:/work/app`" |
| Linting | Runs automatically after every write (hook) | The agent runs `python tools/lint_docs.py output/<mode>/<slug>` itself |
| Interview questions (Modes B and C) | Can use a multiple-choice prompt | Asked in a normal chat message |
| Evals | `python evals/run_evals.py run all` | Use the manual route: `prompt`, run it in the agent, then `collect` (see [`evals/README.md`](evals/README.md)) |

> [!NOTE]
> The eval baseline was measured with Claude. Document quality with other agents has not
> been measured. Run the evals with your agent before relying on it.

## Contributing
Contributions are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for setup, where each
kind of change lives, and how to test it with the unit tests and evals.

## License
Released under the [MIT License](LICENSE). You may use, copy, modify, and share this
repository, including for commercial work, as long as you keep the copyright notice.
Documents you generate with it belong to you.
