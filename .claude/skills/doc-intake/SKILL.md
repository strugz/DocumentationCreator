---
name: doc-intake
description: MODE A (existing code). Analyze a software project the user feeds in (folder path, repo, or pasted material) and build the evidence base output/mode-a/<slug>/00-project-profile.md that every other documentation skill depends on. Use when the user says "here is my project", "analyze this project", "document <path>", or before any other doc-* skill when no profile exists.
argument-hint: <path-to-project> [project name]
---

# Project Intake → Project Profile

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`. Expect a project path (absolute, or relative to `projects/`), and
optionally a product name. If no path is given, ask for one. That is the only question
you ask up front.

Follow `CLAUDE.md`, the shared `rules/`, and the Mode A rules in `mode-a-existing-project/rules/`. The source project is **read-only**.

## Step 1 — Locate and identify
1. Resolve the path. If it is under `projects/`, use that. Confirm it exists.
2. Derive `<slug>` (lowercase-kebab-case of the product name or folder name).
3. Create `output/mode-a/<slug>/` and `output/mode-a/<slug>/assets/`.
4. Record the source revision: `git -C <path> rev-parse --short HEAD`. If the folder is not
   a git repo, use "working copy, <today>".

## Step 2 — Survey (breadth first)
Read in this order. Stop expanding a branch once its purpose is clear.
1. Root listing, plus existing docs (`README*`, `docs/`, `CHANGELOG*`, `LICENSE`).
2. Manifests: `package.json`, `pyproject.toml`, `requirements*.txt`, `pom.xml`,
   `build.gradle`, `*.csproj`, `go.mod`, `Cargo.toml`, `composer.json`, `Gemfile`.
3. Runtime and infra: `Dockerfile`, `docker-compose*.yml`, `Makefile`, `Procfile`,
   `.github/workflows/`, `azure-pipelines.yml`, `.gitlab-ci.yml`, Terraform or Bicep, `k8s/`.
4. Config: `.env.example`, `appsettings*.json`, `config/`, `settings.py`.
5. Entry points: `main.*`, `index.*`, `app.*`, `server.*`, `Program.cs`, `manage.py`,
   CLI definitions, route registrations.
6. Domain: models, schemas, migrations, routes and controllers, UI pages and components.
7. Tests: layout, frameworks, skipped tests (`skip`, `xit`, `@Ignore`, `pytest.mark.skip`).

For large projects (more than ~300 source files), spawn parallel `Explore` agents, one per
top-level area (frontend / backend / infra / tests). Each one returns structured findings
for the profile sections.

## Step 3 — Targeted scans (use Grep)
| Purpose | Pattern (adapt to the language) |
|---------|---------------------------------|
| Incomplete work | `TODO\|FIXME\|HACK\|XXX\|NotImplemented\|not implemented` |
| Env / config reads | `process\.env\|os\.environ\|getenv\|Environment\.GetEnvironmentVariable\|config\.get\|ConfigurationManager` |
| HTTP routes | `@(Get\|Post\|Put\|Delete\|Patch)\|app\.(get\|post\|put\|delete)\|router\.\|@app\.route\|path\(\|Route\(` |
| Roles / permissions | `role\|permission\|isAdmin\|authorize\|@PreAuthorize\|policy` |
| User-facing errors | `toast\|alert\(\|flash\|ValidationError\|errorMessage\|message:` |
| Scheduled jobs | `cron\|schedule\|setInterval\|celery\|Hangfire\|BackgroundService` |
| Secrets risk (do NOT copy values) | `password\s*=\|api[_-]?key\|secret\|token\s*=` |

## Step 4 — Write the profile
Fill `mode-a-existing-project/templates/00-project-profile.md` completely and write it to
`output/mode-a/<slug>/00-project-profile.md`.
- Every row gets an evidence cite (`path:line`) where applicable.
- Features Inventory: assign stable IDs (F-01, F-02, ...). All other documents reuse them.
- Status values: Done / Partial / Stub / Not started / Broken / Planned.
- Fill the Glossary with the canonical terms taken from code (model names, UI labels).
- Put anything the code cannot tell you (client, budget, deadline, team, stakeholders)
  in §2 as `[TBD]`, and add it to §19 Open Questions.

## Step 5 — Report
Give the user:
1. A 5-line summary: what the project is, its stack, maturity, and feature count by status.
2. The **Open Questions** list. Ask the user to answer what they can. Explain that
   answers improve the Plan and the Proposal most (dates, budget, client, team).
3. The next step: `/doc-suite <slug>` for everything, or an individual `/doc-*` skill.

**Automated check:** run `python tools/lint_docs.py output/mode-a/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
