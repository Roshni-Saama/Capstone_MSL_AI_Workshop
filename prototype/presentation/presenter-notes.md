# Presenter notes | Medical Engagement Workbench

Prepared 24 October 2026. Allow 12-15 minutes including a six-minute live walkthrough.

## 01. Medical EngagementWorkbench

Introduce the focused repeat-meeting use case. This is a working local application, not a production deployment. CRM is synthetic. Public retrieval is verified; a saved and human-reviewed live OpenAI run remains pending.

Evidence: `prototype/README.md`, `prototype/data/kol_records.json`

## 02. Continuity across scientific conversations

Present the benefit as a hypothesis. The application supports preparation and documentation; the MSL retains scientific judgment and responsibility for follow-up.

Evidence: `prototype/specs/scope-and-delivery.md`, `prototype/specs/evaluation-and-review.md`

## 03. A complete local workflow, with clear boundaries

Explain the fixed dataset counts and snapshot date. Completed tasks are recorded fixture history, not actions performed by this application. Source retrieval uses public APIs.

Evidence: `prototype/data/kol_records.json`, `prototype/app.py`

## 04. Know the KOL before reviewing the evidence

Show Dr Mira Sen. Point out territory, preferred channel, scientific interests and planned meeting. Changing KOL clears notes, source selections, search results and prior drafts.

Evidence: `prototype/ui.py`, `prototype/presentation.py`, `prototype/tests/test_crm.py`

## 05. Keep the next action and the open question visible

Distinguish fixture ownership from generated follow-up. Full registers remain under expanders. New requests are drafts requiring review and assignment outside this application.

Evidence: `prototype/crm_views.py`, `prototype/crm.py`, `prototype/tests/test_crm.py`

## 06. Filter the right source, using the right meaning

Explain source-specific meanings. PubMed therapy keywords search title/abstract. Trials provide intervention fields. Changing controls clears stale evidence without automatically searching.

Evidence: `prototype/search_filters.py`, `prototype/filter_views.py`, `prototype/specs/advanced-search-and-navigation.md`

## 07. A short overview, with the original evidence available

The screenshot is a real search snapshot in Offline mode. Do not call its excerpt an AI summary. OpenAI mode adds one public-record summary batch per successful nonempty search; CRM and notes are excluded from that request.

Evidence: `prototype/search_result_views.py`, `prototype/search_summaries.py`, `prototype/specs/search-summaries.md`

## 08. One responsibility per agent

These are bounded roles, not three independent autonomous chatbots. The Scientific Source Agent owns explicit retrieval, search summaries and the scientific preparation node; retrieval is not a fourth agent.

Evidence: `prototype/agents.py`, `prototype/workflow.py`, `prototype/specs/llm-agents.md`

## 09. A deterministic flow around bounded model calls

Trace the graph from left to right. Identity resolves before model requests. Each role receives its own payload. Arrows show control order: the scientific model receives selected sources, not CRM context. Search-time requests are separate explicit actions.

Evidence: `prototype/workflow.py`, `prototype/agents.py`, `prototype/search_summaries.py`

## 10. Designed to make unsupported output visible

Do not present controls as clinical validation or compliance certification. They constrain format, source references and quote occurrence. Human review must still assess scientific support, omissions and usefulness.

Evidence: `prototype/llm.py`, `prototype/agents.py`, `prototype/tests/test_llm.py`, `prototype/tests/test_app.py`

## 11. Software behavior tested, with separate evidence types

Open the evidence copies if challenged. Pytest cases use mocked services; browser checks include actual public retrieval and no model calls. Do not sum the counts into a single quality sample. The live OpenAI evaluation remains separate.

Evidence: `prototype/test_scenarios/results/automated_tests.xml`, `prototype/harness/results/agent_evaluation.json`, `prototype/test_scenarios/results/aligned_layout_browser.json`

## 12. A repeatable experiment around the actual agents

Distinguish runtime controls from evaluation. LangGraph and validation surround runtime requests. The evaluation harness supplies scripted responses and grades mechanical behavior. Network guards prevent accidental service calls. There is no model judge or live prompt-injection robustness claim.

Evidence: `prototype/harness/README.md`, `prototype/harness/evaluate.py`, `prototype/harness/cases.json`, `prototype/tests/test_harness.py`

## 13. Behavior contracts, implementation and evidence are separated

Explain the loop: define behavior, implement focused changes, map requirements to tests, run QA, then inspect evidence. Specifications exist; evaluator agreement on scope and thresholds is still pending.

Evidence: `prototype/specs/README.md`, `prototype/specs/requirement-test-matrix.md`, `prototype/harness/run_local_qa.py`, `wiki/index.md`

## 14. A reliable path through the working application

Have the app running first. Enter a key only in its password field, never on a slide. Offline mode preserves sources and formats notes; it does not interpret clinical evidence. The screenshot walkthrough is a fallback, not live model output.

Evidence: `prototype/docs/live-walkthrough.md`, `prototype/docs/workshop-walkthrough.md`, `prototype/test_scenarios/use_cases.md`

## 15. The next milestone is reviewed evidence of usefulness

Ask for a reviewer, date and acceptance decision. Functionality was explored, but no saved and reviewed live OpenAI report exists in the project evidence. No productivity or scientific-quality improvement has been measured.

Evidence: `prototype/specs/evaluation-and-review.md`, `prototype/harness/reviewer_scores.csv`, `prototype/docs/deployment.md`

## 16. A presentation the team can inspect and share

The HTML slides and screenshot walkthrough are self-contained. The ZIP includes the PDF, notes and evidence copies. Markdown evidence may reference repository-relative files; use the source repository for full navigation. No public hosting occurred.

Evidence: `prototype/test_scenarios/results/latest_run.md`, `prototype/harness/results/agent_evaluation.json`
