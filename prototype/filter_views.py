"""Advanced-search controls and stale-search invalidation for both registries."""
from datetime import date
import streamlit as st
from search_filters import (PubMedFilters, TrialFilters, PUBMED_TYPES, LANGUAGES, STATUSES,
    PHASES, STUDY_TYPES, INTERVENTION_TYPES, AGE_GROUPS, SEXES, DATE_FIELDS, PUBMED_SORT, TRIAL_SORT)

FILTER_KEYS = ["pm_start", "pm_end", "pm_types", "pm_languages", "pm_availability", "pm_species", "pm_therapy", "pm_affiliation", "pm_journal", "pm_sort",
               "ct_start", "ct_end", "ct_date_field", "ct_statuses", "ct_phases", "ct_study_type", "ct_intervention_type", "ct_intervention", "ct_location", "ct_age", "ct_sex", "ct_sort"]


def clear_filter_widgets(prefix):
    for key in FILTER_KEYS:
        if key.startswith(prefix):
            st.session_state.pop(key, None)


def pubmed_controls():
    with st.expander("Advanced PubMed filters"):
        st.markdown("**Publication & evidence**")
        one, two, three = st.columns(3)
        with one:
            start = st.date_input("Publication date from", value=None, min_value=date(1900, 1, 1), max_value=date(2100, 12, 31), key="pm_start")
        with two:
            end = st.date_input("Publication date to", value=None, min_value=date(1900, 1, 1), max_value=date(2100, 12, 31), key="pm_end")
        with three:
            types = st.multiselect("Article types", list(PUBMED_TYPES), key="pm_types")
        st.markdown("**Scientific focus & location**")
        one, two, three = st.columns(3)
        with one:
            therapy = st.text_input("Therapy / intervention keyword", max_chars=120, key="pm_therapy", help="Searches title/abstract text, not a standardized therapy classification.")
        with two:
            affiliation = st.text_input("Author affiliation location", max_chars=120, key="pm_affiliation", help="Country, city or institution in author affiliations; not necessarily the study location.")
        with three:
            journal = st.text_input("Journal", max_chars=120, key="pm_journal")
        st.markdown("**Access & preferences**")
        one, two = st.columns(2)
        with one:
            languages = st.multiselect("Article languages", list(LANGUAGES), key="pm_languages")
        with two:
            availability = st.selectbox("Text availability", ["Any", "Abstract available", "Free full text"], key="pm_availability")
        one, two = st.columns(2)
        with one:
            species = st.selectbox("Species", ["Any", "Humans", "Other animals"], key="pm_species")
        with two:
            sort = st.selectbox("Sort PubMed results", list(PUBMED_SORT), key="pm_sort")
        st.caption("Categories combine with AND; selected types/languages use OR. Indexing filters may omit recent citations. Full text is not retrieved by this app.")
        st.button("Reset PubMed filters", key="reset_pm_filters", on_click=clear_filter_widgets, args=("pm_",))
    return PubMedFilters(start, end, tuple(types), tuple(languages), availability, species, therapy, affiliation, journal, sort)


def trial_controls():
    with st.expander("Advanced ClinicalTrials.gov filters"):
        st.markdown("**Treatment & location**")
        one, two, three = st.columns(3)
        with one:
            intervention = st.text_input("Intervention / treatment name", max_chars=120, key="ct_intervention")
        with two:
            intervention_type = st.selectbox("Intervention type", list(INTERVENTION_TYPES), key="ct_intervention_type")
        with three:
            location = st.text_input("Study location", max_chars=120, key="ct_location", help="Country, state, city or facility terms; not a distance or recruiting-site guarantee.")
        st.markdown("**Recruitment & study design**")
        one, two, three = st.columns(3)
        with one:
            statuses = st.multiselect("Recruitment statuses", list(STATUSES), key="ct_statuses")
        with two:
            phases = st.multiselect("Study phases", list(PHASES), key="ct_phases")
        with three:
            study_type = st.selectbox("Study type", list(STUDY_TYPES), key="ct_study_type")
        st.markdown("**Eligibility & record dates**")
        one, two, three = st.columns(3)
        with one:
            age = st.selectbox("Eligible age group", list(AGE_GROUPS), key="ct_age")
            sex = st.selectbox("Eligible sex", list(SEXES), key="ct_sex")
        with two:
            date_field = st.selectbox("Registry date field", list(DATE_FIELDS), key="ct_date_field")
            start = st.date_input("Registry date from", value=None, min_value=date(1900, 1, 1), max_value=date(2100, 12, 31), key="ct_start")
        with three:
            sort = st.selectbox("Sort trial results", list(TRIAL_SORT), key="ct_sort")
            end = st.date_input("Registry date to", value=None, min_value=date(1900, 1, 1), max_value=date(2100, 12, 31), key="ct_end")
        st.caption("Categories combine with AND; selected statuses/phases use OR. Dates refer to registry records. Inspect original eligibility and site details.")
        st.button("Reset trial filters", key="reset_ct_filters", on_click=clear_filter_widgets, args=("ct_",))
    return TrialFilters(start, end, date_field, tuple(statuses), tuple(phases), study_type, intervention_type, intervention, location, age, sex, sort)


def invalidate_changed_search(prefix, query, filters):
    signature = (query, repr(filters))
    old = st.session_state.get(prefix + "_controls_signature")
    if old is not None and signature != old:
        for suffix in ("results", "summaries", "summary_error", "error", "query_submitted", "applied_parameters"):
            st.session_state.pop(prefix + "_" + suffix, None)
        st.session_state.pop("selected_pmids" if prefix == "pubmed" else "selected_nct_ids", None)
        st.session_state.pop("workflow_result", None)
    st.session_state[prefix + "_controls_signature"] = signature


def applied_search(prefix, count):
    parameters = st.session_state.get(prefix + "_applied_parameters")
    if parameters is not None:
        st.caption(f"Showing {count} returned records (up to 5 per search). These are not the total matching records.")
        with st.expander("Applied search criteria"):
            st.json(parameters)
