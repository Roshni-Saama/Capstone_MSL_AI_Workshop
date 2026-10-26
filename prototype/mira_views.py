"""Explicit UI stages for Mira's research-to-follow-up journey."""
import json
import re
from datetime import datetime, timedelta, time
import streamlit as st
from agents import KOLContextAgent, ScientificSourceAgent, FollowUpAgent
from llm import OpenAILLM, LLMError
from mira_research import (MIRA_ID, QUESTION, signature, selected_sources,
                           evidence_links, company_relationship, calendar_invitation)
from search_result_views import render_pubmed_result, render_trial_result
from workflow import run_workflow
from filter_views import pubmed_controls, trial_controls
from presentation import display_id


def render_mira_research(selected, use_llm, api_key, model):
    if selected["kol_id"] != MIRA_ID:
        st.info("The guided oncology story is currently set up for Dr Mira Sen. Select her profile to review the full research flow.")
        return
    st.markdown("### From previous discussion to a source-linked meeting plan")
    st.caption("Review the history, shape the search, select evidence, prepare the discussion, then choose a next step.")
    steps = st.columns(4)
    for column, number, title, detail in zip(
        steps,
        ("01", "02", "03", "04"),
        ("Context", "Search", "Review", "Prepare"),
        ("Prior KOL questions", "Two public sources", "Select records", "Draft next steps"),
    ):
        with column:
            with st.container(border=True):
                st.caption(number)
                st.markdown("**" + title + "**")
                st.caption(detail)
    with st.expander("Previous discussion and follow-up context", expanded=False):
        for item in sorted(selected["interactions"], key=lambda row: row["date"], reverse=True):
            with st.container(border=True):
                st.caption(item["date"] + "  ·  " + item["channel"])
                st.markdown("**KOL asked**")
                st.write(item["observation"])
                st.markdown("**MSL response**")
                st.write(item["msl_response"])
                st.caption("Response: " + item["response_status"])
                for source in item.get("response_sources", []):
                    st.markdown("Source: [" + source["label"] + "](" + source["url"] + ")")
                st.caption("Follow-up: " + item["task"] + " · " + item["status"])
    question = st.text_area("What should the next discussion address?", value=QUESTION, max_chars=2000, key="mira_question")
    current = signature(selected, question, use_llm, model)
    if st.session_state.get("mira_context_signature") != current:
        for key in list(st.session_state):
            if key.startswith("mira_") and key not in ("mira_question",):
                del st.session_state[key]
        st.session_state["mira_context_signature"] = current
    def runtime():
        return OpenAILLM(api_key=api_key or None, model=model) if use_llm else None
    if st.button("Build research plan", key="mira_plan_button", type="primary"):
        for key in ("mira_plan", "mira_evidence", "mira_preparation", "mira_actions", "mira_plan_queries", "mira_plan_trial", "mira_pmids", "mira_ncts"):
            st.session_state.pop(key, None)
        try:
            with st.spinner("Reviewing Mira's recorded questions..."):
                st.session_state["mira_plan"] = KOLContextAgent().plan_research(MIRA_ID, question, runtime())
        except (LLMError, ValueError) as error:
            st.error(str(error))
    plan = st.session_state.get("mira_plan")
    if not plan:
        return
    st.caption(plan["mode"])
    for priority in plan["priorities"]:
        st.write(priority["text"])
        st.caption("CRM/question support: " + priority["quote"])
    st.markdown("#### Review the proposed searches")
    st.caption("The plan uses public scientific terms only. KOL names and CRM notes are not sent to PubMed or ClinicalTrials.gov.")
    search_left, search_right = st.columns(2)
    with search_left:
        pm_text = st.text_area("PubMed query plan (one per line)", value="\n".join(plan["pubmed_queries"]), key="mira_plan_queries", height=105)
    with search_right:
        trial_query = st.text_input("ClinicalTrials.gov query", value=plan["trial_query"], key="mira_plan_trial")
        st.caption("Searches the public trial registry by intervention; review sponsor and collaborator fields in results.")
    pm_filters = pubmed_controls()
    trial_filters = trial_controls()
    queries = [x.strip() for x in pm_text.splitlines() if x.strip()]
    query_sig = signature(queries, trial_query, pm_filters, trial_filters)
    if st.session_state.get("mira_query_signature") != query_sig:
        for key in ("mira_evidence", "mira_preparation", "mira_actions", "mira_pmids", "mira_ncts"):
            st.session_state.pop(key, None)
        st.session_state["mira_query_signature"] = query_sig
    if st.button("Search PubMed and ClinicalTrials.gov", key="mira_search", type="primary", width="stretch"):
        for key in ("mira_evidence", "mira_preparation", "mira_actions", "mira_pmids", "mira_ncts"):
            st.session_state.pop(key, None)
        try:
            with st.spinner("Searching public publications and trial records..."):
                st.session_state["mira_evidence"] = ScientificSourceAgent().search_research(
                    plan, queries, trial_query,
                    pubmed_filters=pm_filters, trial_filters=trial_filters,
                )
        except ValueError as error:
            st.error(str(error))
    evidence = st.session_state.get("mira_evidence")
    if not evidence:
        return
    st.caption("Retrieved (UTC): " + evidence["retrieved_at"] + " | Up to 10 publications and 10 trials. A focused search, not a systematic review.")
    for error in evidence["errors"]:
        st.warning(error)
    with st.expander("Search execution details"):
        st.json(evidence["search_trace"])
    st.caption("Ordering highlights topic matches and verified AbbVie sponsor fields. Review every record before selection.")
    result_left, result_right = st.columns(2)
    with result_left:
        with st.container(border=True):
            st.markdown("**Journal evidence | PubMed**")
            st.caption(f"{len(evidence['articles'])} records returned")
            pmids = st.multiselect("Select publications", options=[x["pmid"] for x in evidence["articles"]],
                                   format_func=lambda v: next(x["title"] for x in evidence["articles"] if x["pmid"] == v), key="mira_pmids")
            with st.expander("Review publications and original abstracts"):
                for article in evidence["articles"]:
                    render_pubmed_result(article, None)
                    linked = sorted(set(re.findall(r"NCT[0-9]{8}", article.get("abstract", ""))))
                    if linked:
                        st.caption("Trial IDs explicitly present in abstract: " + ", ".join(linked))
    with result_right:
        with st.container(border=True):
            st.markdown("**Clinical trial evidence | ClinicalTrials.gov**")
            st.caption(f"{len(evidence['trials'])} records returned")
            ncts = st.multiselect("Select trial records", options=[x["nct_id"] for x in evidence["trials"]],
                                  format_func=lambda v: next(v + " | " + company_relationship(x) + " | " + x["title"] for x in evidence["trials"] if x["nct_id"] == v), key="mira_ncts")
            with st.expander("Review trial designs, sponsor and original records"):
                for trial in evidence["trials"]:
                    st.caption(company_relationship(trial) + " | Registry results posted: " + str(trial.get("has_results", False)))
                    render_trial_result(trial, ScientificSourceAgent(), None)
    notes = st.session_state.get("msl_notes", "")
    st.caption(f"MSL notes for this preparation: {len(notes)} characters (edit in 03 MSL notes).")
    prep_sig = signature(evidence["signature"], pmids, ncts, notes)
    if st.session_state.get("mira_prep_signature") != prep_sig:
        for key in ("mira_preparation", "mira_actions"):
            st.session_state.pop(key, None)
        st.session_state["mira_prep_signature"] = prep_sig
    reviewed = st.checkbox("I reviewed the selected publications and trial records", key="mira_reviewed_" + prep_sig[:12])
    if st.button("Prepare discussion and follow-up", key="mira_prepare", type="primary", disabled=not reviewed, width="stretch"):
        st.session_state.pop("mira_preparation", None)
        st.session_state.pop("mira_actions", None)
        try:
            sources = selected_sources(evidence, pmids, ncts)
            with st.spinner("Running the three-agent preparation workflow..."):
                result = run_workflow(MIRA_ID, sources, notes, use_llm=use_llm, api_key=api_key or None, model=model)
            st.session_state["mira_preparation"] = result
            st.session_state["mira_actions"] = FollowUpAgent().next_actions(result, question, evidence_links(evidence, pmids, ncts))
        except (ValueError, LLMError) as error:
            st.error(str(error))
    result = st.session_state.get("mira_preparation")
    if not result:
        return
    st.caption(result.get("generation_mode", "Offline"))
    for label, key in (("Meeting priorities", "context_draft"), ("Scientific discussion briefing", "briefing"), ("Meeting note and follow-up", "follow_up_draft")):
        with st.expander(label, expanded=key == "briefing"):
            st.text(result.get(key, "Offline: review the history above."))
    with st.expander("Preparation agent trace"):
        st.json(result.get("agent_trace", [{"mode": "Offline", "agents": ["KOL Context Agent", "Scientific Source Agent", "Follow-up Agent"]}]))
    actions = st.session_state["mira_actions"]
    st.markdown("### Choose the next step")
    choice = st.radio("Output", ["Next-step summary", "Email draft", "Meeting proposal"], horizontal=True, key="mira_output")
    if choice in ("Next-step summary", "Email draft"):
        kind = "summary" if choice == "Next-step summary" else "email"
        text = st.text_area("Edit before using", value=actions[kind], height=350, key="mira_edit_" + kind + prep_sig[:10])
        st.download_button("Download " + choice.lower(), text, file_name="mira_" + kind + ".txt", mime="text/plain")
        st.caption("Editable draft for MSL review. No email has been sent.")
    else:
        st.caption("Create a tentative calendar file. Availability is not checked and no invitation is sent.")
        date = st.date_input("Proposed date", value=datetime.now().date() + timedelta(days=1))
        clock = st.time_input("Proposed time", value=time(10, 0))
        zone = st.selectbox("Meeting timezone", ["Asia/Kolkata", "Europe/London", "America/New_York", "UTC"])
        duration = st.selectbox("Duration (minutes)", [30, 45, 60])
        title = st.text_input("Meeting title", value="Scientific discussion with Dr Mira Sen")
        agenda = st.text_area("Meeting agenda", value=actions["agenda"])
        try:
            invitation = calendar_invitation(datetime.combine(date, clock), duration, title, agenda, zone)
            st.download_button("Download meeting proposal (.ics)", invitation, file_name="mira_meeting_proposal.ics", mime="text/calendar")
        except ValueError as error:
            st.warning(str(error))
    report = {"kol_id": display_id(MIRA_ID), "review_status": "Human assessment pending", "plan": plan, "search": evidence,
              "selected_pmids": pmids, "selected_nct_ids": ncts, "preparation": result, "outputs": actions}
    st.download_button("Download Mira workflow record", json.dumps(report, indent=2, default=str), file_name="mira_workflow.json", mime="application/json")
