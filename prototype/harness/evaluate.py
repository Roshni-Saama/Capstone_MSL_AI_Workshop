"""Run fixed mechanical agent evaluations. No credentials, network or LLM judge."""
from __future__ import annotations

import argparse
from contextlib import ExitStack
from datetime import datetime
from hashlib import sha256
from importlib.metadata import version
import json
from pathlib import Path
import platform
import sys
from time import perf_counter
from unittest.mock import patch
from zoneinfo import ZoneInfo

PROTOTYPE = Path(__file__).resolve().parents[1]
if str(PROTOTYPE) not in sys.path:
    sys.path.insert(0, str(PROTOTYPE))
import workflow
from llm import OpenAILLM

ROLES = ["KOL Context Agent", "Scientific Source Agent", "Follow-up Agent"]
SENTINEL = "HARNESS-FAKE-KEY"


class ScriptedRuntime(OpenAILLM):
    """Exercise production request/schema parsing with a local fake transport."""
    def __init__(self, fault=None):
        super().__init__(api_key=SENTINEL, model="mock-harness")
        self.fault = fault
        self.requests = []

    def _post(self, body):
        self.requests.append(body)
        schema = body["text"]["format"]["name"]
        data = json.loads(body["input"][1]["content"])
        if self.fault == "refusal":
            return {"status": "completed", "output": [{"type": "message", "content": [{"type": "refusal"}]}]}
        if self.fault == "malformed":
            result = {"meeting_priorities": "wrong type", "unresolved_requests": []}
        elif schema == "ContextOutput":
            result = {"meeting_priorities": [{"text": "Review this fictional KOL context.", "quote": data["synthetic_crm_context"].splitlines()[0]}], "unresolved_requests": []}
        elif schema == "ScienceOutput":
            source_id, source = next(iter(data["selected_scientific_sources"].items()))
            result = {"findings": [{"text": "A synthetic exercise source is supplied; no clinical conclusion is generated.",
                       "quote": "ABSENT QUOTE" if self.fault == "bad_quote" else source,
                       "source_id": "S999" if self.fault == "bad_source" else source_id}],
                       "discussion_questions": [], "limitations": []}
        else:
            result = {"observations": [], "follow_up_requests": [{"text": "Review the fictional request.", "quote": data["fictional_meeting_notes"]}], "open_questions": []}
        return {"status": "completed", "output": [{"type": "message", "content": [{"type": "output_text", "text": json.dumps(result)}]}]}


def grade_output(case, result, runtime, error_type):
    """Named assertions, also used to reject deliberately corrupted outputs."""
    checks = {"expected_error_or_success": error_type == case["expected_error"]}
    requests = runtime.requests if runtime else []
    attempted = [request["input"][0]["content"].split("Task: ")[-1].split(":")[0] for request in requests]
    checks["agent_order_and_call_budget"] = attempted == case["expected_attempts"] and len(requests) <= 3
    checks["credential_not_in_prompts_or_state"] = SENTINEL not in json.dumps([requests, result])
    checks["strict_schema_no_tools_no_storage"] = all(request["text"]["format"]["strict"] is True and request["store"] is False and "tools" not in request for request in requests)
    for index, request in enumerate(requests):
        schema = request["text"]["format"]["name"]
        data = json.loads(request["input"][1]["content"])
        expected_key = {"ContextOutput": "synthetic_crm_context", "ScienceOutput": "selected_scientific_sources", "FollowUpOutput": "fictional_meeting_notes"}[schema]
        checks[f"role_input_isolation_{index + 1}"] = list(data) == [expected_key]
        checks[f"untrusted_data_boundary_{index + 1}"] = request["input"][1]["role"] == "user" and "untrusted DATA" in request["input"][0]["content"]
        if schema == "ScienceOutput":
            selected = [part for part in case["scientific_sources"].strip().split("\n\n---\n\n") if part.strip()]
            checks["scientific_payload_matches_selected_sources"] = list(data.get(expected_key, {}).values()) == selected
    if case["expected_error"] is not None:
        checks["no_partial_result_accepted"] = result is None
        return checks
    if result is None:
        checks["result_available"] = False
        return checks
    checks["exact_identity"] = result.get("record", {}).get("kol_id") == case["kol_id"]
    other_records = [record for record in workflow.load_records() if record["kol_id"] != case["kol_id"]]
    checks["no_other_kol_context"] = all(record["kol_id"] not in result.get("crm_context", "") and all(item["engagement_id"] not in result.get("crm_context", "") for item in record["interactions"]) for record in other_records)
    source_text = case["scientific_sources"].strip()
    checks["source_preservation_or_abstention"] = (all(part in result.get("briefing", "") for part in source_text.split("\n\n---\n\n")) if source_text else "abstains" in result.get("briefing", ""))
    notes = case["meeting_notes"].strip()
    followup = result.get("follow_up_draft", "")
    checks["notes_preserved_or_empty_notice"] = notes in followup if notes else "No interpretation or follow-up task has been created" in followup
    checks["owners_and_dates_remain_unassigned"] = "Owner and due date: Not assigned" in followup if notes else True
    checks["draft_review_label"] = "DRAFT FOR MSL REVIEW" in followup if notes else True
    if runtime:
        checks["accepted_trace_matches_attempts"] = [call["agent"] for call in result.get("agent_trace", [])] == attempted
    return checks


