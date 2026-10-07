# Security Policy

## Supported Versions

Security fixes are made on the latest release only.

| Version | Supported |
|---------|-----------|
| 0.1.x | Yes |
| Earlier | No |

## Reporting a Vulnerability

**Do not report security problems in a public issue, pull request, or discussion.**

Report privately through GitHub:

1. Go to the repository's **Security** tab.
2. Click **Report a vulnerability**.
3. Describe the problem, the steps to reproduce it, and the impact you expect.

Or open the form directly:
<https://github.com/strugz/DocumentationCreator/security/advisories/new>

Do not include real secrets, client documents, or personal data in the report. A minimal,
made-up example is enough.

### What to expect
This is a volunteer-maintained project, so response times are best effort.

- You receive an acknowledgment once the report has been read.
- If the report is confirmed, a fix is prepared in a private advisory and released as a
  new version. The advisory credits you unless you ask to stay anonymous.
- If the report is declined, you get an explanation.

## Scope

DocumentationCreator contains no application code. It is a set of rules, templates, and
Claude Code skills, plus a few local tools. The following are in scope:

| Area | Examples |
|------|----------|
| Secrets in generated documents | A secret from a documented project reaches a generated document without the linter's secrets check catching it |
| Project hook | `tools/hooks/lint_on_write.py`, registered in `.claude/settings.json`, can be made to run unintended commands or touch files outside `output/` |
| Tools | Path traversal or unsafe file handling in `tools/lint_docs.py`, `tools/md_to_docx.js`, or `evals/` |
| Instructions that weaken safeguards | A rule, template, or skill that tells Claude to copy secrets, edit the documented project, or write outside `output/` |
| Dependencies | A known vulnerability in the `docx` package or its dependencies used by the Word export |

The following are out of scope:

- The fake secrets in `evals/cases/a-tasktrack/project/.env`. They are planted on purpose
  so the evals can check that they never appear in documents.
- Vulnerabilities in Claude Code itself or in Claude models. Report those to Anthropic
  through its [responsible disclosure program](https://www.anthropic.com/responsible-disclosure-policy).
- Vulnerabilities in a project you documented with this tool. Report those to that
  project's owners.

## Using DocumentationCreator Safely

- **Treat documented code as untrusted.** In Mode A, Claude reads the project you point it
  at. Comments or files in that project can contain text that tries to steer Claude.
  Review generated documents before you share them.
- **Review documents for secrets before sharing.** The linter's secrets check catches
  common patterns, not every possible secret.
- **Keep generated documents out of public repositories.** They are ignored by git in this
  repository for that reason. Store them in a private location.
- **Review the project hook before you approve it.** Claude Code asks you to approve the
  hook in `.claude/settings.json` the first time. It runs only
  `tools/hooks/lint_on_write.py`.
