# {{Product Name}} — Project Plan

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Project Plan (new build) |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (rules/35-readability.md).
     The plan on one page (what, who builds, who tests, start, release, effort with method, top risks); the SDLC flow; the ready-to-deploy gate; phases in plain words; a 'Where to Find What' table.
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. Executive Summary
<!-- Bullets (rules/35-readability.md section 2): What / How / When / Effort / Risks /
     Needed to start. Cover in 5–8 sentences in total: what will be built, the phases, the estimated duration (with method)
     or [TBD], the biggest risks, and the decisions needed before work can start. -->

## 2. Project Background and Objectives
### 2.1 Background
### 2.2 Objectives
| Goal (Brief) | Objective | Measure |
|--------------|-----------|---------|
### 2.3 Success Criteria

## 3. Starting Point
<!-- Replaces the Mode A "current state". What must exist before development starts. -->
| Item | Status | Needed by |
|------|--------|-----------|
| Requirements signed off | Not yet | Phase 0 |
| Design decisions resolved (`[DECISION]` items) | Not yet | Phase 0 |
| Team assigned | [TBD] | Phase 0 |
| Source code repository and tools | [TBD] | Phase 0 |
| Environments (dev / test / prod) | [TBD] | Phase 1 |
| Access to integrations / test accounts | [TBD] | Phase 1 |

## 4. Scope
### 4.1 In Scope
<!-- Must equal the Requirements' in-scope features. -->
| Feature | Requirements | Priority |
|---------|--------------|----------|
### 4.2 Out of Scope
### 4.3 Assumptions and Constraints

## 5. Work Breakdown Structure (WBS)
| WBS ID | Work item | Implements | Definition of Done | Depends on | Size | Priority (MoSCoW) |
|--------|-----------|------------|--------------------|-----------|------|-------------------|
| 0.1 | | — | | — | S/M/L/XL | Must |
| 1.1 | | FR-01 | | 0.1 | | |

<!-- Sizes (rules/45-estimation-and-release-gate.md section 1): S = 1, M = 3, L = 5, XL = 10
     person-days (split XL if possible). -->

## 6. Phases and Milestones
| Phase | Goal | WBS items | Exit criteria | Target date |
|-------|------|-----------|---------------|-------------|
| Phase 0 — Mobilize and Setup | | | | [TBD] |
| Phase 1 — Foundation | | | | [TBD] |
| Phase 2 — Core Features (Must) | | | | [TBD] |
| Phase 3 — Additional Features (Should) | | | | [TBD] |
| Phase 4 — Testing and UAT | | | | [TBD] |
| Phase 5 — Deployment, Training, and Handover | | | | [TBD] |

```mermaid
gantt
    title {{Product Name}} Build Timeline (relative; confirm dates)
    dateFormat  YYYY-MM-DD
    section Phase 0
    Mobilize and setup  :p0, {{start}}, {{duration}}
    section Phase 1
    Foundation          :p1, after p0, {{duration}}
    section Phase 2
    Core features       :p2, after p1, {{duration}}
    section Phase 3
    Additional features :p3, after p2, {{duration}}
    section Phase 4
    Testing and UAT     :p4, after p3, {{duration}}
    section Phase 5
    Deploy and handover :p5, after p4, {{duration}}
```

## 7. Resources and Responsibilities
### 7.1 Team
| Role | Name | Allocation |
|------|------|-----------|
### 7.2 RACI Matrix
| Activity | Responsible | Accountable | Consulted | Informed |
|----------|------------|-------------|-----------|----------|

## 8. Effort and Cost Estimate
<!-- Method from rules/45-estimation-and-release-gate.md sections 1–3. Keep the AI-assisted row
     only when the evidence base says the team uses AI-assisted coding. Cost amounts stay [TBD]
     unless the user gave rates. -->
| Item | Basis | Estimate |
|------|-------|----------|
| Build effort (unassisted) | Sum of WBS sizes | |
| Build effort (AI-assisted) | Code-heavy items × 0.6 [ASSUMPTION] | |
| Testing and acceptance | Test schedule, full size | |
| Capacity | Developers × 20 days × 75 % focus [ASSUMPTION] | |
| Duration | Effort ÷ capacity + testing + contingency (n %) | |
| Cost | Effort × rate | [TBD] |

## 9. Risk Register
| ID | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner |
|----|------|--------------------|----------------|------------|-------|

## 10. Quality Assurance
<!-- Summary only; details in the Test Plan (05-test-plan.md). -->
| Test type | When | Exit criteria |
|-----------|------|---------------|

## 11. Deployment and Go-Live Plan
### 11.1 Environments
### 11.2 Data Migration
### 11.3 Go-Live Checklist
<!-- Starts with the ready-to-deploy gate (Rule 45 section 5). Client rollouts that depend on a
     later agreement get a checklist here, without dates. -->
- [ ] Ready to deploy: all Must test cases pass, {{testers by role}} sign off, user acceptance signed
- [ ] ...
### 11.4 Rollback Plan

## 12. Training and Handover
- [ ] User Manual (final)
- [ ] Technical Manual (final)
- [ ] Developer Manual (final)
- [ ] Source code and credentials transfer (via secure channel)
- [ ] Training session(s) per role
- [ ] Warranty / support period agreed

## 13. Project Definition of Done
- [ ] All "Must" requirements implemented and passing their test cases
- [ ] UAT signed off by {{approver / [TBD]}}
- [ ] Ready-to-deploy gate met (Rule 45 section 5), the same wording as the Test Plan
- [ ] ...

## 14. Communication and Reporting
| Meeting / Report | Frequency | Audience | Owner |
|------------------|-----------|----------|-------|

## 15. Change Control
<!-- How new requests are evaluated against scope, timeline, and budget. -->

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
