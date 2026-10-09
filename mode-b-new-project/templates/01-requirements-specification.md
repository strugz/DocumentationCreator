# {{Product Name}} — Software Requirements Specification

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Software Requirements Specification (SRS) |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## 1. Introduction
### 1.1 Purpose of This Document
### 1.2 Product Scope
<!-- What the product will do and the business goal it serves (Brief section 1–2). -->
### 1.3 Definitions and Acronyms
<!-- Link to the Glossary in Appendix A. -->
### 1.4 References
<!-- Project Brief v{{n}}; any material the user supplied. -->

## 2. Overall Description
### 2.1 Product Perspective
<!-- Standalone or part of a larger landscape? Which systems it replaces or connects to. -->
```mermaid
flowchart LR
    U[Users] --> S[{{Product}}]
    S --> E[External system]
```
### 2.2 User Classes and Characteristics
| Role ID | Role | Description | Technical skill | Approx. count |
|---------|------|-------------|-----------------|---------------|
| R-01 | | | Low / Medium / High | [TBD] |
### 2.3 Operating Environment
<!-- Platforms, devices, browsers (Brief section 8). Proposed items labeled. -->
### 2.4 Design and Implementation Constraints
| ID | Constraint | Source |
|----|-----------|--------|
### 2.5 Assumptions and Dependencies

## 3. Functional Requirements
<!-- Group by feature (F-xx). One "shall" per requirement. -->
### 3.1 {{F-01 Feature name}}
**Description:** {{...}}
**Priority:** Must / Should / Could

| ID | Requirement | Priority | Source | Acceptance criteria |
|----|-------------|----------|--------|---------------------|
| FR-01 | The system shall … | Must | F-01 | {{testable condition}} |

**User stories**
| ID | Story | Acceptance criteria (Given / When / Then) |
|----|-------|--------------------------------------------|
| US-01 | As a {{role}}, I want {{goal}}, so that {{benefit}}. | Given …, when …, then …. |

### 3.2 {{F-02 Feature name}}

## 4. Non-Functional Requirements
| ID | Category | Requirement | Target | Source | How verified |
|----|----------|-------------|--------|--------|--------------|
| NFR-01 | Performance | | Proposed: {{value}} | Proposed / Brief section 11 | |
| NFR-02 | Availability | | | | |
| NFR-03 | Security | | | | |
| NFR-04 | Privacy / Data protection | | | | |
| NFR-05 | Usability and Accessibility | | | | |
| NFR-06 | Compatibility | | | | |
| NFR-07 | Maintainability | | | | |
| NFR-08 | Backup and Recovery | | | | |
| NFR-09 | Logging and Audit | | | | |

## 5. Data Requirements
### 5.1 Main Entities
| Entity | Description | Key attributes | Retention |
|--------|-------------|----------------|-----------|
### 5.2 Data Validation Rules
| Entity.field | Rule |
|--------------|------|
### 5.3 Data Migration
<!-- Existing data to import (Excel, old system)? Otherwise "Not applicable — no existing data". -->

## 6. External Interface Requirements
### 6.1 User Interfaces
<!-- General UI expectations: responsive, language, branding. Detailed screens are in the System Design. -->
### 6.2 Software Interfaces (integrations)
| ID | System | Data exchanged | Direction | Method (Proposed) |
|----|--------|----------------|-----------|-------------------|
### 6.3 Hardware Interfaces
### 6.4 Communication Interfaces
<!-- Email, SMS, push notifications. -->

## 7. Reports
| ID | Report | Audience | Content | Filters | Format |
|----|--------|----------|---------|---------|--------|

## 8. Out of Scope
-

## 9. Acceptance Approach
<!-- How the client will accept the system: UAT scenarios (see Test Plan), sign-off authority. -->

## 10. Traceability Matrix
| Feature | Requirement | Design component | WBS item | Test case |
|---------|-------------|------------------|----------|-----------|
| F-01 | FR-01 | {{filled by /new-design}} | {{filled by /new-plan}} | {{filled by /new-test-plan}} |

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
