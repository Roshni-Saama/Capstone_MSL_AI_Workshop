from __future__ import annotations

import json
from urllib.parse import parse_qs, urlparse

import pytest

import clinical_trials


STUDY_RESPONSE = {
    "studies": [
        {
            "protocolSection": {
                "identificationModule": {
                    "nctId": "NCT01234567",
                    "briefTitle": "Fictional Registry Test Study",
                },
                "statusModule": {
                    "overallStatus": "RECRUITING",
                    "lastUpdatePostDateStruct": {"date": "2026-09-15"},
                },
                "designModule": {
                    "studyType": "INTERVENTIONAL",
                    "phases": ["PHASE2"],
                    "designInfo": {"primaryPurpose": "TREATMENT"},
                    "enrollmentInfo": {"count": 120, "type": "ESTIMATED"},
                },
                "conditionsModule": {"conditions": ["Fictional condition"]},
                "armsInterventionsModule": {
                    "interventions": [{"name": "Example intervention"}]
                },
                "outcomesModule": {
                    "primaryOutcomes": [{"measure": "Example primary measure"}]
                },
                "eligibilityModule": {
                    "eligibilityCriteria": "Inclusion: adult participants.",
                    "minimumAge": "18 Years",
                    "sex": "ALL",
                },
                "contactsLocationsModule": {
                    "locations": [
                        {"country": "United States"},
                        {"country": "Canada"},
                        {"country": "United States"},
                    ]
                },
            }
        }
    ]
}


def test_search_clinical_trials_parses_registry_fields_and_query(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    requested: list[str] = []

    def fake_get_json(url: str) -> dict:
        requested.append(url)
        return STUDY_RESPONSE

    monkeypatch.setattr(clinical_trials, "_get_json", fake_get_json)

    studies = clinical_trials.search_clinical_trials("fictional condition", page_size=3)

    assert len(studies) == 1
    study = studies[0]
    assert study["nct_id"] == "NCT01234567"
    assert study["title"] == "Fictional Registry Test Study"
    assert study["status"] == "RECRUITING"
    assert study["last_updated"] == "2026-09-15"
    assert study["conditions"] == ["Fictional condition"]
    assert study["interventions"] == ["Example intervention"]
    assert study["primary_outcomes"] == ["Example primary measure"]
    assert study["countries"] == ["Canada", "United States"]
    assert study["url"] == "https://clinicaltrials.gov/study/NCT01234567"
    query = parse_qs(urlparse(requested[0]).query)
    assert query["query.cond"] == ["fictional condition"]
    assert query["pageSize"] == ["3"]
    assert query["format"] == ["json"]


@pytest.mark.parametrize("query", ["", "  "])
def test_search_rejects_empty_trial_query(query: str) -> None:
    with pytest.raises(ValueError, match="Enter a condition, intervention, or topic"):
        clinical_trials.search_clinical_trials(query)


def test_search_rejects_page_size_above_limit() -> None:
    with pytest.raises(ValueError, match="between 1 and 10"):
        clinical_trials.search_clinical_trials("condition", page_size=11)


def test_no_studies_returns_empty_list(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(clinical_trials, "_get_json", lambda url: {"studies": []})

    assert clinical_trials.search_clinical_trials("no results") == []


def test_discussion_prompts_are_neutral_and_field_based() -> None:
    study = clinical_trials._study_record(STUDY_RESPONSE["studies"][0])

    prompts = clinical_trials.discussion_prompts(study)

    assert any("current status" in prompt for prompt in prompts)
    assert any("eligibility criteria" in prompt for prompt in prompts)
    assert any("primary outcome measures" in prompt for prompt in prompts)
    assert all("recommend" not in prompt.casefold() for prompt in prompts)
