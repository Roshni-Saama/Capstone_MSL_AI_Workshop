"""Streamlit interface for the synthetic MSL repeat-meeting prototype."""

from __future__ import annotations

import os
import json

import streamlit as st
from llm import DEFAULT_MODEL, LLMError, OpenAILLM
from search_result_views import render_pubmed_result, render_trial_result

from agents import ScientificSourceAgent
from clinical_trials import ClinicalTrialsError
from pubmed import PubMedError
from crm import crm_summary, task_rows
from workflow import load_records, run_workflow
from ui import apply_theme, hero, section_label, profile_card, render_draft
from walkthrough import DEMO_QUERY, DEMO_NOTES, build_report, save_report


st.set_page_config(page_title="Medical Engagement Workbench", page_icon="M", layout="wide")
apply_theme()
hero()
public_demo = os.environ.get("MSL_PUBLIC_DEMO") == "1"
st.info("Fictional workshop data. Review all drafts and sources; do not enter patient or real HCP information.")


def load_walkthrough():
    st.session_state["drafting_mode"] = "OpenAI LLM"
    st.session_state["selected_kol"] = load_records()[0]
    st.session_state["walkthrough_seed_pending"] = True
    st.session_state.pop("workflow_result", None)


with st.sidebar:
    st.markdown("### Medical Engagement\nYour scientific workspace")
    st.divider()
    st.header("Drafting mode")
    drafting_mode = st.radio("Choose mode", ["Offline", "OpenAI LLM"], key="drafting_mode")
    use_llm = drafting_mode == "OpenAI LLM"
    api_key = ""
    model = os.environ.get("OPENAI_MODEL", DEFAULT_MODEL)
    if use_llm:
        st.caption("Searching in OpenAI mode sends retrieved public records to OpenAI for short summaries. Preparing drafts sends the selected fictional KOL context, selected sources, and fictional notes. API usage may incur charges.")
        api_key = st.text_input("OpenAI API key", type="password", key="openai_api_key",
                                help="Used for this session only. Never paste keys into chat or project files.")
        if not public_demo and os.environ.get("OPENAI_API_KEY"):
            st.caption("A server-side OpenAI API key is available.")
        if public_demo:
            st.caption("Public demo: use your own API key for this session. No shared API credit is provided.")
        model = st.text_input("OpenAI model", value=model, key="openai_model")
        st.caption("Model drafts can be wrong. Supporting quotes and source IDs help the MSL review them.")
    runtime_signature = (drafting_mode, model)
    if st.session_state.get("runtime_signature") != runtime_signature:
        st.session_state.pop("workflow_result", None)
        for summary_key in ("pubmed_summaries", "pubmed_summary_error", "trial_summaries", "trial_summary_error"):
            st.session_state.pop(summary_key, None)
        st.session_state["runtime_signature"] = runtime_signature

records = load_records()
source_agent = ScientificSourceAgent()


def populate_search_summaries(prefix, results, kind):
    if not results:
        return
    try:
        runtime = OpenAILLM(api_key=api_key or None, model=model) if use_llm else None
        with st.spinner("Summarizing search results..."):
            st.session_state[prefix + "_summaries"] = source_agent.summarize_search_results(results, kind, llm=runtime)
    except LLMError as error:
        st.session_state[prefix + "_summary_error"] = "AI summaries unavailable. " + str(error) + " Showing the compact offline preview instead."

with st.expander("Live OpenAI walkthrough - Dr Mira Sen"):
    st.write("Start with fictional CRM context, find a public scientific source, then review the three agent drafts.")
    st.button("Load Dr Mira Sen walkthrough", key="load_walkthrough", on_click=load_walkthrough)
    st.caption("Loads the KOL, a scientific query and fictional notes. It does not make model calls or send searches.")
    st.markdown("**1. Connect:** enter your key in the sidebar. **2. Find evidence:** Search PubMed, inspect a summary and select an article. **3. Prepare:** review the notes and prepare the drafts. **4. Record:** review agent details and save the run evidence.")

selected = st.selectbox(
    "Select a fictional KOL",
    options=records,
    key="selected_kol",
    format_func=lambda record: f"{record['display_name']} Â· {record['kol_id']}",
)

