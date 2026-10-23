# Engagement workflow

Status: proposed workflow template, not a validated company process.
Owner: [To complete]. Last reviewed: [To complete].

## Evidence to review
See "An illustrative engagement" and "Possible AI scope" in the [original notes](../../raw/Capstone_notes.md).
The example in those notes is fictional.
The proposed prototype fixture is [three synthetic KOL CRM records](../demo-data/synthetic-crm/index.md); those records are invented interaction history, not scientific evidence.

## Workflow design
| Stage | Current process and evidence | Proposed AI assistance | Human review | Output and owner |
| --- | --- | --- | --- | --- |
| Preparation for a repeat meeting | Proposed demo uses synthetic prior CRM-style records and a source pack | Retrieve prior topics, open questions, and unfinished commitments; draft a briefing with evidence links | MSL verifies identity, history, sources, and relevance | Reviewed meeting brief owned by the MSL |
| Scientific engagement | Fictional scenario; the MSL conducts the conversation | No autonomous participation in the initial demo | MSL owns the exchange and records notes | MSL-authored meeting notes |
| Insight capture | Synthetic notes entered after the meeting | Draft a structured record separating KOL observations, MSL interpretation, and follow-up tasks | MSL edits and approves the draft | Reviewed engagement record owned by the MSL |
| Follow-up and routing | Synthetic task records model ownership and status; no live system connection | Carry forward unresolved questions, draft a response task, and show owner, due date, and status | MSL reviews tasks and any response before release; specialist decisions stay with the relevant team | Tracked draft follow-up with clear owner and status |
| Closure and learning | [To complete] | [To complete] | [To complete] | [To complete] |

## Scope and inputs
- Selected use case: proposed repeat-meeting preparation and follow-up assistant for an MSL.
- Input sources: a fictional KOL profile, multiple dated prior interaction records, a prior open scientific question, follow-up task status, and a small scientific source pack. All CRM-shaped data is synthetic; no live CRM credentials, records, or integrations are used.
- Minimum synthetic CRM fields: fictional KOL and organization IDs; engagement ID and date; meeting purpose; discussion topics; KOL observation; separate MSL interpretation; open question or commitment; task owner role; due date; status; and source reference where relevant.
- Demo scenario: three fictional KOL records support retrieval and record-isolation checks. The primary walkthrough uses KOL-DEMO-001: an earlier scientific evidence question has an open follow-up task before the next meeting. The assistant surfaces the history and task in the briefing, then drafts a new reviewed record and follow-up task after the next fictional engagement. The other two records support additional retrieval examples, not population-level conclusions.
- Excluded activities: use of real or identifiable HCP/patient records, live CRM access, autonomous external messaging, patient treatment recommendations, and final safety-reporting decisions.
- Expected outputs: source-backed briefing, reviewed structured engagement draft, and visible follow-up task with owner and status.

## Evaluation
- Baseline and target measures: [To complete; validate before selecting targets]
- Test cases and acceptance criteria: [To complete]
- Failure handling and escalation owner: [To complete]

## Related pages
- [Concepts](../concepts/msl-kol.md)
- [Human oversight](../governance/oversight.md)
- [Wiki home](../index.md)
