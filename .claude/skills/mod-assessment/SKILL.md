---
name: mod-assessment
description: MODE C (modernize an existing project). Write the Current State Assessment of an existing system from its Mode A Project Profile and source code, with severity-rated findings (technology currency, architecture, code quality, security, operations, data), a keep list, and modernization drivers. Use when the user asks for a technical assessment, legacy assessment, modernization readiness, health check, or "what is wrong with the current system" before a rebuild.
argument-hint: <project-slug>
---

# Current State Assessment

> **Mode C — Modernize an existing project.** For a plain tech-debt section inside the
> existing system's own documentation, use the Mode A Developer Manual instead.

> **Rules:** Before starting, read `mode-c-modernize-project/rules/30-evidence-from-profile.md`,
> `mode-c-modernize-project/rules/40-document-specific.md`, and (for citing code)
> `mode-a-existing-project/rules/30-evidence-and-accuracy.md`. They are not preloaded.

> **Also read** `mode-c-modernize-project/rules/50-readability-and-refinement.md`, and
> follow the brief section 4 answers on rollout, testers, release gate, names and wording.

Input: `$ARGUMENTS` (slug).

## Preconditions
1. Resolve `<slug>`. `output/mode-c/<slug>/00-modernization-brief.md` must exist (run
   `mod-brief` if not). Read it, the Mode A profile it names, and any other Mode A
   documents for the project (Completion Plan section current state and risks, Technical
   Manual, Developer Manual tech-debt section).
2. Read `mode-c-modernize-project/templates/01-current-state-assessment.md` and
   `mode-c-modernize-project/rules/40-document-specific.md` section 01.
3. The source project (brief `Source location`) is **read-only**. Open files to confirm
   findings and to cite `path:line`.

## Procedure
1. **Summary and overview:** describe the system as built, in the present tense, from the
   profile (sections 1, 3 and 6). Draw one architecture diagram of what exists.
2. **Stack currency:** for each layer in Profile section 3, record the version in use and the
   latest supported or LTS version you are confident of. Mark every end-of-support date
   `[VERIFY: vendor page]`. Classify each layer Current / Ageing / Unsupported.
3. **Findings:** one row per finding, `D-01`…, with category, severity, evidence, and the
   consequence for the target system. Cover every area in Rule 40 section 01. Draw on:
   - Profile section 14 Quality Signals (tests, linters, CI, TODO count), section 15 Incomplete Work,
     section 16 Security Observations, section 18 Discrepancies.
   - The code itself for anything the profile only hints at (open the file, cite the line).
   - The brief's pain points (`P-xx`): confirm each against the evidence or mark `[VERIFY]`.
   Severity reasoning is one line. No invented numbers.
4. **Keep list:** what works well and should survive: stable modules, a sound data model,
   integrations that work, tests worth porting. Cite evidence.
5. **Drivers:** map every brief pain point and goal to the findings that explain it.
6. **Risks of not modernizing:** from the Critical and High findings.
7. **Recommendations:** what the target requirements and design must address, in
   priority order. These become the `D-xx` sources in the Target Requirements.

## Readability layer
Write the `Read This First` section (Rule 50 section 1): the assessment on one page (does the
workflow work, where the problems are, counts by severity, the most serious findings, what
should be done), a severity guide, the main problems in plain words with what the target
does instead, and the "problem to fix" flow. Add an "In short" note under every numbered
section. Statements about the current system stay in the present tense.

## Output
`output/mode-c/<slug>/01-current-state-assessment.md`

Run the review checklist. Report the file path, the finding counts by severity, the top
three findings, the keep list size, and the Open Items.

**Automated check:** run `python tools/lint_docs.py output/mode-c/<slug>` and fix every
error before reporting. The project hook also lints each write; this final run catches
cross-document issues (IDs, traceability, citations).
