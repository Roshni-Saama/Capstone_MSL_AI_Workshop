# Test use cases and demo walkthrough

Status: fictional demonstration pack, 23 October 2026. Application: http://localhost:8501 when the local Streamlit server is running. The [canonical fixture](../data/kol_records.json) is the source of displayed CRM data.

| Use case | Fictional KOL | Prior question | Current main task |
| --- | --- | --- | --- |
| UC-001 | KOL-DEMO-001, Dr Mira Sen | Representation of older adults in source materials | Open |
| UC-002 | KOL-DEMO-002, Dr Arjun Rao | Sources for discussing biomarker-testing workflows | In progress |
| UC-003 | KOL-DEMO-003, Dr Leah Park | Distinguishing reported outcomes from interpretation | Awaiting review |

Each KOL has three past interactions, three current tasks and two medical-information requests. Each has two active tasks, of which one is overdue at the 23 October snapshot. The completed task is a fictional administrative profile check; it is not a completed scientific response. No request has an actual reviewed response recorded.

## UC-001 through UC-003: repeat-meeting preparation and follow-up

1. Select the named KOL, using Offline mode for a key-free demonstration.
2. Inspect CRM profile: ID, institution, assigned demo role, interests, territory and preferred channel.
3. Inspect Interaction timeline. Expand a dated meeting and distinguish KOL observation from draft MSL interpretation.
4. Inspect Follow-up tasks: latest status, assigned fictional owner, due date, overdue indicator and administrative closure evidence.
5. Inspect Medical requests: question, linked task, request owner and response status. These are requests, not scientific findings.
6. Copy the matching scenario's source text and notes from [scenario_inputs.json](fixtures/scenario_inputs.json). The source is deliberately synthetic; it only tests formatting and preservation.
7. Click Prepare. Expect the correct CRM history, original source text and original notes, with visible draft labeling. New follow-up owner/due date remain unassigned; prior fixture tasks still have their historical owners/dates.
8. Select another KOL. Expect the previous draft, user-entered notes and scientific source/search selections to clear. Profile, task and request IDs must now belong only to the new KOL.

Automated coverage: test_crm.py, test_app.py and test_workflow.py. Offline case inputs run automatically for each KOL. Live LLM generation is separate and pending agent-observed verification.

## UC-004: missing scientific evidence

Prepare with no selected or pasted scientific source. Expect explicit scientific abstention even though CRM data exists. In OpenAI mode only the scientific model step is skipped; CRM priorities may still be drafted and notes may still be processed. No medical conclusion should be inferred from historical CRM notes.

## UC-005: explicit scientific-source selection

Search PubMed or ClinicalTrials.gov, inspect a result, then prepare before and after selecting it. Before selection, the result is not briefing evidence. After selection, the source identifier and original URL remain available. Automated versions use mocked registry responses and check actual inclusion/exclusion.

## UC-006: model and registry failure recovery

Automated checks simulate model refusal, incomplete/malformed output, unknown source IDs, mismatched quotes, HTTP errors and timeouts. UI checks verify visible errors, empty-results recovery and removal of stale drafts after a failed model run. Do not induce outages against real services to demonstrate these tests.

## UC-007: human review scenarios

Use conflicting synthetic source text, an instruction-like source, a fictional off-label question or a general potential-safety note. Assess whether wording is supported and uncertainty is visible. The prompt-boundary test checks request construction only; it does not prove live resistance to injection. Medical handling, specialist review, live output quality and business benefit remain unverified. See [live/manual status](live_and_manual_checks.md).

## UC-008: summary-first scientific search

Run either registry search and open a record. Expect a short AI summary draft in OpenAI mode, or a labeled offline excerpt/overview otherwise. Original abstract or registry data is available under View original details. Check source links, supporting quotes, missing abstracts, a failed AI summary and repeated UI edits without another model call. Preparing without selecting the result must still abstain. Executable coverage: test_search_summaries.py. Live AI summary usefulness remains a reviewer task.

## UC-009: guided Dr Mira Sen OpenAI walkthrough

Use the guided walkthrough at the top of the app to load Dr Mira Sen, a public PubMed query and fictional notes. Confirm loading alone triggers no model or registry calls. Enter the API key locally, Search PubMed, inspect a summary, select an article, then Prepare. Review all three agent steps, citations, uncertainties, preserved notes and unassigned new owner/date. Download the report or explicitly save it locally. Report completion records software execution; human scientific review and usefulness scores remain separate.

Automated tests mock the calls and test setup plus report handling. Real model completion is pending until the user finishes the key-configured walkthrough. See [the live walkthrough guide](../docs/live-walkthrough.md).
