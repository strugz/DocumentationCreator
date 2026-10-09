# Rule 40 — Document-Specific Rules

> **Scope: Mode A only (project with existing code).** Mode B uses `mode-b-new-project/rules/`.

## 1. Project Completion Plan ("planning to finish")
- Start with an honest **current-state assessment**: what is done, partially done,
  not started, and broken. Base it on code evidence: implemented routes, screens,
  and modules; stubs; `TODO` / `FIXME` / `HACK` comments; skipped or failing tests;
  `NotImplementedError` / `throw new Error("not implemented")`; empty handlers;
  disabled features.
- Express completion as a **feature-by-feature status table**, not one vague percentage.
  If you give an overall percentage, show how you calculated it.
- Break remaining work into a **Work Breakdown Structure (WBS)**. Each item has an ID,
  a description, a definition of done, dependencies, a size (S/M/L/XL or points),
  and a priority (MoSCoW: Must / Should / Could / Won't).
- Timelines come only from user-provided dates or capacity. Otherwise give relative
  phases ("Phase 1: ~2 weeks after start") marked `[ASSUMPTION]`.
- Always include: Risks (likelihood × impact), Definition of Done for the whole project,
  a quality and testing plan, a deployment and go-live plan, and a handover checklist.
- Estimate and gate with `rules/45-estimation-and-release-gate.md`: fixed sizes for the
  remaining work, the AI-assisted factor when the profile says so, capacity, and one
  ready-to-deploy gate.

## 2. Project Proposal
- Structure: problem → proposed solution → scope → approach → timeline → resources
  and cost → risks → benefits → recommendation and call to action.
- Write an **Executive Summary** (≤ 1 page) that a decision-maker can read alone.
- Scope has explicit **In Scope** and **Out of Scope** lists.
- Every benefit links to a concrete feature. No benefit without a mechanism.
- Cost and budget sections use `[TBD]` unless the user gives figures. You may provide
  a cost **structure** (line items) without amounts.
- Keep technical depth light. Put architecture detail in an appendix.
- PowerPoint slides of the proposal, when requested, follow `rules/60-proposal-slides.md`
  and carry exactly the proposal's facts and markers.

## 3. User Manual
- Organized by **user goals and tasks**, not by code modules.
- Separate sections per **user role** if roles exist in the code (RBAC, permissions).
- Each task has: purpose, who can do it, prerequisites, numbered steps,
  expected result, and common errors.
- Error messages are quoted **exactly** from the code's UI strings, with their meaning
  and fix explained in a Troubleshooting table.
- No code, terminal commands, or internal file paths. Exception: CLI tools, where the
  "UI" *is* the command line.
- Include an FAQ and a Glossary of business terms.

## 4. Technical Manual (operations / administration)
- Audience: system administrators, DevOps, IT support. Not code authors.
- Must cover: system overview and architecture, hardware and software requirements,
  installation, configuration reference (every env var or config key with type, default,
  required?, and description), deployment, user and role administration, integrations,
  security, backup and restore, monitoring and logging, maintenance tasks,
  troubleshooting, and disaster recovery.
- Commands are exact and copy-pasteable, with the target OS shell named.
- The configuration reference is built by scanning the code for env and config reads
  (`process.env`, `os.environ`, `getenv`, `config.get`, `.env.example`, `appsettings.json`,
  etc.), not only from docs.

## 5. Developer Manual
- Audience: a new developer who must make a change in their first week.
- Must cover: tech stack with versions, repository structure map, local environment
  setup (verified commands), architecture and design patterns, module-by-module guide,
  data model (ERD), API reference (or link to API.md), coding standards (from linters
  and formatters actually configured), testing guide, build and CI/CD pipeline,
  branching and release process, how to add a feature (worked example), and known
  technical debt.
- Cite code locations (`path:line`) generously.
- Only document conventions that exist (lint configs, folder patterns, naming in code).
  Recommended conventions go in a separate "Recommendations" subsection.

## Repo docs (README.md / ARCHITECTURE.md / API.md)
- **README.md**: overview and purpose, prerequisites, quickstart install commands,
  core CLI or usage examples, and an architecture summary table (Module → Responsibility).
- **ARCHITECTURE.md**: directory structure map, high-level data flow and key entry
  points, component interactions, and external dependencies.
- **API.md**: for each primary function, class, or endpoint: signature, inputs, outputs,
  error conditions, and a usage snippet.
