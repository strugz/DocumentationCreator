# LLM Judge Rubric

The deterministic checks in each `case.json` catch the measurable failures. This rubric
covers what only a careful reader can judge. The judge must be a **fresh agent** that did
not write the documents.

## Inputs the judge reads
1. Every document in the run's `output/` folder.
2. The evidence: Mode A, the source project in `evals/cases/<case>/project/`; Mode B,
   `idea.md` and `answers.md` in the case folder.
3. The repository rules: `rules/` plus the mode's `rules/30-*.md` and `rules/40-*.md`.

## Criteria (score each document 1–5)
| Criterion | 5 means | 1 means |
|-----------|---------|---------|
| `grounded` | Every factual claim traces to the evidence; inferences are marked | Several claims invented or contradicted by the evidence |
| `audience` | Written for the document's stated reader and what they must do next | Wrong level of detail or jargon for the reader |
| `complete` | Every template section is meaningfully filled or justified as Not applicable | Many sections empty, boilerplate, or missing |
| `actionable` | The reader can act on it (decide, install, follow steps, build) without asking | Vague; the reader cannot act |
| `clear` | Plain, concise, consistent terminology; follows Rule 10 | Wordy, inconsistent, or confusing |

Score 3 is "acceptable for a first draft a human would edit". Be strict: do not give 5
unless you would send the document to a client unchanged.

## Output format
Write `judge.json` in the run's case folder (next to `output/`) with exactly this shape:

```json
{
  "judge_model": "<model id>",
  "documents": [
    {"file": "01-project-completion-plan.md",
     "scores": {"grounded": 4, "audience": 4, "complete": 3, "actionable": 4, "clear": 4},
     "notes": "One or two sentences on the main weakness."}
  ],
  "issues": [
    "02-project-proposal.md:L88 — states a 6-week timeline with no method shown"
  ]
}
```

`issues` lists the most important concrete problems with `file:Lline` references, worst
first, at most 10. Do not include praise.
