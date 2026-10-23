from pathlib import Path
from unittest.mock import Mock

import pytest
from streamlit.testing.v1 import AppTest

from agents import ScientificSourceAgent
from pubmed import PubMedError
from clinical_trials import ClinicalTrialsError

APP = Path(__file__).resolve().parents[1] / "app.py"


def start_app(monkeypatch):
    pubmed = Mock(side_effect=AssertionError("Unexpected PubMed request"))
    trials = Mock(side_effect=AssertionError("Unexpected registry request"))
    monkeypatch.setattr(ScientificSourceAgent, "search_pubmed", pubmed)
    monkeypatch.setattr(ScientificSourceAgent, "search_trials", trials)
    app = AppTest.from_file(str(APP)).run()
    assert not app.exception
    return app, pubmed, trials


def test_drafts_separate_sources_and_history_without_external_search(monkeypatch):
    app, pubmed, trials = start_app(monkeypatch)
    app.text_area(key="scientific_source_text").input("SYNTHETIC SOURCE ONLY")
    app.text_area(key="meeting_notes").input("Fictional KOL asked for sources.")
    app.button[2].click().run()
    assert not app.exception
    text = "\n".join(element.value for element in app.markdown)
    assert "Draft briefing" in [element.value for element in app.subheader]
    assert "Draft note and follow-up" in [element.value for element in app.subheader]
    assert "Requires MSL review" in "\n".join(element.value for element in app.caption)
    assert "Meeting context (synthetic CRM history):" in text
    assert "Selected scientific source text" in text
    assert "SYNTHETIC SOURCE ONLY" in text
    assert "Owner and due date: Not assigned" in text
    pubmed.assert_not_called()
    trials.assert_not_called()


def test_switching_kol_clears_previous_draft_notes_sources_and_search_state(monkeypatch):
    app, pubmed, trials = start_app(monkeypatch)
    pubmed.side_effect = None
    pubmed.return_value = []
    app.text_input(key="pubmed_query").input("fictional topic")
    app.button[0].click().run()
    app.text_area(key="scientific_source_text").input("KOL ONE SOURCE")
    app.text_area(key="meeting_notes").input("KOL ONE asked a question.")
    app.button[2].click().run()
    assert app.session_state["workflow_result"]["kol_id"] == "KOL-DEMO-001"
    app.selectbox[0].select_index(1).run()
    assert not app.exception
    assert app.text_area(key="scientific_source_text").value == ""
    assert app.text_area(key="meeting_notes").value == ""
    assert app.text_input(key="pubmed_query").value == ""
    assert "workflow_result" not in app.session_state
    assert "pubmed_results" not in app.session_state
    text = "\n".join(element.value for element in app.markdown)
    assert "KOL ONE" not in text
    assert "ENG-DEMO-001" not in text
    app.button[2].click().run()
    assert app.session_state["workflow_result"]["kol_id"] == "KOL-DEMO-002"
    assert "abstains" in app.session_state["workflow_result"]["briefing"]
    trials.assert_not_called()


def test_missing_source_abstains_and_fixture_is_not_modified(monkeypatch):
    fixture = APP.parent / "data" / "kol_records.json"
    before = fixture.read_bytes()
    app, pubmed, trials = start_app(monkeypatch)
    app.button[2].click().run()
    assert not app.exception
    assert "abstains" in app.session_state["workflow_result"]["briefing"]
    assert fixture.read_bytes() == before
    assert "does not create CRM records or send messages" in "\n".join(x.value for x in app.caption)
    pubmed.assert_not_called()
    trials.assert_not_called()


@pytest.mark.parametrize("button_index,error", [
    (0, PubMedError("Demo connection failure")),
    (1, ClinicalTrialsError("Demo connection failure")),
])
def test_explicit_search_failure_and_empty_results_are_visible(monkeypatch, button_index, error):
    app, pubmed, trials = start_app(monkeypatch)
    search = pubmed if button_index == 0 else trials
    query_key = "pubmed_query" if button_index == 0 else "trial_query"
    app.text_input(key=query_key).input("fictional topic")
    search.side_effect = error
    app.button[button_index].click().run()
    assert not app.exception
    assert "Demo connection failure" in [x.value for x in app.error]
    search.side_effect = None
    search.return_value = []
    app.button[button_index].click().run()
    assert not app.exception
    assert not app.error
    assert any("No " in x.value and "found" in x.value for x in app.info)


@pytest.mark.parametrize("button_index", [0, 1])
def test_registry_material_requires_explicit_selection(monkeypatch, button_index):
    from clinical_trials import _study_record
    app, pubmed, trials = start_app(monkeypatch)
    if button_index == 0:
        record = dict(pmid="12345678", title="Synthetic article selection test",
                      authors="Demo author", journal="Demo", year="2026",
                      abstract="SYNTHETIC ABSTRACT FOR SELECTION TEST", doi="",
                      url="https://pubmed.ncbi.nlm.nih.gov/12345678/")
        search, identifier, query_key = pubmed, "12345678", "pubmed_query"
        selected_key = "selected_pmids"
    else:
        record = _study_record({"protocolSection": {"identificationModule": {
            "nctId": "NCT01234567", "briefTitle": "Synthetic trial selection test"}}})
        search, identifier, query_key = trials, "NCT01234567", "trial_query"
        selected_key = "selected_nct_ids"
    search.side_effect = None
    search.return_value = [record]
    app.text_input(key=query_key).input("fictional topic")
    app.button[button_index].click().run()
    assert not app.exception
    app.button[2].click().run()
    assert "abstains" in app.session_state["workflow_result"]["briefing"]
    app.multiselect(key=selected_key).select(identifier).run()
    app.button[2].click().run()
    assert not app.exception
    briefing = app.session_state["workflow_result"]["briefing"]
    assert identifier in briefing
    assert record["url"] in briefing
    search.assert_called_once()



def test_llm_mode_missing_key_shows_error_without_stale_draft(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    app, _, _ = start_app(monkeypatch)
    app.button[2].click().run()
    assert "workflow_result" in app.session_state
    app.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    assert "workflow_result" not in app.session_state
    app.button[2].click().run()
    assert not app.exception
    assert any("API key" in x.value for x in app.error)
    assert "workflow_result" not in app.session_state


def test_llm_mode_success_then_failure_does_not_show_old_output(monkeypatch):
    import workflow
    from test_llm import FakeLLM
    from llm import LLMError
    runtime = FakeLLM()
    factory = Mock(return_value=runtime)
    monkeypatch.setattr(workflow, "OpenAILLM", factory)
    app, _, _ = start_app(monkeypatch)
    app.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    app.text_input(key="openai_api_key").input("TEST-KEY")
    app.text_area(key="scientific_source_text").input("SYNTHETIC SOURCE TEXT")
    app.text_area(key="meeting_notes").input("KOL asked for sources.")
    app.button[2].click().run()
    assert not app.exception
    assert "Draft meeting priorities" in [x.value for x in app.subheader]
    assert len(app.session_state["workflow_result"]["agent_trace"]) == 3
    factory.side_effect = LLMError("Demo OpenAI failure")
    app.button[2].click().run()
    assert not app.exception
    assert "workflow_result" not in app.session_state
    assert "Demo OpenAI failure" in [x.value for x in app.error]
