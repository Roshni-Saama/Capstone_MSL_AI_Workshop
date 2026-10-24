"""Build a scenario inventory from an actual pytest JUnit report; never runs tests."""
import argparse
import csv
from collections import Counter
from datetime import date
from pathlib import Path
import xml.etree.ElementTree as ET

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument("--date", required=True, help="Report date in the user's local timezone, YYYY-MM-DD")
args = parser.parse_args()
report_date = date.fromisoformat(args.date).isoformat()
folder = Path(__file__).resolve().parent
report_path = folder / "results" / "automated_tests.xml"
root = ET.parse(report_path).getroot()
cases = list(root.iter("testcase"))
if not cases:
    raise SystemExit("No executed test cases in XML; no report was generated.")
categories = {
    "test_search_filters": ("Advanced registry filters and navigation", "Validate server-side filter encoding, date/option rejection, query state clearing, reset and three-workspace navigation using mocked services."),
    "test_harness": ("Agent evaluation harness and grader", "Run the fixed synthetic evaluation pack without network and ensure deliberately corrupted outputs fail the grader."),
    "test_public_deployment": ("Prepared public runtime protections", "Check visitor-key isolation and download-only reporting locally; no hosted deployment is performed."),
    "test_walkthrough": ("Guided walkthrough and run evidence", "Load fictional Mira Sen inputs without network calls and verify credential-free, explicitly saved run records."),
    "test_search_summaries": ("Scientific search summaries", "Exercise compact previews or mocked batch summaries; inspect source validation, original-detail UI, explicit selection and session recovery."),
    "test_agents": ("Agent contracts", "Run the role-specific input through the agent and verify returned context/draft assertions."),
    "test_workflow": ("Workflow and evidence boundaries", "Run fixture lookup, missing-source or note/source preservation checks with the named inputs."),
    "test_pubmed": ("PubMed parsing and validation", "Use mocked PubMed payloads or invalid query/count inputs; inspect metadata or raised error."),
    "test_clinical_trials": ("ClinicalTrials.gov parsing and prompts", "Use mocked registry payloads or invalid inputs; inspect fields, links and neutral prompts."),
    "test_app": ("UI and LLM failure recovery", "Interact with Streamlit AppTest widgets and assert visible draft/error/state behavior; external services are mocked."),
    "test_llm": ("OpenAI integration contracts", "Use fake model/transport responses to assert request construction, response validation, role isolation or safe failure."),
    "test_crm": ("Synthetic CRM data and UI", "Load or deliberately corrupt a fixture copy, run the selected case, or switch the KOL in Streamlit AppTest."),
}
expected = {
    "test_crm_record_has_linked_profile_interactions_tasks_and_requests": "Three interactions, three tasks and two requests belong to the chosen KOL; two tasks active and one overdue.",
    "test_retrieved_crm_context_excludes_other_kol_profiles_tasks_and_requests": "Only the selected KOL's CRM profile, tasks and request identifiers appear in context.",
    "test_invalid_crm_relationships_and_unsubstantiated_completion_are_rejected": "Foreign KOL links, missing references, duplicate IDs or unsupported task completion raise ValueError.",
    "test_overdue_uses_fixed_snapshot_and_excludes_due_today_and_completed": "Overdue uses 23 October snapshot, excludes due-today tasks and excludes completed tasks.",
    "test_demo_scenario_inputs_run_for_each_kol_without_creating_scientific_evidence": "Correct KOL and original source/notes preserved; no owner/date invented; absent sources still cause abstention.",
    "test_crm_csv_exports_match_the_runtime_fixture": "Exported profile, interaction, task and request counts and identifiers match the runtime fixture.",
    "test_crm_tabs_metrics_and_tables_switch_to_the_selected_kol_only": "Four CRM tabs and correct metrics render; task/request tables follow the selected KOL without leakage.",
    "test_prompt_injection_is_data_not_system_instruction": "Instruction-like input remains user data, not system text; does not establish live injection resistance.",
    "test_three_llm_agents_are_orchestrated_and_keys_stay_out_of_state": "Three mocked role calls occur in order; keys stay out of state and sources/notes remain isolated by role.",
    "test_transport_posts_json_to_fixed_endpoint_with_bearer_header": "Mocked transport uses POST to the fixed OpenAI endpoint with JSON body and bearer header.",
    "test_invalid_refused_or_partial_response_is_rejected": "Incomplete, refused, malformed, extra-field, empty or invalid responses raise a safe LLMError.",
    "test_http_errors_are_sanitized": "HTTP failures raise a safe message without raw body, credential or exception text.",
    "test_unknown_source_or_mismatched_quote_is_rejected": "Unselected source IDs and quotes absent from their designated source reject the draft.",
    "test_explicit_search_failure_and_empty_results_are_visible": "Search failure is visible; subsequent empty results clear the error and show a no-results message.",
    "test_registry_material_requires_explicit_selection": "Unselected registry result is excluded; selecting it includes its identifier and URL in the briefing.",
}
rows = []
for number, case in enumerate(cases, 1):
    module = case.get("classname", "").split(".")[-1]
    name = case.get("name", "")
    base_name = name.split("[", 1)[0]
    category, steps = categories.get(module, ("Other", "See executable test assertions."))
    if case.find("failure") is not None or case.find("error") is not None:
        result = "Failed"
    elif case.find("skipped") is not None:
        result = "Skipped"
    else:
        result = "Passed"
    rows.append({
        "scenario_id": f"AUTO-{number:03d}", "category": category,
        "scenario": base_name.removeprefix("test_").replace("_", " "),
        "parameter_case": name[len(base_name):] or "Single case",
        "steps": steps,
        "expected_behavior": expected.get(base_name, base_name.removeprefix("test_").replace("_", " ").capitalize() + "; exact assertions are in the linked executable test."),
        "test_reference": f"tests/{module}.py::{name}",
        "result": result, "validation_type": "Automated; mocked external services where applicable",
        "evidence": "results/automated_tests.xml", "report_date": report_date,
    })
