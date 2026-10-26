"""Bounded context-led research and local follow-up exports for Mira."""
from __future__ import annotations
import hashlib
import json
import re
import uuid
from dataclasses import asdict
from datetime import datetime, timedelta, timezone
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from llm import StrictOutput, GroundedItem, LLMError, validate_items
from agents import KOLContextAgent, ScientificSourceAgent, format_crm_context
from pubmed import PubMedError
from clinical_trials import ClinicalTrialsError

MIRA_ID = "KOL-DEMO-001"
QUESTION = "How were older adults represented in LUMINOSITY, what limitations matter, and what is AbbVie investigating in TeliMET NSCLC-01?"
NOTES = "Dr Mira Sen asked for further information about age-specific outcomes and functional-status eligibility in LUMINOSITY and TeliMET NSCLC-01. She requested a source-linked scientific discussion. No owner or deadline was agreed."
CONCEPTS = {
    "programme": '"telisotuzumab vedotin"',
    "population": '(older OR elderly OR aged)',
    "disease": '(NSCLC OR "non-small cell lung cancer")',
    "biomarker": '("c-Met" OR MET)',
}
class PlanOutput(StrictOutput):
    priorities: list[GroundedItem]
    concepts: list[Literal["programme", "population", "disease", "biomarker"]]


def signature(*values):
    return hashlib.sha256(json.dumps(values, sort_keys=True, default=str).encode()).hexdigest()


def plan_research(kol_id, question, llm=None):
    if kol_id != MIRA_ID:
        raise ValueError("Guided research currently supports Dr Mira Sen only.")
    if not question.strip() or len(question) > 2000:
        raise ValueError("Enter a research question of 1-2000 characters.")
    record = KOLContextAgent().get_record(kol_id)
    context = format_crm_context(record)
    material = context + "\nCurrent MSL question: " + question
    if llm:
        output = llm.generate(
            "KOL Context Agent: identify up to six priorities from this selected KOL history and current question. Each needs an exact quote from material. Select relevant scientific concept codes from the enum; programme and disease are mandatory. Do not generate registry query text or clinical conclusions.",
            {"material": material}, PlanOutput)
        validate_items(output.priorities, material)
        priorities = [x.model_dump() for x in output.priorities]
        concepts = list(dict.fromkeys(["programme", "disease"] + output.concepts))
        mode = "OpenAI research plan; MSL review required"
    else:
        priorities = [{"text": x["observation"], "quote": x["observation"]}
                      for x in record["interactions"]]
        concepts = list(CONCEPTS)
        mode = "Offline curated research plan; no AI interpretation"
    broad = CONCEPTS["programme"] + " AND " + CONCEPTS["disease"]
    focused = broad + " AND " + " AND ".join(CONCEPTS[x] for x in concepts if x not in ("programme", "disease"))
    # Only approved scientific concepts leave the app, never model text or CRM.
    queries = list(dict.fromkeys([broad, focused.rstrip(" AND ")]))
    return {"kol_id": kol_id, "question": question, "priorities": priorities,
            "pubmed_queries": queries, "trial_query": "telisotuzumab vedotin",
            "mode": mode, "context_signature": signature(record, question),
            "calls": list(llm.calls) if llm else []}


def validate_queries(pubmed_queries, trial_query):
    # Edits are restricted to recombinations of approved public scientific terms.
    allowed = set(re.findall(r"[a-z0-9-]+", " ".join(CONCEPTS.values()).lower())) | {"and", "or", "not"}
    if not 1 <= len(pubmed_queries) <= 2:
        raise ValueError("Use one or two PubMed queries.")
    for query in [*pubmed_queries, trial_query]:
        if not query.strip() or len(query) > 250 or re.search(r'[^a-zA-Z0-9\s()"-]', query):
            raise ValueError("Use only the displayed scientific vocabulary and Boolean operators.")
        if not set(re.findall(r"[a-z0-9-]+", query.lower())) <= allowed:
            raise ValueError("Queries may contain only approved scientific terms; CRM text and identities cannot be searched.")
        if query.count("(") != query.count(")") or query.count('"') % 2:
            raise ValueError("Balance query parentheses and quotation marks.")


def company_relationship(trial):
    if trial.get("lead_sponsor", "").strip().casefold() == "abbvie":
        return "AbbVie lead sponsor"
    if any(x.strip().casefold() == "abbvie" for x in trial.get("collaborators", [])):
        return "AbbVie collaborator"
    return "AbbVie relationship not established in sponsor fields"


def search_evidence(plan, pubmed_queries, trial_query, agent=None,
                    pubmed_filters=None, trial_filters=None):
    validate_queries(pubmed_queries, trial_query)
    agent = agent or ScientificSourceAgent()
    articles, trials, errors, trace = {}, {}, [], []
    for query in pubmed_queries:
        try:
            found = agent.search_pubmed(query, retmax=5, filters=pubmed_filters)
            articles.update({x["pmid"]: x for x in found})
            trace.append({"source": "PubMed", "query": query, "count": len(found), "status": "completed"})
        except (PubMedError, ValueError):
            errors.append("A PubMed search failed. Review or retry; this evidence set is incomplete.")
            trace.append({"source": "PubMed", "query": query, "status": "failed"})
    try:
        found = agent.search_trials(trial_query, page_size=10, filters=trial_filters)
        trials.update({x["nct_id"]: x for x in found})
        trace.append({"source": "ClinicalTrials.gov", "query": trial_query, "count": len(found), "status": "completed"})
    except (ClinicalTrialsError, ValueError):
        errors.append("ClinicalTrials.gov search failed. Review or retry; trial evidence is unavailable.")
        trace.append({"source": "ClinicalTrials.gov", "query": trial_query, "status": "failed"})
    # Transparent deterministic ranking; semantic discussion is generated only from selected sources.
    def rank(x):
        text = (x.get("title", "") + " " + x.get("abstract", "")).lower()
        return sum(term in text for term in ("luminosity", "telisotuzumab", "older", "elderly"))
    return {"articles": sorted(articles.values(), key=rank, reverse=True),
            "trials": sorted(trials.values(), key=lambda x: company_relationship(x) == "AbbVie lead sponsor", reverse=True),
            "errors": errors, "search_trace": trace,
            "retrieved_at": datetime.now(timezone.utc).isoformat(),
            "applied_filters": {
                "pubmed": asdict(pubmed_filters) if pubmed_filters is not None else {},
                "clinical_trials": asdict(trial_filters) if trial_filters is not None else {},
            },
            "signature": signature(plan, pubmed_queries, trial_query, pubmed_filters, trial_filters)}


