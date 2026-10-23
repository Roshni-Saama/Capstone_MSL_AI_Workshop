# Synthetic CRM Demo Data

Status: fictional demonstration fixture. Created 23 October 2026.

Every person, institution, identifier, interaction, task, date, and statement in this folder is invented for the capstone. These records do not describe real healthcare professionals, company CRM records, or verified scientific evidence. Do not use them for clinical, commercial, outreach, or safety-reporting decisions.

## Records

- [KOL-DEMO-001: Dr Mira Sen](kol-demo-001.md)
- [KOL-DEMO-002: Dr Arjun Rao](kol-demo-002.md)
- [KOL-DEMO-003: Dr Leah Park](kol-demo-003.md)

## Demo purpose

The fixture demonstrates continuity across repeat MSL meetings: retrieve a fictional profile and prior interactions, surface open questions, draft a briefing, then structure new notes and track follow-up. The main walkthrough can use KOL-DEMO-001. The other two records provide varied examples for testing retrieval and review; three fictional records are not a representative sample and cannot support population-level conclusions.

## Data model

Each record uses the same basic sections:

- `KOL ID`, `Organization ID`, and `Engagement ID`: fictional stable identifiers.
- Profile: fictional role, expertise topics, and expert category, for scientific context only.
- Interaction history: fictional dates, meeting purposes, topics, observations, and separate MSL interpretations.
- Follow-up: task ID, owner role, due date, status, and the requested next action.
- Next meeting: a fictional planned date and preparation objective.

No contact details, patient information, product claims, or literature citations are included. Scientific evidence must come from a separately supplied, reviewable source pack. CRM notes here are fictional interaction history, not evidence that a scientific statement is true.

## Suggested walkthrough

1. Select KOL-DEMO-001 and review the planned meeting purpose.
2. Retrieve prior interactions and show the unresolved task without converting the MSL interpretation into a KOL quote.
3. Draft a briefing that separates synthetic CRM context from citations in the scientific source pack.
4. Enter new fictional notes, review the structured draft, and create a follow-up task with an owner and status.
5. Repeat retrieval with KOL-DEMO-002 and KOL-DEMO-003 to check record isolation and avoid merging profiles.

## Related project pages

- [KOL categories and expert directory](../../concepts/kol-directory.md)
- [Engagement workflow](../../workflows/engagement.md)
- [Human oversight and guardrails](../../governance/oversight.md)
- [Wiki home](../../index.md)