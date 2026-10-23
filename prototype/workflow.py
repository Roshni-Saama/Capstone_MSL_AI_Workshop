"""Bounded repeat-meeting workflow for the synthetic MSL prototype."""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

from langgraph.graph import END, START, StateGraph
from llm import OpenAILLM, LLMError, MAX_INPUT_CHARS

from agents import DATA_PATH, FollowUpAgent, KOLContextAgent, ScientificSourceAgent

_kol_context_agent = KOLContextAgent()
_scientific_source_agent = ScientificSourceAgent()
_follow_up_agent = FollowUpAgent()


class WorkflowState(TypedDict, total=False):
    kol_id: str
    meeting_notes: str
    scientific_sources: str
    record: dict
    crm_context: str
    briefing: str
    follow_up_draft: str
    generation_mode: str
    context_draft: str
    agent_trace: list[dict]


def load_records(path: Path = DATA_PATH) -> list[dict]:
    """Compatibility wrapper for the KOL Context Agent's fixture loader."""
    if path == _kol_context_agent.records_path:
        return _kol_context_agent.load_records()
    return KOLContextAgent(records_path=path).load_records()


def get_record(kol_id: str, records: list[dict] | None = None) -> dict:
    """Return one exact KOL record; never fuzzy-match identities."""
    if records is None:
        return _kol_context_agent.get_record(kol_id)
    for record in records:
        if record["kol_id"] == kol_id:
            return record
    raise KeyError(f"Unknown synthetic KOL ID: {kol_id}")


def retrieve_context(state: WorkflowState, llm: OpenAILLM | None = None) -> WorkflowState:
    """Compatibility workflow node delegated to the KOL Context Agent."""
    return _kol_context_agent.retrieve(state["kol_id"], llm=llm)


def draft_briefing(state: WorkflowState, llm: OpenAILLM | None = None) -> WorkflowState:
    """Compatibility workflow node delegated to the Scientific Source Agent."""
    return _scientific_source_agent.prepare_briefing(
        state.get("crm_context", ""),
        state.get("scientific_sources", ""),
        llm=llm,
    )


def draft_follow_up(state: WorkflowState, llm: OpenAILLM | None = None) -> WorkflowState:
    """Compatibility workflow node delegated to the Follow-up Agent."""
    return {"follow_up_draft": _follow_up_agent.draft(state.get("meeting_notes", ""), llm=llm)}


def build_workflow(llm: OpenAILLM | None = None):
    graph = StateGraph(WorkflowState)
    graph.add_node("kol_context_agent", lambda state: retrieve_context(state, llm))
    graph.add_node("scientific_source_agent", lambda state: draft_briefing(state, llm))
    graph.add_node("follow_up_agent", lambda state: draft_follow_up(state, llm))
    graph.add_edge(START, "kol_context_agent")
    graph.add_edge("kol_context_agent", "scientific_source_agent")
    graph.add_edge("scientific_source_agent", "follow_up_agent")
    graph.add_edge("follow_up_agent", END)
    return graph.compile()


def run_workflow(
    kol_id: str,
    scientific_sources: str = "",
    meeting_notes: str = "",
    *,
    use_llm: bool = False,
    api_key: str | None = None,
    model: str | None = None,
    llm: OpenAILLM | None = None,
) -> WorkflowState:
    # Resolve identity before any model request. Keys never enter graph state.
    selected_record = get_record(kol_id)
    if use_llm:
        if len(json.dumps(selected_record)) + len(scientific_sources) + len(meeting_notes) > MAX_INPUT_CHARS:
            raise LLMError("Selected input is too large. Reduce sources or notes and retry.")
    runtime = (llm or OpenAILLM(api_key=api_key, model=model)) if use_llm else None
    graph = build_workflow(runtime)
    result = graph.invoke(
        {
            "kol_id": kol_id,
            "scientific_sources": scientific_sources,
            "meeting_notes": meeting_notes,
        }
    )
    if runtime is not None:
        result["agent_trace"] = list(runtime.calls)
        result["generation_mode"] = f"OpenAI LLM: {runtime.model}; MSL review required"
    return result
