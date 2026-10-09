---
name: mod-proposal
description: MODE C (modernize an existing project). Write a Modernization Proposal for clients, management, or approvers, built from the Current State Assessment, Target Requirements, and Migration Plan. It covers the problems with the current system, options considered, the proposed target and strategy, scope by disposition, timeline, cost structure including parallel run and decommissioning, risks, benefits, and the approval request. Use when the user asks for a modernization proposal, business case for a rewrite, migration pitch, or approval document for rebuilding an existing system.
argument-hint: <project-slug> [client / budget / rates]
---

# Modernization Proposal

> **Mode C — Modernize an existing project.** For a brand-new system use the Mode B
> `/new-proposal`; for completing the existing system as it is, use the Mode A
> `/doc-proposal`.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`
> and `mode-c-modernize-project/rules/40-document-specific.md`. They are not preloaded.

> **Also read** `mode-c-modernize-project/rules/50-readability-and-refinement.md`, and
> follow the brief section 4 answers on rollout, testers, release gate, names and wording.

Input: `$ARGUMENTS` (slug, plus optional client, budget, and rates, recorded in the
brief section 4 first).

## Preconditions
1. Resolve `<slug>`. The brief, assessment, and requirements must exist. If
   `04-migration-plan.md` is missing, run the `mod-plan` procedure first.
2. Read the brief, the assessment, the requirements, the design (section 3 Stack Comparison),
   the plan, `mode-c-modernize-project/templates/05-modernization-proposal.md`, and
   `mode-c-modernize-project/rules/40-document-specific.md` section 05.

## Procedure
1. **Executive summary:** one page a sponsor can read alone: the current system, why it
   must change, the proposed target and strategy, headline timeline and cost (or `[TBD]`),
   and the approval requested.
2. **Problem statement:** the assessment's Critical and High findings, rewritten for a
   non-technical reader, each with its business consequence and the `D-xx` it comes
   from. No numbers the evidence does not contain.
3. **Options considered:** Do nothing / Upgrade in place / Partial modernization / Full
   rebuild, with what each addresses and misses. Mark the recommended option and tie it
   to the brief's strategy decision (or the `[DECISION]` if still open).
4. **Proposed solution:** plain language, future tense. Key features tagged with their
   disposition; a non-technical summary of the target technology (details in Appendix A).
5. **Scope:** in-scope list equal to the requirements and the plan's WBS; Drop features
   under out of scope with reasons; deliverables with acceptance criteria.
6. **Approach, timeline, team:** reuse the plan's strategy, phases, and milestones
   exactly. Do not restate figures differently.
7. **Cost:** the line-item structure including data migration, parallel run, and
   decommissioning. Amounts `[TBD]` unless the user supplied rates; an effort estimate
   only with the plan's method.
8. **Benefits and risks:** every benefit names the feature or finding that enables it.
   Risks come from the plan's register, condensed.
9. **Recommendation and approval:** a clear call to action with the next phase and the
   decisions the approver must make.
10. **Appendix A:** the Stack Comparison summary and one target architecture diagram.

## Readability layer
Write the `Read This First` section (Rule 50 section 1): the proposal on one page (what we ask
for, why, what we get, who builds, who tests, when it is ready, effort), the system in one
picture, the case flow, the SDLC flow and the ready-to-deploy gate, using the same Mermaid
source as the design and plan. Add an "In short" note under every numbered section. Write
the problems from the users' point of view, the options as one short paragraph, a plain
tech stack table and a Support Needed table (Rule 40 section 05). Use roles, not personal names,
as the brief section 4 says.

## Output
`output/mode-c/<slug>/05-modernization-proposal.md`

Run the review checklist. Report the file path, the recommended option, the headline
scope counts by disposition, the cost and timeline status (given or `[TBD]`), and the
Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
