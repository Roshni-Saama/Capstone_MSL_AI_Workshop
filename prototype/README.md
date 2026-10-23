# MSL Repeat-Meeting Assistant (Prototype)

This Streamlit proof of concept demonstrates a repeat MSL-KOL meeting workflow over three fictional CRM-shaped records. It is separate from the capstone research wiki and does not connect to a live CRM.

## What it demonstrates

1. Select a fictional KOL and retrieve only that record's profile, interaction history, and open follow-up.
2. Search PubMed through NCBI E-utilities and ClinicalTrials.gov through its current API v2, inspect cited records, and explicitly select articles/studies to include as source text. The trial registry also gets neutral, rule-based discussion prompts tied to registered fields. The app accepts optional user-supplied scientific source text. Without source text, it abstains from scientific claims; selected records/source text are preserved and not interpreted.
3. Structure new meeting notes into a review draft using deterministic rules. Notes remain verbatim, interpretation is left to the MSL, and a generic follow-up prompt is suggested only when question/request/evidence terms appear.

The workflow nodes are implemented as LangGraph steps: `retrieve_context`, `draft_briefing`, and `draft_follow_up`. PubMed access uses NCBI E-utilities ESearch/EFetch; clinical trial search uses the ClinicalTrials.gov API v2 `GET /studies` endpoint. Both are read-only and user-triggered; HTTPS verification uses the operating-system trust store. No LLM or model API is used. Python code performs citation formatting, source preservation, and neutral field-based discussion prompts. This prototype does not interpret abstracts or generate medical summaries. See the [NCBI E-utilities documentation](https://www.ncbi.nlm.nih.gov/books/NBK25500/) and [ClinicalTrials.gov API documentation](https://clinicaltrials.gov/data-api/api).

## Run locally

From this folder, create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
streamlit run app.py
```

PubMed and ClinicalTrials.gov searches require internet access. Each requests at most five records per search and does not require an API key for this low-volume demonstration.

Run tests with:

```powershell
python -m pytest -q
```

## Demo data

`data/kol_records.json` contains the three invented KOL profiles, prior interaction notes, and follow-up statuses. No real people, organizations, patient details, or scientific claims are represented. PubMed results and ClinicalTrials.gov records are external metadata retrieved by user search; they display source identifiers and links and are not copied into the synthetic CRM fixture. Selected source input is used only for the current workflow run and is not saved.

## Human review and limitations

All briefings and follow-up outputs are drafts. The MSL must verify identity, sources, interpretation, and task ownership. This prototype has no CRM writes, external communications, patient-specific recommendations, safety-case submission, authentication, or production data controls. Any potential safety information must be handled through the organization's established process; this demo does not make safety-reporting decisions.

## Acceptance criteria

- Exactly three synthetic KOLs are available with distinct IDs.
- Selecting a KOL returns only that KOL's history and tasks.
- PubMed search returns article metadata and PMID links; article selection is explicit.
- ClinicalTrials.gov search returns registry fields and NCT links; study selection is explicit and discussion prompts are neutral templates.
- CRM history is clearly separated from scientific source text.
- No source text means no scientific claims are generated; the app shows an abstention.
- New notes are preserved, interpretation remains for MSL review, and follow-up prompts use deterministic rules.
- Drafts are visibly marked as requiring human review.
- Tests cover record isolation, evidence abstention, source preservation, rule-based follow-up, and mocked PubMed/ClinicalTrials.gov parsing without live network calls.