st.caption("Changing the KOL clears the current notes, source selections, searches, and drafts.")

# Switching identities starts a fresh meeting workspace.
if st.session_state.get("active_kol_id") != selected["kol_id"]:
    for state_key in (
        "workflow_result", "pubmed_results", "pubmed_error", "pubmed_query_submitted",
        "trial_results", "trial_error", "trial_query_submitted", "pubmed_query",
        "trial_query", "selected_pmids", "selected_nct_ids", "scientific_source_text",
        "meeting_notes", "pubmed_summaries", "pubmed_summary_error", "trial_summaries", "trial_summary_error",
    ):
        st.session_state.pop(state_key, None)
    st.session_state["active_kol_id"] = selected["kol_id"]

if st.session_state.pop("walkthrough_seed_pending", False):
    st.session_state["pubmed_query"] = DEMO_QUERY
    st.session_state["meeting_notes"] = DEMO_NOTES
    st.session_state["scientific_source_text"] = ""

left, right = st.columns([0.95, 1.15], gap="large")
with left:
    section_label("01", "KOL context", "Continuity before the next conversation")
    profile_card(selected)
    profile = selected["crm_profile"]
    st.caption(f"Fully fictional CRM data | Snapshot: {profile['snapshot_date']} | CRM history is not scientific evidence")
    summary = crm_summary(selected)
    cards = st.columns(3)
    cards[0].metric("Interactions", summary["interactions"])
    cards[1].metric("Active tasks", summary["active_tasks"])
    cards[2].metric("Overdue tasks", summary["overdue_tasks"])
    profile_tab, history_tab, tasks_tab, requests_tab = st.tabs(
        ["CRM profile", "Interaction timeline", "Follow-up tasks", "Medical requests"]
    )
    with profile_tab:
        st.markdown(f"**CRM record:** {profile['crm_record_id']}  \n"
                    f"**KOL ID:** {selected['kol_id']}  \n"
                    f"**Organization ID:** {selected['organization_id']}  \n"
                    f"**Territory:** {profile['territory']}  \n"
                    f"**Location:** {profile['city']}, {profile['country']}  \n"
                    f"**Assigned role:** {profile['assigned_msl_role']}  \n"
                    f"**Relationship:** {profile['relationship_stage']}  \n"
                    f"**Preferred channel:** {profile['preferred_channel']}  \n"
                    f"**Profile reviewed:** {profile['profile_reviewed_on']}")
        st.markdown("**Scientific interests (topics only):**")
        for interest in profile["scientific_interests"]:
            st.write(interest)
        st.markdown(f"**Planned meeting:** {selected['planned_meeting']['date']}")
        st.write(selected["planned_meeting"]["purpose"])
    with history_tab:
        st.caption("Past interactions are fictional historical snapshots; the task tab shows latest fixture status.")
        for interaction in sorted(selected["interactions"], key=lambda row: row["date"], reverse=True):
            with st.expander(f"{interaction['date']} | {interaction['engagement_id']} | {interaction['channel']}"):
                st.markdown(f"**Purpose:** {interaction['purpose']}")
                st.markdown(f"**Synthetic observation:** {interaction['observation']}")
                st.markdown(f"**Draft MSL interpretation:** {interaction['msl_interpretation']}")
                st.markdown(f"**Follow-up at this interaction:** {interaction['task']}  \n"
                            f"**Owner:** {interaction['owner_role']} | **Status:** {interaction['status']} | "
                            f"**Due:** {interaction['due_date']}")
                st.caption(f"Fixture reference: {interaction['source_reference']}")
    with tasks_tab:
        st.caption(f"Read-only synthetic tasks. Overdue is calculated as of {profile['snapshot_date']}, not the current date. Completed entries are fictional history, not actions performed by this app.")
        st.dataframe(task_rows(selected), hide_index=True, width="stretch")
    with requests_tab:
        st.caption("Fictional evidence requests; no scientific response is implied and no requests are sent.")
        st.dataframe([
            {"Request ID": request["request_id"], "Received": request["received_on"],
             "Question": request["question"], "Status": request["status"],
             "Owner": request["owner_role"], "Linked task": request["task_id"],
             "Response": request["response_status"], "Sources": request["source_pack_status"]}
            for request in selected["medical_requests"]
        ], hide_index=True, width="stretch")

