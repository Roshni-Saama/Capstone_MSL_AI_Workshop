"""Bounded repeat-meeting workflow for the synthetic MSL prototype."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph


DATA_PATH = Path(__file__).parent / "data" / "kol_records.json"


class WorkflowState(TypedDict, total=False):
    kol_id: str
    meeting_notes: str
    scientific_sources: str
    record: dict
    crm_context: str
    briefing: str
    follow_up_draft: str
    generation_mode: str


def load_records(path: Path = DATA_PATH) -> list[dict]:
    """Load only the explicitly synthetic demo records."""
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("synthetic") is not True:
        raise ValueError("Prototype data must be explicitly marked synthetic.")
    records = payload.get("records")
    if not isinstance(records, list) or len(records) != 3:
        raise ValueError("Expected exactly three synthetic KOL records.")
    ids = [record.get("kol_id") for record in records]
    if len(ids) != len(set(ids)) or any(not identifier for identifier in ids):
        raise ValueError("Synthetic KOL IDs must be present and unique.")
    return records


def get_record(kol_id: str, records: list[dict] | None = None) -> dict:
    """Return one exact KOL record; never fuzzy-match identities."""
    available = records if records is not None else load_records()
    for record in available:
        if record["kol_id"] == kol_id:
            return record
    raise KeyError(f"Unknown synthetic KOL ID: {kol_id}")


def _format_context(record: dict) -> str:
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


def retrieve_context(state: WorkflowState) -> WorkflowState:
    record = get_record(state["kol_id"])
    return {"record": record, "crm_context": _format_context(record)}


def draft_briefing(state: WorkflowState) -> WorkflowState:
    sources = state.get("scientific_sources", "").strip()
    if not sources:
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
            f"{state['crm_context']}\n\n"
            "Selected scientific source text (PubMed metadata/abstracts and/or user-provided; "
            "verbatim; not independently verified):\n"
            f"{sources}\n\n"
            "Evidence summary: Not generated. Review the source text and write a "
            "summary manually; this code-only prototype does not interpret clinical evidence."
        ),
        "generation_mode": "Code-only: source-preserving draft, no model call",
    }


def draft_follow_up(state: WorkflowState) -> WorkflowState:
    notes = state.get("meeting_notes", "").strip()
    if not notes:
        return {
            "follow_up_draft": (
                "Add fictional meeting notes to create a structured draft. "
                "No interpretation or follow-up task has been created."
            ),
        }

    request_terms = ("ask", "asked", "question", "request", "evidence", "source")
    has_request = any(term in notes.casefold() for term in request_terms)
    suggested_task = (
        "Review the request in the notes against approved scientific sources."
        if has_request
        else "MSL to define a follow-up after reviewing the notes."
    )
    return {
        "follow_up_draft": (
            "DRAFT FOR MSL REVIEW\n\n"
            "MSL-entered notes (preserved verbatim):\n"
            f"{notes}\n\n"
            "Observation: Review the notes and confirm the stakeholder statement.\n"
            "MSL interpretation: Not generated; enter only after review.\n"
            f"Suggested follow-up (rule-based): {suggested_task}\n"
            "Owner and due date: Not assigned.\n"
            "Status: Draft for review.\n"
            "The suggested task is a generic workflow prompt, not a scientific conclusion.\n"
            "Safety reminder: If notes contain potential safety information, use the "
            "organization's established process. This prototype does not detect or submit reports."
        )
    }


def build_workflow():
    graph = StateGraph(WorkflowState)
    graph.add_node("retrieve_context", retrieve_context)
    graph.add_node("draft_briefing", draft_briefing)
    graph.add_node("draft_follow_up", draft_follow_up)
    graph.add_edge(START, "retrieve_context")
    graph.add_edge("retrieve_context", "draft_briefing")
    graph.add_edge("draft_briefing", "draft_follow_up")
    graph.add_edge("draft_follow_up", END)
    return graph.compile()


def run_workflow(
    kol_id: str,
    scientific_sources: str = "",
    meeting_notes: str = "",
) -> WorkflowState:
    graph = build_workflow()
    return graph.invoke(
        {
            "kol_id": kol_id,
            "scientific_sources": scientific_sources,
            "meeting_notes": meeting_notes,
        }
    )