# {{Product Name}} — Migration Test Plan

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Migration Test Plan |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Profile {{mode-a slug}} @ {{git SHA / "working copy, YYYY-MM-DD"}}; Modernization Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (mode-c-modernize-project/rules/50-readability-and-refinement.md sections 1 and 3).
     Who tests what (role, what they test, when); the testing flow step by step; the integration or driver release flow; the defect flow; the ready-to-deploy gate.
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. Introduction
### 1.1 Purpose
### 1.2 Scope of Testing
<!-- The target system, the data migration, the cutover, and parity with the current system. -->
### 1.3 Related Documents
<!-- Mode A Profile, Target Requirements, Target System Design, Migration Plan. -->

## 2. Test Strategy
| Level | Purpose | Who | Tooling (Proposed) | When |
|-------|---------|-----|--------------------|------|
| Unit | | Developers | | Every change |
| Integration | | Developers | | |
| System | | QA | | |
| Parity (old vs new) | | QA + business users | | Phase 2 onward |
| Data migration | | Developers + data owner | | Phase 4 |
| Cutover and rollback rehearsal | | Ops + QA | | Phase 4–5 |
| User Acceptance (UAT) | | Client users | | Phase 4 |
| Performance | | | | |
| Security | | | | |
| Accessibility | | | | |

## 3. Test Environments
| Environment | Purpose | Data | Access |
|-------------|---------|------|--------|
| Current system (reference) | Parity comparison | Production copy (anonymized) | |
| Target staging | | Migrated copy | |

## 4. Test Data
<!-- Copy of production data for rehearsal; how personal data is anonymized; synthetic data for new features. -->

## 5. Entry and Exit Criteria
| Level | Entry criteria | Exit criteria |
|-------|----------------|---------------|

## 6. Functional Test Cases
<!-- At least one per Must and Should requirement. -->
| TC ID | Title | Requirement | Preconditions | Steps | Expected result | Priority |
|-------|-------|-------------|---------------|-------|-----------------|----------|
| TC-01 | | FR-01 | | 1. … 2. … | | High |

## 7. Parity Test Cases
<!-- One per Keep and Improve feature. Expected result = current behaviour (Keep) or the stated change (Improve). -->
| TC ID | Feature | Disposition | Requirement | Current behaviour (evidence) | Steps | Expected result |
|-------|---------|-------------|-------------|------------------------------|-------|-----------------|
| TC-P-01 | F-01 | Keep | FR-01 | `path:line` / Profile section 7 | | Same as current |

## 8. Data Migration Test Cases
| TC ID | Requirement | Check | Method | Pass condition |
|-------|-------------|-------|--------|----------------|
| TC-D-01 | FR-xx | Record counts per entity | | Counts match source ± documented exclusions |
| TC-D-02 | FR-xx | Referential integrity | | No orphaned rows |
| TC-D-03 | FR-xx | Spot checks | | Sampled records match |

## 9. Cutover and Rollback Test Cases
| TC ID | Requirement | Check | Pass condition |
|-------|-------------|-------|----------------|
| TC-C-01 | NFR-xx | Go / no-go checklist rehearsal | All items pass in staging |
| TC-C-02 | NFR-xx | Rollback rehearsal | Current system restored within the time limit |

## 10. Non-Functional Test Cases
| TC ID | Requirement | Method | Target | Pass condition |
|-------|-------------|--------|--------|----------------|
| TC-NF-01 | NFR-01 | | | |

## 11. User Acceptance Test Scenarios
<!-- Business language, one per key workflow; side-by-side with the current system where the strategy allows. -->
| UAT ID | Scenario | Role | Requirements covered | Compared with current system? | Acceptance |
|--------|----------|------|----------------------|-------------------------------|------------|
| UAT-01 | | | FR-01, FR-02 | Yes / No | |

## 12. Defect Management
### 12.1 Severity Definitions
| Severity | Definition | Example | Must fix before cutover? |
|----------|-----------|---------|--------------------------|
| Critical | | | Yes |
| High | | | Yes |
| Medium | | | [DECISION] |
| Low | | | No |
### 12.2 Defect Workflow

## 13. Requirements Coverage
| Requirement | Priority | Test cases | Covered? |
|-------------|----------|------------|----------|

## 14. Roles and Responsibilities
| Role | Responsibility | Name |
|------|----------------|------|

## 15. Test Schedule
<!-- Align with the Migration Plan phases. -->

## 16. UAT Sign-Off
| Name | Role | Decision (Accept / Accept with conditions / Reject) | Date |
|------|------|------------------------------------------------------|------|

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
