# Repeat-Meeting Preparation and Follow-up Specification

Status: prototype specification, 23 October 2026. Synthetic scenario only; not an approved company process.

## User and goal

The primary user is an MSL preparing for and documenting a repeat meeting with a fictional KOL. The prototype should surface prior CRM-style context, help prepare from supplied sources, and draft reviewable follow-up from new notes.

## Inputs

- One exact fictional KOL ID from `data/kol_records.json`.
- That KOL's synthetic profile, prior interactions, and task records.
- Optional scientific source text entered for the current run; it is not persisted.
- Optional user-triggered PubMed query; returned citation metadata and abstracts are selected explicitly and are not saved to CRM.
- Optional user-triggered ClinicalTrials.gov query; returned registry metadata are selected explicitly and are not saved to CRM.
- Optional fictional meeting notes entered by the user; they are not written to CRM.

## Workflow

1. Retrieve the exact KOL and only that KOL's history.
2. Display profile, planned meeting, prior observations, separately labeled MSL interpretations, and open tasks.
3. Search PubMed using NCBI E-utilities only when the user explicitly requests a search.
4. Display article title, authors, journal, year, abstract, PMID, DOI when available, and a PubMed record link.
5. Search ClinicalTrials.gov API v2 only when the user explicitly requests a search.
6. Display NCT ID, title, registry status, last update, study type/phase, conditions, interventions, primary outcomes, enrollment, eligibility, and the registry URL when available.
7. Generate only neutral discussion prompts derived from the displayed registry fields; MSL reviews, edits, or ignores them.
8. Require explicit record selection before including trial metadata in the briefing source text.
9. If no scientific source text is supplied or selected, abstain from scientific claims.
10. Preserve supplied abstracts/source text; do not summarize or interpret clinical evidence.
11. Structure new notes using deterministic rules, preserve original notes, and leave interpretation to MSL review.
12. Suggest only a generic follow-up prompt when question/request/evidence terms appear; leave owner and due date unassigned.
13. Mark all outputs as drafts. Do not create tasks in a real system.

## Outputs

- Retrieved synthetic CRM context.
- Source-preserving briefing draft or explicit abstention.
- Structured note draft with MSL review fields and a rule-based follow-up prompt.

## Failure and safety behavior

- Unknown KOL ID: fail closed with an error.
- Invalid or non-synthetic data file: reject it.
- Missing evidence: abstain from scientific claims.
- No external model or network inference is used.
- Potential safety information: state that the organization's established process applies; no reporting action is performed.
- No live CRM, patient data, external messaging, or real-world action is permitted.

## Acceptance criteria

- The application exposes exactly three unique synthetic KOL IDs.
- Selecting one ID cannot retrieve another KOL's interactions.
- CRM history and scientific source text are visibly distinct.
- No source text yields explicit abstention.
- Supplied source text is preserved and not presented as an AI-generated evidence summary.
- New notes remain a draft and are not written to a CRM.
- The UI discloses synthetic data and human review requirements.