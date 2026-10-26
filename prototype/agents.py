"""Three bounded agents for the MSL workshop prototype.

Offline mode is deterministic. Explicit OpenAI mode adds bounded, quote-checked
drafting. Registry searches remain read-only and user-triggered.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from clinical_trials import discussion_prompts, search_clinical_trials
from pubmed import search_pubmed
from presentation import display_crm
from crm import validate_crm_records, format_crm_details
from llm import (ContextOutput, ScienceOutput, FollowUpOutput, OpenAILLM, LLMError,
                 validate_items, render_items)


DATA_PATH = Path(__file__).parent / "data" / "kol_records.json"
Record = dict[str, Any]


def format_crm_context(record: Record) -> str:
    record = display_crm(record)
    interactions = []
    for item in record["interactions"]:
        interactions.append(
            "\n".join(
                [
                    f"- {item['date']} ({item['engagement_id']}): {item['purpose']}",
                    f"  KOL observation: {item['observation']}",
                    f"  MSL response: {item['msl_response']}",
                    f"  Response status: {item['response_status']}",
                    "  Sources discussed: " + "; ".join(
                        f"{source['label']} ({source['url']})"
                        for source in item.get("response_sources", [])
                    ),
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
            "Prior interactions (CRM history):",
            *interactions,
            format_crm_details(record),
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
        validate_crm_records(records)
        return records

    def get_record(self, kol_id: str, records: list[Record] | None = None) -> Record:
        available = records if records is not None else self.load_records()
        for record in available:
            if record["kol_id"] == kol_id:
                return record
        raise KeyError(f"Unknown synthetic KOL ID: {kol_id}")

    def plan_research(self, kol_id, question, llm=None):
        from mira_research import plan_research
        return plan_research(kol_id, question, llm)

    def retrieve(self, kol_id: str, llm: OpenAILLM | None = None) -> dict[str, Any]:
        record = self.get_record(kol_id)
        context = format_crm_context(record)
        result = {"record": record, "crm_context": context}
        if llm is not None:
            draft = llm.generate(
                "KOL Context Agent: extract meeting priorities and unresolved requests from this exact synthetic CRM context. Do not make scientific claims.",
                {"synthetic_crm_context": context}, ContextOutput,
            )
            validate_items(draft.meeting_priorities + draft.unresolved_requests, context)
            result["context_draft"] = (
                "DRAFT FOR MSL REVIEW\n\nMeeting priorities:\n" + render_items(draft.meeting_priorities)
                + "\n\nUnresolved requests:\n" + render_items(draft.unresolved_requests)
            )
        return result


class ScientificSourceAgent:
    """Retrieves selected sources and optionally drafts a quote-backed briefing."""

    @staticmethod
    def summarize_search_results(records, kind, llm=None):
        from search_summaries import summarize_results
        return summarize_results(records, kind, llm=llm)

    def search_pubmed(self, query: str, retmax: int = 5, *, filters=None) -> list[dict[str, str]]:
        return search_pubmed(query, retmax=retmax, **({"filters": filters} if filters is not None else {}))

    def search_trials(self, query: str, page_size: int = 5, *, filters=None) -> list[dict[str, Any]]:
        return search_clinical_trials(query, page_size=page_size, **({"filters": filters} if filters is not None else {}))

    def search_research(self, plan, pubmed_queries, trial_query, *, pubmed_filters=None, trial_filters=None):
        from mira_research import search_evidence
        return search_evidence(
            plan, pubmed_queries, trial_query, agent=self,
            pubmed_filters=pubmed_filters, trial_filters=trial_filters,
        )

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
                    f"Lead sponsor: {study.get('lead_sponsor', 'Not reported')}",
                    f"Collaborators: {', '.join(study.get('collaborators', [])) or 'Not reported'}",
                    f"Registry results posted: {study.get('has_results', False)} (absence does not establish absence of publications)",
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
        llm: OpenAILLM | None = None,
    ) -> dict[str, str]:
        source_text = sources.strip()
        if not source_text:
            return {
                "briefing": (
                    "No scientific source text was supplied, so the assistant abstains "
                    "from scientific claims. Use the CRM history only to review "
                    "prior topics and open follow-up. Add an approved source pack before "
                    "drafting evidence content."
                ),
                "generation_mode": "Abstention: no scientific source supplied",
            }
        if llm is not None:
            sources_by_id = {f"S{index}": text for index, text in
                             enumerate(source_text.split("\n\n---\n\n"), 1) if text.strip()}
            draft = llm.generate(
                "Scientific Source Agent: draft findings, neutral discussion questions and limitations using only selected scientific sources. Every item needs its source_id and an exact quote from that source. Do not use CRM as evidence. Omit unsupported findings.",
                {"selected_scientific_sources": sources_by_id}, ScienceOutput,
            )
            for item in draft.findings + draft.discussion_questions + draft.limitations:
                if item.source_id not in sources_by_id:
                    raise LLMError("Draft cited a source that was not selected. No draft was accepted.")
                validate_items([item], sources_by_id[item.source_id])
            source_appendix = "\n\n".join(f"[{key}]\n{value}" for key, value in sources_by_id.items())
            return {
                "briefing": "DRAFT FOR MSL REVIEW\n\nAI-drafted findings:\n" + render_items(draft.findings)
                + "\n\nNeutral discussion questions:\n" + render_items(draft.discussion_questions)
                + "\n\nLimitations to review:\n" + render_items(draft.limitations)
                + "\n\nSelected scientific source text (not independently verified):\n" + source_appendix,
                "generation_mode": f"OpenAI LLM: {llm.model}; source quotes checked; MSL review required",
            }
        return {
            "briefing": (
                "DRAFT FOR MSL REVIEW\n\n"
                "Meeting context (CRM history):\n"
                f"{crm_context}\n\n"
                "Selected scientific source text (PubMed metadata/abstracts, "
                "ClinicalTrials.gov registry fields, and/or user-provided; verbatim; "
                "not independently verified):\n"
                f"{source_text}\n\n"
                "Evidence summary: Not generated. Review the source text and write a "
                "summary manually; Offline mode does not interpret clinical evidence."
            ),
            "generation_mode": "Offline: source-preserving draft, no model call",
        }


class FollowUpAgent:
    """Preserves notes and drafts bounded offline or LLM follow-up content."""

    def next_actions(self, result, question, links):
        from mira_research import next_actions
        return next_actions(result, question, links)

    def draft(self, notes: str, llm: OpenAILLM | None = None) -> str:
        meeting_notes = notes.strip()
        if not meeting_notes:
            return (
                "Add meeting notes to create a structured draft. "
                "No interpretation or follow-up task has been created."
            )

        if llm is not None:
            draft = llm.generate(
                "Follow-up Agent: extract stakeholder observations, explicit follow-up requests and open questions from the fictional notes only. Do not answer scientific questions or generate clinical conclusions. Use exact quotes. Do not invent commitments, owners or due dates.",
                {"fictional_meeting_notes": meeting_notes}, FollowUpOutput,
            )
            validate_items(draft.observations + draft.follow_up_requests + draft.open_questions, meeting_notes)
            return (
                "DRAFT FOR MSL REVIEW\n\nMSL-entered notes (preserved verbatim):\n" + meeting_notes
                + "\n\nDraft observations:\n" + render_items(draft.observations)
                + "\n\nDraft follow-up requests:\n" + render_items(draft.follow_up_requests)
                + "\n\nOpen questions:\n" + render_items(draft.open_questions)
                + "\n\nMSL interpretation: Enter only after review."
                + "\nOwner and due date: Not assigned.\nStatus: Draft for review."
                + "\nSafety reminder: Use the organization's established process for potential safety information; this app does not detect or submit reports."
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
            f"Suggested follow-up: {suggested_task}\n"
            "Owner and due date: Not assigned.\n"
            "Status: Draft for review.\n"
            "The suggested task is a generic workflow prompt, not a scientific conclusion.\n"
            "Safety reminder: If notes contain potential safety information, use the "
            "organization's established process. This app does not detect or submit reports."
        )
