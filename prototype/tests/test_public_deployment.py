"""Public hosting must not expose shared credits or server-side run files."""
from unittest.mock import Mock

import pytest

from llm import LLMError, OpenAILLM
from test_app import start_app


def test_public_runtime_requires_visitor_key_even_if_server_key_exists(monkeypatch):
    monkeypatch.setenv("MSL_PUBLIC_DEMO", "1")
    monkeypatch.setenv("OPENAI_API_KEY", "SERVER-SECRET")
    with pytest.raises(LLMError, match="Add an OpenAI API key"):
        OpenAILLM()
    assert OpenAILLM(api_key="VISITOR-KEY")._api_key == "VISITOR-KEY"


def test_public_ui_downloads_without_server_save_and_isolates_sessions(monkeypatch):
    import walkthrough
    import workflow
    from test_llm import FakeLLM
    monkeypatch.setattr(workflow, "OpenAILLM", Mock(return_value=FakeLLM()))
    monkeypatch.setenv("MSL_PUBLIC_DEMO", "1")
    saver = Mock(side_effect=AssertionError("Public report must not be saved"))
    monkeypatch.setattr(walkthrough, "save_report", saver)
    first, _, _ = start_app(monkeypatch)
    first.button(key="load_walkthrough").click().run()
    first.text_input(key="openai_api_key").input("VISITOR-ONE-KEY")
    first.text_area(key="scientific_source_text").input("Synthetic source for mechanics only.")
    first.text_area(key="meeting_notes").input("Fictional session one notes")
    first.button(key="prepare_drafts").click().run()
    assert not first.exception
    assert "save_walkthrough" not in [button.key for button in first.button]
    assert len(first.get("download_button")) == 1
    first.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    first.text_input(key="openai_api_key").input("VISITOR-ONE-KEY").run()
    second, _, _ = start_app(monkeypatch)
    second.radio(key="drafting_mode").set_value("OpenAI LLM").run()
    assert second.text_input(key="openai_api_key").value == ""
    assert second.text_area(key="meeting_notes").value == ""
    assert "workflow_result" not in second.session_state
    saver.assert_not_called()