def evaluate_case(case):
    runtime = ScriptedRuntime(case.get("fault")) if case["mode"] == "mock" else None
    result = None
    error_type = None
    started = perf_counter()
    with ExitStack() as stack:
        # Fail closed if any code accidentally attempts network traffic.
        for target in ("socket.socket.connect", "socket.create_connection", "socket.getaddrinfo", "urllib.request.urlopen"):
            stack.enter_context(patch(target, side_effect=AssertionError("Network forbidden in agent harness")))
        stack.enter_context(patch.object(workflow, "OpenAILLM", side_effect=AssertionError("Real runtime forbidden in harness")))
        try:
            sources = "X" * case.get("source_repeat_chars", 0) or case["scientific_sources"]
            result = workflow.run_workflow(case["kol_id"], sources, case["meeting_notes"], use_llm=case["mode"] == "mock", llm=runtime)
        except Exception as error:
            # Only the class is reported; raw exceptions can contain inputs/secrets.
            error_type = type(error).__name__
    checks = grade_output(case, result, runtime, error_type)
    return {"id": case["id"], "mode": case["mode"], "passed": all(checks.values()),
            "checks": checks, "error_type": error_type, "expected_error": case["expected_error"],
            "mock_transport_calls": len(runtime.requests) if runtime else 0,
            "duration_ms": round((perf_counter() - started) * 1000, 2)}


def run_cases(path=None):
    path = Path(path or Path(__file__).with_name("cases.json"))
    pack = json.loads(path.read_text(encoding="utf-8"))
    cases = pack["cases"]
    if pack.get("synthetic") is not True or not cases or len({case["id"] for case in cases}) != len(cases):
        raise ValueError("Harness requires unique, explicitly synthetic cases.")
    if any(case["mode"] not in ("offline", "mock") for case in cases):
        raise ValueError("Only offline and mock harness modes are allowed.")
    results = [evaluate_case(case) for case in cases]
    files = [Path(__file__), path, PROTOTYPE / "workflow.py", PROTOTYPE / "agents.py", PROTOTYPE / "llm.py", PROTOTYPE / "data/kol_records.json"]
    return {"run_at": datetime.now(ZoneInfo("Asia/Kolkata")).isoformat(timespec="seconds"),
            "validation_type": "Mechanical regression evaluation; offline and scripted model transport only",
            "live_openai_evaluated": False, "clinical_quality_evaluated": False,
            "human_review_status": "Pending evaluator scoring using specs/evaluation-and-review.md",
            "python": platform.python_version(), "versions": {name: version(name) for name in ("streamlit", "langgraph", "pydantic")},
            "input_sha256": {str(file.relative_to(PROTOTYPE)).replace(chr(92), "/"): sha256(file.read_bytes()).hexdigest() for file in files},
            "total": len(results), "passed": sum(result["passed"] for result in results),
            "failed": sum(not result["passed"] for result in results), "cases": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path(__file__).with_name("results"))
    args = parser.parse_args()
    report = run_cases()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    (args.output_dir / "agent_evaluation.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    lines = ["# Agent harness execution", "", f"Run: {report['run_at']}", "", f"Cases: {report['total']}; passed: {report['passed']}; failed: {report['failed']}.",
             "", "Offline/scripted transport only. No live model quality, clinical correctness or business benefit was evaluated.",
             "", "| Case | Mode | Result | Failed checks |", "| --- | --- | --- | --- |"]
    for result in report["cases"]:
        failures = ", ".join(name for name, passed in result["checks"].items() if not passed) or "None"
        lines.append(f"| {result['id']} | {result['mode']} | {'Passed' if result['passed'] else 'Failed'} | {failures} |")
    lines += ["", "Expected rejection cases pass only when the expected error and call sequence occur and no result is accepted.", "", "See [machine-readable checks and provenance](agent_evaluation.json) and [harness instructions](../README.md)."]
    (args.output_dir / "agent_evaluation.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Agent harness: {report['passed']}/{report['total']} passed; {report['failed']} failed (mock/offline only).")
    return 1 if report["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
