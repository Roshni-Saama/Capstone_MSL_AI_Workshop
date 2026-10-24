from datetime import date
from urllib.parse import parse_qs, urlparse
from unittest.mock import Mock

import pytest

import clinical_trials
import pubmed
from search_filters import PubMedFilters, TrialFilters, pubmed_parameters, trial_parameters
from test_app import start_app
from test_search_summaries import article, trial


def test_pubmed_filter_categories_use_and_and_choices_use_or():
    parameters = pubmed_parameters("cancer OR leukemia", PubMedFilters(
        start=date(2024, 1, 1), end=date(2026, 10, 24),
        article_types=("Randomized controlled trial", "Systematic review"), languages=("English", "Hindi"),
        availability="Abstract available", species="Humans", therapy="immunotherapy", affiliation="India", journal="Blood", sort="Publication date"))
    term = parameters["term"]
    assert term.startswith("(cancer OR leukemia) AND ")
    assert '2024/01/01:2026/10/24[dp]' in term
    assert '("Randomized Controlled Trial"[pt] OR systematic[sb])' in term
    assert '(english[la] OR hindi[la])' in term
    assert '"India"[ad]' in term and '"immunotherapy"[tiab]' in term
    assert '"Blood"[ta]' in term and 'humans[mh]' in term and 'hasabstract' in term
    assert parameters["sort"] == "pub_date"


def test_trial_parameters_use_documented_native_fields_and_advanced_expressions():
    parameters = trial_parameters("cancer", TrialFilters(
        start=date(2024, 1, 1), date_field="First posted", statuses=("Recruiting", "Not yet recruiting"),
        phases=("Phase 2", "Phase 3"), study_type="Interventional", intervention_type="Drug",
        intervention="pembrolizumab", location="India", age="Older adult (65+)", sex="Female", sort="Last updated"))
    assert parameters["query.cond"] == "cancer"
    assert parameters["query.intr"] == '"pembrolizumab"'
    assert parameters["query.locn"] == '"India"'
    assert parameters["filter.overallStatus"] == "RECRUITING,NOT_YET_RECRUITING"
    advanced = parameters["filter.advanced"]
    assert '(AREA[Phase]PHASE2 OR AREA[Phase]PHASE3)' in advanced
    for text in ('AREA[StudyType]INTERVENTIONAL', 'AREA[InterventionType]DRUG', 'AREA[StdAge]OLDER_ADULT', 'AREA[Sex]FEMALE', 'AREA[StudyFirstPostDate]RANGE[2024-01-01,MAX]'):
        assert text in advanced
    assert parameters["sort"] == "LastUpdatePostDate:desc"
    assert "filter.phase" not in parameters


@pytest.mark.parametrize("kind,filters", [
    ("pubmed", PubMedFilters(start=date(2026, 1, 2), end=date(2026, 1, 1))),
    ("pubmed", PubMedFilters(article_types=("Invented type",))),
    ("pubmed", PubMedFilters(therapy='drug" OR all[filter]')),
    ("pubmed", PubMedFilters(languages=("Invented language",))),
    ("trials", TrialFilters(phases=("Phase 9",))),
    ("trials", TrialFilters(start=date(2026, 1, 2), end=date(2026, 1, 1))),
    ("trials", TrialFilters(location='India" OR AREA[Phase]PHASE3')),
    ("trials", TrialFilters(study_type="Invented type")),
])
def test_invalid_filters_fail_before_registry_network(monkeypatch, kind, filters):
    request = Mock(side_effect=AssertionError("Unexpected network"))
    monkeypatch.setattr(pubmed, "_request_bytes", request)
    monkeypatch.setattr(clinical_trials, "_get_json", request)
    with pytest.raises(ValueError):
        if kind == "pubmed":
            pubmed.search_pubmed("cancer", filters=filters)
        else:
            clinical_trials.search_clinical_trials("cancer", filters=filters)
    request.assert_not_called()


