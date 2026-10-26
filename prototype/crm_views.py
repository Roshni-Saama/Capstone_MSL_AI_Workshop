"""Readable read-only CRM cards; full registers remain available underneath."""
from html import escape
import streamlit as st
from crm import task_rows
from presentation import display_id


def fields(items):
    return '<dl class="crm-field-grid">' + ''.join(
        f'<div class="crm-field"><dt>{escape(label)}</dt><dd>{escape(str(value))}</dd></div>'
        for label, value in items) + '</dl>'


def render_task_cards(record):
    cards = []
    rows = task_rows(record)
    for row in rows:
        state = 'completed' if row["Status"] == 'Completed' else 'overdue' if row["Overdue"] else 'open'
        overdue = '<span class="status-badge status-overdue">Overdue</span>' if row["Overdue"] else ''
        body = fields([("Owner", row["Owner"]), ("Due date", row["Due date"]),
                       ("Completed on", row["Completed on"]), ("Task ID", display_id(row["Task ID"]))])
        closure = f'<div class="crm-record-note"><span>Closure evidence</span><p>{escape(row["Closure evidence"])}</p></div>'
        cards.append(f'<article class="crm-work-card"><div class="crm-card-top"><span class="status-badge status-{state}">{escape(row["Status"])}</span>{overdue}</div><h3>{escape(row["Task"])}</h3>{body}{closure}</article>')
    st.markdown(f'<div class="crm-list-heading"><h3>Follow-up tasks</h3><span>{len(rows)} tasks ? Read only</span></div><div class="crm-task-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)


def render_request_cards(record):
    cards = []
    for request in record["medical_requests"]:
        interaction = next((row for row in record["interactions"]
                            if row["engagement_id"] == request["engagement_id"]), None)
        response = interaction.get("msl_response", "Response pending") if interaction else "Response pending"
        response_state = interaction.get("response_status", request["response_status"]) if interaction else request["response_status"]
        body = fields([("Received", request["received_on"]), ("Owner", request["owner_role"]),
                       ("Response status", response_state), ("Request ID", display_id(request["request_id"])),
                       ("Linked task", display_id(request["task_id"]))])
        source_links = "".join(
            f'<a href="{escape(item["url"], quote=True)}" target="_blank" rel="noopener">{escape(item["label"])}</a>'
            for item in (interaction or {}).get("response_sources", []))
        response_panel = f'<div class="crm-record-note"><span>MSL response</span><p>{escape(response)}</p><div class="response-source-links">{source_links}</div></div>'
        cards.append(f'<article class="crm-work-card"><div class="crm-card-top"><span class="status-badge status-open">{escape(request["status"])}</span></div><h3>{escape(request["question"])}</h3>{body}{response_panel}</article>')
    st.markdown(f'<div class="crm-list-heading"><h3>Medical requests</h3><span>{len(cards)} requests ? Read only</span></div><div class="crm-request-grid">' + ''.join(cards) + '</div>', unsafe_allow_html=True)
