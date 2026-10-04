# Rule 30 — Evidence and Accuracy

> **Scope: Mode A only (project with existing code).** Mode B uses `mode-b-new-project/rules/`.

## Evidence hierarchy (strongest first)
1. Source code, schemas, migrations, and configuration files.
2. Tests: they describe intended behavior.
3. Build, CI, container, and infrastructure files (`package.json`, `pyproject.toml`,
   `Dockerfile`, `docker-compose.yml`, `.github/workflows/`, Terraform, etc.).
4. Existing docs, comments, commit messages, issue or TODO notes.
5. Information the user states in chat.
6. Reasonable inference. This must always be marked (see below).

If two sources conflict, trust the stronger source, and record the conflict in the
profile's **Discrepancies** section.

## Markers (use exactly these forms)
| Marker | Meaning | Example |
|--------|---------|---------|
| `[TBD: ...]` | Information needed but not in the evidence. A human must supply it. | `[TBD: project budget]` |
| `[ASSUMPTION: ...]` | Inferred from indirect evidence; plausible but unconfirmed. | `[ASSUMPTION: deployed on a single VM, based on docker-compose.yml]` |
| `[VERIFY: ...]` | Found in evidence but possibly stale or contradictory. | `[VERIFY: README says Node 16, package.json engines says >=20]` |

- Never remove a marker unless the evidence or the user resolves it.
- Every document ends with an **Open Items** section that lists all its markers.

## Never invent
- Costs, budgets, prices, rates, or effort hours (estimates are allowed only when
  labeled as estimates with the method shown, e.g. story points × velocity).
- Dates, deadlines, or milestones not given by the user or the evidence.
- Names of people, clients, organizations, or stakeholders.
- Performance figures, user counts, SLAs, or uptime.
- Features, endpoints, CLI flags, config keys, or screens that do not exist in code.
  Planned features must be labeled **Planned** and cite their source (TODO, issue, user).
- Screenshots or UI text you have not seen in the code.

## Verification habits
- For every endpoint, command, or config key you document, open the file that defines it.
- For every install or run command, confirm it from scripts, a Makefile, or CI.
  If not confirmed, mark `[VERIFY]`.
- Record the source revision (`git rev-parse --short HEAD`) in the Document Control block.
