import copy
import json

from presentation import display_crm
from workflow import load_records, run_workflow
from test_app import start_app


def test_crm_presentation_preserves_provenance_identifiers_and_original_records():
    record = load_records()[0]
    before = copy.deepcopy(record)
    view = display_crm(record)
    assert view["institution"] == "Harborview Cancer Institute"
    assert view["crm_profile"]["city"] == "Kolkata"
    assert view["crm_profile"]["territory"] == "East territory"
    assert view["kol_id"] == record["kol_id"]
    assert view["crm_profile"]["provenance"] == record["crm_profile"]["provenance"]
    assert view["interactions"][0]["source_reference"] == record["interactions"][0]["source_reference"]
    assert record == before
    assert view is not record
    assert all("for the demo" not in task["title"] for task in view["tasks"])


def test_copy_cleanup_never_rewrites_user_notes_or_scientific_sources():
    source = "An article discusses fictional cases and synthetic biology. Demo is an exact quoted word."
    notes = "Original notes: fictional and demo are stakeholder words."
    result = run_workflow("KOL-DEMO-001", source, notes)
    assert source in result["briefing"]
    assert notes in result["follow_up_draft"]
    assert result["record"]["institution"].endswith("(fictional)")


def test_visible_labels_are_neutral_with_one_data_disclosure(monkeypatch):
    app, pubmed, trials = start_app(monkeypatch)
    assert app.selectbox(key="selected_kol").label == "Select a KOL"
    assert app.text_area(key="meeting_notes").label == "Meeting notes"
    assert any("Illustrative engagement history" in info.value for info in app.info)
    labels = [element.label for elements in (app.selectbox, app.text_area, app.expander) for element in elements]
    assert not any("fictional" in label.lower() or "demo" in label.lower() for label in labels)
    pubmed.assert_not_called()
    trials.assert_not_called()
