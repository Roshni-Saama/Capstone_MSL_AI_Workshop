# Local prototype update — 26 October 2026

Status: **Local prototype; public hosting remains on hold.** The application is available on the development machine at `http://localhost:8503`.

## What changed

- The KOL interaction history now records a response from the MSL for all nine illustrative engagements, including the response state, evidence references and open follow-up.
- The CRM timeline and medical-request view display the KOL question beside the MSL response and source links.
- The Mira research planner receives the prior questions, MSL responses, response states and source references when preparing the next search.
- The left sidebar was removed. Drafting mode now appears on the main page, and the session-only API key and model controls are under **OpenAI settings**.
- Workshop markers are omitted from identifiers shown in the interface. A brief illustrative-record disclosure remains so example engagement history is not mistaken for real CRM data.

## Public evidence used in sample replies

The sample conversations cite [LUMINOSITY](https://pubmed.ncbi.nlm.nih.gov/42368479/), [TeliMET NSCLC-01](https://clinicaltrials.gov/study/NCT04928846), an [NSCLC molecular-testing consensus paper](https://pubmed.ncbi.nlm.nih.gov/38904502/) and [EPCORE NHL-1](https://pubmed.ncbi.nlm.nih.gov/39322711/). The replies distinguish reported findings from open questions and study limitations. The dialogue itself is illustrative; it is not a record of actual HCP interactions.

## Review status

- Browser review confirmed that the page renders without the left sidebar and that the interaction timeline displays a tracked MSL reply.
- JSON and Python syntax checks passed; `git diff --check` reported no whitespace errors.
- The full automated test suite was not run for this update.
- No CRM write, outgoing communication or public deployment was performed.

## Implementation references

- [Prototype README](../../prototype/README.md)
- [Streamlit application](../../prototype/app.py)
- [Mira research flow](../../prototype/mira_research.py)
- [CRM interaction data](../../prototype/data/kol_records.json)
