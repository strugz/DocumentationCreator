# Rule 30 (Mode B) — Evidence from the Brief

> **Scope: Mode B only (new project, no code yet).** Mode A uses
> `mode-a-existing-project/rules/30-evidence-and-accuracy.md`.

In Mode B there is no code to read. The **user is the evidence**. Claude's job is to
record what the user wants, fill the gaps with clearly labeled proposals, and never
present a proposal as a decision or a plan as a finished product.

## Evidence hierarchy (strongest first)
1. Decisions and answers the user states in chat, recorded in the brief.
2. Material the user supplies: notes, emails, existing forms, spreadsheets, sample
   reports, screenshots of a current system, regulations they name.
3. Earlier approved Mode B documents for the same project (e.g. an approved
   Requirements Specification outranks a later design draft).
4. Industry practice and well-known standards (e.g. OWASP, WCAG, GDPR) — usable as the
   basis for a **Proposed** item, never as a claim about the user's business.
5. Reasonable inference — always marked (see below).

If two sources conflict, trust the stronger source and record the conflict in the
brief's **Discrepancies** section.

## Labels and markers (use exactly these forms)
| Label / Marker | Meaning | Example |
|----------------|---------|---------|
| **Proposed** | A design or technical choice Claude suggests because the user did not decide it. Always give a one-line reason. | `Database: PostgreSQL 16 — **Proposed** (relational data, free, wide hosting support)` |
| `[DECISION: ...]` | The user must choose between named options before work can continue. List the options and Claude's recommendation. | `[DECISION: hosting — on-premise server / Azure / AWS. Recommended: Azure, because the client already uses Microsoft 365]` |
| `[TBD: ...]` | Information needed that the user has not given. | `[TBD: go-live date]` |
| `[ASSUMPTION: ...]` | Inferred from what the user said; plausible but unconfirmed. | `[ASSUMPTION: about 20 staff users, based on "a small team"]` |
| `[VERIFY: ...]` | Stated by the user but possibly inconsistent or risky. | `[VERIFY: brief says offline use, but also real-time sync between branches]` |

- Never remove a marker unless the user resolves it. When resolved, update the brief
  first, then every document that uses the fact.
- Every document ends with an **Open Items** section that lists all its markers,
  including every `[DECISION]`.

## Never invent
- Costs, budgets, prices, rates, or effort hours. Estimates are allowed only when labeled
  as estimates with the method shown (e.g. WBS size × team capacity).
- Dates, deadlines, or milestones not given by the user.
- Names of people, clients, organizations, vendors, or stakeholders.
- Business statistics: current losses, error rates, user counts, transaction volumes,
  growth. Use `[TBD]` and ask.
- Performance targets, SLAs, or uptime figures presented as agreed. Claude may suggest
  targets only as **Proposed** values in the Requirements Specification.
- Regulations that apply to the user. Claude may say "If you handle personal data of
  EU residents, GDPR applies" and mark it `[VERIFY]`.

## Tense and status
- Describe the system in the **future tense or as a requirement**: "The system shall
  send a confirmation email", "Users will be able to…". Never "The system sends…" as if
  it already exists.
- Feature status values in Mode B: **Must / Should / Could / Won't** (priority) and
  **Proposed / Agreed / Deferred** (decision state). Never use Done, Partial, or Broken.
- Draft manuals carry a banner: "This manual describes the planned system. Screens,
  labels, and commands will change during development."

## Traceability
- Brief features get stable IDs `F-01, F-02…`; roles get `R-01…`; constraints `C-01…`.
- Requirements get `FR-01…` (functional) and `NFR-01…` (non-functional), each pointing
  back to a feature `F-xx` or a brief section (`Brief §n`).
- Design components, WBS items, and test cases point to the `FR`/`NFR` IDs they serve.
- The Requirements Specification holds the master **Traceability Matrix**.

## Source revision
Mode B documents have no git commit. In the Document Control block write
`Source revision | Brief v<n>, YYYY-MM-DD` using the brief's version and date.
