import copy
import csv
import json
from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest

from agents import KOLContextAgent
from crm import validate_crm_records, task_rows, crm_summary
from workflow import load_records, run_workflow

ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.parametrize("index", [0, 1, 2])
def test_crm_record_has_linked_profile_interactions_tasks_and_requests(index):
    records = load_records()
    record = records[index]
    assert len(record["interactions"]) == 3
    assert len(record["tasks"]) == 3
    assert len(record["medical_requests"]) == 2
    assert all(child["kol_id"] == record["kol_id"] for key in
               ["interactions", "tasks", "medical_requests"] for child in record[key])
    assert crm_summary(record) == {"interactions": 3, "active_tasks": 2, "overdue_tasks": 1, "requests": 2}


@pytest.mark.parametrize("kol_id", ["KOL-DEMO-001", "KOL-DEMO-002", "KOL-DEMO-003"])
def test_retrieved_crm_context_excludes_other_kol_profiles_tasks_and_requests(kol_id):
    context = KOLContextAgent().retrieve(kol_id)["crm_context"]
    for record in load_records():
        if record["kol_id"] == kol_id:
            assert record["crm_profile"]["crm_record_id"] in context
            assert all(item["task_id"] in context for item in record["tasks"])
            assert all(item["request_id"] in context for item in record["medical_requests"])
        else:
            assert record["display_name"] not in context
            assert record["crm_profile"]["crm_record_id"] not in context
            assert all(item["request_id"] not in context for item in record["medical_requests"])
            assert all(item["task_id"] not in context for item in record["tasks"])


@pytest.mark.parametrize("corruption", ["foreign_kol", "missing_task", "missing_engagement", "duplicate_id", "missing_closure"])
def test_invalid_crm_relationships_and_unsubstantiated_completion_are_rejected(corruption):
    records = copy.deepcopy(load_records())
    record = records[0]
    if corruption == "foreign_kol":
        record["medical_requests"][0]["kol_id"] = records[1]["kol_id"]
    elif corruption == "missing_task":
        record["medical_requests"][0]["task_id"] = "TASK-NOT-PRESENT"
    elif corruption == "missing_engagement":
        record["tasks"][0]["engagement_id"] = "ENG-NOT-PRESENT"
    elif corruption == "duplicate_id":
        record["tasks"][1]["task_id"] = record["tasks"][0]["task_id"]
    else:
        record["tasks"][2]["closure_note"] = None
    with pytest.raises(ValueError):
        validate_crm_records(records)


def test_overdue_uses_fixed_snapshot_and_excludes_due_today_and_completed():
    record = copy.deepcopy(load_records()[0])
    record["tasks"][0]["due_date"] = record["crm_profile"]["snapshot_date"]
    rows = task_rows(record)
    assert rows[0]["Overdue"] is False
    assert rows[1]["Overdue"] is True
    assert rows[2]["Overdue"] is False
    assert rows[2]["Status"] == "Completed"


@pytest.mark.parametrize("index", [0, 1, 2])
def test_demo_scenario_inputs_run_for_each_kol_without_creating_scientific_evidence(index):
    scenarios = json.loads((ROOT / "test_scenarios/fixtures/scenario_inputs.json").read_text())["scenarios"]
    case = scenarios[index]
    result = run_workflow(case["kol_id"], case["scientific_sources"], case["meeting_notes"])
    assert result["record"]["kol_id"] == case["kol_id"]
    assert case["scientific_sources"] in result["briefing"]
    assert case["meeting_notes"] in result["follow_up_draft"]
    assert "Owner and due date: Not assigned" in result["follow_up_draft"]
    empty = run_workflow(case["kol_id"])
    assert "abstains" in empty["briefing"]


def test_crm_csv_exports_match_the_runtime_fixture():
    records = load_records()
    expected = {"profiles.csv": {r["kol_id"] for r in records}}
    for name, field, identifier in [("interactions.csv", "interactions", "engagement_id"),
                                    ("tasks.csv", "tasks", "task_id"),
                                    ("medical_requests.csv", "medical_requests", "request_id")]:
        expected[name] = {item[identifier] for r in records for item in r[field]}
    for name, identifiers in expected.items():
        with (ROOT / "data/synthetic_crm" / name).open(encoding="utf-8-sig", newline="") as source:
            rows = list(csv.DictReader(source))
        key = {"profiles.csv": "kol_id", "interactions.csv": "engagement_id",
               "tasks.csv": "task_id", "medical_requests.csv": "request_id"}[name]
        assert len(rows) == len(identifiers)
        assert {row[key] for row in rows} == identifiers


def test_crm_tabs_metrics_and_tables_switch_to_the_selected_kol_only():
    app = AppTest.from_file(str(ROOT / "app.py")).run()
    for index, record in enumerate(load_records()):
        app.selectbox[0].select_index(index).run()
        assert not app.exception
        assert {"CRM profile", "Interaction timeline", "Follow-up tasks", "Medical requests"}.issubset({tab.label for tab in app.tabs})
        assert {metric.label: metric.value for metric in app.metric} == {
            "Interactions": "3", "Active tasks": "2", "Overdue tasks": "1"}
        assert set(app.dataframe[0].value["Task ID"]) == {task["task_id"] for task in record["tasks"]}
        assert set(app.dataframe[1].value["Request ID"]) == {request["request_id"] for request in record["medical_requests"]}
        assert record["crm_profile"]["crm_record_id"] in "\n".join(x.value for x in app.markdown)


def test_profile_cards_keep_selected_record_fields_and_escape_markup():
    import copy
    from unittest.mock import patch
    from ui import crm_profile_details
    from presentation import display_crm
    record = display_crm(copy.deepcopy(load_records()[0]))
    record["crm_profile"]["territory"] = "<script>unsafe</script>"
    with patch("ui.st.markdown") as render:
        crm_profile_details(record)
    markup = render.call_args.args[0]
    assert markup.count('class="crm-detail-card"') == 4
    assert record["kol_id"] in markup
    assert record["crm_profile"]["crm_record_id"] in markup
    assert record["planned_meeting"]["date"] in markup
    assert all(topic in markup for topic in record["crm_profile"]["scientific_interests"])
    assert "&lt;script&gt;unsafe&lt;/script&gt;" in markup
    assert "<script>" not in markup


def test_task_and_request_cards_preserve_ids_statuses_and_escape_content():
    import copy
    from unittest.mock import patch
    from crm_views import render_task_cards, render_request_cards
    from presentation import display_crm
    record = display_crm(copy.deepcopy(load_records()[0]))
    record["medical_requests"][0]["question"] = "<script>untrusted</script>"
    with patch("crm_views.st.markdown") as render:
        render_task_cards(record)
        tasks = render.call_args.args[0]
        render_request_cards(record)
        requests = render.call_args.args[0]
    assert tasks.count('class="crm-work-card"') == 3
    assert requests.count('class="crm-work-card"') == 2
    assert all(task["task_id"] in tasks for task in record["tasks"])
    assert all(request["request_id"] in requests for request in record["medical_requests"])
    assert 'Overdue' in tasks and 'Completed' in tasks
    assert '&lt;script&gt;untrusted&lt;/script&gt;' in requests
    assert '<script>' not in requests