with right:
    section_label("02", "Scientific evidence", "Find relevant sources. Keep their limitations in view.")
    st.markdown("### PubMed literature")
    st.caption(
        "Search NCBI PubMed by scientific topic. Do not enter patient details, "
        "identifiable information, or confidential CRM content."
    )
    pubmed_query = st.text_input(
        "Search terms",
        placeholder='Example: oncology trial population older adults',
        max_chars=300,
        key="pubmed_query",
    )
    search_clicked = st.button("Search PubMed", key="search_pubmed", width="stretch")
    if search_clicked:
        for state_key in ("pubmed_summaries", "pubmed_summary_error", "selected_pmids"):
            st.session_state.pop(state_key, None)
        st.session_state["pubmed_query_submitted"] = True
        if not pubmed_query.strip():
            st.session_state["pubmed_error"] = "Enter search terms before searching."
            st.session_state["pubmed_results"] = []
        else:
            try:
                st.session_state["pubmed_results"] = source_agent.search_pubmed(pubmed_query, retmax=5)
                st.session_state.pop("pubmed_error", None)
                populate_search_summaries("pubmed", st.session_state["pubmed_results"], "pubmed")
            except (PubMedError, ValueError) as error:
                st.session_state["pubmed_results"] = []
                st.session_state["pubmed_error"] = str(error)

    if st.session_state.get("pubmed_error"):
        st.error(st.session_state["pubmed_error"])

    if st.session_state.get("pubmed_summary_error"):
        st.warning(st.session_state["pubmed_summary_error"])

    pubmed_results = st.session_state.get("pubmed_results", [])
    selected_pmids: list[str] = []
    if pubmed_results:
        result_by_pmid = {article["pmid"]: article for article in pubmed_results}
        selected_pmids = st.multiselect(
            "Select articles to include as source text",
            options=list(result_by_pmid),
            key="selected_pmids",
            format_func=lambda pmid: (
                f"{result_by_pmid[pmid]['year'] or 'Year n/a'} Â· "
                f"{result_by_pmid[pmid]['title']} Â· PMID {pmid}"
            ),
        )
        for article in pubmed_results:
            render_pubmed_result(article, st.session_state.get("pubmed_summaries", {}).get(article["pmid"]))
    elif st.session_state.get("pubmed_query_submitted") and not st.session_state.get("pubmed_error"):
        st.info("No PubMed results found for that search.")

    st.divider()
    st.markdown("### Clinical trial registry")
    st.caption(
        "Search public registry records by condition/topic. Registry records are "
        "not proof of study quality, results, or current operational status."
    )
    trial_query = st.text_input(
        "Condition or study topic",
        placeholder="Example: chronic lymphocytic leukemia",
        max_chars=250,
        key="trial_query",
    )
    trial_search_clicked = st.button("Search ClinicalTrials.gov", key="search_trials", width="stretch")
    if trial_search_clicked:
        for state_key in ("trial_summaries", "trial_summary_error", "selected_nct_ids"):
            st.session_state.pop(state_key, None)
        st.session_state["trial_query_submitted"] = True
        if not trial_query.strip():
            st.session_state["trial_error"] = "Enter a condition or topic before searching trials."
            st.session_state["trial_results"] = []
        else:
            try:
                st.session_state["trial_results"] = source_agent.search_trials(trial_query, page_size=5)
                st.session_state.pop("trial_error", None)
                populate_search_summaries("trial", st.session_state["trial_results"], "trials")
            except (ClinicalTrialsError, ValueError) as error:
                st.session_state["trial_results"] = []
                st.session_state["trial_error"] = str(error)

    if st.session_state.get("trial_error"):
        st.error(st.session_state["trial_error"])

    if st.session_state.get("trial_summary_error"):
        st.warning(st.session_state["trial_summary_error"])

    trial_results = st.session_state.get("trial_results", [])
    selected_nct_ids: list[str] = []
    if trial_results:
        trial_by_nct_id = {trial["nct_id"]: trial for trial in trial_results}
        selected_nct_ids = st.multiselect(
            "Select registry records for this meeting",
            options=list(trial_by_nct_id),
            key="selected_nct_ids",
            format_func=lambda nct_id: (
                f"{trial_by_nct_id[nct_id]['status']} Â· "
                f"{trial_by_nct_id[nct_id]['title']} Â· {nct_id}"
            ),
        )
        for trial in trial_results:
            render_trial_result(trial, source_agent, st.session_state.get("trial_summaries", {}).get(trial["nct_id"]))
    elif st.session_state.get("trial_query_submitted") and not st.session_state.get("trial_error"):
        st.info("No ClinicalTrials.gov records found for that search.")

    st.divider()
    section_label("03", "Meeting notes & follow-up", "Turn a scientific conversation into a reviewable draft")
    scientific_source_text = st.text_area(
        "Optional source text from approved materials",
        key="scientific_source_text",
        height=130,
        placeholder="Paste permitted text for local source preservation. OpenAI mode sends this text to OpenAI.",
    )
    meeting_notes = st.text_area(
        "New fictional meeting notes",
        key="meeting_notes",
        height=130,
        placeholder="Enter synthetic demo notes only. Do not enter patient details or real HCP information.",
    )
    generate = st.button("Prepare selected sources and notes", key="prepare_drafts", type="primary", width="stretch")