def selected_sources(evidence, pmids, nct_ids):
    articles = {x["pmid"]: x for x in evidence["articles"]}
    trials = {x["nct_id"]: x for x in evidence["trials"]}
    if not set(pmids) <= articles.keys() or not set(nct_ids) <= trials.keys():
        raise ValueError("Select only records returned by the current search.")
    if not pmids or not nct_ids:
        raise ValueError("Select at least one publication and one trial for this dual-source story.")
    agent = ScientificSourceAgent()
    # One source per block preserves exact S-ID attribution through existing validation.
    return "\n\n---\n\n".join(
        [agent.format_pubmed_sources([articles[x]]) for x in pmids] +
        [agent.format_trial_sources([trials[x]]) for x in nct_ids])


def evidence_links(evidence, pmids, nct_ids):
    return [x["url"] for x in evidence["articles"] if x["pmid"] in pmids] + [
        x["url"] for x in evidence["trials"] if x["nct_id"] in nct_ids]


def next_actions(result, question, links):
    if result.get("kol_id") != MIRA_ID:
        raise ValueError("Mira outputs require Mira's preparation result.")
    # Reuse the quote-validated scientific draft; never make a new ungrounded clinical claim.
    briefing = result["briefing"].split("Selected scientific source text")[0].strip()
    if not result.get("generation_mode", "").startswith("OpenAI"):
        briefing = "Offline: no scientific interpretation generated. Review the selected original sources before the discussion."
    agenda = ("1. Confirm the outstanding question.\n"
              "2. Review published findings, population representation and limitations.\n"
              "3. Review AbbVie-associated trial objectives, eligibility and current status.\n"
              "4. Agree remaining questions and follow-up after review.")
    references = "\n".join(links)
    summary = "DRAFT FOR MSL REVIEW\n\nQuestion: " + question + "\n\n" + agenda + "\n\n" + briefing + "\n\nSources:\n" + references
    email = ("Subject: Proposed scientific discussion - lung cancer evidence and research\n\n"
             "Dear Dr Sen,\n\nFor our next scientific discussion, I propose revisiting the following question:\n"
             + question + "\n\nProposed agenda:\n" + agenda +
             "\n\nEvidence briefing for your review:\n" + briefing +
             "\n\nSource links:\n" + references +
             "\n\nPlease let me know whether this agenda reflects your interests and what time would suit you.\n\nKind regards,\n[MSL name]")
    return {"summary": summary, "email": email, "agenda": agenda}


def calendar_invitation(start, duration, title, description, tz_name):
    if not 15 <= duration <= 120 or not title.strip() or len(title) > 180 or len(description) > 15000:
        raise ValueError("Use a title, a 15-120 minute duration, and an agenda under 15000 characters.")
    try:
        zone = ZoneInfo(tz_name)
    except ZoneInfoNotFoundError:
        raise ValueError("Choose a supported timezone.") from None
    # Reject nonexistent and ambiguous wall times rather than silently shifting a meeting.
    options = [start.replace(tzinfo=zone, fold=f) for f in (0, 1)]
    valid = [x for x in options if x.astimezone(timezone.utc).astimezone(zone).replace(tzinfo=None) == start]
    if not valid or (len(valid) == 2 and valid[0].utcoffset() != valid[1].utcoffset()):
        raise ValueError("This time is ambiguous or does not exist due to daylight saving. Choose another time.")
    begin = valid[0].astimezone(timezone.utc)
    if begin <= datetime.now(timezone.utc):
        raise ValueError("Choose a future meeting time.")
    def esc(value):
        return value.replace("\\", "\\\\").replace("\r", "").replace("\n", "\\n").replace(";", "\\;").replace(",", "\\,")
    lines = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//MSL Workbench//Meeting proposal//EN", "BEGIN:VEVENT",
             "UID:" + str(uuid.uuid4()) + "@msl-workbench.local",
             "DTSTAMP:" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ"),
             "DTSTART:" + begin.strftime("%Y%m%dT%H%M%SZ"),
             "DTEND:" + (begin + timedelta(minutes=duration)).strftime("%Y%m%dT%H%M%SZ"),
             "SUMMARY:" + esc(title), "DESCRIPTION:" + esc(description),
             "STATUS:TENTATIVE", "END:VEVENT", "END:VCALENDAR"]
    # RFC 5545 physical lines <=75 octets, including continuation space.
    folded = []
    for line in lines:
        chunk = ""
        for char in line:
            if len((chunk + char).encode("utf-8")) > 75:
                folded.append(chunk)
                chunk = " "
            chunk += char
        folded.append(chunk)
    return "\r\n".join(folded) + "\r\n"
