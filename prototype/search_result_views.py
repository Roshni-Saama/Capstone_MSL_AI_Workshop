"""Summary-first result presentation; original evidence stays accessible."""
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
    with st.expander(f"{article['title']} | PMID {identifier}"):
        preview = preview or summarize_results([article], "pubmed")[identifier]
        render_summary(preview)
        st.caption(f"{article['journal'] or 'Journal unavailable'} ({article['year'] or 'Year unavailable'}) | PMID {identifier}")
        st.markdown(f"[Open PubMed record]({article['url']})")
        with st.expander("View original details"):
            st.markdown(f"**Authors:** {article['authors'] or 'Unavailable'}")
            st.markdown(f"**DOI:** {article['doi'] or 'Unavailable'}")
            st.markdown("**Original abstract (not full article text):**")
            st.write(article["abstract"] or "No abstract is available in the PubMed record.")


def render_trial_result(trial, source_agent, preview=None):
    identifier = trial["nct_id"]
    with st.expander(f"{trial['title']} | {identifier}"):
        preview = preview or summarize_results([trial], "trials")[identifier]
        render_summary(preview)
        st.caption(f"NCT ID: {identifier} | Last posted update: {trial['last_updated'] or 'Not listed'}")
        st.caption("Registry overview; planned outcomes are not study results.")
        st.markdown(f"[Open ClinicalTrials.gov record]({trial['url']})")
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
