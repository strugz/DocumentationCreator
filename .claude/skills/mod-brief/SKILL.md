---
name: mod-brief
description: MODE C (modernize an existing project). Turn a Mode A Project Profile into a Modernization Brief by interviewing the user about the target tech stack, migration strategy, and which features to keep, improve, replace, or drop. Writes output/mode-c/<slug>/00-modernization-brief.md, which every other mod-* skill depends on. Use when the user says "modernize this project", "rebuild it with a new stack", "optimize the existing system into a new project", "migrate it to <technology>", or before any other mod-* skill when no modernization brief exists.
argument-hint: <mode-a project-slug or code path> [project name] [target stack hints]
---

# Modernization Intake → Modernization Brief

> **Mode C — Modernize an existing project.** The current system exists and is documented
> by Mode A; the target system does not exist yet. If there is no code at all, use the
> Mode B `/new-brief` skill instead. If you only need documentation of what exists, use
> Mode A.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`,
> `mode-c-modernize-project/rules/40-document-specific.md`, and
> `mode-c-modernize-project/rules/50-readability-and-refinement.md`. They are not preloaded.

Input: `$ARGUMENTS`: a Mode A slug (preferred) or a code path, an optional product name,
and optional hints about the target stack. If it is empty, ask: "Which project do you want
to modernize? Give the Mode A slug under `output/mode-a/` or the path to its code."

Follow `CLAUDE.md`, the shared `rules/`, and the Mode C rules in
`mode-c-modernize-project/rules/`. Write documents only, never application code.

## Step 1 — Find or build the Mode A profile
1. If the input is a slug and `output/mode-a/<slug>/00-project-profile.md` exists, read it.
2. If the input is a code path, derive the slug (lowercase-kebab-case of the project name)
   and look for the profile. If it does not exist, run the `doc-intake` procedure
   (`.claude/skills/doc-intake/SKILL.md`) on the path first. The source code is
   **read-only**.
3. Also read, if they exist: `01-project-completion-plan.md` (remaining work, risks),
   `04-technical-manual.md` (operations, configuration), and `05-developer-manual.md`
   (tech debt). They are evidence level 3.
4. Use the same slug for Mode C. Create `output/mode-c/<slug>/` and
   `output/mode-c/<slug>/assets/`.
5. If `output/mode-c/<slug>/00-modernization-brief.md` already exists, read it. You are
   **updating** it: increase the brief version and add a Revision History row.

## Step 2 — Carry the current facts into the brief
From the profile, fill brief section 1 (description, type, maturity, current stack), section 5 (roles,
`R-xx`), section 6 (every `F-xx` from Profile section 7 with its current status), section 9 (entities from
Profile section 10), section 10 (integrations from Profile section 12), and section 17 (glossary from Profile section 17).
Copy `Source location` and `Source revision` into the Document Control block. Keep the
profile's IDs unchanged so that documents in both modes refer to the same features.

Do not ask the user about anything the profile already answers.

## Step 3 — Interview (one round)
**Questionnaire answers:** if `output/mode-c/<slug>/07-tech-stack-questionnaire.md` exists
with consolidated responses (section 7), use them as interview answers (source "Questionnaire
(<role>)" in the Interview Log) and ask only what they leave open. If the user wants the
stack decided by stakeholders and developers rather than in this interview, record the
undecided layers as `[DECISION]`; `/mod-suite` always writes the questionnaire that
collects their answers.

**Non-interactive runs:** if the input already contains interview answers, or says it is a
non-interactive or evaluation run, do not ask anything. Record the given answers in the
Interview Log, treat every unanswered question as `[TBD]` or `[DECISION]` (do **not**
silently accept defaults; a suggested default may appear only as **Proposed**), and
continue to Step 4.

Ask the remaining questions in **one message**, grouped and numbered. Ask at most about
15 questions; skip any the request or the profile already answers. For each one, give a suggested default in brackets so the user can reply
quickly. Group C (target tech stack) is **always asked**, layer by layer, and shows the
current technology next to each layer so the user can say "keep" or name a replacement.

| Group | Questions to cover |
|-------|--------------------|
| A. Why | Who asked for this, and what exactly did they ask for (paste the request if there is one)? What is wrong with the current system **in the words of the people who use it every day** (for example laboratory staff, not developers)? What should be true after the modernization (goals)? What must not change? |
| B. Strategy | Is the current system in production? Can it be frozen during migration? Big-bang rewrite, incremental (strangler fig), lift-and-shift then refactor, or re-platform only? [default from the profile's maturity: production → incremental] |
| C. Target tech stack | For each layer: language, backend framework, frontend / UI, database, authentication, hosting / infrastructure, CI/CD, testing. Show "current: X → keep / replace with …?" with a suggested default and a one-line reason. Also: team skills the stack must fit; licensing or vendor constraints; must-use or must-avoid technologies. |
| D. Scope | Confirm the Feature Disposition table: for each `F-xx`, Keep / Improve / Replace / Drop, with Claude's default. Any new features? Anything explicitly excluded? |
| E. Data | Must existing data migrate? Which entities, roughly how much data? Anything to archive or drop? |
| F. Integrations | For each integration in the profile: keep, replace, or drop? New ones? |
| G. Quality | Performance, availability, security, or compliance expectations that the target must meet (numbers only if they have them). |
| H. Constraints | Target year or deadline, budget, team (how many developers, full time?), development approach (AI-assisted coding such as Claude? [default: yes, estimate ×0.6, checked at the first milestone]), regulations, parallel-run limits. |
| I. Rollout | Where does the new version run first (pilot site)? When does a client or site receive it [default: only after it is thoroughly tested and ready to deploy]? Is any data migrated from the current system [default: none in release 1; an option at the end]? |
| J. Testing | Who tests integrations or analyzer transmission and the full system (for example QA and an IT or interface team)? Who runs user acceptance? [default: release gate = all Must tests pass, testers sign off, UAT signed, pilot stable two weeks] |
| K. Audience and wording | Who approves (name the body, for example Management)? Use personal names or roles in the documents [default: roles — "Management", "the development team"]? Any words or phrases to avoid? |
| L. Deliverables | Word files, a presentation deck (online and PowerPoint), a starter kit for the new code repository [default: all]. The tech stack questionnaire is always written. |

Where it helps, use the `AskUserQuestion` tool for the highest-impact choices: the
migration strategy, and the backend, frontend, database, and hosting layers. Offer three
to four concrete options per question, with the current technology as one option
("Keep <current>, upgrade to the supported version") and Claude's recommendation first.
Put every other question in the single chat message.

End the message with: "Answer what you can. Reply **use defaults** to accept my
suggestions, or **skip** for anything you don't know yet; I'll mark it `[TBD]` or
`[DECISION]`."

Wait for the reply. Ask a **second round** only if the migration strategy or the
disposition of the Must features is still unknown. These block every other document.

## Step 4 — Write the brief
Fill `mode-c-modernize-project/templates/00-modernization-brief.md` completely and write
it to `output/mode-c/<slug>/00-modernization-brief.md`.
- Record answers in the **Interview Log**, in the user's words.
- Section 2: pain points get `P-01`…; where the profile has evidence for a pain point, cite it
  (`Profile section 15`, `path:line`); where it has none, mark `[VERIFY]`.
- Section 6 Feature Disposition: dispositions the user confirmed are **Agreed**; Claude's
  defaults are **Proposed** with a reason. New features continue the `F-xx` numbering.
- Section 7 Target Tech Stack: one row per layer with Current, User preference, Target, and
  Reason. A layer the user decided is Agreed. A layer with no decision gets a
  **Proposed** value here and a `[DECISION]` in section 16 with the options and recommendation.
  Prefer mainstream, supported technologies the stated team can work with; mark vendor
  end-of-support dates `[VERIFY]`.
- Section 8 Migration Strategy: the user's choice, or `[DECISION]` with a recommendation that
  cites the profile's maturity.
- Put unknown business facts (budget, dates, volumes, names) in sections 4 and 9 as `[TBD]` and
  list them in sections 19. to 4 records the rollout, testing, release gate, naming, wording and deliverables answers
  (groups I to L). These bind every later document and the slides (Rule 50 sections 2 and 4). Pain
  points in section 2 keep the users' wording.
- Record conflicts between the user's statements and the profile in section 18 Discrepancies.
- Where the user accepted defaults, record the value with Source = "Proposed (accepted
  default)".

## Step 5 — Report
Give the user:
1. A 5-line summary: what is being modernized, the strategy, the target stack per layer
   (Agreed vs Proposed), and the feature counts by disposition (Keep / Improve / Replace /
   Drop / New).
2. The **Decisions Needed** and the most important **Open Questions**.
3. The next step: `/mod-suite <slug>` for the full document set, or a single skill such
   as `/mod-assessment <slug>`.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
