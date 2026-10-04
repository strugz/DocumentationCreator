---
name: doc-proposal
description: MODE A (existing code). Write a Project Proposal for a fed-in project, aimed at clients, management, or approvers. It covers the problem, solution, scope, timeline, budget structure, risks, benefits, and approval. Use when the user asks for a proposal, project proposal, pitch document, business case, or approval document.
argument-hint: <project-slug or path> [client / purpose / budget]
---

# Project Proposal

> **Mode A — Existing project.** Use this skill only when source code exists. For an idea with no code yet, use the Mode B `new-*` skills.

> **Rules:** Before starting, read `mode-a-existing-project/rules/30-evidence-and-accuracy.md` and
> `mode-a-existing-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS` (project slug or path, plus optional client name, purpose such as
new build / continuation / enhancement, budget, or deadline).

## Preconditions
1. Resolve `<slug>`. Run the `doc-intake` procedure if the profile is missing.
2. Read the profile, `mode-a-existing-project/templates/02-project-proposal.md`, and `mode-a-existing-project/rules/40-document-specific.md` §2.
3. If `output/mode-a/<slug>/01-project-completion-plan.md` exists, reuse its scope, phases,
   milestones, and risks so the two documents agree.

## Determine the proposal type
Pick one from the evidence and the user's request, and state it in §1:
- **New system proposal:** pitch the solution as designed. Existing code is a prototype
  or proof of concept.
- **Completion / continuation proposal:** request approval or resources to finish.
  Scope is the remaining work from the Plan.
- **Enhancement proposal:** add features to a production system.
If you are unclear, default to the type that matches the project's maturity, and mark it
`[ASSUMPTION]`.

## Procedure
1. **Problem statement:** derive it from the domain (models, workflows, README) and from the
   user's input. Do not invent statistics about the client's business. Use `[TBD]` for
   quantified pain points.
2. **Key Features:** take them from the Features Inventory. Tag each one
   Existing / In progress / Planned.
3. **Benefits:** every benefit row must name the feature that enables it.
4. **Scope:** In Scope = features plus deliverables. Out of Scope = things a reader might
   assume are included but are not (e.g. mobile app, data migration, 24/7 support),
   based on what is absent from the code.
5. **Timeline:** reuse the Plan's phases if available. Otherwise use relative milestones.
6. **Budget:** give a line-item structure. Amounts stay `[TBD]` unless the user supplied them.
7. **Executive Summary:** write it last, at most 1 page, ending with the explicit approval request.
8. Keep technical detail in Appendix A (stack, a simple architecture diagram).

## Output
`output/mode-a/<slug>/02-project-proposal.md`

Run the review checklist. Report the file path, the proposal type chosen, and the Open
Items. Budget, client, and approver names are usually the most important ones.

**Automated check:** run `python tools/lint_docs.py output/mode-a/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
