"""Guided fictional live-run inputs and an explicitly saved, credential-free report."""
from datetime import datetime, timezone, timedelta
from pathlib import Path
import json

DEMO_QUERY = "older adults cancer clinical trial representation review"
DEMO_NOTES = "Dr Mira Sen asked for a source-linked explanation of how older adults were represented in the selected study and its limitations. She requested a reviewed follow-up; no response, owner or deadline was promised."
REPORT_PATH = Path(__file__).parent / "test_scenarios/results/live_openai_walkthrough.json"


def build_report(result):
    fields = ("kol_id", "generation_mode", "context_draft", "briefing", "follow_up_draft", "agent_trace")
    report = {"recorded_at": datetime.now(timezone(timedelta(hours=5, minutes=30))).isoformat(timespec="seconds"),
              "review_status": "Model outputs require human review; scientific accuracy and usefulness are not yet established.",
              "workflow": {field: result[field] for field in fields if field in result}}
    report["all_three_agents_completed"] = len(result.get("agent_trace", [])) == 3
    report["mode"] = "OpenAI workflow" if result.get("generation_mode", "").startswith("OpenAI LLM:") else "Offline workflow"
    return report


def save_report(result, path=REPORT_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(build_report(result), indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    return path
