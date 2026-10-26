"""Streamlit interface for the synthetic MSL repeat-meeting prototype."""

from __future__ import annotations

import os
import streamlit as st
from mira_views import render_mira_research
from llm import DEFAULT_MODEL

from crm_views import render_task_cards, render_request_cards
from crm import crm_summary, task_rows
from workflow import load_records
from presentation import display_crm, display_id
from ui import apply_theme, hero, section_label, profile_card, crm_profile_details
from filter_views import FILTER_KEYS
from walkthrough import DEMO_NOTES


st.set_page_config(page_title="Medical Engagement Workbench", page_icon="M", layout="wide")
apply_theme()
hero()
public_demo = os.environ.get("MSL_PUBLIC_DEMO") == "1"
st.info("Illustrative engagement history. Review all drafts and sources; do not enter patient or real HCP information.")


def load_walkthrough():
    st.session_state["drafting_mode"] = "OpenAI LLM"
    st.session_state["selected_kol"] = load_records()[0]
    st.session_state["walkthrough_seed_pending"] = True
    for key in ("workflow_result", "mira_evidence", "mira_preparation", "mira_actions"):
        st.session_state.pop(key, None)


drafting_mode = st.radio("Drafting mode", ["Offline", "OpenAI LLM"], key="drafting_mode", horizontal=True)
use_llm = drafting_mode == "OpenAI LLM"
api_key = ""
model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
if use_llm:
    with st.expander("OpenAI settings", expanded=False):
        st.caption("Research planning sends the selected KOL history and question to OpenAI. Preparing sends selected sources and MSL notes. API usage may incur charges.")
        api_key = st.text_input("OpenAI API key", type="password", key="openai_api_key",
                                help="Used for this session only. Never paste keys into chat or project files.",
                                placeholder="Enter your API key for this session")
        if not public_demo and os.environ.get("OPENAI_API_KEY"):
            st.caption("A server-side OpenAI API key is available.")
        if public_demo:
            st.caption("Use your own API key for this session. No shared API credit is provided.")
        model = st.text_input("OpenAI model", value=model, key="openai_model")
        st.caption("Model drafts can be wrong. Supporting quotes and source IDs help the MSL review them.")
runtime_signature = (drafting_mode, model)
if st.session_state.get("runtime_signature") != runtime_signature:
    for key in list(st.session_state):
        if key.startswith("mira_") and key not in ("mira_question",):
            st.session_state.pop(key, None)
    st.session_state["runtime_signature"] = runtime_signature

records = load_records()

with st.expander("Guided preparation - Dr Mira Sen"):
    st.write("Follow Mira's previous question through journal evidence, trial evidence and a reviewed discussion plan.")
    st.button("Load Dr Mira Sen case", key="load_walkthrough", on_click=load_walkthrough)
    st.caption("Loads the KOL and an example MSL note. It does not make model calls or send searches.")
    st.markdown("**1. Plan:** connect in OpenAI mode and build the research plan. **2. Search:** review filters and search both public sources. **3. Prepare:** select records and review the discussion drafts. **4. Choose:** download a summary, email draft or meeting proposal.")

selected = st.selectbox(
    "Select a KOL",
    options=records,
    key="selected_kol",
    format_func=lambda record: record['display_name'],
)

st.caption("Changing the KOL clears the current notes, evidence search and preparation.")

# Switching identities starts a fresh meeting workspace.
if st.session_state.get("active_kol_id") != selected["kol_id"]:
    for key in list(st.session_state):
        if key.startswith("mira_"):
            st.session_state.pop(key, None)
    for state_key in (
        "msl_notes", "mira_evidence", "mira_preparation", "mira_actions",
    ):
        st.session_state.pop(state_key, None)
    for key in FILTER_KEYS + ["mira_query_signature", "mira_filter_signature"]:
        st.session_state.pop(key, None)
    st.session_state["active_kol_id"] = selected["kol_id"]

if st.session_state.pop("walkthrough_seed_pending", False):
    st.session_state.pop("msl_notes", None)

