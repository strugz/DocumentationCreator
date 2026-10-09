# Project Profile — {{Product Name}}

<!-- INTERNAL evidence base produced by /doc-intake. All other documents reuse these facts.
     Keep it factual; cite sources as `path:line`. Remove these comments in output. -->

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Slug | {{project-slug}} |
| Source location | {{absolute path or repo URL}} |
| Source revision | {{git short SHA / "working copy, YYYY-MM-DD"}} |
| Intake date | {{YYYY-MM-DD}} |
| Version (from code) | {{version from package manifest, or [TBD]}} |

## 1. Identity
- **One-line description:** {{what it is, for whom}}
- **Problem it solves:** {{grounded in README, domain models, or the user's statement}}
- **Project type:** {{web app / API / CLI / desktop / mobile / library / data pipeline / ...}}
- **Maturity:** {{prototype / MVP / in development / production}}. Evidence: {{...}}

## 2. Context Supplied by the User
<!-- Client name, deadline, budget, team, goals: anything not in code. -->
| Item | Value |
|------|-------|
| Client / Organization | [TBD] |
| Stakeholders | [TBD] |
| Target deadline | [TBD] |
| Budget | [TBD] |
| Team size and roles | [TBD] |
| Approvers (body or role) | [TBD] |
| Testers and user acceptance | [TBD] |
| Users' pain points (their words) | [TBD] |
| Names in documents | Proposed: roles ("Management", "the development team") |
| Deliverables | Proposed: Markdown and Word; proposal as PowerPoint slides on request |

## 3. Tech Stack
| Layer | Technology | Version | Evidence |
|-------|------------|---------|----------|
| Language | | | |
| Framework | | | |
| Database | | | |
| UI | | | |
| Auth | | | |
| Hosting / Infra | | | |
| CI/CD | | | |
| Testing | | | |

## 4. Repository Map
```text
{{tree of top 2–3 levels with one-line purpose per folder}}
```

## 5. Entry Points
| Entry point | Type | File |
|-------------|------|------|
| | main / server / CLI / worker / scheduled job | |

## 6. Modules / Components
| Module | Responsibility | Key files | Status |
|--------|----------------|-----------|--------|
| | | | Done / Partial / Stub / Broken |

## 7. Features Inventory
| ID | Feature | User-facing? | Roles | Status | Evidence |
|----|---------|--------------|-------|--------|----------|
| F-01 | | Yes/No | | Done / Partial / Not started / Planned | `path:line` |

## 8. User Roles and Permissions
| Role | Capabilities | Evidence |
|------|-------------|----------|

## 9. Screens / Commands / Endpoints
### 9.1 UI Screens / Routes
| Route / Screen | Purpose | File |
|----------------|---------|------|
### 9.2 API Endpoints
| Method | Path | Auth | Purpose | File |
|--------|------|------|---------|------|
### 9.3 CLI Commands
| Command | Purpose | File |
|---------|---------|------|

## 10. Data Model
| Entity / Table | Key fields | Relations | File |
|----------------|-----------|-----------|------|

## 11. Configuration and Environment
| Key | Required | Default | Purpose | Read at |
|-----|----------|---------|---------|---------|

## 12. External Dependencies and Integrations
| Service / Library | Purpose | How it connects |
|-------------------|---------|-----------------|

## 13. Build, Run, Test, Deploy
| Task | Command | Source of truth | Verified? |
|------|---------|-----------------|-----------|
| Install | | | |
| Run (dev) | | | |
| Test | | | |
| Build | | | |
| Deploy | | | |

## 14. Quality Signals
- **Tests:** {{count / frameworks / coverage config / skipped tests}}
- **Linters / formatters:** {{configs found}}
- **CI:** {{pipelines and what they check}}
- **TODO / FIXME / HACK count:** {{n}}. Top items:
  | File:line | Note |
  |-----------|------|

## 15. Incomplete Work and Gaps
| Gap | Evidence | Impact |
|-----|----------|--------|

## 16. Security Observations
<!-- Auth model, input validation, secret handling. Do NOT copy secrets. -->

## 17. Glossary (canonical terms)
| Term | Definition | Used in code as |
|------|-----------|-----------------|

### 17.1 Words to Avoid
<!-- Binding wording rules from the user (Rule 10). One row per word or phrase.
     tools/lint_docs.py reports any use of the "Avoid" column in other documents. -->
| Avoid | Use instead | Source |
|-------|-------------|--------|

## 18. Discrepancies
| Topic | Source A says | Source B says | Resolution |
|-------|---------------|---------------|------------|

## 19. Open Questions for the User
1. {{question}}
