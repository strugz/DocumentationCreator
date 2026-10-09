# {{Product Name}} — Developer Manual

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Developer Manual |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | {{name}} |
| Status | Draft |
| Source revision | {{SHA}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (rules/35-readability.md).
     The codebase on one page (stack, run it locally, where to start reading, how to test, how to ship); the system in one picture or the request flow; a 'Where to Find What' table (I want to add a screen, an endpoint, a migration, a test → section).
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. Introduction
### 1.1 Purpose and Audience
### 1.2 Project Overview
### 1.3 Quick Links
<!-- Repo, issue tracker, CI, environments: [TBD] if unknown. -->

## 2. Technology Stack
| Layer | Technology | Version | Docs |
|-------|------------|---------|------|

## 3. Repository Structure
```text
{{annotated tree}}
```
| Path | Responsibility |
|------|----------------|

## 4. Local Development Setup
### 4.1 Prerequisites
### 4.2 Clone and Install
```bash
```
### 4.3 Environment Configuration
<!-- Point to .env.example; link to Technical Manual section 5 for the full reference. -->
### 4.4 Database Setup and Seeding
### 4.5 Running the Application
### 4.6 Common Setup Problems
| Problem | Fix |
|---------|-----|

## 5. Architecture
### 5.1 High-Level Architecture
```mermaid
flowchart LR
```
### 5.2 Design Patterns and Conventions in Use
<!-- e.g. MVC, repository pattern, DI, CQRS. Cite where each is used. -->
### 5.3 Request / Data Lifecycle
```mermaid
sequenceDiagram
```
### 5.4 Key Entry Points
| Entry point | File | Description |
|-------------|------|-------------|

## 6. Module Guide
<!-- Repeat per module. -->
### 6.1 {{Module name}}
- **Location:** `{{path}}`
- **Responsibility:**
- **Key files / classes / functions:**
  | Symbol | File:line | Purpose |
  |--------|-----------|---------|
- **Depends on:**
- **Used by:**
- **Gotchas:**

## 7. Data Model
```mermaid
erDiagram
```
| Entity | Table / Collection | Key fields | Notes |
|--------|--------------------|-----------|-------|
### 7.1 Migrations

## 8. API Reference
<!-- Summary here; full detail in API.md if it is large. -->
| Method | Path | Auth | Request | Response | Errors | Handler |
|--------|------|------|---------|----------|--------|---------|

## 9. Coding Standards
### 9.1 Style and Linting (as configured)
### 9.2 Naming Conventions (observed)
### 9.3 Error Handling Pattern
### 9.4 Logging Pattern
### 9.5 Recommendations (not yet enforced)

## 10. Testing
### 10.1 Test Strategy and Layout
### 10.2 Running Tests
```bash
```
### 10.3 Writing a New Test (example)
### 10.4 Coverage

## 11. Build and CI/CD
### 11.1 Build Process
### 11.2 CI Pipeline Stages
| Stage | What it does | Defined in |
|-------|-------------|-----------|
### 11.3 Release and Versioning

## 12. Git Workflow
### 12.1 Branching Strategy
### 12.2 Commit Message Convention
### 12.3 Pull Request / Code Review Process

## 13. How-To Guides
### 13.1 Add a New Feature (worked example)
### 13.2 Add a New API Endpoint
### 13.3 Add a Database Field / Migration
### 13.4 Add a New Configuration Setting

## 14. Debugging and Troubleshooting

## 15. Known Issues and Technical Debt
| Item | Location | Impact | Suggested fix |
|------|----------|--------|---------------|

## 16. Security Notes for Developers

## Appendix A — Glossary
## Appendix B — Useful Commands

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial draft |
