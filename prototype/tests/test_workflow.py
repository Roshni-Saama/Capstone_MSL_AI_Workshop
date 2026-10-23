from __future__ import annotations

from pathlib import Path

import pytest

from workflow import draft_briefing, draft_follow_up, get_record, load_records


def test_loads_exactly_three_unique_synthetic_records() -> None:
    records = load_records()

    assert len(records) == 3
    assert {record["kol_id"] for record in records} == {
        "KOL-DEMO-001",
        "KOL-DEMO-002",
        "KOL-DEMO-003",
    }


def test_record_lookup_does_not_mix_kol_history() -> None:
    first = get_record("KOL-DEMO-001")
    second = get_record("KOL-DEMO-002")

    assert first["planned_meeting"]["engagement_id"] == "ENG-DEMO-003"
    assert second["planned_meeting"]["engagement_id"] == "ENG-DEMO-103"
    assert all(item["engagement_id"].startswith("ENG-DEMO-00") for item in first["interactions"])
    assert all(item["engagement_id"].startswith("ENG-DEMO-10") for item in second["interactions"])


def test_unknown_kol_id_fails_closed() -> None:
    with pytest.raises(KeyError, match="Unknown synthetic KOL ID"):
        get_record("KOL-REAL-001")


def test_loader_rejects_non_synthetic_fixture(tmp_path: Path) -> None:
    path = tmp_path / "records.json"
    path.write_text('{"synthetic": false, "records": []}', encoding="utf-8")

    with pytest.raises(ValueError, match="explicitly marked synthetic"):
        load_records(path)


def test_briefing_abstains_without_scientific_source() -> None:
    result = draft_briefing({"scientific_sources": "", "crm_context": "synthetic CRM text"})

    assert "abstains" in result["briefing"]
    assert "scientific claims" in result["briefing"]
    assert result["generation_mode"].startswith("Abstention")


def test_briefing_preserves_sources_without_interpreting_them() -> None:
    source_text = "Example source excerpt: study methods were described in the supplied text."

    result = draft_briefing(
        {"scientific_sources": source_text, "crm_context": "synthetic CRM history"}
    )

    assert source_text in result["briefing"]
    assert "not independently verified" in result["briefing"]
    assert "does not interpret clinical evidence" in result["briefing"]
    assert result["generation_mode"].startswith("Code-only")


def test_follow_up_preserves_notes_and_does_not_invent_tasks() -> None:
    notes = "KOL asked for a source on the prior evidence question."

    result = draft_follow_up({"meeting_notes": notes, "crm_context": "synthetic CRM history"})

    assert notes in result["follow_up_draft"]
    assert "MSL interpretation: Not generated" in result["follow_up_draft"]
    assert "Suggested follow-up (rule-based)" in result["follow_up_draft"]
    assert "Review the request in the notes against approved scientific sources." in result["follow_up_draft"]
    assert "Owner and due date: Not assigned" in result["follow_up_draft"]