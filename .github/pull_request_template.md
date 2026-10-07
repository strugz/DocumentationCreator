## What and why

<!-- What did you change, and what problem does it solve? Link the issue: "Fixes #123". -->

## Type of change

- [ ] Rule (`rules/` or a mode's `rules/`)
- [ ] Template
- [ ] Skill (`.claude/skills/`)
- [ ] New document type
- [ ] Tool (linter, Word export, eval runner)
- [ ] Eval case
- [ ] Repo docs only

## Testing

- [ ] Unit tests pass: `python -m unittest discover -s tests`
- [ ] Rule, template, or skill change: evals run on `main` and on this branch (each case at least twice)

| Case | Before | After |
|------|--------|-------|
| a-tasktrack | | |
| b-clinic-booking | | |

<!-- List any check that started failing. A newly failing trap check (copied secret, invented cost, nonexistent feature) blocks the change. -->

## Checklist

- [ ] `CLAUDE.md` and the READMEs are updated if commands, files, or behavior changed
- [ ] No generated documents from `output/mode-a/` or `output/mode-b/` are included
- [ ] No real secrets, personal data, or client details (fixture secrets are obviously fake)
- [ ] I followed [CONTRIBUTING.md](https://github.com/strugz/DocumentationCreator/blob/main/CONTRIBUTING.md) and agree my contribution is released under the MIT License
