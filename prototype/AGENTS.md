# Prototype Development Instructions

## Purpose

Build a demonstrable MSL repeat-meeting assistant using only the fictional CRM fixture and user-provided scientific source text. This folder is a prototype, not a production or validated medical system.

## Required workflow

1. Read `README.md` and the relevant acceptance criteria before changing behavior.
2. Keep the application to three bounded capabilities: KOL context retrieval, read-only scientific-source retrieval (PubMed and ClinicalTrials.gov), and reviewed note/follow-up drafting.
3. Keep workflow processing deterministic; PubMed is the only external read-only source, and no LLM or model API may be called.
4. Treat synthetic CRM notes as interaction history, never as scientific evidence.
5. Do not add real HCP/patient data, real CRM connections or writes, external messages, or real safety reporting.
6. Add or update focused tests and run `python -m pytest -q` before reporting completion.
7. Never claim tests passed unless the command ran successfully.

## Safety and evidence rules

- Without scientific source text, abstain from scientific claims. With source text, preserve it verbatim; do not summarize or interpret clinical evidence.
- Display source text separately from synthetic interaction history.
- PubMed access must remain read-only; preserve PMID and article URL with every selected abstract.
- PubMed search must be explicit and user-triggered; do not send CRM notes or personal/patient data as a query.
- ClinicalTrials.gov access must be read-only and use API v2; preserve NCT ID and registry URL with selected study context.
- Trial discussion prompts must be neutral questions tied to available registry fields, not scientific interpretation or recommendations.
- Label all generated content as a draft requiring MSL review.
- Potential safety information is not processed as a real report by this prototype; direct users to their organization's established process.
- Do not add model secrets or API-key configuration; this prototype makes no model calls.