def test_filters_reach_registry_requests_instead_of_filtering_first_five_locally(monkeypatch):
    urls = []
    def request_pubmed(url):
        urls.append(url)
        return b'{"esearchresult":{"idlist":[]}}'
    monkeypatch.setattr(pubmed, "_request_bytes", request_pubmed)
    pubmed.search_pubmed("cancer", filters=PubMedFilters(affiliation="India"))
    assert '"India"[ad]' in parse_qs(urlparse(urls[0]).query)["term"][0]
    def request_trials(url):
        urls.append(url)
        return {"studies": []}
    monkeypatch.setattr(clinical_trials, "_get_json", request_trials)
    clinical_trials.search_clinical_trials("cancer", filters=TrialFilters(location="India", statuses=("Recruiting",)))
    parameters = parse_qs(urlparse(urls[1]).query)
    assert parameters["query.locn"] == ['"India"']
    assert parameters["filter.overallStatus"] == ["RECRUITING"]


@pytest.mark.parametrize("kind", ["pubmed", "trials"])
def test_filter_change_clears_results_selections_summaries_and_draft_without_requests(monkeypatch, kind):
    app, pubmed_mock, trial_mock = start_app(monkeypatch)
    search = pubmed_mock if kind == "pubmed" else trial_mock
    search.side_effect = None
    search.return_value = [article()] if kind == "pubmed" else [trial()]
    prefix, query_key, search_key, selection_key, identifier, filter_key = (
        ("pubmed", "pubmed_query", "search_pubmed", "selected_pmids", "12345678", "pm_affiliation") if kind == "pubmed" else
        ("trial", "trial_query", "search_trials", "selected_nct_ids", "NCT01234567", "ct_location"))
    app.text_input(key=query_key).input("cancer")
    app.button(key=search_key).click().run()
    assert not app.exception
    app.multiselect(key=selection_key).select(identifier).run()
    app.button(key="prepare_drafts").click().run()
    assert "workflow_result" in app.session_state
    app.text_input(key=filter_key).input("India").run()
    assert not app.exception
    assert prefix + "_results" not in app.session_state
    assert prefix + "_summaries" not in app.session_state
    assert "workflow_result" not in app.session_state
    search.assert_called_once()
    app.button(key=search_key).click().run()
    assert not app.exception
    assert search.call_args.kwargs["filters"].affiliation == "India" if kind == "pubmed" else search.call_args.kwargs["filters"].location == "India"
    assert app.multiselect(key=selection_key).value == []


def test_workspace_tabs_reset_filters_and_kol_switch_preserve_boundaries(monkeypatch):
    app, pubmed_mock, trial_mock = start_app(monkeypatch)
    labels = [tab.label for tab in app.tabs]
    assert all(name in labels for name in ("01  KOL context", "02  Evidence search", "03  Drafts & follow-up", "PubMed", "ClinicalTrials.gov"))
    app.text_input(key="pm_therapy").input("immunotherapy").run()
    app.button(key="reset_pm_filters").click().run()
    assert not app.exception
    assert app.text_input(key="pm_therapy").value == ""
    app.text_input(key="ct_location").input("India").run()
    app.selectbox(key="selected_kol").select_index(1).run()
    assert not app.exception
    assert app.text_input(key="ct_location").value == ""
    pubmed_mock.assert_not_called()
    trial_mock.assert_not_called()


def test_invalid_date_range_is_visible_without_a_search_or_summary_call(monkeypatch):
    app, pubmed_mock, _ = start_app(monkeypatch)
    app.text_input(key="pubmed_query").input("cancer")
    app.date_input(key="pm_start").set_value(date(2026, 1, 2))
    app.date_input(key="pm_end").set_value(date(2026, 1, 1))
    app.button(key="search_pubmed").click().run()
    assert not app.exception
    assert any("start date" in error.value for error in app.error)
    pubmed_mock.assert_not_called()


def test_date_controls_allow_historical_literature_and_future_study_dates(monkeypatch):
    app, pubmed_mock, trial_mock = start_app(monkeypatch)
    for key in ("pm_start", "pm_end", "ct_start", "ct_end"):
        assert app.date_input(key=key).proto.min == "1900-01-01"
        assert app.date_input(key=key).proto.max == "2100-12-31"
    app.date_input(key="pm_start").set_value(date(2000, 1, 1)).run()
    app.date_input(key="ct_end").set_value(date(2040, 1, 1)).run()
    assert not app.exception
    pubmed_mock.assert_not_called()
    trial_mock.assert_not_called()
