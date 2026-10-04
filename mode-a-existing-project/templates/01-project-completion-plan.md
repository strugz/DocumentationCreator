# {{Product Name}} — Project Completion Plan

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Project Completion Plan |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | {{name}} |
| Status | Draft |
| Source revision | {{SHA}} |

## Table of Contents
<!-- generate from headings -->

## 1. Executive Summary
<!-- 5–8 sentences: where the project stands, what remains, the biggest risks,
     the target finish (or [TBD]), and the decision(s) needed from stakeholders. -->

## 2. Project Background and Objectives
### 2.1 Background
### 2.2 Objectives
<!-- Measurable where possible. Mark unknown targets [TBD]. -->
### 2.3 Success Criteria

## 3. Current State Assessment
### 3.1 Summary
| Metric | Value | Method |
|--------|-------|--------|
| Features done | {{x of y}} | Features inventory in project profile |
| Overall completion (estimate) | {{%}} | {{how calculated}} |
| Open TODO/FIXME | {{n}} | Code scan |
| Test status | {{passing/failing/skipped/none}} | {{source}} |

### 3.2 Feature Status
| ID | Feature | Status | Evidence | Remaining work |
|----|---------|--------|----------|----------------|
| F-01 | | ✅ Done / 🟡 Partial / ⬜ Not started / 🔴 Broken | `path:line` | |

### 3.3 Technical Health
<!-- Tests, CI, tech debt, security gaps, documentation gaps, dependency staleness. -->

### 3.4 Key Issues and Blockers
| # | Issue | Impact | Evidence |
|---|-------|--------|----------|

## 4. Scope to Completion
### 4.1 In Scope (to finish)
### 4.2 Out of Scope / Deferred
### 4.3 Assumptions and Constraints

## 5. Work Breakdown Structure (WBS)
| WBS ID | Work item | Feature | Definition of Done | Depends on | Size | Priority (MoSCoW) |
|--------|-----------|---------|--------------------|-----------|------|-------------------|
| 1.1 | | F-01 | | — | S/M/L/XL | Must |

## 6. Phases and Milestones
| Phase | Goal | WBS items | Exit criteria | Target date |
|-------|------|-----------|---------------|-------------|
| Phase 1 — Stabilize | | | | [TBD] |
| Phase 2 — Complete core features | | | | [TBD] |
| Phase 3 — Hardening and QA | | | | [TBD] |
| Phase 4 — Deployment and Handover | | | | [TBD] |

```mermaid
gantt
    title {{Product Name}} Completion Timeline (relative; confirm dates)
    dateFormat  YYYY-MM-DD
    section Phase 1
    Stabilize           :p1, {{start}}, {{duration}}
    section Phase 2
    Core features       :p2, after p1, {{duration}}
    section Phase 3
    Hardening and QA    :p3, after p2, {{duration}}
    section Phase 4
    Deploy and handover :p4, after p3, {{duration}}
```

## 7. Resources and Responsibilities
### 7.1 Team
| Role | Name | Allocation |
|------|------|-----------|
### 7.2 RACI Matrix
| Activity | Responsible | Accountable | Consulted | Informed |
|----------|------------|-------------|-----------|----------|

## 8. Effort and Cost Estimate
<!-- Only with a shown method. Otherwise give the line-item structure with [TBD] amounts. -->
| Item | Basis | Estimate |
|------|-------|----------|

## 9. Risk Register
| ID | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner |
|----|------|--------------------|----------------|------------|-------|

## 10. Quality Assurance and Testing Plan
| Test type | Scope | Tooling | Entry/Exit criteria |
|-----------|-------|---------|---------------------|
| Unit | | | |
| Integration | | | |
| UAT | | | |
| Performance / Security | | | |

## 11. Deployment and Go-Live Plan
### 11.1 Environments
### 11.2 Go-Live Checklist
- [ ] ...
### 11.3 Rollback Plan

## 12. Handover and Documentation Deliverables
- [ ] User Manual
- [ ] Technical Manual
- [ ] Developer Manual
- [ ] Source code and credentials transfer (via secure channel)
- [ ] Training session(s)

## 13. Project Definition of Done
- [ ] All "Must" WBS items complete
- [ ] ...

## 14. Communication and Reporting
| Meeting / Report | Frequency | Audience | Owner |
|------------------|-----------|----------|-------|

## 15. Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
