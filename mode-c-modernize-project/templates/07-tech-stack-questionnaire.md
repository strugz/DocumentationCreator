# {{Product Name}} — Tech Stack Questionnaire

<!-- MODE C questionnaire, written by /mod-suite in every run right after the brief. It collects tech stack input from
     stakeholders (Part A, no technical knowledge needed) and developers (Parts B and C)
     before the stack is decided. Current facts come from the Mode A profile; Proposed
     values and open questions come from the brief (section 7 Target Tech Stack, section 16 Decisions
     Needed) when it exists. Ask only what the profile and the brief do not already answer.
     The Response Summary (section 7) stays empty until answers return. Remove comments in output. -->

| Field | Value |
|-------|-------|
| Project | {{Product Name}} |
| Document | Tech Stack Questionnaire (stakeholders and developers) |
| Version | 0.1 (Draft) |
| Date | {{YYYY-MM-DD}} |
| Prepared by | Generated with Claude, reviewed by {{role / [TBD]}} |
| Status | Draft / Sent / Responses received / Consolidated |
| Source revision | Profile {{mode-a slug}} @ {{git SHA / "working copy, YYYY-MM-DD"}}; Modernization Brief v{{n}}, {{YYYY-MM-DD}} (or "no brief yet") |
| Reply by | {{YYYY-MM-DD / [TBD]}} |
| Return answers to | {{role, for example "the development team"}} |

## Table of Contents

## Read This First
<!-- Plain-language entry page (mode-c-modernize-project/rules/50-readability-and-refinement.md section 1).
     One-page table: Why are we asking? Who answers which part? How long does it take
     (about N minutes per part)? By when? What happens with the answers? Each answer has a
     section reference. Then the questionnaire flow:
     Mode A profile → questionnaire sent → stakeholders answer Part A, developers answer
     Parts B and C → answers summarized (section 7) → brief updated → stack decided → documents updated.
     Add an 'In short' note under every numbered ## section:
     > [!NOTE]
     > **In short:** <one or two plain sentences> -->

## 1. How to Answer
- Answer only the parts for your role: **Part A** for management, system owners and key
  users; **Parts B and C** for developers and IT staff.
- Tick one box (☐ → ☒) per question unless the question says "tick all that apply".
- **Current** is what today's system uses. **Proposed** is our suggestion, with the reason.
  You may keep, accept, or replace either one.
- "Don't know" is a valid answer. Leave the comment box empty if you have nothing to add.
- Never write passwords, keys, server addresses or personal data in your answers.

## 2. The Current System at a Glance
<!-- Plain language, from brief section 1, or Profile sections 1 and 3. No code paths. -->
- **What it does:** {{one line}}
- **Who uses it:** {{roles from brief section 5 / Profile section 8}}
- **Main problems today:** {{P-xx from brief section 2, in the users' words, or "not yet collected"}}

| Layer | Today's technology | Version | In plain words |
|-------|--------------------|---------|----------------|
| Language | | | |
| Backend framework | | | |
| Frontend / UI | | | |
| Database | | | |
| Authentication | | | |
| Hosting / Infrastructure | | | |
| CI/CD | | | |
| Testing | | | |

## 3. Part A — Stakeholder Questions
<!-- For management, system owners and key users. No technical terms without a plain
     explanation. Each row: ID, question, why we ask (one line), answer options, answer.
     Skip a question the brief already answers; keep the ID numbering continuous. -->

### 3.1 Goals and Priorities
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-A-01 | What must the new version do better than today? | Sets the goals (brief section 3) | |
| Q-A-02 | Rank from 1 (most important) to 5: delivery speed, low cost, ease of use, security, room to grow. | Guides every stack trade-off | Speed __ Cost __ Ease __ Security __ Growth __ |
| Q-A-03 | What must not change for the people who use it every day? | Protects what works (Keep features) | |

### 3.2 Users and Access
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-A-04 | Where do users work? (tick all that apply) | Decides web vs desktop and network design | ☐ On site, company network ☐ Remote / home ☐ Mobile devices ☐ Other: ____ |
| Q-A-05 | About how many people use it at the same time? | Sizes servers and the database | ☐ Under 20 ☐ 20–100 ☐ 100–500 ☐ Over 500 ☐ Don't know |
| Q-A-06 | Must it keep working when the network or internet is down? | Decides offline support | ☐ Yes ☐ No ☐ Only some tasks: ____ |

### 3.3 Hosting, Security and Compliance
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-A-07 | Where may the system and its data be hosted? | Decides hosting (brief section 7) | ☐ Our own servers ☐ Cloud ☐ Either ☐ Don't know |
| Q-A-08 | Which rules or regulations apply to the data (for example data privacy laws or industry standards)? | Sets security and audit requirements | |
| Q-A-09 | How long may the system be down before work stops? | Sets availability and backup needs | ☐ Minutes ☐ Hours ☐ A day ☐ Don't know |
| Q-A-10 | Does IT have an approved list of technologies or vendors? | Rules out options early | ☐ Yes (attach or name it) ☐ No ☐ Don't know |

### 3.4 Budget, Licences and Support
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-A-11 | Preference for software licences? | Decides open-source vs paid products | ☐ Free / open-source preferred ☐ Paid is fine if justified ☐ No preference |
| Q-A-12 | Who supports the system after go-live? | Stack must fit the support team's skills | ☐ The development team ☐ IT department ☐ Outside vendor ☐ Not decided |
| Q-A-13 | Is depending on one vendor or product a concern? | Weighs lock-in risk | ☐ Yes ☐ No ☐ Don't know |

### 3.5 Timeline and Rollout
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-A-14 | Is there a target date or deadline? | Limits stack choices the team must learn | |
| Q-A-15 | Where should the new version run first (pilot)? | Plans the pilot environment | |
| Q-A-16 | May the current system be frozen (no changes) during the rebuild? | Decides the migration strategy | ☐ Yes ☐ No ☐ Only urgent fixes |

## 4. Part B — Developer Questions: Tech Stack by Layer
<!-- One subsection per layer, in brief section 7 order. Current from Profile section 3; Proposed and
     reason from brief section 7 (or Claude's suggestion labeled Proposed when no brief exists).
     Mark a layer whose brief row is a [DECISION] with "(decision needed)" in its heading
     text after the layer name. Options: keep current (upgrade to a supported version),
     Proposed, one or two mainstream alternatives, Other. -->

### 4.1 Backend Language and Framework
| Item | Answer |
|------|--------|
| Current | {{technology and version}} |
| Proposed | {{technology and version}}. Reason: {{one line}} |
| Your choice (Q-B-01) | ☐ Keep current, upgrade to the supported version ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.2 Frontend / User Interface
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-02) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.3 Database
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-03) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.4 Data Access
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-04) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.5 Authentication and Access Control
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-05) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.6 Reporting and Printing
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-06) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.7 Integrations and Interfaces
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-07) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.8 Hosting and Infrastructure
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-08) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.9 Source Control and CI/CD
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-09) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.10 Testing
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-10) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

