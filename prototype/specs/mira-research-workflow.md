# Mira guided research workflow

Status: implemented locally on 26 October 2026. This guided flow uses the existing three agents. Mira and her CRM history are synthetic; linked publications and trial records are public evidence.

## Story

Dr Mira Sen is a synthetic clinical oncologist and researcher with an interest in older-adult representation in lung cancer research. Her recorded question asks how older adults were represented in LUMINOSITY, what limitations affect interpretation, and what AbbVie is investigating in TeliMET NSCLC-01. Her profile does not imply that she or her institution participates in a clinical trial.

The research anchors are the LUMINOSITY publication (PMID 38843488), its phase 2 registry entry (NCT03539536), and AbbVie's phase 3 TeliMET NSCLC-01 study (NCT04928846). Current status, sponsor and results fields must be checked against the live sources when presenting. Registry results availability does not establish whether publications exist. This workflow does not infer local availability, site participation or patient eligibility.

## Agent flow

1. **KOL Context Agent:** reads only the selected CRM record and the MSL's current question. It extracts priorities with exact supporting quotes and chooses from a fixed scientific vocabulary. It does not generate clinical conclusions or arbitrary registry queries.
2. **Scientific Source Agent:** the MSL reviews proposed PubMed queries and a ClinicalTrials.gov intervention query. Validation restricts editable search strings to approved public scientific terms, operators and balanced syntax. Both public registries are searched only after the MSL explicitly clicks Search. Results preserve identifiers, links, abstracts/registry fields, sponsor, collaborators, update dates and the registry results indicator. MSL selection is required before briefing preparation.
3. **Scientific preparation node:** the same Scientific Source Agent drafts findings, neutral questions and limitations from selected source text only. CRM informs priorities but never supports scientific claims. Registry design and planned outcomes are not treated as results.
4. **Follow-up Agent:** structures the MSL's session-only notes from the dedicated 03 MSL notes workspace with the existing quote checks. A separate output choice inside Guided research prepares a source-linked next-step summary, an editable email draft, or a tentative calendar file containing the meeting agenda.

The first research-plan call is explicit and occurs before registry search. The later three-node LangGraph preparation follows the established bounded roles. The combined path may use the research-plan call plus up to three agent preparation calls, with additional summary-batch calls only when separately requested. There are no autonomous retries or loops.

## Action boundaries

- CRM and previous conversation history remain synthetic. MSL notes are session-only and are not sent in registry search terms.
- OpenAI mode sends the selected KOL context and current question for research planning; selected publication/trial records and notes are sent during preparation. Review OpenAI data handling and usage before providing any data beyond workshop fixtures.
- Search terms are constrained to the displayed concept vocabulary; the model cannot inject raw CRM text, identities, arbitrary web instructions or company terms into registry queries.
- The MSL reviews evidence and explicitly selects at least one publication and one trial. Retrieval is bounded and is not a systematic review.
- Summary and email outputs are editable drafts. No email is sent. The calendar output is a tentative downloadable ICS proposal; availability is not checked and no invitation is scheduled or sent.
- No owner, due date, medical conclusion, investigator status or patient eligibility is invented. MSL review is required.

## Evidence and failure handling

Every registry request has a trace entry with its query, count and success/failure status. A failed source is called out as an incomplete evidence set; a search returning no records is not evidence of absence. Result ordering is a transparent, limited relevance heuristic and requires MSL review. Source identifiers and direct URLs remain in the downloaded workflow record. Changing KOL clears all Mira-specific plans, searches, selections, notes and drafts.

The output record is downloadable and marked pending human assessment. It excludes credentials. Live OpenAI execution, scientific quality and workshop evaluator acceptance remain separate review items.

## Manual walkthrough

See [live walkthrough](../docs/live-walkthrough.md). The primary steps are: review the history, build and edit a search plan, search both registries, select sources, review notes, prepare the three-agent briefing and choose a summary, email or calendar proposal.
