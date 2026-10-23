"""Streamlit interface for the synthetic MSL repeat-meeting prototype."""

from __future__ import annotations

import streamlit as st

from agents import ScientificSourceAgent
from clinical_trials import ClinicalTrialsError
from pubmed import PubMedError
from workflow import load_records, run_workflow


st.set_page_config(page_title="Medical Engagement Workbench", page_icon="M", layout="wide")
st.title("Medical Engagement Workbench")
st.caption("Repeat-meeting preparation and follow-up | Local-only prototype")
st.warning(
    "Fictional demo data only. Draft support tool, not clinical advice or a live CRM. "
    "Verify all content; do not enter patient-identifiable or real HCP information."
)

records = load_records()
source_agent = ScientificSourceAgent()
selected = st.selectbox(
    "Select a fictional KOL",
    records,
    format_func=lambda record: f"{record['display_name']} · {record['kol_id']}",
)

left, right = st.columns([1, 1])
with left:
    st.subheader("Prior interaction context")
    st.markdown(f"**{selected['display_name']}** · {selected['role']}")
    st.caption(f"{selected['institution']} · {selected['therapy_area']}")
    st.markdown(f"**Planned meeting:** {selected['planned_meeting']['date']}")
    st.write(selected["planned_meeting"]["purpose"])
    for interaction in selected["interactions"]:
        with st.expander(f"{interaction['date']} · {interaction['engagement_id']}"):
            st.markdown(f"**Purpose:** {interaction['purpose']}")
            st.markdown(f"**Synthetic observation:** {interaction['observation']}")
            st.markdown(f"**Draft MSL interpretation:** {interaction['msl_interpretation']}")
            st.markdown(
                f"**Follow-up:** {interaction['task']}  \n"
                f"**Owner:** {interaction['owner_role']} · **Status:** {interaction['status']} · "
                f"**Due:** {interaction['due_date']}"
            )

