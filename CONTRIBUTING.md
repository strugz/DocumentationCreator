# Contributing to DocumentationCreator

Thank you for helping improve DocumentationCreator. This repository contains no
application code. It holds the rules, templates, skills, and checks that Claude Code uses
to write documentation. Most contributions change how the documents are written, so this
guide focuses on keeping them accurate.

## Contents
- [Ways to Contribute](#ways-to-contribute)
- [Setup](#setup)
- [Where Things Live](#where-things-live)
- [Making a Change](#making-a-change)
- [Testing Your Change](#testing-your-change)
- [Pull Requests](#pull-requests)
- [Ground Rules](#ground-rules)

## Ways to Contribute
- **Report a problem:** open an issue using the **Document problem** form. It asks for
  the command you ran, what you expected, and what the document contained. Paste only a short excerpt, and remove any client or
  project details first.
- **Improve a template or rule:** fix a missing section, unclear wording, or a check that
  is too strict or too loose.
- **Add a document type:** a new template and skill for either mode.
- **Add an eval case:** a new fixture that catches a mistake the current cases miss.
- **Improve the tools:** the linter (`tools/lint_docs.py`), the Word export
  (`tools/md_to_docx.js`), or the eval runner (`evals/run_evals.py`).

## Setup
1. Fork the repository on GitHub, then clone your fork:
   ```bash
   git clone https://github.com/<your-username>/DocumentationCreator.git
   ```
2. Install the prerequisites listed in the [README](README.md#prerequisites).
3. Confirm the tests pass before you change anything:
   ```bash
   python -m unittest discover -s tests
   ```

## Where Things Live
| To change… | Edit | Also update |
|------------|------|-------------|
| Style, formatting, or review rules for both modes | `rules/` | `tools/lint_docs.py` if the rule is mechanical |
| Mode A evidence or per-document rules | `mode-a-existing-project/rules/` | — |
| Mode B evidence or per-document rules | `mode-b-new-project/rules/` | — |
| Sections of a document | `mode-*/templates/NN-*.md` | The matching skill, if it names sections |
| How Claude produces a document | `.claude/skills/<name>/SKILL.md` | The suite skill (`doc-suite` or `new-suite`) if the order or inputs change |
| Mechanical checks | `tools/lint_docs.py` | `tests/test_lint_docs.py` |
| Eval scoring | `evals/grade.py`, `evals/rubric.md` | `tests/test_grade.py` |

`CLAUDE.md` is the entry point that Claude reads first. Update its tables whenever you add,
rename, or remove a skill or template.

## Making a Change
1. Create a branch from `main`:
   ```bash
   git checkout -b improve-user-manual-template
   ```
2. Keep the change focused: one rule, template, skill, or tool per pull request.
3. Follow the repository's own writing rules in your changes, too: plain English, short
   sentences, active voice, and no marketing language (`rules/10-writing-style.md`).

### Adding a document type
1. Add the template to the mode's `templates/` folder. Start with the Document Control
   block and end with Open Items and Revision History, like the existing templates.
2. Copy an existing skill of the same mode into `.claude/skills/<name>/SKILL.md`. Keep the
   frontmatter (`name`, `description`, `argument-hint`) and the line that tells Claude to
   read the mode's rules first.
3. Add a section for the document to the mode's `rules/40-document-specific.md`.
4. Register it in `CLAUDE.md`, in the mode's README, in the root README's command table,
   and in the suite skill.

### Template and skill conventions
- Mode A facts must come from the code. Mode B facts must come from the brief. Never add
  template content that invites Claude to invent numbers, dates, costs, or names.
- Gaps are marked with `[TBD]`, `[ASSUMPTION]`, `[VERIFY]`, and (Mode B) `[DECISION]`.
  Do not introduce new marker types without updating the linter.
- Use `{{placeholder}}` for values Claude fills in. The linter fails any that are left.

## Testing Your Change
| You changed | Run |
|-------------|-----|
| `tools/`, `evals/grade.py`, or `tests/` | The unit tests |
| A rule, template, or skill | The unit tests, then the evals, before and after your change |

Unit tests (standard library only):

```bash
python -m unittest discover -s tests
```

Evals measure whether a rule, template, or skill change made the documents better or
worse. Run them on `main` first, then on your branch, and compare:

```bash
python evals/run_evals.py run all
```

```bash
python evals/run_evals.py compare <NEW_RUN_ID>
```

Generation is not deterministic, so run each case at least twice. A newly failing trap
check (a copied secret, an invented cost, a feature that does not exist) blocks the
change. See [`evals/README.md`](evals/README.md) for running without the CLI and for adding
a case.

> [!IMPORTANT]
> Do not "fix" the fixture project in `evals/cases/a-tasktrack/project/`. Its flaws,
> including the fake secrets in its `.env` file, are what the evals test.

If you change the linter, run it on a real output folder to check for false positives:

```bash
python tools/lint_docs.py output/mode-b/<slug>
```

## Pull Requests
- Use a short, imperative commit subject that says what changed, for example
  `Add MIT License` or `README: add install steps`.
- The pull request template includes a checklist. In the description, state:
  - what you changed and why;
  - the unit test result;
  - for rule, template, or skill changes, the eval scores before and after.
- Update the README and `CLAUDE.md` when commands, files, or behavior change.
- Add a line under **Unreleased** in [CHANGELOG.md](CHANGELOG.md) for any change users would
  notice.
- Line endings are normalized to LF by `.gitattributes`. You do not need to configure this.

## Ground Rules
- **Never commit generated documents.** Everything under `output/mode-a/` and
  `output/mode-b/` is ignored by git on purpose, because it often contains client or
  project details. Share a short, cleaned excerpt in an issue instead.
- **Never commit real secrets or personal data,** including in eval fixtures. Fixture
  secrets must be obviously fake.
- **Never commit files from `projects/`.** That folder holds other people's code for
  documentation and is ignored by git.
- By contributing, you agree that your contribution is released under the
  [MIT License](LICENSE).
