# Rule 45 — Estimation Method and Release Gate

> **Scope: Modes A and B.** Mode C uses the same method through
> `mode-c-modernize-project/rules/40-document-specific.md` section 04 and the gate in
> `mode-c-modernize-project/rules/50-readability-and-refinement.md` section 4. This rule
> is not preloaded: `/doc-plan`, `/new-plan`, `/doc-proposal`, `/new-proposal`, and
> `/new-test-plan` read it.

## 1. Sizes
Every WBS item gets one size. Use these values so totals are the same in every run.

| Size | Effort | Use for |
|------|--------|---------|
| S | 1 person-day | A small fix, one field, one config change |
| M | 3 person-days | One screen, one endpoint, one report |
| L | 5 person-days | A feature across screen, API, and data |
| XL | 10 person-days | Split it into smaller items when you can |

- For repeated work, use a count × unit ("12 reports × M").
- Mode A: size only remaining work. Done features have no effort. A Partial feature is
  sized for what is missing, not for the whole feature.

## 2. AI-assisted factor
Apply it only when the evidence base says the team uses AI-assisted coding (Mode A
Profile section 2, Mode B Brief section 3 "Development approach").

- Multiply **code-heavy** items (build, fix, refactor, unit tests) by **0.6**. Mark the
  factor `[ASSUMPTION]`.
- Testing by testers, user acceptance, approvals, training, pilot, and waiting time keep
  their full size. They do not shrink with faster coding; say so in the plan.
- Show **both** totals: assisted and unassisted.
- Check the factor against actual effort at the first milestone. If actual effort is more
  than 20 % above the assisted estimate, re-plan with the unassisted figure.

## 3. Capacity and duration
1. Capacity per month = developers × about 20 working days × focus. Focus defaults to
   75 % and is `[ASSUMPTION]` unless the user gave it.
2. Build duration = total build effort ÷ capacity per month.
3. Add the testing and acceptance time from the Test Plan, and a contingency. State the
   contingency percentage.
4. Use real dates only when the user gave a start date or deadline and the team size.
   Otherwise give relative durations ("month 1–3") marked `[ASSUMPTION]`.
5. If the deadline is shorter than the duration, say so plainly in the Executive Summary,
   and name the Should and Could items that move to a later release.

Show the method in the plan's Effort and Cost Estimate section with this table:

| Item | Basis | Estimate |
|------|-------|----------|
| Build effort (unassisted) | Sum of WBS sizes (section 1) | n person-days |
| Build effort (AI-assisted) | Code-heavy items × 0.6 `[ASSUMPTION]` | n person-days |
| Testing and acceptance | Test Plan schedule, full size | n person-days |
| Capacity | Developers × 20 days × 75 % focus `[ASSUMPTION]` | n person-days per month |
| Duration | Effort ÷ capacity + testing + contingency (n %) | n months |
| Cost | Effort × rate, only if the user gave rates | `[TBD]` otherwise |

## 4. When scope changes
- Re-check the total against capacity after every scope addition.
- Say plainly when the slack is gone. Add a risk for it, and name what moves to a later
  release if it slips.

## 5. Ready-to-deploy gate
Define **one** gate and use the same wording in the plan, the test plan, and the proposal.

> **Ready to deploy** when: all Must test cases pass; the testers sign off; user
> acceptance is signed; and, when there is a pilot, the pilot runs stable for the agreed
> period.

- **Testers by role**, as the evidence base records them (Profile section 2, Brief
  section 3): "QA personnel", "the IT team", "the client's users". Mark `[TBD]` when not
  given. Never invent a person's name.
- Where the gate appears:

| Document | Section |
|----------|---------|
| Plan | Milestones (the release milestone), Go-Live Checklist, Definition of Done, Read This First |
| Test Plan | Exit criteria of the last level, UAT Sign-Off, Read This First |
| Proposal | Approach and Methodology, Timeline and Milestones |

- **Milestone names:** "Release 1.0 tested and ready to deploy". With a pilot, add
  "<Site> pilot live" before it.
- **Client rollout:** a client or site deployment that depends on a later agreement is
  not scheduled. Describe it in the go-live section with a checklist instead.