with (folder / "scenario_catalog.csv").open("w", newline="", encoding="utf-8-sig") as output:
    writer = csv.DictWriter(output, fieldnames=list(rows[0]))
    writer.writeheader()
    writer.writerows(rows)
counts = Counter(row["result"] for row in rows)
by_category = Counter(row["category"] for row in rows)
lines = ["# Latest automated test execution", "", f"Report date: {report_date} (Asia/Kolkata).",
         "", f"Executed cases: **{len(rows)}**. Passed: **{counts['Passed']}**. Failed: **{counts['Failed']}**. Skipped: **{counts['Skipped']}**.",
         "", "Results are derived from [the pytest JUnit XML](automated_tests.xml); this report does not infer pass status from file presence or earlier runs.",
         "", "| Area | Executed cases |", "| --- | --- |"]
for category, count in sorted(by_category.items()):
    lines.append(f"| {category} | {count} |")
lines += ["", "Run from the prototype folder:", "", "```powershell",
          "./.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --junitxml=test_scenarios/results/automated_tests.xml",
          f"./.venv/Scripts/python.exe -B test_scenarios/build_report.py --date {report_date}",
          "```", "", "The suite uses fictional CRM fixtures and mocked model/registry responses; no live OpenAI completion or medical accuracy was verified by this test run.",
          "", "Additional evidence: [scenario catalog](../scenario_catalog.csv), [use cases](../use_cases.md), [live/manual checks](../live_and_manual_checks.md).",
          "", "Test code is maintained in [prototype/tests](../../tests). The report describes the latest run, not a complete archive of all historical runs."]
(folder / "results" / "latest_run.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
print(f"Built catalog/report for {len(rows)} executed cases: {dict(counts)}")
