# {{Product Name}} — Migration Plan

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Migration Plan (modernization) |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Profile {{mode-a slug}} @ {{git SHA / "working copy, YYYY-MM-DD"}}; Modernization Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (mode-c-modernize-project/rules/50-readability-and-refinement.md sections 1 and 3).
     The plan on one page (what, who builds, who tests, start, pilot, ready to deploy, handover, effort, migration); the SDLC process flow; the sprint flow; the integration or driver release flow; the ready-to-deploy gate; phases in plain words; a 'Where to Find What' table.
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. Executive Summary
<!-- 5–8 sentences: what is being modernized, the strategy, the phases, the estimated
     duration (with method) or [TBD], the cutover approach, the biggest risks, and the
     decisions needed before work can start. -->

## 2. Background and Objectives
### 2.1 Background
### 2.2 Objectives
| Goal (Brief) | Objective | Measure |
|--------------|-----------|---------|
### 2.3 Success Criteria

## 3. Starting Point
| Item | Status | Evidence / Needed by |
|------|--------|----------------------|
| Current system in production | Yes / No / [TBD] | Brief section 1 |
| Current users and data volume | [TBD] | Brief sections 1 and 9 |
| Freeze policy during migration | [TBD] | Brief section 4 |
| Decisions resolved (`[DECISION]` items) | Not yet | Phase 0 |
| Team assigned | [TBD] | Phase 0 |
| Target repository and tools | [TBD] | Phase 0 |
| Environments (dev / test / staging / prod) | [TBD] | Phase 1 |
| Copy of production data for rehearsal | [TBD] | Phase 4 |

## 4. Migration Strategy
<!-- From Brief section 8. State the chosen strategy and why; for incremental, list the increments. -->
| Increment | Features that move (F-xx) | Routing change | Exit criteria |
|-----------|---------------------------|----------------|---------------|

## 5. Scope
### 5.1 In Scope
| Feature | Disposition | Requirements | Priority |
|---------|-------------|--------------|----------|
### 5.2 Out of Scope (Dropped and excluded)
### 5.3 Assumptions and Constraints

## 6. Work Breakdown Structure (WBS)
| WBS ID | Work item | Implements | Definition of Done | Depends on | Size | Priority (MoSCoW) |
|--------|-----------|------------|--------------------|-----------|------|-------------------|
| 0.1 | | — | | — | S/M/L/XL | Must |
| 1.1 | | FR-01 | | 0.1 | | |

<!-- Size guide (estimates): S ≈ ≤1 day, M ≈ 2–3 days, L ≈ 1 week, XL ≈ >1 week (split if possible). -->

## 7. Phases and Milestones
| Phase | Goal | WBS items | Exit criteria | Target date |
|-------|------|-----------|---------------|-------------|
| Phase 0 — Mobilize and Decide | | | | [TBD] |
| Phase 1 — Foundation | | | | [TBD] |
| Phase 2 — Parity (Keep and Improve, Must) | | | | [TBD] |
| Phase 3 — Resolve Findings and New Features (Should) | | | | [TBD] |
| Phase 4 — Data Migration Rehearsal and Testing | | | | [TBD] |
| Phase 5 — Cutover and Stabilization | | | | [TBD] |
| Phase 6 — Decommission and Handover | | | | [TBD] |

```mermaid
gantt
    title {{Product Name}} Migration Timeline (relative; confirm dates)
    dateFormat  YYYY-MM-DD
    section Phase 0
    Mobilize and decide     :p0, {{start}}, {{duration}}
    section Phase 1
    Foundation              :p1, after p0, {{duration}}
    section Phase 2
    Parity                  :p2, after p1, {{duration}}
    section Phase 3
    Findings and new        :p3, after p2, {{duration}}
    section Phase 4
    Rehearsal and testing   :p4, after p3, {{duration}}
    section Phase 5
    Cutover                 :p5, after p4, {{duration}}
    section Phase 6
    Decommission            :p6, after p5, {{duration}}
```

## 8. Resources and Responsibilities
### 8.1 Team
| Role | Name | Allocation |
|------|------|-----------|
### 8.2 RACI Matrix
| Activity | Responsible | Accountable | Consulted | Informed |
|----------|------------|-------------|-----------|----------|

## 9. Effort and Cost Estimate
<!-- Only with a shown method. Otherwise give the line-item structure with [TBD] amounts.
     Include parallel-run and decommissioning lines. -->
| Item | Basis | Estimate |
|------|-------|----------|

## 10. Risk Register
| ID | Risk | Likelihood (L/M/H) | Impact (L/M/H) | Mitigation | Owner |
|----|------|--------------------|----------------|------------|-------|

## 11. Quality Assurance
<!-- Summary only; details in the Migration Test Plan (06-migration-test-plan.md). -->
| Test type | When | Exit criteria |
|-----------|------|---------------|

## 12. Data Migration
### 12.1 Approach
### 12.2 Rehearsals
### 12.3 Verification

## 13. Cutover Plan
### 13.1 Go / No-Go Checklist
- [ ] ...
### 13.2 Cutover Steps
1. {{step}}
### 13.3 Freeze or Parallel-Run Window
<!-- [TBD] dates. -->
### 13.4 Verification After Cutover
### 13.5 Rollback Plan
| Trigger | Steps back to the current system | Owner | Time limit |
|---------|----------------------------------|-------|------------|

## 14. Decommission of the Current System
- [ ] Data archived and verified
- [ ] DNS / routing switched
- [ ] Licences and subscriptions cancelled
- [ ] Repositories archived
- [ ] Documentation marked superseded

## 15. Training and Handover
- [ ] User Manual (final, from the new code)
- [ ] Technical Manual (final)
- [ ] Developer Manual (final)
- [ ] Source code and credentials transfer (via secure channel)
- [ ] Training session(s) per role
- [ ] Warranty / support period agreed

## 16. Project Definition of Done
- [ ] All "Must" requirements implemented and passing their test cases
- [ ] All parity tests passing
- [ ] Data migration verified
- [ ] UAT signed off by {{approver / [TBD]}}
- [ ] Current system decommissioned

## 17. Communication and Reporting
| Meeting / Report | Frequency | Audience | Owner |
|------------------|-----------|----------|-------|

## 18. Change Control

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
