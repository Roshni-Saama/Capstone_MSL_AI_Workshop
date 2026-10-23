# Prototype scope and delivery plan

Status: working implementation scope, 23 October 2026. Stakeholder approval and value validation remain pending.

## Problem and intended value

For repeat KOL meetings, the MSL needs to recover prior discussion context and unfinished commitments, inspect relevant scientific sources, and preserve new questions for reviewed follow-up. The proposed value is less preparation effort and fewer missed commitments. These are hypotheses to measure, not demonstrated benefits.

Basis: [Project notes, Operational and technical challenges and Possible AI scope](../../raw/MSL%20KOL%20engagement%20note.md), [proposed engagement workflow](../../wiki/workflows/engagement.md), and [repeat-meeting specification](repeat-meeting.md). The source notes describe candidate problems and a fictional example; they do not establish a validated company workflow.

## Current delivery boundary

The implementation is a Streamlit demonstrator over three fictional KOL records. Exactly three agents are coordinated with LangGraph. The user authorized OpenAI LLM mode on 23 October 2026; Offline remains the default. LLM mode sends selected fictional context, selected sources and notes to OpenAI for bounded draft generation. PubMed and ClinicalTrials.gov searches remain explicit and read-only. See the [LLM specification](llm-agents.md) for the current contract.

| Agent | Implemented responsibility | Why separate it | Human decision |
| --- | --- | --- | --- |
| KOL Context Agent | Exact-ID retrieval plus optional LLM priorities and unresolved requests, checked against context quotes | Makes record isolation and provenance independently checkable | Confirm the selected identity and relevant prior context |
| Scientific Source Agent | Search public sources, preserve selected identifiers/text, and optionally draft quote-backed scientific briefing items | Separates source retrieval from CRM history and scientific judgment | Select sources and assess their relevance, limitations, and meaning |
| Follow-up Agent | Preserve notes and optionally extract quote-backed observations, requests and open questions | Makes note preservation and task-drafting limits independently checkable | Confirm observations, enter interpretations, and assign ownership and due dates |

Implementation evidence: [agents.py](../agents.py), [workflow.py](../workflow.py), and [app.py](../app.py). These are bounded workflow components. The implementation now adds bounded model drafting; autonomous planning and external action remain excluded. Live OpenAI access and scientific quality have not yet been verified because no API key is configured. Workshop evaluator acceptance remains pending.

## Demonstration storyline

1. Select KOL-DEMO-001 and inspect the planned meeting, dated prior discussions, and outstanding task in the fictional fixture.
2. Confirm that changing the selection to another KOL shows only that person's synthetic history.
3. Run the workflow without sources and show the explicit abstention from scientific claims.
4. Search a registry explicitly, inspect a result and its source identifier, and select it for the briefing; alternatively provide clearly labeled demonstration source text.
5. Generate a briefing and show CRM history separately from selected scientific material. Explain that source text is preserved; in OpenAI mode quote-backed model drafts require MSL verification and interpretation.
6. Enter fictional notes such as: "KOL asked for sources addressing the prior evidence question."
7. Show the draft notes, generic follow-up prompt, and unassigned owner/due date. Explain that review and task closure occur outside this demonstrator.

No real CRM updates, external messages, safety submissions, or claims of completed follow-up should appear in the walkthrough. A reviewed persistent task lifecycle would be a future extension, subject to a separate design decision.

## Remaining delivery work

| Priority | Work | Evidence required to close it | Status |
| --- | --- | --- | --- |
| 1 | Validate problem, users, scope, and OpenAI agent approach with an MSL or Medical Affairs reviewer | Named reviewer, dated feedback, and an explicit scope decision | Workshop evaluator identified; name, date and decision pending |
| 2 | Validate UI draft labels, source separation, record switching, and no-write behavior | Focused UI/workflow checks and updated requirement-test matrix | Automated UI regression checks implemented; see test matrix |
| 3 | Complete governance ownership and failure handling | Populated controls, review responsibilities, evidence, and unresolved concerns | Controls and proposed role owners drafted; approval pending |
| 4 | Evaluate usefulness and reliability | Manual baseline, agreed targets, fixed fictional cases/source pack, and reviewer-scored results | Fixed fictional cases and review protocol prepared; results unmeasured |
| 5 | Verify live retrieval for demonstration | Dated PubMed and ClinicalTrials.gov smoke checks, including failures/no results | Topic/no-result smoke checks passed on 23 October 2026; failures tested with mocks |
| 6 | Prepare final presentation and walkthrough | One coherent problem-to-outcome narrative, architecture view, limitations, and actual evaluation results | Presentation script drafted; review and measured results pending |

For evaluation, keep software acceptance checks separate from business outcomes. Existing unit tests can establish record isolation and formatting behavior; they cannot establish reduced preparation time or scientific usefulness. Include missing evidence, conflicting sources, off-label questions, and potential safety information as reviewer scenarios without claiming automated classification or routing.

## Decisions still requiring evidence

- Scope reviewer role: workshop evaluator (user-confirmed). Name and review date: [To complete].
- Agreement that the selected workflow and bounded OpenAI agents meet the capstone expectations: [To complete].
- Manual preparation baseline and numeric improvement target: [To complete after baseline].
- Agreed quality rubric and acceptance threshold: [To complete with reviewer].
- Whether reviewed task tracking belongs in this delivery or a later extension: [To complete].

## Workspace layout

The application lives only in `Capstone_MSL_AI_Workshop/prototype`. Its `.venv` is the application environment. Research proposals under the parent `Team_POV_MSL_Capstone` folder and the historical conversation remain background material; their broader proposals remain background; OpenAI mode is the current authorized LLM integration. The parent workspace's separate `.venv` is retained because its usage has not been established.

## Delivery artifacts

- [Evaluation cases, rubric and evaluator decisions](evaluation-and-review.md)
- [Workshop presentation and demonstration script](../docs/workshop-walkthrough.md)
- [Automated acceptance matrix](requirement-test-matrix.md)
- [Proposed governance controls and failure handling](../../wiki/governance/oversight.md)

## Current next priority

OpenAI integration and mocked tests are implemented. Configure a key in the app sidebar, verify a live three-agent run, then evaluate quote support and usefulness with the workshop evaluator. No business benefit or scientific accuracy is established by the automated checks.

## Expanded synthetic CRM and scenario evidence

The fictional fixture now includes three profiles, nine historical interactions, nine current tasks and six medical-information requests, using a fixed 23 October 2026 snapshot. The UI has separate profile, timeline, task and request tabs. Existing tasks are fixture history; no live CRM or task write-back is added. See [the CRM data folder](../data/synthetic_crm/README.md) and [the dedicated test-scenario folder](../test_scenarios/README.md) for human-readable exports and actual test evidence.

## Summary-first search results

PubMed and ClinicalTrials.gov results show concise previews with originals under View original details. OpenAI-mode searches may make one additional public-source summary batch request via the Scientific Source Agent; offline previews require no model. Original records remain the briefing evidence. See [the search-summary contract](search-summaries.md).