context_page, evidence_page, notes_page = st.tabs(["01  KOL context", "02  Guided research", "03  MSL notes"])
display_record = display_crm(selected)

with notes_page:
    section_label("03", "MSL notes", "Capture the questions or context you want to carry into guided research")
    default_notes = DEMO_NOTES if selected["kol_id"] == "KOL-DEMO-001" else ""
    msl_notes = st.text_area(
        "Notes for the next scientific discussion",
        value=default_notes,
        key="msl_notes",
        height=260,
        placeholder="Add comments or notes for this KOL. Avoid patient details or real HCP information.",
    )
    st.caption("Notes stay in this browser session. Guided research can use them when preparing the discussion; they are not saved to CRM.")
    st.caption(f"{len(msl_notes)} characters")

with context_page:
    section_label("01", "KOL context", "Continuity before the next conversation")
    profile_card(display_record)
    profile = display_record["crm_profile"]
    st.caption(f"CRM snapshot: {profile['snapshot_date']} | CRM history is not scientific evidence")
    summary = crm_summary(display_record)
    cards = st.columns(4)
    cards[0].metric("Interactions", summary["interactions"])
    cards[1].metric("MSL replies", sum(bool(item.get("msl_response")) for item in display_record["interactions"]))
    cards[2].metric("Active tasks", summary["active_tasks"])
    cards[3].metric("Overdue tasks", summary["overdue_tasks"])
    profile_tab, history_tab, tasks_tab, requests_tab = st.tabs(
        ["CRM profile", "Interaction timeline", "Follow-up tasks", "Medical requests"]
    )
    with profile_tab:
        crm_profile_details(display_record)
    with history_tab:
        st.caption("Each interaction pairs the KOL question with the MSL response, supporting sources and follow-up status.")
        for interaction in sorted(display_record["interactions"], key=lambda row: row["date"], reverse=True):
            with st.expander(f"{interaction['date']} | {interaction['channel']}"):
                st.markdown(f"**Purpose:** {interaction['purpose']}")
                st.markdown(f"**KOL asked**\n\n{interaction['observation']}")
                st.markdown(f"**MSL response**\n\n{interaction['msl_response']}")
                st.caption("Response status: " + interaction["response_status"])
                if interaction.get("response_sources"):
                    st.markdown("**Sources discussed**")
                    for source in interaction["response_sources"]:
                        st.markdown(f"- [{source['label']}]({source['url']})")
                st.markdown(f"**Agreed follow-up:** {interaction['task']}  \n"
                            f"**Owner:** {interaction['owner_role']} | **Status:** {interaction['status']} | "
                            f"**Due:** {interaction['due_date']}")
                st.caption(f"Interaction reference: {interaction['engagement_id']}")
    with tasks_tab:
        st.caption(f"Read-only tasks. Overdue is calculated as of {profile['snapshot_date']}, not the current date. Completed entries reflect recorded history; this app does not complete tasks.")
        render_task_cards(display_record)
        with st.expander("View complete task register"):
            st.dataframe([{**row, "Task ID": display_id(row["Task ID"])}
                          for row in task_rows(display_record)], hide_index=True, width="stretch")
    with requests_tab:
        st.caption("Each request is linked to the MSL response and source references; remaining review is shown by status.")
        render_request_cards(display_record)
        with st.expander("View complete request register"):
            st.dataframe([
                {"Request ID": display_id(request["request_id"]), "Received": request["received_on"],
                 "Question": request["question"], "Status": request["status"],
                 "Owner": request["owner_role"], "Linked task": display_id(request["task_id"]),
                 "Response": request["response_status"], "Sources": request["source_pack_status"]}
                for request in display_record["medical_requests"]
            ], hide_index=True, width="stretch")


with evidence_page:
    section_label("02", "Guided research", "One flow connects KOL context, publications, clinical trials and discussion preparation.")
    render_mira_research(selected, use_llm, api_key, model)

st.divider()
st.caption(
    "The guided flow uses three bounded agents. Public-source searches are explicit and read-only. "
    "MSL notes remain in the session; email and meeting outputs are drafts only."
)
