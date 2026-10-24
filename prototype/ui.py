"""Presentation helpers for the medical engagement workbench."""
from html import escape
from pathlib import Path
import streamlit as st


def apply_theme():
    st.markdown("<style>" + Path(__file__).with_name("styles.css").read_text(encoding="utf-8") + "</style>", unsafe_allow_html=True)


def hero():
    st.markdown("""<section class="workbench-hero">
      <div class="hero-eyebrow">MEDICAL AFFAIRS / ENGAGEMENT WORKSPACE</div>
      <h1>Medical Engagement <span class="hero-accent">Workbench</span></h1>
      <p>Know the KOL. Find the evidence. Prepare a thoughtful follow-up.</p>
      <div class="hero-pills"><span>01 &nbsp; Understand the KOL</span><span>02 &nbsp; Review the evidence</span><span>03 &nbsp; Prepare &amp; follow up</span></div>
    </section>""", unsafe_allow_html=True)


def section_label(number, title, subtitle):
    st.markdown(f'<div class="section-heading"><span class="section-number">{escape(number)}</span><div><h2>{escape(title)}</h2><p>{escape(subtitle)}</p></div></div>', unsafe_allow_html=True)


def profile_card(record):
    profile=record["crm_profile"]
    initials="".join(part[0] for part in record["display_name"].replace("Dr ", "").split()[:2])
    st.markdown(f"""<div class="profile-card"><div class="profile-top"><div class="avatar">{escape(initials)}</div>
      <div><div class="card-eyebrow">YOUR SELECTED KOL</div><h3>{escape(record['display_name'])}</h3><p>{escape(record['institution'])}</p></div></div>
      <div class="profile-role">{escape(record['role'])}</div>
      <div class="profile-tags"><span>{escape(profile['relationship_stage'])}</span><span>{escape(profile['territory'])}</span></div>
      <div class="next-meeting"><span>NEXT CONVERSATION</span><strong>{escape(record['planned_meeting']['date'])}</strong><p>{escape(record['planned_meeting']['purpose'])}</p></div></div>""", unsafe_allow_html=True)


def render_draft(text):
    # The original source appendix is useful for inspection, but long on first view.
    markers=["Selected scientific source text ("]
    for marker in markers:
        if marker in text:
            body, appendix=text.split(marker,1)
            st.write(body.strip())
            with st.expander("View briefing source text and citations"):
                st.write(marker+appendix)
            return
    st.write(text)


def crm_profile_details(record):
    """Four responsive cards with escaped labels and values from the selected record."""
    profile = record["crm_profile"]
    def fields(items):
        return '<dl class="crm-field-grid">' + ''.join(
            f'<div class="crm-field"><dt>{escape(label)}</dt><dd>{escape(str(value))}</dd></div>'
            for label, value in items) + '</dl>'
    assignment = fields([
        ("CRM record", profile["crm_record_id"]), ("KOL ID", record["kol_id"]),
        ("Organization ID", record["organization_id"]), ("Territory", profile["territory"]),
        ("Location", f"{profile['city']}, {profile['country']}"), ("Assigned role", profile["assigned_msl_role"]),
    ])
    engagement = fields([
        ("Relationship", profile["relationship_stage"]), ("Preferred channel", profile["preferred_channel"]),
        ("Profile reviewed", profile["profile_reviewed_on"]), ("CRM snapshot", profile["snapshot_date"]),
    ])
    interests = '<ul class="crm-interests">' + ''.join(f'<li>{escape(topic)}</li>' for topic in profile["scientific_interests"]) + '</ul>'
    meeting = record["planned_meeting"]
    cards = [
        ("Record & assignment", assignment), ("Engagement preferences", engagement),
        ("Scientific interests", '<p class="crm-card-caption">Topics for discussion</p>' + interests),
        ("Planned meeting", f'<div class="crm-meeting-date">{escape(meeting["date"])}</div><p class="crm-meeting-purpose">{escape(meeting["purpose"])}</p>'),
    ]
    markup = '<div class="crm-profile-grid">' + ''.join(
        f'<section class="crm-detail-card"><h3>{escape(title)}</h3>{body}</section>' for title, body in cards) + '</div>'
    st.markdown(markup, unsafe_allow_html=True)
