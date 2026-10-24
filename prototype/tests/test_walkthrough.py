import json
from unittest.mock import Mock

from test_app import start_app
from walkthrough import DEMO_QUERY, DEMO_NOTES, build_report, save_report


def test_load_walkthrough_selects_mira_and_seeds_inputs_without_network(monkeypatch):
    import workflow
    model = Mock(side_effect=AssertionError("Unexpected model call"))
    monkeypatch.setattr(workflow, "OpenAILLM", model)
    app, pubmed, trials = start_app(monkeypatch)
    app.selectbox[0].select_index(1).run()
    app.text_area(key="meeting_notes").input("Prior KOL notes.")
    app.button(key="load_walkthrough").click().run()
    assert not app.exception
    assert app.selectbox[0].value["kol_id"] == "KOL-DEMO-001"
    assert app.radio(key="drafting_mode").value == "OpenAI LLM"
    assert app.text_input(key="pubmed_query").value == DEMO_QUERY
    assert app.text_area(key="meeting_notes").value == DEMO_NOTES
    assert app.text_area(key="scientific_source_text").value == ""
    assert "workflow_result" not in app.session_state
    pubmed.assert_not_called()
    trials.assert_not_called()
    model.assert_not_called()


def test_walkthrough_report_excludes_credential_fields_and_marks_review_pending():
    result = {"kol_id": "KOL-DEMO-001", "generation_mode": "OpenAI LLM: test-model",
              "briefing": "Source-linked draft.", "follow_up_draft": "Fictional notes.",
              "agent_trace": [{"agent": name, "model": "test-model", "status": "Mock only"}
                              for name in ["KOL Context Agent", "Scientific Source Agent", "Follow-up Agent"]],
              "api_key": "SECRET-KEY", "session_state": {"openai_api_key": "SECRET-KEY"}}
    report = build_report(result)
    assert report["all_three_agents_completed"] is True
    assert "human review" in report["review_status"]
    assert "SECRET-KEY" not in json.dumps(report)
    assert "api_key" not in json.dumps(report)
    assert report["recorded_at"].endswith("+05:30")


def test_explicit_save_writes_the_requested_evidence_path(tmp_path):
    destination = tmp_path / "results" / "walkthrough.json"
    result = {"kol_id": "KOL-DEMO-001", "generation_mode": "Offline", "briefing": "Draft"}
    saved = save_report(result, destination)
    report = json.loads(saved.read_text())
    assert saved == destination
    assert report["mode"] == "Offline workflow"
    assert report["all_three_agents_completed"] is False


def test_save_control_receives_result_without_sidebar_key(monkeypatch, tmp_path):
    import workflow
    import walkthrough
    from test_llm import FakeLLM
    monkeypatch.setattr(workflow, "OpenAILLM", Mock(return_value=FakeLLM()))
    saver = Mock(return_value=tmp_path / "run.json")
    monkeypatch.setattr(walkthrough, "save_report", saver)
    app, _, _ = start_app(monkeypatch)
    app.button(key="load_walkthrough").click().run()
    app.text_input(key="openai_api_key").input("TEST-KEY-NOT-FOR-REPORT")
    app.text_area(key="scientific_source_text").input("Synthetic source for mechanics only.")
    app.button(key="prepare_drafts").click().run()
    assert not app.exception
    app.button(key="save_walkthrough").click().run()
    assert not app.exception
    saver.assert_called_once()
    assert "TEST-KEY-NOT-FOR-REPORT" not in json.dumps(saver.call_args.args[0])
