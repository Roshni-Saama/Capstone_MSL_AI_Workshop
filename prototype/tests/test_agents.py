from __future__ import annotations

from pathlib import Path

import pytest

from agents import FollowUpAgent, KOLContextAgent, ScientificSourceAgent
from workflow import run_workflow


def test_kol_context_agent_retrieves_one_exact_synthetic_record() -> None:
    result = KOLContextAgent().retrieve("KOL-DEMO-001")

    assert result["record"]["kol_id"] == "KOL-DEMO-001"
    assert "ENG-DEMO-001" in result["crm_context"]
    assert "ENG-DEMO-101" not in result["crm_context"]
    assert "CRM history" in result["crm_context"]


def test_kol_context_agent_rejects_unknown_record() -> None:
    with pytest.raises(KeyError, match="Unknown synthetic KOL ID"):
        KOLContextAgent().retrieve("KOL-REAL-001")


def test_scientific_source_agent_abstains_without_sources() -> None:
    result = ScientificSourceAgent.prepare_briefing("synthetic CRM", "")

    assert "abstains" in result["briefing"]
    assert result["generation_mode"].startswith("Abstention")


def test_scientific_source_agent_preserves_selected_text() -> None:
    source_text = "PMID: 12345\nAbstract: Synthetic test source text."

    result = ScientificSourceAgent.prepare_briefing("CRM context", source_text)

    assert source_text in result["briefing"]
    assert "does not interpret clinical evidence" in result["briefing"]


def test_follow_up_agent_preserves_note_and_leaves_decisions_to_msl() -> None:
    note = "KOL asked to discuss the registry eligibility criteria."

    draft = FollowUpAgent().draft(note)

    assert note in draft
    assert "MSL interpretation: Not generated" in draft
    assert "Owner and due date: Not assigned" in draft


def test_langgraph_orchestrates_all_three_agents() -> None:
    result = run_workflow(
        kol_id="KOL-DEMO-001",
        scientific_sources="PMID: 12345\nAbstract: Synthetic source text.",
        meeting_notes="KOL asked a question about the source.",
    )

    assert result["record"]["kol_id"] == "KOL-DEMO-001"
    assert "PMID: 12345" in result["briefing"]
    assert "KOL asked a question about the source." in result["follow_up_draft"]