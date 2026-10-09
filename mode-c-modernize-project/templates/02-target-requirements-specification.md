# {{Product Name}} — Target Requirements Specification

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Target Requirements Specification (SRS for the modernized system) |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Profile {{mode-a slug}} @ {{git SHA / "working copy, YYYY-MM-DD"}}; Modernization Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (mode-c-modernize-project/rules/50-readability-and-refinement.md sections 1 and 3).
     How to read a requirement row (ID, type, priority, acceptance criteria); what the system must do by area (area, requirement range, examples); the case flow; the 'requirement to acceptance' flow.
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. Introduction
### 1.1 Purpose of This Document
### 1.2 Product Scope
<!-- What the target system will do, which current system it replaces, and the goals it serves (Brief section 2–3). -->
### 1.3 Definitions and Acronyms
<!-- Link to the Glossary in Appendix A. -->
### 1.4 References
<!-- Mode A Project Profile; Modernization Brief v{{n}}; Current State Assessment. -->

## 2. Overall Description
### 2.1 Product Perspective
<!-- The target system in its landscape; what it replaces; interim coexistence if incremental. -->
```mermaid
flowchart LR
    U[Users] --> S[{{Target system}}]
    S --> E[External system]
```
### 2.2 User Classes and Characteristics
| Role ID | Role | Description | Technical skill | Approx. count |
|---------|------|-------------|-----------------|---------------|
| R-01 | | | Low / Medium / High | [TBD] |
### 2.3 Operating Environment
<!-- Target platforms, devices, browsers (Brief section 7). Proposed items labeled. -->
### 2.4 Design and Implementation Constraints
| ID | Constraint | Source |
|----|-----------|--------|
### 2.5 Assumptions and Dependencies

## 3. Functional Requirements
<!-- Group by feature (F-xx), in disposition order: Keep, Improve, Replace, New.
     One "shall" per requirement. Every Keep/Improve feature has a parity requirement. -->
### 3.1 {{F-01 Feature name}} — {{Keep / Improve / Replace / New}}
**Current behaviour:** {{one line, with `path:line` or Profile section 7/section 9}}
**Priority:** Must / Should / Could

| ID | Requirement | Type | Priority | Source | Acceptance criteria |
|----|-------------|------|----------|--------|---------------------|
| FR-01 | The target system shall … | Parity / Improvement / New / Finding | Must | F-01 / D-xx | {{testable condition; for Parity: "matches the current system's behaviour in `path:line`"}} |

**User stories**
| ID | Story | Acceptance criteria (Given / When / Then) |
|----|-------|--------------------------------------------|
| US-01 | As a {{role}}, I want {{goal}}, so that {{benefit}}. | Given …, when …, then …. |

### 3.2 {{F-02 Feature name}} — {{disposition}}

## 4. Non-Functional Requirements
<!-- Each NFR that resolves an assessment finding names it in Source. -->
| ID | Category | Requirement | Current (evidence) | Target | Source | How verified |
|----|----------|-------------|--------------------|--------|--------|--------------|
| NFR-01 | Performance | | | Proposed: {{value}} | Proposed / Brief section 12 / D-xx | |
| NFR-02 | Availability | | | | | |
| NFR-03 | Security | | | | | |
| NFR-04 | Privacy / Data protection | | | | | |
| NFR-05 | Usability and Accessibility | | | | | |
| NFR-06 | Compatibility | | | | | |
| NFR-07 | Maintainability | | | | | |
| NFR-08 | Backup and Recovery | | | | | |
| NFR-09 | Logging and Audit | | | | | |
| NFR-10 | Observability (monitoring, alerting) | | | | | |

## 5. Data Requirements
### 5.1 Main Entities
| Entity | Description | Key attributes | Retention |
|--------|-------------|----------------|-----------|
### 5.2 Data Validation Rules
| Entity.field | Rule |
|--------------|------|
### 5.3 Data Migration
<!-- From Brief section 9. Which entities move, transform, or archive, and how the migration is verified. -->
| Current entity / table | Target entity | Action (migrate / transform / archive / drop) | Verification |
|------------------------|---------------|-----------------------------------------------|--------------|

## 6. External Interface Requirements
### 6.1 User Interfaces
### 6.2 Software Interfaces (integrations)
| ID | System | Current (Profile section 12) | Target | Data exchanged | Direction | Method (Proposed) |
|----|--------|-----------------------|--------|----------------|-----------|-------------------|
### 6.3 Hardware Interfaces
### 6.4 Communication Interfaces

## 7. Reports
| ID | Report | Audience | Content | Filters | Format | Disposition |
|----|--------|----------|---------|---------|--------|-------------|

## 8. Out of Scope
<!-- Every Drop feature with its reason, plus anything else excluded. -->
| Item | Reason | Source |
|------|--------|--------|
| F-xx {{feature}} (Drop) | | Brief section 6 |

## 9. Acceptance Approach
<!-- UAT with side-by-side comparison where possible (see Migration Test Plan); sign-off authority. -->

## 10. Traceability Matrix
| Feature | Finding | Requirement | Design component | WBS item | Test case |
|---------|---------|-------------|------------------|----------|-----------|
| F-01 | — | FR-01 | {{filled by /mod-design}} | {{filled by /mod-plan}} | {{filled by /mod-test-plan}} |
| — | D-01 | NFR-03 | | | |

## Appendix A — Glossary
| Term | Definition |
|------|-----------|

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
