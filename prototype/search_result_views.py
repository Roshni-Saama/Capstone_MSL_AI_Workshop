"""Summary-first result presentation; original evidence stays accessible."""
from html import escape
import streamlit as st
from search_summaries import summarize_results


def render_summary(preview):
    st.markdown("**Summary**")
    st.caption(preview["mode"])
    for point in preview["points"]:
        st.write("- " + point)
    if preview["quotes"]:
        with st.expander("View summary supporting quotes"):
            for text in preview["quotes"]:
                st.write(text)


def render_pubmed_result(article, preview=None):
    identifier = article["pmid"]
    with st.container(border=True, key=f"pubmed_result_{identifier}"):
        st.markdown(f'<div class="evidence-result-header"><span class="source-label">PubMed</span><h3>{escape(article["title"])}</h3></div>', unsafe_allow_html=True)
        preview = preview or summarize_results([article], "pubmed")[identifier]
        st.caption(f"{article['journal'] or 'Journal unavailable'} ({article['year'] or 'Year unavailable'}) | PMID {identifier}")
        st.markdown(f"[Open PubMed record]({article['url']})")
        render_summary(preview)
        with st.expander("View original details"):
            st.markdown(f"**Authors:** {article['authors'] or 'Unavailable'}")
            st.markdown(f"**DOI:** {article['doi'] or 'Unavailable'}")
            st.markdown("**Original abstract (not full article text):**")
            st.write(article["abstract"] or "No abstract is available in the PubMed record.")


def render_trial_result(trial, source_agent, preview=None):
    identifier = trial["nct_id"]
    with st.container(border=True, key=f"trial_result_{identifier}"):
        st.markdown(f'<div class="evidence-result-header"><span class="source-label">ClinicalTrials.gov</span><h3>{escape(trial["title"])}</h3></div>', unsafe_allow_html=True)
        preview = preview or summarize_results([trial], "trials")[identifier]
        st.caption(f"NCT ID: {identifier} | Last posted update: {trial['last_updated'] or 'Not listed'}")
        st.caption("Registry overview; planned outcomes are not study results.")
        st.markdown(f"[Open ClinicalTrials.gov record]({trial['url']})")
        render_summary(preview)
        with st.expander("View original details"):
            st.markdown(
                f"**Registry status:** {trial['status']}  \n"
                f"**Study type / phase:** {trial['study_type']} / {trial['phase']}  \n"
                f"**Conditions:** {', '.join(trial['conditions']) or 'Not listed'}  \n"
                f"**Interventions:** {', '.join(trial['interventions']) or 'Not listed'}  \n"
                f"**Enrollment:** {trial['enrollment']} {trial['enrollment_type']}"
            )
            st.markdown(f"**Registered eligibility:**\n\n{trial['eligibility']}")
            st.markdown("**Primary outcomes:** " + ('; '.join(trial['primary_outcomes']) or 'Not listed'))
        with st.expander("View neutral discussion prompts (draft)"):
            for prompt in source_agent.trial_discussion_prompts(trial):
                st.write("- " + prompt)
