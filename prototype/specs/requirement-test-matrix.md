# Requirement-to-Test Matrix

| Requirement | Validation | Test or location | Status |
| --- | --- | --- | --- |
| Three bounded agents have distinct responsibilities; offline compatibility retained | Direct agent contracts and orchestrated graph output | `tests/test_agents.py` | Implemented |
| Exactly three unique synthetic KOLs | Load fixture and assert count/IDs | `tests/test_workflow.py::test_loads_exactly_three_unique_synthetic_records` | Implemented |
| Exact KOL lookup; no cross-record leakage | Compare returned IDs and engagement IDs | `tests/test_workflow.py::test_record_lookup_does_not_mix_kol_history` | Implemented |
| Unknown identity fails closed | Request unknown ID and expect error | `tests/test_workflow.py::test_unknown_kol_id_fails_closed` | Implemented |
| Fixture must declare synthetic provenance | Load fixture marked non-synthetic and expect rejection | `tests/test_workflow.py::test_loader_rejects_non_synthetic_fixture` | Implemented |
| Missing source yields no scientific claims | Verify explicit abstention | `tests/test_workflow.py::test_briefing_abstains_without_scientific_source` | Implemented |
| Supplied source is preserved without interpretation | Verify verbatim presence and no summary claims | `tests/test_workflow.py::test_briefing_preserves_sources_without_interpreting_them` | Implemented |
| PubMed citations/abstracts parse with provenance | Mock ESearch and EFetch payloads; verify PMID, metadata, abstract, and URL | `tests/test_pubmed.py::test_search_pubmed_parses_citation_and_abstract` | Implemented |
| PubMed input is bounded and no-result queries are handled | Test empty query, invalid count, and empty PMID response | `tests/test_pubmed.py` | Implemented |
| ClinicalTrials.gov records parse with NCT provenance | Mock API v2 payload and verify registry fields, NCT link, and encoded query | `tests/test_clinical_trials.py::test_search_clinical_trials_parses_registry_fields_and_query` | Implemented |
| Trial discussion prompts remain neutral | Verify prompts derive from registry fields and contain no recommendations | `tests/test_clinical_trials.py::test_discussion_prompts_are_neutral_and_field_based` | Implemented |
| Notes are preserved and follow-up uses deterministic rules | Verify original notes, review placeholders, and no invented owner/task details | `tests/test_workflow.py::test_follow_up_preserves_notes_and_does_not_invent_tasks` | Implemented |
| UI labels output drafts and separates source/context | Streamlit AppTest checks visible draft labels, source/history sections and abstention | `tests/test_app.py` | Automated checks implemented |
| Follow-up remains draft; no external writes | AppTest checks draft flow, unchanged fixture and no search calls; source review confirms no write connectors | `tests/test_app.py`, `app.py`, `agents.py` | Tested scope only; no security certification |
| KOL switching clears previous meeting workspace | AppTest generates a draft, switches identity, verifies old result/notes/sources/search state cleared | `tests/test_app.py::test_switching_kol_clears_previous_draft_notes_sources_and_search_state` | Implemented |
| Registry selection is explicit | AppTest compares briefing before and after selecting an article or study | `tests/test_app.py::test_registry_material_requires_explicit_selection` | Implemented |
| Search failures and no matches are visible | Mock each registry failure then empty results | `tests/test_app.py::test_explicit_search_failure_and_empty_results_are_visible` | Implemented |
| Three LLM roles execute in graph order | Mock runtime with isolated role inputs | `tests/test_llm.py` | Implemented; live key required for real generation |
| LLM output schema, completion and refusal checks | Reject malformed, refused or partial Responses outputs | `tests/test_llm.py` | Implemented |
| LLM source IDs and exact quotes match designated input | Reject unknown source and invented quote | `tests/test_llm.py` | Implemented; semantic correctness requires review |
| Missing key/identity and oversized input fail without model call | Configuration/preflight checks | `tests/test_llm.py` | Implemented |
| Keys stay outside prompts and graph state; API errors sanitized | Mock request-body/state/transport assertions | `tests/test_llm.py` | Implemented |
| Failed model run and mode change clear old result | Streamlit AppTest success/failure sequence | `tests/test_app.py` | Implemented |
| Live OpenAI generation and scientific quality | Key-configured run plus human assessment | `specs/llm-agents.md` | Pending; no API key configured |
| Expanded CRM links and snapshot dates | Validate KOL/task/request ownership and references; reject corrupt fixture copies | `tests/test_crm.py` | Implemented |
| CRM metrics, tabs and tables isolate selected KOL | Streamlit AppTest checks all three profiles and table identifiers | `tests/test_crm.py` | Implemented |
| Every executed test instance has scenario evidence | Catalog generated from actual JUnit XML | `test_scenarios/README.md` | See latest execution report |
| Summary-first scientific search and retained original details | Offline excerpts/trial overviews; batch LLM validation; UI order, caching and labeled failure preview | `tests/test_search_summaries.py` | Implemented; live summary quality pending |
| Guided Mira Sen setup makes no external calls | Selects correct fictional KOL, mode, query and notes without requests | `tests/test_walkthrough.py` | Implemented |
| Explicit run evidence excludes credential fields | Whitelisted report fields, local save and UI save invocation | `tests/test_walkthrough.py` | Implemented; actual live record pending |

| Fixed agent evaluation pack, provenance and grader regression detection | 16 Offline/scripted cases plus intentional output/request corruption tests | `harness/evaluate.py`, `tests/test_harness.py`, `specs/agent-harness.md` | Implemented; see latest harness results |
| Local QA executes consistently from repository or prototype folder | Absolute runner paths and root pytest pythonpath configuration | `harness/run_local_qa.py`, `../pytest.ini` | Implemented |

| Source-specific advanced filters apply at the public API before result limits | Validate dates/enums, Boolean grouping and outgoing query parameters | `tests/test_search_filters.py` | Implemented; live acceptance recorded separately |
| Filter/query edits invalidate old results and drafts without calls | AppTest checks both registries, reset controls and KOL switching | `tests/test_search_filters.py` | Implemented |
| Three full-width workspaces retain explicit evidence selection | Navigation, source-selection and CRM tests plus desktop/mobile browser checks | `tests/test_search_filters.py`, `tests/test_app.py`, `tests/test_crm.py` | Implemented |
