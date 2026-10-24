"""Ensure the harness detects regressions rather than merely producing reports."""
import json
from pathlib import Path

import pytest

from harness.evaluate import ScriptedRuntime, grade_output, run_cases
from workflow import run_workflow


def test_fixed_agent_pack_passes_without_network_or_credentials(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    report = run_cases()
    assert report["failed"] == 0, [(case["id"], case["checks"]) for case in report["cases"] if not case["passed"]]
    assert report["total"] == 16
    assert report["live_openai_evaluated"] is False
    assert "HARNESS-FAKE-KEY" not in json.dumps(report)
    assert report["input_sha256"]["data/kol_records.json"]


@pytest.mark.parametrize("corruption", ["identity", "notes", "source", "credential", "role_input", "call_order", "cross_kol_context"])
def test_grader_rejects_corrupted_outputs_and_requests(corruption):
    cases = json.loads((Path(__file__).parents[1] / "harness/cases.json").read_text())["cases"]
    case = next(case for case in cases if case["id"] == "mock-kol-001")
    runtime = ScriptedRuntime()
    result = run_workflow(case["kol_id"], case["scientific_sources"], case["meeting_notes"], use_llm=True, llm=runtime)
    if corruption == "identity":
        result["record"] = {"kol_id": "OTHER-KOL"}
    elif corruption == "notes":
        result["follow_up_draft"] = "Invented notes"
    elif corruption == "source":
        result["briefing"] = "Invented source"
    elif corruption == "cross_kol_context":
        result["crm_context"] += " KOL-DEMO-002"
    elif corruption == "credential":
        result["credential"] = "HARNESS-FAKE-KEY"
    elif corruption == "role_input":
        runtime.requests[1]["input"][1]["content"] = json.dumps({"synthetic_crm_context": "Cross-role data"})
    else:
        runtime.requests.reverse()
    assert not all(grade_output(case, result, runtime, None).values())
