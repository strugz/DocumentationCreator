# evals/ — measuring documentation quality

The eval set answers one question: **did a change to a rule, template, or skill make the
documents better or worse?** Run it before and after the change and compare.

## How it works
| Layer | What | Cost |
|-------|------|------|
| 1. Lint | `tools/lint_docs.py` on the whole output folder (structure, markers, IDs, citations, secrets) | Free |
| 2. Case checks | Facts each case **must** contain and traps it **must not** fall into (`case.json`) | Free |
| 3. LLM judge (optional) | A fresh agent scores each document 1–5 against `rubric.md` | Tokens |

Layers 1–2 produce the **score** (weighted pass rate, 0–100). Layer 3 is reported next to
it but kept separate, because model judgments vary between runs.

## Cases
| Case | Mode | Input | Traps it tests |
|------|------|-------|----------------|
| `a-tasktrack` | A | Small Flask app in `cases/a-tasktrack/project/` | README feature with no code (Slack), planted secrets in `.env`, stub endpoint, env var missing from `.env.example`, unused config |
| `b-clinic-booking` | B | `idea.md` + scripted `answers.md` | Excluded feature (payments), undecided hosting → `[DECISION]`, no budget → no amounts, given deadline, unnamed client |
| `c-tasktrack-modernize` | C | The `a-tasktrack` fixture project + scripted `answers.md` (target stack NestJS/React/PostgreSQL, strangler-fig migration, feature dispositions) | Planted secrets, Slack (README-only) must be Drop and never a current capability, stub export must be reported unfinished, undecided hosting → `[DECISION]`, user-skipped testing layer → Proposed, no budget or dates → no amounts or phase dates, unnamed organization. Also: every profile `F-xx` in the Feature Disposition table, parity requirements and `TC-P-xx` tests, data migration and cutover tests |

Do not "fix" the fixture project: its flaws are the test.

### Prerequisites (Mode C)
A Mode C case depends on a Mode A profile. Its `case.json` names it in `prerequisite`
(mode, slug, file, and the skill that builds it). The generation prompt tells the agent to
reuse `output/mode-a/<slug>/00-project-profile.md` if it exists and to build it with
`doc-intake` first if it does not, so the case runs on its own. `collect` copies that
folder into the run as `prerequisite/` (next to `output/`), and checks refer to it with
the `prerequisite/` prefix, for example `prerequisite/00-project-profile.md`. The case
shares the slug `eval-tasktrack` with `a-tasktrack`, so a profile left over from a Mode A
run is reused; `collect a-tasktrack` moves it away, in which case the Mode C run rebuilds
it.

## Running

With the Claude Code CLI installed (headless):

```bash
python evals/run_evals.py run all --judge
```

Without the CLI (for example, from the desktop app): generate in a Claude Code session,
then collect.

```bash
python evals/run_evals.py prompt b-clinic-booking
```

Paste the printed prompt into a fresh Claude Code session (or give it to a subagent), then:

```bash
python evals/run_evals.py collect b-clinic-booking --run 20261004-baseline
```

Optional judge: print the judge prompt, run it in a **separate** fresh session, then re-grade.

```bash
python evals/run_evals.py judge-prompt 20261004-baseline b-clinic-booking
```

```bash
python evals/run_evals.py grade 20261004-baseline
```

## Comparing against the baseline

```bash
python evals/run_evals.py baseline 20261004-baseline
```

```bash
python evals/run_evals.py compare <NEW_RUN_ID>
```

`compare` lists score changes per case and every check that started failing (exit code 1
if any did). Treat a newly failing trap check (secrets, invented costs, false features) as
a blocker.

> [!NOTE]
> Generation is not deterministic. Before concluding that a change helped, run each case
> at least twice. A difference of one minor check is noise; a trap check flipping is not.

## Adding a case
1. Create `cases/<id>/` with `case.json` plus either `project/` (Mode A), `idea.md` and
   `answers.md` (Mode B), or an `input` pointing at a Mode A fixture project, a
   `prerequisite` block, and `answers.md` (Mode C). Use the slug prefix `eval-`; a Mode C
   case uses the same slug as its Mode A profile.
2. Plant at least three traps that a careless generator would fall into, and write one
   check per trap with a high `weight`.
3. Add checks for the facts a correct document **must** contain. Prefer facts that come
   from one specific place in the evidence.
4. Run `python -m unittest discover -s tests`. It validates every `case.json`.

Check types are documented at the top of `grade.py`.
