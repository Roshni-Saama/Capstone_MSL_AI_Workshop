# Requirement-to-Test Matrix

| Requirement | Validation | Test or location | Status |
| --- | --- | --- | --- |
| Three code-only agents have distinct responsibilities | Direct agent contracts and orchestrated graph output | `tests/test_agents.py` | Implemented |
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
| UI labels output drafts and separates source/context | Manual UI review or Streamlit AppTest | Pending test |
| Follow-up remains draft; no external writes | Verify workflow output and absence of connector/write tools | Pending test |