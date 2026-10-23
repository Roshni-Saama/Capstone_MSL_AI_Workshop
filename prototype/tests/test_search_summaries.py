import copy
from unittest.mock import Mock

import pytest

import llm as llm_module
from clinical_trials import _study_record
from llm import GroundedItem, LLMError
from search_summaries import SearchSummary, SearchSummaryBatch, summarize_results
from test_app import start_app


def article(identifier="12345678", abstract=None):
    return dict(pmid=identifier, title="Synthetic summary test article", authors="Demo author",
                journal="Demo journal", year="2026", doi="", url=f"https://pubmed.ncbi.nlm.nih.gov/{identifier}/",
                abstract=abstract if abstract is not None else
                "BACKGROUND: A fictional study question is described. METHODS: Synthetic methods only. "
                + "Additional demonstration text. " * 40 + "END_OF_ORIGINAL_ABSTRACT")


def trial():
    return _study_record({"protocolSection": {
        "identificationModule": {"nctId": "NCT01234567", "briefTitle": "Synthetic registry summary test"},
        "statusModule": {"overallStatus": "RECRUITING"},
        "conditionsModule": {"conditions": ["Fictional condition"]},
        "outcomesModule": {"primaryOutcomes": [{"measure": "Fictional planned outcome"}]},
        "eligibilityModule": {"eligibilityCriteria": "ORIGINAL_ELIGIBILITY_DETAILS " * 30},
    }})


class FakeSummaryLLM:
    def __init__(self): self.calls = []
    def generate(self, task, data, output_type):
        self.calls.append(data)
        return SearchSummaryBatch(summaries=[SearchSummary(source_id=key, points=[
            GroundedItem(text="A concise summary of the supplied record.", quote=value["source_text"][:70])])
            for key, value in data["sources"].items()])


def test_offline_abstract_preview_is_short_and_original_is_preserved():
    record = article()
    before = copy.deepcopy(record)
    result = summarize_results([record], "pubmed")[record["pmid"]]
    assert "not an AI summary" in result["mode"]
    assert len(result["points"][0]) <= 503
    assert "END_OF_ORIGINAL_ABSTRACT" not in result["points"][0]
    assert record == before


def test_trial_overview_describes_planned_outcomes_without_full_eligibility():
    record = trial()
    result = summarize_results([record], "trials")[record["nct_id"]]
    assert len(result["points"]) == 3
    assert "RECRUITING" in " ".join(result["points"])
    assert "Planned primary outcomes" in " ".join(result["points"])
    assert "ORIGINAL_ELIGIBILITY_DETAILS" not in " ".join(result["points"])


def test_missing_pubmed_abstract_skips_model_and_discloses_limitation():
    runtime = FakeSummaryLLM()
    result = summarize_results([article(abstract="")], "pubmed", runtime)
    assert runtime.calls == []
    assert "No abstract available" in result["12345678"]["points"][0]


@pytest.mark.parametrize("kind", ["pubmed", "trials"])
def test_one_model_batch_contains_only_retrieved_sources(kind):
    records = [article(), article("87654321")] if kind == "pubmed" else [trial()]
    before = copy.deepcopy(records)
    runtime = FakeSummaryLLM()
    result = summarize_results(records, kind, runtime)
    assert len(runtime.calls) == 1
    assert set(runtime.calls[0]) == {"registry", "sources"}
    assert all("AI summary draft" in summary["mode"] for summary in result.values())
    assert all(summary["quotes"] for summary in result.values())
    assert records == before


