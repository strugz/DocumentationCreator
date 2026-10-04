---
name: new-proposal
description: MODE B (new project, no code yet). Write a New System Project Proposal for clients, management, or approvers, based on the brief, requirements, and plan. It covers the problem, proposed solution, scope, approach, timeline, budget structure, risks, benefits, and the approval request. Use when the user asks for a proposal, pitch, business case, or approval document for a system that is not built yet.
argument-hint: <project-slug> [client / budget / rates]
---

# Project Proposal (new system)

> **Mode B — New project.** For a project that already has code, use the Mode A
> `/doc-proposal` instead.

Input: `$ARGUMENTS` (slug, plus an optional client name, budget, or day rates).

## Preconditions
1. Resolve `<slug>`. Requires the brief and the requirements. The plan is strongly
   recommended. If `03-project-plan.md` is missing, run `new-plan` first so scope,
   timeline, and effort match.
2. Read the brief, requirements, plan, the design's §2–3 (for Appendix A),
   `mode-b-new-project/templates/04-project-proposal.md`, and
   `mode-b-new-project/rules/40-document-specific.md` §04.

## Procedure
1. **Problem statement:** from Brief §2, in the user's terms. Do not invent statistics
   about the client's business. Quantified pain points are `[TBD]` unless the user gave
   them.
2. **Objectives:** from the brief's goals (`G-xx`) with their measures.
3. **Proposed solution:** a plain-language overview, one simple diagram, and the Key
   Features table built from the in-scope features, all tagged **Planned**.
4. **Benefits:** every benefit names the feature that enables it. No benefit without a
   mechanism.
5. **Scope and deliverables:** In Scope = the Requirements' in-scope features. Out of
   Scope = the Requirements' Out of Scope list. Deliverables = the software plus the Mode B
   documents and the final manuals, with acceptance criteria (link to UAT).
6. **Approach and timeline:** summarize the Plan's phases and milestones. Use the same
   durations or dates.
7. **Team and budget:** roles from the Plan. Budget is a line-item structure. Compute
   amounts only if the user gave rates, as effort (from the Plan) × rate, and show the
   formula. Otherwise use `[TBD]`.
8. **Risks:** the top 5–8 from the Plan's register, in business language.
9. **Executive Summary:** write it last, at most one page, ending with the explicit
   approval request (e.g. "Approve Phase 0–1 to start on <date / [TBD]>").
10. **Appendix A:** the proposed stack and the context diagram from the design.

## Output
`output/mode-b/<slug>/04-project-proposal.md`

Run the review checklist. Confirm that the proposal scope equals the Requirements' scope
and the Plan's WBS. Report the file path and the Open Items. Client, approver, budget,
and dates are usually the most important ones.