if generate:
    selected_articles = [
        article
        for article in st.session_state.get("pubmed_results", [])
        if article["pmid"] in selected_pmids
    ]
    selected_pubmed_text = source_agent.format_pubmed_sources(selected_articles)
    selected_trials = [
        trial
        for trial in st.session_state.get("trial_results", [])
        if trial["nct_id"] in selected_nct_ids
    ]
    selected_trial_text = source_agent.format_trial_sources(selected_trials)
    source_parts = [
        part
        for part in (selected_pubmed_text, selected_trial_text, scientific_source_text.strip())
        if part
    ]
    st.session_state.pop("workflow_result", None)
    try:
        with st.spinner("Preparing review drafts..."):
            result = run_workflow(
                kol_id=selected["kol_id"],
                scientific_sources="\n\n---\n\n".join(source_parts),
                meeting_notes=meeting_notes,
                use_llm=use_llm, api_key=api_key or None, model=model,
            )
        st.session_state["workflow_result"] = result
    except LLMError as error:
        st.error(str(error))

result = st.session_state.get("workflow_result")
if result and result.get("kol_id") == selected["kol_id"]:
    st.divider()
    section_label("04", "Your review workspace", "Verify the source support and refine the next action")
    if result.get("context_draft"):
        st.subheader("Draft meeting priorities")
        with st.container(border=True):
            render_draft(result["context_draft"])
    st.subheader("Draft briefing")
    st.caption(f"Mode: {result.get('generation_mode', 'Code-only')} Â· Requires MSL review")
    with st.container(border=True):
        render_draft(result.get("briefing", "No briefing available."))
    st.subheader("Draft note and follow-up")
    st.caption("Requires MSL review. This prototype does not create CRM records or send messages.")
    with st.container(border=True):
        render_draft(result.get("follow_up_draft", "No new notes were submitted."))
    if result.get("agent_trace"):
        with st.expander("Agent run details"):
            st.table(result["agent_trace"])
        if len(result["agent_trace"]) == 3:
            st.success("All three agent steps completed. Review the drafts before recording your findings.")
        report = build_report(result)
        st.download_button("Download walkthrough record", json.dumps(report, indent=2),
                           file_name="openai_walkthrough.json", mime="application/json", key="download_walkthrough")
        if not public_demo and st.button("Save walkthrough record locally", key="save_walkthrough"):
            try:
                saved_path = save_report(result)
                st.success(f"Saved run evidence to {saved_path}")
            except OSError:
                st.error("The run record could not be saved locally. Use Download walkthrough record instead.")
        st.caption("The record includes model drafts and agent status, not your API key. Saved results still need human review.")

st.divider()
st.caption(
    "LangGraph coordinates three bounded agents. OpenAI drafting runs only in OpenAI LLM mode "
    "when you prepare a draft or search for source summaries. Registry searches are explicit read-only requests. "
    "There are no CRM writes, external messages, or safety submissions."
)