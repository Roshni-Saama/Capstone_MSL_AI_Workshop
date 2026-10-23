"""Three bounded local agents for the MSL prototype.

All agent drafting and workflow logic is deterministic Python. Registry searches
are read-only web requests initiated explicitly by the user.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from clinical_trials import discussion_prompts, search_clinical_trials
from pubmed import search_pubmed


DATA_PATH = Path(__file__).parent / "data" / "kol_records.json"
Record = dict[str, Any]


def format_crm_context(record: Record) -> str:
    interactions = []
    for item in record["interactions"]:
        interactions.append(
            "\n".join(
                [
                    f"- {item['date']} ({item['engagement_id']}): {item['purpose']}",
                    f"  Synthetic KOL observation: {item['observation']}",
                    f"  Draft MSL interpretation: {item['msl_interpretation']}",
                    f"  Follow-up: {item['task']} Owner: {item['owner_role']}. "
                    f"Status: {item['status']}. Due: {item['due_date']}.",
                ]
            )
        )
    meeting = record["planned_meeting"]
    return "\n".join(
        [
            f"KOL: {record['display_name']} ({record['kol_id']})",
            f"Institution: {record['institution']}",
            f"Role: {record['role']}",
            f"Therapy area: {record['therapy_area']}",
            f"Planned meeting: {meeting['date']} ({meeting['engagement_id']})",
            f"Purpose: {meeting['purpose']}",
            "Prior interactions (synthetic CRM history):",
            *interactions,
        ]
    )


class KOLContextAgent:
    """Retrieves one exact fictional CRM record and its interaction history."""

    def __init__(self, records_path: Path = DATA_PATH) -> None:
        self.records_path = records_path

    def load_records(self) -> list[Record]:
        payload = json.loads(self.records_path.read_text(encoding="utf-8"))
        if payload.get("synthetic") is not True:
            raise ValueError("Prototype data must be explicitly marked synthetic.")
        records = payload.get("records")
        if not isinstance(records, list) or len(records) != 3:
            raise ValueError("Expected exactly three synthetic KOL records.")
        ids = [record.get("kol_id") for record in records]
        if len(ids) != len(set(ids)) or any(not identifier for identifier in ids):
            raise ValueError("Synthetic KOL IDs must be present and unique.")
        return records

    def get_record(self, kol_id: str, records: list[Record] | None = None) -> Record:
        available = records if records is not None else self.load_records()
        for record in available:
            if record["kol_id"] == kol_id:
                return record
        raise KeyError(f"Unknown synthetic KOL ID: {kol_id}")

    def retrieve(self, kol_id: str) -> dict[str, Any]:
        record = self.get_record(kol_id)
        return {"record": record, "crm_context": format_crm_context(record)}


class ScientificSourceAgent:
    """Searches public registries and preserves selected sources locally."""

    def search_pubmed(self, query: str, retmax: int = 5) -> list[dict[str, str]]:
        return search_pubmed(query, retmax=retmax)

    def search_trials(self, query: str, page_size: int = 5) -> list[dict[str, Any]]:
        return search_clinical_trials(query, page_size=page_size)

    def trial_discussion_prompts(self, study: dict[str, Any]) -> list[str]:
        return discussion_prompts(study)

    @staticmethod
    def format_pubmed_sources(articles: list[dict[str, str]]) -> str:
        return "\n\n".join(
            "\n".join(
                [
                    f"Title: {article['title']}",
                    f"Authors: {article['authors'] or 'Unavailable'}",
                    f"Journal: {article['journal'] or 'Unavailable'} ({article['year'] or 'Year unavailable'})",
                    f"PMID: {article['pmid']}",
                    f"PubMed URL: {article['url']}",
                    f"DOI: {article['doi'] or 'Unavailable'}",
                    f"Abstract: {article['abstract'] or 'No abstract available.'}",
                ]
            )
            for article in articles
        )

    @staticmethod
    def format_trial_sources(studies: list[dict[str, Any]]) -> str:
        return "\n\n".join(
            "\n".join(
                [
                    "Registry source: ClinicalTrials.gov",
                    f"NCT ID: {study['nct_id']}",
                    f"Title: {study['title']}",
                    f"Record URL: {study['url']}",
                    f"Registry status: {study['status']}",
                    f"Last posted update: {study['last_updated'] or 'Not listed'}",
                    f"Study type: {study['study_type']}; phase: {study['phase']}",
                    f"Conditions: {', '.join(study['conditions']) or 'Not listed'}",
                    f"Interventions: {', '.join(study['interventions']) or 'Not listed'}",
                    f"Primary outcomes: {'; '.join(study['primary_outcomes']) or 'Not listed'}",
                    f"Enrollment: {study['enrollment']} {study['enrollment_type']}",
                    f"Eligibility: {study['eligibility']}",
                ]
            )
            for study in studies
        )

    @staticmethod
    def prepare_briefing(
        crm_context: str,
        sources: str,
    ) -> dict[str, str]:
        source_text = sources.strip()
        if not source_text:
            return {
                "briefing": (
                    "No scientific source text was supplied, so this prototype abstains "
                    "from scientific claims. Use the synthetic CRM history only to review "
                    "prior topics and open follow-up. Add an approved source pack before "
                    "drafting evidence content."
                ),
                "generation_mode": "Abstention: code-only, no scientific source supplied",
            }
        return {
            "briefing": (
                "DRAFT FOR MSL REVIEW\n\n"
                "Meeting context (synthetic CRM history):\n"
                f"{crm_context}\n\n"
                "Selected scientific source text (PubMed metadata/abstracts, "
                "ClinicalTrials.gov registry fields, and/or user-provided; verbatim; "
                "not independently verified):\n"
                f"{source_text}\n\n"
                "Evidence summary: Not generated. Review the source text and write a "
                "summary manually; this code-only prototype does not interpret clinical evidence."
            ),
            "generation_mode": "Code-only: source-preserving draft, no model call",
        }


class FollowUpAgent:
    """Preserves notes and provides a generic, rule-based review prompt."""

    def draft(self, notes: str) -> str:
        meeting_notes = notes.strip()
        if not meeting_notes:
            return (
                "Add fictional meeting notes to create a structured draft. "
                "No interpretation or follow-up task has been created."
            )

        request_terms = ("ask", "asked", "question", "request", "evidence", "source")
        has_request = any(term in meeting_notes.casefold() for term in request_terms)
        suggested_task = (
            "Review the request in the notes against approved scientific sources."
            if has_request
            else "MSL to define a follow-up after reviewing the notes."
        )
        return (
            "DRAFT FOR MSL REVIEW\n\n"
            "MSL-entered notes (preserved verbatim):\n"
            f"{meeting_notes}\n\n"
            "Observation: Review the notes and confirm the stakeholder statement.\n"
            "MSL interpretation: Not generated; enter only after review.\n"
            f"Suggested follow-up (rule-based): {suggested_task}\n"
            "Owner and due date: Not assigned.\n"
            "Status: Draft for review.\n"
            "The suggested task is a generic workflow prompt, not a scientific conclusion.\n"
            "Safety reminder: If notes contain potential safety information, use the "
            "organization's established process. This prototype does not detect or submit reports."
        )