with right:
    st.subheader("Preparation and follow-up")
    st.markdown("**PubMed literature search**")
    st.caption(
        "Search NCBI PubMed by scientific topic. Do not enter patient details, "
        "identifiable information, or confidential CRM content."
    )
    pubmed_query = st.text_input(
        "Search terms",
        placeholder='Example: oncology trial population older adults',
        max_chars=300,
    )
    search_clicked = st.button("Search PubMed", use_container_width=True)
    if search_clicked:
        st.session_state["pubmed_query_submitted"] = True
        if not pubmed_query.strip():
            st.session_state["pubmed_error"] = "Enter search terms before searching."
            st.session_state["pubmed_results"] = []
        else:
            try:
                st.session_state["pubmed_results"] = source_agent.search_pubmed(pubmed_query, retmax=5)
                st.session_state.pop("pubmed_error", None)
            except (PubMedError, ValueError) as error:
                st.session_state["pubmed_results"] = []
                st.session_state["pubmed_error"] = str(error)

    if st.session_state.get("pubmed_error"):
        st.error(st.session_state["pubmed_error"])

    pubmed_results = st.session_state.get("pubmed_results", [])
    selected_pmids: list[str] = []
    if pubmed_results:
        result_by_pmid = {article["pmid"]: article for article in pubmed_results}
        selected_pmids = st.multiselect(
            "Select articles to include as source text",
            options=list(result_by_pmid),
            format_func=lambda pmid: (
                f"{result_by_pmid[pmid]['year'] or 'Year n/a'} · "
                f"{result_by_pmid[pmid]['title']} · PMID {pmid}"
            ),
        )
        for article in pubmed_results:
            with st.expander(f"{article['title']} · PMID {article['pmid']}"):
                st.markdown(
                    f"**{article['authors']}**  \n"
                    f"{article['journal']} ({article['year'] or 'Year unavailable'})"
                )
                st.markdown(f"[Open PubMed record]({article['url']})")
                st.write(article["abstract"] or "No abstract is available in the PubMed record.")
    elif st.session_state.get("pubmed_query_submitted") and not st.session_state.get("pubmed_error"):
        st.info("No PubMed results found for that search.")

    st.markdown("**ClinicalTrials.gov registry search**")
    st.caption(
        "Search public registry records by condition/topic. Registry records are "
        "not proof of study quality, results, or current operational status."
    )
    trial_query = st.text_input(
        "Condition or study topic",
        placeholder="Example: chronic lymphocytic leukemia",
        max_chars=250,
    )
    trial_search_clicked = st.button("Search ClinicalTrials.gov", use_container_width=True)
    if trial_search_clicked:
        st.session_state["trial_query_submitted"] = True
        if not trial_query.strip():
            st.session_state["trial_error"] = "Enter a condition or topic before searching trials."
            st.session_state["trial_results"] = []
        else:
            try:
                st.session_state["trial_results"] = source_agent.search_trials(trial_query, page_size=5)
                st.session_state.pop("trial_error", None)
            except (ClinicalTrialsError, ValueError) as error:
                st.session_state["trial_results"] = []
                st.session_state["trial_error"] = str(error)

    if st.session_state.get("trial_error"):
        st.error(st.session_state["trial_error"])

    trial_results = st.session_state.get("trial_results", [])
    selected_nct_ids: list[str] = []
    if trial_results:
        trial_by_nct_id = {trial["nct_id"]: trial for trial in trial_results}
        selected_nct_ids = st.multiselect(
            "Select registry records for this meeting",
            options=list(trial_by_nct_id),
            format_func=lambda nct_id: (
                f"{trial_by_nct_id[nct_id]['status']} · "
                f"{trial_by_nct_id[nct_id]['title']} · {nct_id}"
            ),
        )
        for trial in trial_results:
            with st.expander(f"{trial['title']} · {trial['nct_id']}"):
                st.markdown(
                    f"**Registry status:** {trial['status']}  \n"
                    f"**Last posted update:** {trial['last_updated'] or 'Not listed'}  \n"
                    f"**Study type / phase:** {trial['study_type']} / {trial['phase']}  \n"
                    f"**Conditions:** {', '.join(trial['conditions']) or 'Not listed'}  \n"
                    f"**Interventions:** {', '.join(trial['interventions']) or 'Not listed'}  \n"
                    f"**Enrollment:** {trial['enrollment']} {trial['enrollment_type']}"
                )
                st.markdown(f"[Open ClinicalTrials.gov record]({trial['url']})")
                prompts = source_agent.trial_discussion_prompts(trial)
                st.markdown("**Neutral discussion prompts (draft):**")
                for prompt in prompts:
                    st.markdown(f"- {prompt}")
                with st.expander("View registered eligibility and primary outcomes"):
                    st.markdown(f"**Eligibility:**\n\n{trial['eligibility']}")
                    st.markdown(
                        "**Primary outcomes:** "
                        f"{'; '.join(trial['primary_outcomes']) or 'Not listed'}"
                    )
    elif st.session_state.get("trial_query_submitted") and not st.session_state.get("trial_error"):
        st.info("No ClinicalTrials.gov records found for that search.")

    scientific_source_text = st.text_area(
        "Optional source text from approved materials",
        height=130,
        placeholder="Paste permitted text for local source preservation. No model service is used.",
    )
    meeting_notes = st.text_area(
        "New fictional meeting notes",
        height=130,
        placeholder="Enter synthetic demo notes only. Do not enter patient details or real HCP information.",
    )
    generate = st.button("Prepare selected sources and notes", type="primary", use_container_width=True)

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
    result = run_workflow(
        kol_id=selected["kol_id"],
        scientific_sources="\n\n---\n\n".join(source_parts),
        meeting_notes=meeting_notes,
    )
    st.session_state["workflow_result"] = result

result = st.session_state.get("workflow_result")
if result:
    st.divider()
    st.subheader("Draft briefing")
    st.caption(f"Mode: {result.get('generation_mode', 'Code-only')} · Requires MSL review")
    st.write(result.get("briefing", "No briefing available."))
    st.subheader("Draft note and follow-up")
    st.caption("Requires MSL review. This prototype does not create CRM records or send messages.")
    st.write(result.get("follow_up_draft", "No new notes were submitted."))

st.divider()
st.caption(
    "LangGraph coordinates three bounded local agents. PubMed and ClinicalTrials.gov searches "
    "are explicit read-only web requests; no model service, CRM writes, external messages, "
    "or safety submissions are used."
)