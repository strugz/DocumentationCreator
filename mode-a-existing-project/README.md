# Mode A — Existing Project

Use this mode when **code already exists**. Claude reads the project (read-only) and
documents what is actually there. Every claim cites the code (`path:line`).

## Commands
| Command | Output (`output/mode-a/<slug>/`) |
|---------|----------------------------------|
| `/doc-intake <path> [name]` | `00-project-profile.md` (evidence base) |
| `/doc-plan <slug> [deadline/team]` | `01-project-completion-plan.md` |
| `/doc-proposal <slug> [client/budget]` | `02-project-proposal.md` |
| `/doc-user-manual <slug> [roles]` | `03-user-manual.md` |
| `/doc-technical-manual <slug> [env]` | `04-technical-manual.md` |
| `/doc-developer-manual <slug>` | `05-developer-manual.md` |
| `/doc-repo-files <slug> [readme\|architecture\|api\|all]` | `repo/*.md` |
| `/doc-suite <path> [--only ...] [--format docx\|pdf]` | All of the above + `INDEX.md` |

## Example
```text
/doc-suite D:/work/inventory-system
```

## Contents of this folder
| Path | Purpose |
|------|---------|
| `templates/` | Document skeletons for Mode A (00–05, plus `repo/`) |
| `rules/30-evidence-and-accuracy.md` | Evidence hierarchy: code first; markers `[TBD]`, `[ASSUMPTION]`, `[VERIFY]` |
| `rules/40-document-specific.md` | What each Mode A document must contain |

Shared writing, formatting, and review rules live in the top-level `rules/` folder.
