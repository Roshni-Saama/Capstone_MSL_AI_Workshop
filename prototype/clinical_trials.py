"""Read-only ClinicalTrials.gov API v2 search for study metadata."""

from __future__ import annotations

import json
import ssl
import urllib.error
import urllib.parse
import urllib.request

import truststore
from search_filters import TrialFilters, trial_parameters


API_URL = "https://clinicaltrials.gov/api/v2/studies"
USER_AGENT = "MSLRepeatMeetingPrototype/0.1 (educational capstone)"


class ClinicalTrialsError(RuntimeError):
    """Raised when ClinicalTrials.gov cannot provide a valid response."""


def _get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    try:
        with urllib.request.urlopen(request, timeout=20, context=context) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise ClinicalTrialsError(
            "ClinicalTrials.gov could not be reached. Check the connection and retry."
        ) from error
    except json.JSONDecodeError as error:
        raise ClinicalTrialsError("ClinicalTrials.gov returned unreadable JSON.") from error
    if not isinstance(payload, dict):
        raise ClinicalTrialsError("ClinicalTrials.gov returned an unexpected response.")
    return payload


def _study_record(study: dict) -> dict[str, str | list[str]]:
    protocol = study.get("protocolSection", {})
    identification = protocol.get("identificationModule", {})
    status = protocol.get("statusModule", {})
    design = protocol.get("designModule", {})
    conditions = protocol.get("conditionsModule", {})
    interventions_module = protocol.get("armsInterventionsModule", {})
    outcomes = protocol.get("outcomesModule", {})
    eligibility = protocol.get("eligibilityModule", {})
    locations_module = protocol.get("contactsLocationsModule", {})

    nct_id = identification.get("nctId", "")
    status_date = status.get("studyFirstPostDateStruct", {}).get("date", "")
    last_updated = status.get("studyFirstPostDateStruct", {}).get("date", "")
    update_struct = status.get("studyFirstPostDateStruct", {})
    last_update_struct = status.get("lastUpdatePostDateStruct", {})
    last_updated = last_update_struct.get("date") or update_struct.get("date", "")

    design_info = design.get("designInfo", {})
    enrollment = design.get("enrollmentInfo", {})
    primary_outcomes = outcomes.get("primaryOutcomes", [])
    locations = locations_module.get("locations", [])
    countries = sorted(
        {
            location.get("country", "").strip()
            for location in locations
            if location.get("country", "").strip()
        }
    )
    interventions = [
        item.get("name", "").strip()
        for item in interventions_module.get("interventions", [])
        if item.get("name", "").strip()
    ]
    outcomes_list = [
        item.get("measure", "").strip()
        for item in primary_outcomes
        if item.get("measure", "").strip()
    ]

    return {
        "nct_id": nct_id,
        "lead_sponsor": protocol.get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "Not reported"),
        "collaborators": [x.get("name", "") for x in protocol.get("sponsorCollaboratorsModule", {}).get("collaborators", [])],
        "has_results": bool(study.get("hasResults", False)),
        "title": identification.get("briefTitle", "Title unavailable"),
        "status": status.get("overallStatus", "Status unavailable"),
        "last_updated": last_updated,
        "study_type": design.get("studyType", "Not reported"),
        "phase": ", ".join(design.get("phases", [])) or "Not reported",
        "conditions": conditions.get("conditions", []),
        "interventions": interventions,
        "primary_outcomes": outcomes_list,
        "enrollment": str(enrollment.get("count", "Not reported")),
        "enrollment_type": enrollment.get("type", ""),
        "primary_purpose": design_info.get("primaryPurpose", "Not reported"),
        "eligibility": eligibility.get("eligibilityCriteria", "Not reported"),
        "minimum_age": eligibility.get("minimumAge", "Not reported"),
        "sex": eligibility.get("sex", "Not reported"),
        "locations_count": str(len(locations)),
        "countries": countries,
        "url": f"https://clinicaltrials.gov/study/{nct_id}" if nct_id else "",
    }


def search_clinical_trials(query: str, page_size: int = 5, *, filters: TrialFilters | None = None) -> list[dict[str, str | list[str]]]:
    """Search current public registry records; return at most ten studies."""
    search_term = query.strip()
    if not search_term:
        raise ValueError("Enter a condition, intervention, or topic to search trials.")
    if len(search_term) > 250:
        raise ValueError("Clinical trial search text must be 250 characters or fewer.")
    if not 1 <= page_size <= 10:
        raise ValueError("Clinical trial result count must be between 1 and 10.")

    params = urllib.parse.urlencode(
        {**trial_parameters(search_term, filters), "pageSize": page_size, "format": "json"}
    )
    payload = _get_json(f"{API_URL}?{params}")
    studies = payload.get("studies", [])
    if not isinstance(studies, list):
        raise ClinicalTrialsError("ClinicalTrials.gov returned an unreadable study list.")
    return [
        record
        for record in (_study_record(study) for study in studies if isinstance(study, dict))
        if record["nct_id"]
    ]


def discussion_prompts(study: dict[str, str | list[str]]) -> list[str]:
    """Generate neutral prompts from registered fields without interpreting results."""
    prompts = [
        f"The registry lists the study as {study['status']}. What questions, if any, would you like to discuss about its current status?",
    ]
    if study["eligibility"] != "Not reported":
        prompts.append(
            "The registry provides eligibility criteria. Which aspects of the registered population would be useful to clarify?"
        )
    if study["primary_outcomes"]:
        prompts.append(
            "The registry lists primary outcome measures. Which measure or endpoint would you like to discuss?"
        )
    if study["last_updated"]:
        prompts.append(
            f"The registry record shows an update posted on {study['last_updated']}. Is there a specific update you would like to review?"
        )
    return prompts