### 4.11 Logging and Monitoring
| Item | Answer |
|------|--------|
| Current | |
| Proposed | |
| Your choice (Q-B-11) | ☐ Keep current ☐ Proposed ☐ {{alternative}} ☐ Other: ____ |
| Your experience with your choice | ☐ None ☐ Some ☐ Strong |
| Reasons, risks or concerns | |

## 5. Part C — Developer Questions: Team, Tools and Operations

### 5.1 Team Skills
<!-- One column per developer role from brief section 4 (Developer 1, Developer 2…), never
     personal names unless brief section 4 allows them. Rows: the current and Proposed
     technologies from section 4. -->
| Technology | Developer 1 | Developer 2 |
|------------|-------------|-------------|
| | ☐ None ☐ Some ☐ Strong | ☐ None ☐ Some ☐ Strong |

### 5.2 Ways of Working
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-C-01 | Which AI coding assistant, if any, will you use? | Affects estimates (Migration Plan section 9) | ☐ Claude ☐ Other: ____ ☐ None |
| Q-C-02 | Which editor or IDE do you use? | Sets project setup and tooling | |
| Q-C-03 | How are changes reviewed today? | Sets the review and merge rules | ☐ Pull requests ☐ Pair review ☐ None |
| Q-C-04 | Which environments exist or can be made available? (tick all that apply) | Plans test, staging and pilot environments | ☐ Development ☐ Test ☐ Staging ☐ Production |
| Q-C-05 | How is the system deployed today, and how would you prefer it? | Decides the deployment approach | Today: ____ Preferred: ☐ Manual ☐ Scripts ☐ Containers ☐ Other |

### 5.3 Constraints and Risks
| ID | Question | Why we ask | Answer |
|----|----------|------------|--------|
| Q-C-06 | Technologies we must use, and why | Hard constraints (brief section 11) | |
| Q-C-07 | Technologies we must avoid, and why | Hard constraints (brief section 11) | |
| Q-C-08 | Which parts of today's code are worth keeping? | Feeds the assessment's Keep list | |
| Q-C-09 | What is the biggest technical risk of the rebuild, in your view? | Feeds the risk register | |

## 6. Respondent Details
<!-- Roles, not personal names, unless brief section 4 allows names. -->
| Item | Answer |
|------|--------|
| Your role | |
| Parts answered | ☐ Part A ☐ Part B ☐ Part C |
| Date | |

## 7. Response Summary
<!-- Filled when /mod-suite <slug> is run with the returned answers (Rule 40 section 07). Until then write:
     "Not applicable — no responses received yet." in each subsection. -->

### 7.1 Responses Received
| # | Role | Parts answered | Date received |
|---|------|----------------|---------------|

### 7.2 Tech Stack Results by Layer
<!-- Agreement: Agreed (all or nearly all answers pick the same option), Split, or No
     answer. A Split layer becomes or stays a [DECISION] in brief section 16. -->
| Layer | Current | Proposed | Answers per option | Agreement | Result | Brief update |
|-------|---------|----------|--------------------|-----------|--------|--------------|

### 7.3 Stakeholder Results
| Question | Summary of answers | Brief section updated |
|----------|--------------------|-----------------------|

### 7.4 Conflicts to Resolve
| Topic | Answer 1 (role) | Answer 2 (role) | Recommendation |
|-------|-----------------|-----------------|----------------|

## Open Items
| Marker | Item | Needed from |
|--------|------|-------------|

## Revision History
| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 0.1 | {{date}} | {{author}} | Initial questionnaire |
