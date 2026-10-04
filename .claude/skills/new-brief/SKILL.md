---
name: new-brief
description: MODE B (new project, no code yet). Turn a project idea into a Project Brief by interviewing the user, writing output/mode-b/<slug>/00-project-brief.md that every other Mode B document depends on. Use when the user says "I want to build…", "create a project like…", "plan a new system for…", "I have an idea for an app", or before any other new-* skill when no brief exists.
argument-hint: <project idea in plain words> [project name]
---

# New Project Intake → Project Brief

> **Mode B — New project.** Use this skill when there is no code yet. If code already
> exists, use the Mode A `/doc-intake` skill instead.

> **Rules:** Before starting, read `mode-b-new-project/rules/30-evidence-from-brief.md` and
> `mode-b-new-project/rules/40-document-specific.md`. They are not preloaded.

Input: `$ARGUMENTS`. This is the user's idea, as short or as long as they like. If it is
empty, ask: "Describe the system you want to build in a few sentences: what it does and
who uses it."

Follow `CLAUDE.md`, the shared `rules/`, and the Mode B rules in
`mode-b-new-project/rules/`. Write documents only, never application code.

## Step 1 — Set up
1. Derive a working product name. Use the name the user gave; otherwise use a plain
   descriptive name (e.g. "Warehouse Inventory System") and mark it `[ASSUMPTION]`.
2. Derive `<slug>` (lowercase-kebab-case) and create `output/mode-b/<slug>/` and
   `output/mode-b/<slug>/assets/`.
3. If `output/mode-b/<slug>/00-project-brief.md` already exists, read it. You are
   **updating** it: increase the brief version and add a Revision History row.
4. If the user attached or pointed to material (notes, forms, spreadsheets, an old
   system's screenshots), read it now. It is evidence level 2.

## Step 2 — Extract what is already known
Read the idea and map every fact in it to the brief sections in
`mode-b-new-project/templates/00-project-brief.md`. Do not ask about things the user
already said.

## Step 3 — Interview (one round)
**Non-interactive runs:** if the input already contains interview answers, or says it is a
non-interactive or evaluation run, do not ask anything. Record the given answers in the
Interview Log, treat every unanswered question as `[TBD]` (do **not** silently accept
defaults; a suggested default may appear only as **Proposed**), and continue to Step 4.

Ask the remaining questions in **one message**, grouped and numbered. Ask at most about
12 questions. For each one, give a suggested default in brackets so the user can reply
quickly. Skip any group the idea already answers.

| Group | Questions to cover |
|-------|--------------------|
| A. Purpose | What problem does this solve? How is the work done today? What does success look like? |
| B. Users | Who uses it (roles)? Roughly how many of each? Who is the administrator? |
| C. Features | The must-have features for the first release. Nice-to-haves. Anything explicitly excluded. |
| D. Workflows | The 2–3 most important things a user does, start to finish. |
| E. Data and reports | What information is stored? Which reports or exports are needed? Is there existing data to import? |
| F. Platform | Web, mobile, or desktop? Cloud or on-premise? Any required tech stack? Sign-in method? Languages? Offline use? |
| G. Integrations | Other systems it must connect to (email, payments, ERP, Active Directory, SMS). |
| H. Constraints | Deadline, budget, team size, regulations (data privacy, industry rules). |
| I. Context | Client or organization name, approver, stakeholders. |

End the message with: "Answer what you can. Reply **use defaults** to accept my
suggestions, or **skip** for anything you don't know yet; I'll mark it `[TBD]`."

Optionally, when two to four high-impact choices have clear options (platform, hosting,
sign-in method), use the `AskUserQuestion` tool for those instead of free text.

Wait for the reply. Ask a **second round** only if the purpose, the main users, or the
core features are still unknown. These three block every other document.

## Step 4 — Write the brief
Fill `mode-b-new-project/templates/00-project-brief.md` completely and write it to
`output/mode-b/<slug>/00-project-brief.md`.
- Record answers in the **Interview Log**, in the user's words.
- Features: assign stable IDs (`F-01`…), a MoSCoW priority, and a decision state.
  Features the user named are **Agreed**. Features Claude suggests (e.g. password reset,
  audit log) are **Proposed** and must give a reason.
- Roles get `R-01`…, constraints `C-01`….
- Where the user accepted defaults, record the value with Source = "Proposed (accepted
  default)".
- Put unknown business facts (budget, dates, names) in §3 as `[TBD]` and in §19.
- Put real choices in §18 Decisions Needed as `[DECISION: ...]` with a recommendation.
- Build the Glossary from the user's own words for things (e.g. "job order", not "ticket",
  if that is what they say).

## Step 5 — Report
Give the user:
1. A 5-line summary: what will be built, for whom, the platform, and the feature count by
   priority (Must / Should / Could).
2. The **Decisions Needed** and the most important **Open Questions**.
3. The next step: `/new-suite <slug>` for the full document set, or a single skill such
   as `/new-requirements <slug>`.

**Automated check:** run `python tools/lint_docs.py output/mode-b/<slug>` and fix every error before
reporting. The project hook also lints each write; this final run catches cross-document
issues (IDs, traceability, citations).