@pytest.mark.parametrize("issue", ["unknown_id", "duplicate_id", "missing_id", "wrong_quote", "too_many_points", "too_long"])
def test_bad_summary_batch_is_rejected_instead_of_accepting_partial_output(issue):
    runtime = FakeSummaryLLM()
    item = GroundedItem(text="Short source summary.", quote="A fictional abstract for a demonstration.")
    entries = [SearchSummary(source_id="12345678", points=[item])]
    if issue == "unknown_id": entries[0].source_id = "NOT-RETURNED"
    elif issue == "duplicate_id": entries.append(entries[0])
    elif issue == "missing_id": entries = []
    elif issue == "wrong_quote": entries[0].points[0].quote = "Completely invented evidence."
    elif issue == "too_many_points": entries[0].points = [item] * 4
    else: entries[0].points[0].text = "word " * 121
    runtime.generate = lambda *args: SearchSummaryBatch(summaries=entries)
    with pytest.raises(LLMError):
        summarize_results([article(abstract="A fictional abstract for a demonstration.")], "pubmed", runtime)


def test_empty_search_does_not_call_model():
    runtime = FakeSummaryLLM()
    assert summarize_results([], "pubmed", runtime) == {}
    assert runtime.calls == []


@pytest.mark.parametrize("registry_index", [0, 1])
def test_ui_shows_summary_before_collapsed_original_details(registry_index, monkeypatch):
    app, pubmed, trials = start_app(monkeypatch)
    search = pubmed if registry_index == 0 else trials
    record = article() if registry_index == 0 else trial()
    search.side_effect = None
    search.return_value = [record]
    query_key = "pubmed_query" if registry_index == 0 else "trial_query"
    app.text_input(key=query_key).input("fictional topic")
    app.button[registry_index].click().run()
    assert not app.exception
    details = next(expander for expander in app.expander if expander.label == "View original details")
    original = "\n".join(element.value for element in details.markdown)
    marker = "END_OF_ORIGINAL_ABSTRACT" if registry_index == 0 else "ORIGINAL_ELIGIBILITY_DETAILS"
    assert marker in original
    assert any(element.value == "**Summary**" for element in app.markdown)
    prefix = "pubmed" if registry_index == 0 else "trial"
    preview = next(iter(app.session_state[prefix + "_summaries"].values()))
    assert marker not in " ".join(preview["points"])
    app.button[2].click().run()
    assert "abstains" in app.session_state["workflow_result"]["briefing"]


def test_ai_summaries_are_cached_on_rerun_and_cleared_on_kol_switch(monkeypatch):
    runtime = FakeSummaryLLM()
    monkeypatch.setattr(llm_module, "OpenAILLM", lambda **kwargs: runtime)
    app, pubmed, _ = start_app(monkeypatch)
    pubmed.side_effect = None
    pubmed.return_value = [article()]
    app.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    app.text_input(key="pubmed_query").input("fictional topic")
    app.button[0].click().run()
    assert not app.exception
    assert len(runtime.calls) == 1
    assert "AI summary draft" in app.session_state["pubmed_summaries"]["12345678"]["mode"]
    app.text_area(key="meeting_notes").input("Fictional notes.").run()
    assert len(runtime.calls) == 1
    app.selectbox[0].select_index(1).run()
    assert "pubmed_summaries" not in app.session_state


def test_failed_ai_summary_shows_labeled_preview_and_clears_previous_ai_text(monkeypatch):
    runtime = FakeSummaryLLM()
    monkeypatch.setattr(llm_module, "OpenAILLM", lambda **kwargs: runtime)
    app, pubmed, _ = start_app(monkeypatch)
    pubmed.side_effect = None
    pubmed.return_value = [article()]
    app.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    app.text_input(key="pubmed_query").input("fictional topic")
    app.button[0].click().run()
    assert "pubmed_summaries" in app.session_state
    runtime.generate = Mock(side_effect=LLMError("Demo summary failure"))
    app.button[0].click().run()
    assert not app.exception
    assert "pubmed_summaries" not in app.session_state
    assert any("Demo summary failure" in warning.value for warning in app.warning)
    assert any("not an AI summary" in caption.value for caption in app.caption)
    assert not any("AI summary draft" in caption.value for caption in app.caption)
    assert len(app.session_state["pubmed_results"]) == 1
