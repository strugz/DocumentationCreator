# {{Product Name}} — Current State Assessment

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Current State Assessment |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{name / [TBD]}} |
| Status | Draft |
| Source revision | Profile {{mode-a slug}} @ {{git SHA / "working copy, YYYY-MM-DD"}}; Modernization Brief v{{n}}, {{YYYY-MM-DD}} |

## Table of Contents

## 1. Introduction
### 1.1 Purpose and Audience
### 1.2 Scope of the Assessment
<!-- Which parts of the current system were assessed, and from which evidence. -->
### 1.3 Related Documents
<!-- Mode A Project Profile, Completion Plan, Technical and Developer Manuals; Modernization Brief. -->

## 2. Summary
<!-- 5–8 sentences: the system's maturity, the most serious findings, what works well,
     and what the modernization must fix first. No numbers the evidence does not contain. -->
| Severity | Findings |
|----------|----------|
| Critical | {{n}} |
| High | {{n}} |
| Medium | {{n}} |
| Low | {{n}} |

## 3. System Overview (as built)
### 3.1 Architecture
<!-- Present tense, with evidence. -->
```mermaid
flowchart LR
    U[Users] --> A[{{Current system}}]
    A --> DB[(Database)]
```
### 3.2 Tech Stack Currency
| Layer | Technology | Version in use | Latest supported / LTS | End of support | Status |
|-------|------------|----------------|------------------------|----------------|--------|
| | | Profile §3 | [VERIFY] | [VERIFY: vendor page] | Current / Ageing / Unsupported |

## 4. Findings
<!-- One row per finding. Evidence: `path:line` or Profile §n. -->
| ID | Category | Finding | Severity | Evidence | Consequence for the target system |
|----|----------|---------|----------|----------|-----------------------------------|
| D-01 | Technology / Architecture / Code quality / Security / Operations / Data / Process / Documentation | | Critical / High / Medium / Low | | |

### 4.1 Technology
### 4.2 Architecture
### 4.3 Code Quality and Tests
### 4.4 Security
### 4.5 Operations (deployment, backup, monitoring)
### 4.6 Data Model
### 4.7 Incomplete Work (Profile §15)
### 4.8 Documentation and Process

## 5. What Works Well (Keep List)
| Item | Why it should survive | Evidence |
|------|-----------------------|----------|

## 6. Modernization Drivers
<!-- Map the brief's pain points (P-xx) and goals (G-xx) to the findings that explain them. -->
| Driver (Brief) | Related findings | Must be resolved by |
|----------------|------------------|---------------------|
| P-01 | D-01, D-03 | Target requirements |

## 7. Risks of Not Modernizing
| Risk | Related findings | Likelihood (L/M/H) | Impact (L/M/H) |
|------|------------------|--------------------|----------------|

## 8. Recommendations
| # | Recommendation | Addresses | Priority |
|---|----------------|-----------|----------|

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
