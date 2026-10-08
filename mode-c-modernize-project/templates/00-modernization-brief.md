# Modernization Brief — {{Product Name}}

<!-- MODE C evidence base produced by /mod-brief. All other Mode C documents reuse these
     facts. Keep three things apart: what EXISTS (from the Mode A profile), what the user
     DECIDED (interview), and what Claude PROPOSES. Remove comments in output. -->

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Slug | {{project-slug}} |
| Mode | C — Modernize an existing project |
| Source profile | `output/mode-a/{{mode-a slug}}/00-project-profile.md` |
| Source location | {{absolute path or repo URL, copied from the profile}} |
| Source revision | {{git short SHA / "working copy, YYYY-MM-DD", copied from the profile}} |
| Brief version | v{{n}} |
| Brief date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude from the profile and an interview with {{user / [TBD]}} |
| Status | Draft / Confirmed by user |

## 1. The Current System (from the profile)
- **One-line description:** {{Profile §1}}
- **Project type:** {{Profile §1}}
- **Maturity:** {{prototype / MVP / in development / production}}. Evidence: {{Profile §1}}
- **In production?** {{Yes / No / [TBD]}}. Users today: {{[TBD] unless the user said}}
- **Current tech stack (Profile §3):**

| Layer | Technology | Version | Evidence |
|-------|------------|---------|----------|
| Language | | | Profile §3 |
| Framework | | | |
| Database | | | |
| UI | | | |
| Auth | | | |
| Hosting / Infra | | | |
| CI/CD | | | |
| Testing | | | |

## 2. Why Modernize
- **Original request (user's words):**
  > {{verbatim request as the user gave it}}
- **Pain points named by the user:**
  | # | Pain point | Evidence in the profile (if any) | Source |
  |---|-----------|----------------------------------|--------|
  | P-01 | | Profile §15 / `path:line` / none → [VERIFY] | User |
- **Known gaps from the profile (Profile §15, §16):**

## 3. Goals of the Modernization
| # | Goal | How success is measured | Source |
|---|------|-------------------------|--------|
| G-01 | | [TBD] unless the user gave a measure | User / Proposed |

## 4. Business Context
| Item | Value |
|------|-------|
| Client / Organization | {{Profile §2 or [TBD]}} |
| Sponsor / Approver | [TBD] |
| Stakeholders | [TBD] |
| Target cutover date | [TBD] |
| Budget | [TBD] |
| Team (size and roles) | [TBD] |
| Can the current system be frozen during migration? | [TBD] |
| Methodology preference | [TBD] / Proposed: Agile, 2-week sprints |

## 5. Users and Roles (carried from Profile §8)
| ID | Role | Who they are | Changes in the target system | Approx. count |
|----|------|--------------|------------------------------|---------------|
| R-01 | | | None / {{change}} | [TBD] |

## 6. Feature Disposition
<!-- Every F-xx from Profile §7, in the same order, then new features. -->
| ID | Feature | Current status (Profile §7) | Disposition | What changes | Priority (MoSCoW) | Decision state | Source |
|----|---------|-----------------------------|-------------|--------------|-------------------|----------------|--------|
| F-01 | | Done / Partial / Stub / Broken | Keep / Improve / Replace / Drop / New | | Must / Should / Could / Won't | Agreed / Proposed / Deferred | User / Proposed |

## 7. Target Tech Stack
<!-- One row per layer. "Current" from Profile §3. A layer without a user decision is a
     [DECISION] in §16 and a Proposed value here. -->
| Layer | Current | User preference | Target (Agreed / Proposed) | Reason |
|-------|---------|-----------------|----------------------------|--------|
| Language | | | | |
| Backend framework | | | | |
| Frontend / UI | | | | |
| Database | | | | |
| Authentication | | | | |
| Hosting / Infra | | | | |
| CI/CD | | | | |
| Testing | | | | |

## 8. Migration Strategy
| Item | Value | Source |
|------|-------|--------|
| Strategy | Big-bang rewrite / Strangler fig (incremental) / Lift-and-shift then refactor / Re-platform only | User / [DECISION] |
| Parallel run or freeze | | |
| Data migration needed? | Yes / No / [TBD] | |
| Rollback expectation | | |
| Reason for the recommendation | | Proposed |

## 9. Data (carried from Profile §10)
| Entity / Table | Migrate? | Transform? | Archive? | Volume | Source |
|----------------|----------|------------|----------|--------|--------|
| | Yes / No | | | [TBD] | Profile §10 / User |

## 10. Integrations (carried from Profile §12)
| System | Purpose | Keep / Replace / Drop | Source |
|--------|---------|-----------------------|--------|

## 11. Constraints
| ID | Constraint | Type (time / budget / legal / technical / organizational) | Source |
|----|-----------|------------------------------------------------------------|--------|
| C-01 | | | |

## 12. Quality Expectations for the Target System
<!-- Performance, availability, security, privacy, accessibility. Numbers only if the user gave them. -->
| Area | Current (profile evidence) | Expectation | Source |
|------|----------------------------|-------------|--------|

## 13. Out of Scope (stated or proposed)
-

## 14. Assumptions
-

## 15. Risks Noted During Intake
| Risk | Why it matters |
|------|----------------|

## 16. Decisions Needed
| # | Decision | Options | Recommendation | Blocking? |
|---|----------|---------|----------------|-----------|

## 17. Glossary (canonical terms, carried from Profile §17)
| Term | Definition |
|------|-----------|

## 18. Discrepancies
| Topic | Profile / code says (A) | User said (B) | Resolution |
|-------|-------------------------|---------------|------------|

## 19. Open Questions for the User
1. {{question}}

## Interview Log
| # | Question | Answer (user's words) | Brief section updated |
|---|----------|-----------------------|-----------------------|

## Revision History
| Version | Date | Changes |
|---------|------|---------|
| v1 | {{date}} | Initial brief from the profile and the interview |
