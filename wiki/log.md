# Wiki change log

Append new entries; preserve earlier entries.

## 23 October 2026 - Add synthetic CRM history to proposed demo scope

- Updated the draft problem and use case to focus on repeat KOL meetings and continuity of open scientific questions.
- Defined synthetic, enterprise-shaped CRM records as demo inputs, with fictional identifiers and no live CRM connection or real HCP/patient data.
- Added the minimum interaction/task fields and a repeat-meeting scenario to the proposed workflow.
- This is a scope proposal; the workspace contains no runnable prototype application to integrate data into yet.

## 13 October 2026 - Initial wiki structure
- Added the wiki home, concepts, workflow, and governance templates.
- Added root instructions for Codex.
- Preserved a byte-for-byte [snapshot of the original project notes](../raw/MSL%20KOL%20engagement%20note.md).
- Templates contain placeholders; no company process or policy has been approved.
- Evidence gap: the manager brief DOCX referenced in the notes is not present in the repository.
- External references in the original notes have not been independently verified during setup.
- [Wiki home](index.md)

## 13 October 2026 - Populate project decisions from discussion notes

- Filled the four project decision items in [Wiki home](index.md) with a draft business problem, user roles, proposed preparation and follow-up scope, and a proposed evaluation plan.
- Linked supporting sections of the preserved notes snapshot. The engagement example remains explicitly fictional.
- Marked prototype exclusions and evaluation measures as new proposals for review, not approved decisions or measured results.
- Retained placeholders for named reviewers, baselines, numeric targets, test data, and acceptance criteria.
- Preserved existing source evidence and the manager brief evidence gap.

## 13 October 2026 - Extract and explain the manager brief summary

- Added [Understanding the Manager Brief](manager-brief.md) with the requested section from the notes in the parent capstone folder.
- Used a SHA-256 snapshot of the named source for provenance. Preserved existing evidence; displayed the missing DOCX reference as a filename rather than a broken link.
- Added a draft explanation of the open-ended challenge, a preparation table, and questions for stakeholder validation.
- Linked the new page from the wiki index. The original notes were left unchanged.

## 13 October 2026 - Explain the MSL structure

- Filled the MSL definition and added an MSL structure section within the existing [concepts page](concepts/msl-kol.md).
- Distinguished professional reporting guidance from an illustrative chart and proposed collaboration map.
- Added a SHA-256-named research note from the professional position statement and linked it in the index.
- Left KOL, scientific-engagement, observation-versus-insight, and business-problem placeholders for subsequent discussion.
- Company reporting lines, named reviewers, and stakeholder approval remain open.

## 13 October 2026 - Prepare capstone updates for Git

- Recovered the missing manager brief page and hash-named MSL evidence file to resolve existing links.
- Preserved the locally changed notes as a new hash-named snapshot. Restored the original snapshot from the parent source after verifying its filename hash; the earlier committed version had a line-ending difference.
- Retained the readable MSL role note and MSL structure PDF as supporting material; the PDF has not been independently reviewed.
- Obsidian workspace settings remain local.

## 13 October 2026 - Revise MSL concepts for user review

- Expanded the [concepts page](concepts/msl-kol.md) using the annotated explanation of MSL work and organisational value.
- Revised the definitions and separated the illustrative reporting hierarchy from scientific exchange and internal collaboration.
- Added the observation-versus-insight example, candidate operational and technical challenges, local evidence links, and direct paper references.
- Added a hash-named supporting research note for scientific training and the MAPS insights process; preserved prior evidence.
- Kept company-specific assumptions open and the revision in draft for user review before further work or publication.

## 13 October 2026 - Publish KOL discussion to the wiki

- Added [KOL categories and expert directory](concepts/kol-directory.md) covering the six requested topics and references.
- Distinguished working categories and proposed maintenance steps from professional guidance and vendor capabilities.
- Linked the saved WHO page and Veeva PDF, recorded a source-backed research note, and added index navigation.
- Prepared the KOL page and its evidence for GitHub; the Markdown also resides in the existing Obsidian vault.
- The separate MSL concepts revision remains a local draft outside this publication.

## 13 October 2026 - Save edits made in Obsidian

- Saved the user's revised MSL concepts content and readable source filenames for VS Code and GitHub.
- Corrected source links to use relative paths to raw so they resolve in GitHub and Obsidian.
- Retained original hash-named evidence versions alongside the readable aliases and added a snapshot of the current Capstone notes.
- Kept the historical original-snapshot links pointing to their original evidence.
- Obsidian workspace configuration remains local.

## 23 October 2026 - Prepare three synthetic KOL CRM records

- Added a wiki-formatted demo-data folder with three fictional KOL profiles, dated interaction histories, and follow-up task statuses.
- Added stable fictional IDs and explicit provenance warnings; excluded real contact details, patient information, and scientific claims.
- Linked the fixture from the wiki home and repeat-meeting workflow.
- The records are demo inputs only; no runnable application or live CRM integration is present in this workspace.

## 23 October 2026 - Decide the three-agent prototype runtime

- Recorded the runtime decision: three bounded deterministic agents coordinated by LangGraph, with no LLM or Gemini runtime.
- Assigned KOL history retrieval, read-only scientific source retrieval, and reviewed follow-up drafting to separate agents.
- Clarified that PubMed and ClinicalTrials.gov source text is preserved, not interpreted, and registry discussion prompts are neutral templates.
- Updated the decision to match the working prototype; it remains a demonstrator, not a validated medical system.

## 23 October 2026 - Keep model drafting local-only

- Removed the optional OpenAI Responses API integration, API-key configuration, SDK dependency, and cloud-only tests.
- Kept the three deterministic local agents and read-only, user-triggered PubMed/ClinicalTrials.gov search connectors.
- Clarified that registry searches send only user-entered query terms to the public APIs; scientific drafts remain source-preserving and are not interpreted by a model.
- No OpenAI request or API key was used. Previously pushed GitHub commits are being withdrawn from the remote main branch separately; prior public API search queries cannot be recalled.

## 23 October 2026 - Clean workspace and reconcile prototype delivery scope

- Removed the parent workspace's verified empty MSL AI Solution POV.md and unused prototype folder, which contained only a virtual environment.
- Removed generated prototype Python and pytest caches; preserved the application environment and research evidence.
- Added the [scope and delivery plan](../prototype/specs/scope-and-delivery.md) with implementation-backed agent responsibilities, a demonstration storyline, and completion evidence for remaining work.
- Distinguished deterministic workflow orchestration from unimplemented model reasoning and evidence synthesis. Stakeholder acceptance, governance review, and measured value remain pending.
- Historical log entries and source snapshots remain unchanged.

## 23 October 2026 - Validate meeting UI and prepare remaining delivery artifacts

- Reproduced and fixed stale briefing and note display after switching KOL identities; added a complete meeting-state reset and focused Streamlit regression checks.
- Added checks for draft labels, source/history separation, abstention, explicit registry selection, unchanged fixture and simulated search errors/no matches.
- Live read-only topic/no-result searches succeeded for PubMed and ClinicalTrials.gov; no scientific interpretation or CRM updates were performed.
- Recorded the user-confirmed workshop evaluator role; approval, reviewer name/date and measured business value remain pending.
- Populated proposed governance controls/failure handling and prepared fixed fictional evaluation cases, a scoring protocol, and a workshop presentation script.
- Updated the delivery plan and workflow to distinguish implemented draft behavior from manual ownership, review and task closure.

## 23 October 2026 - Add user-authorized OpenAI LLM agents

- The user requested working LLM agents and selected OpenAI API, superseding the previous no-model constraint.
- Added explicit OpenAI mode alongside Offline default, with three LangGraph-coordinated role-specific model calls and unchanged exact-ID lookup.
- Added strict structured output, local schema/source-ID/quote validation, sanitized API errors, bounded input and stale-result clearing. Matching quotes do not establish scientific validity.
- Added session/environment credential support, explicit data-transmission disclosure and secret-file exclusions; no key is saved in code or graph state.
- Updated current scope, instructions, governance, evaluation and walkthrough references while preserving historical source evidence and log entries.
- No OpenAI API key was configured; model integration checks use mocked responses. Live generation and human quality evaluation remain pending.

## 23 October 2026 - Verify OpenAI integration contracts

- Full offline/mocked suite: 58 tests passed. Added HTTP method/endpoint/header/payload verification alongside role isolation, strict schema, citation/quote rejection and UI failure recovery.
- Local links validated in 19 documents; eight source snapshot hashes verified. No raw evidence changed.
- Streamlit health returned HTTP 200; Offline and OpenAI LLM sidebar modes rendered without errors.
- No live OpenAI completion was attempted because no API key was configured. User can configure the key locally in the app sidebar; scientific quality and workshop acceptance remain pending.

## 23 October 2026 - Expand fictional CRM and publish test-scenario evidence

- Expanded the three fictional KOL records with profile metadata, dated interaction channels, normalized task snapshots and medical-information requests. Totals: 3 profiles, 9 interactions, 9 tasks and 6 requests.
- Added read-only CRM profile, timeline, task and request views; overdue uses the fixed 23 October snapshot. No real CRM writes, external communications or scientific evidence were added.
- Added linked-record validation and regression tests for all KOLs, corrupted relationships, snapshot overdue behavior, demo inputs, CSV IDs and UI isolation.
- Full suite: 75 tests passed, recorded in test_scenarios/results/automated_tests.xml. Added an exact executed-case catalog, fictional use cases, reproducible inputs, report builder and separate manual/live status.
- Earlier live registry observations remain labeled historical; no real OpenAI completion or scientific quality assessment was performed for this change.

## 23 October 2026 - Give raw sources readable names and remove proven duplicates

- Reviewed all 16 raw files, including the full local six-page MSL position paper, ten-page Veeva paper, saved WHO HTML, source metadata and Markdown note variants.
- Renamed the original engagement note to [MSL KOL engagement note](../raw/MSL%20KOL%20engagement%20note.md), with descriptive names for the other research notes and references.
- Removed seven redundant files: five exact duplicates and two further note variants containing no unique text. Original source note/PDF/HTML bytes remain unchanged in canonical copies.
- Preserved all former filenames, checksums and removal reasons in [the source manifest](../raw/source-manifest.json). Updated the two download-metadata local_file pointers.
- Updated source links in current documentation and the historical log so they resolve to canonical files; historical event descriptions remain intact.
- Updated source-naming instructions to reflect the user's request. The existing original-note DOCX link remains an identified evidence gap; no source text was rewritten to conceal it.

## 23 October 2026 - Show scientific search summaries before original details

- Added summary-first PubMed/ClinicalTrials.gov result views with source links and original data under View original details.
- Offline mode shows labeled compact excerpts/registry overviews. Explicit OpenAI searches can request one batch of quote-checked short summaries through the Scientific Source Agent, without CRM data.
- Added per-session summaries and clearing on new search, mode/model or identity changes. Failed AI summaries show a warning and labeled offline previews; original records remain briefing evidence.
- Full automated suite: 91 passed. Added 16 summary-specific cases; live OpenAI summary quality remains unverified in this development run.

## 24 October 2026 - Refresh interface and prepare guided live walkthrough

- Improved type scale, spacing, contrast, sidebar, profile card, metrics and draft review panels with a navy/teal theme and responsive styling.
- Added explicit Mira Sen walkthrough setup, loading only fictional notes and a public query without external calls. Selected scientific sources remain a separate explicit choice.
- Added downloadable and explicitly saved run records that exclude credential fields and keep review pending. No real CRM write was introduced.
- Verified 95 automated cases with mocked external services; browser checks at desktop and 430px widths found no horizontal document overflow. User-key-configured live output is still pending.

## 24 October 2026 - Clarify live walkthrough status

- The user clarified they are exploring prototype functionality and have not saved the live run report.
- Kept independent live completion/output verification pending. No generated clinical content or model-quality result was invented.
- Guided setup and explicit evidence-save controls remain ready for a later user-run walkthrough; UI improvements and the 95-case automated verification are complete.

## 24 October 2026 ? Public hosting preparation

User chose public sharing and confirmed roshni.srivastava@saama.com for sign-in. Added [deployment instructions](../prototype/docs/deployment.md), a root Community Cloud entrypoint and theme configuration. Public mode requires a visitor key, ignores server-side OpenAI credentials, and offers report downloads instead of shared-server saves. Added focused public credential and session-isolation checks. Authenticated publication, hosted smoke checks and recorded live OpenAI evaluation remain pending.

## 24 October 2026 ? Local QA and explicit agent harness

User put hosting on hold pending team confirmation and requested local QA plus harness documentation. Baseline suite rerun passed 97 tests. Added [fixed agent evaluation](../prototype/harness/README.md), network-blocked scripted transport, per-check reports with source hashes, a caller-independent QA runner and tests that reject intentionally corrupted outputs. Added [harness contract](../prototype/specs/agent-harness.md) and [specification index](../prototype/specs/README.md). Live OpenAI quality and reviewer scoring remain pending; latest execution totals are reported in the generated QA artifacts.

Local QA closeout: **105 automated tests passed** and **16 fixed harness cases passed**; catalog and machine-readable evidence refreshed. Local wiki/prototype links and all nine raw-source checksums validated. See [closeout](../prototype/test_scenarios/results/local_qa_summary.md). Reviewer scoring and real OpenAI evidence remain pending.

## 24 October 2026 ? Advanced search and balanced workspace

User requested date/location/therapy filters and a cleaner layout. Added [source-specific advanced filters](../prototype/specs/advanced-search-and-navigation.md), verified against official PubMed guidance and the ClinicalTrials.gov OpenAPI specification. Replaced the uneven two-column layout with three full-width workspace tabs. Filter/query changes invalidate old evidence and drafts, with no automatic search. Added focused QA, [live API evidence](../prototype/test_scenarios/results/advanced_filters_live.json) and [browser evidence](../prototype/test_scenarios/results/advanced_filters_browser.json). Hosting stays on hold; no live model quality was evaluated.

Advanced-filter closeout: **121 automated tests passed** and **16 harness cases passed**. Both combined-filter API requests returned records; desktop/mobile browser checks passed. Reports and [QA closeout](../prototype/test_scenarios/results/local_qa_summary.md) refreshed. Fresh local preview: http://localhost:8502. Hosting remains on hold.

## 24 October 2026 ? Neutral interface wording

User requested removal of repeated fictional/demo terminology. Cleaned visible labels, helper text and CRM presentation, including neutral draft headings and guided-preparation controls. Preserved a brief synthetic-data disclosure, original CRM records and identifiers, raw scientific evidence, entered notes and MSL-review requirements. Added preservation and visible-copy checks in [presentation tests](../prototype/tests/test_presentation.py). Latest automated results are in the [QA report](../prototype/test_scenarios/results/latest_run.md).

Neutral-copy closeout: **124 tests passed**, **16 harness cases passed**. Refreshed the running preview on port 8502 and verified neutral labels, retained data disclosure and updated Offline draft wording. No scientific source text, entered notes or canonical CRM data was rewritten.

## 24 October 2026 ? CRM profile card layout

User requested side-by-side CRM information. Replaced the vertical list with four responsive cards covering record/assignment, engagement preferences, scientific interests and planned meeting. Preserved all existing values and added a focused field-preservation/HTML-escaping check. See [layout specification](../prototype/specs/advanced-search-and-navigation.md).

CRM layout closeout: **125 tests passed**, **16 harness cases passed**. Browser checks confirm two-column desktop cards and stacked mobile cards without overflow. [Layout previews](../prototype/test_scenarios/results/crm_profile_browser.json) saved; local preview restarted on port 8502.

## 24 October 2026 ? Task/request and registry alignment

User requested cleaner follow-up tasks, medical requests and both search tabs. Added responsive task/request cards with preserved read-only registers, aligned query/action toolbars, grouped filter rows and summary-first result cards. Original source details, selections, status values, ownership and evidence links remain available. [Layout contract](../prototype/specs/advanced-search-and-navigation.md) updated; QA totals are recorded in generated reports.

Alignment closeout: **126 automated tests** and **16 harness cases** passed. Eight desktop/mobile browser checks passed, including aligned card metadata and both live public searches. [QA evidence](../prototype/test_scenarios/results/aligned_layout_browser.json) and previews saved. Local preview refreshed on port 8502.

## 24 October 2026 - Presentation and portable showcase

User requested a presentation covering delivered capabilities, structure, agents, testing and harness, plus a demo link. Prepared [16-slide HTML/PDF materials](../prototype/presentation/README.md), speaker notes, architecture diagram, eight-view screenshot walkthrough and dated evidence snapshots. Local-only slides/showcase served on port 8765; working app remains on 8502. HTML works offline and can be shared as a file. Presentation QA: 47 checks passed; PDF has 16 pages. Application evidence remains 126 tests, 16 overlapping harness cases and eight browser checks. Live OpenAI output review, evaluator acceptance and hosting approval remain pending.

## 24 October 2026 - Team credits and palette selection

User requested the cover credit Prepared by: Sayali Shedge, Asawari U, Roshni Srivastava. Rebuilt HTML/PDF and verified all names. Prepared [four matching slide/application palette proposals](../prototype/presentation/palettes.html), comparison and individual PNG samples, plus numerical text/button contrast checks. No new palette is applied pending the user selection. Presentation QA remains 47 passing checks; palette/name preview checks passed. Updated the shareable presentation ZIP.

## 24 October 2026 - Navy & Azure selected and applied

User selected palette A. Applied primary #2563EB, navy #102A43, text #172B4D, background #F4F7FC and soft #EFF6FF across app CSS, Streamlit themes, slide template and architecture diagram. Refreshed every embedded app screenshot and rebuilt the HTML/PDF. Team credits remain Sayali Shedge, Asawari U and Roshni Srivastava. QA: 126 tests, 16 harness scenarios, eight refreshed browser checks and 47 presentation checks passed. [Theme evidence](../prototype/test_scenarios/results/navy_azure_browser.json). Updated the ZIP; no hosting action performed.

## 26 October 2026 - Conversational CRM and local workspace update

Added an MSL response, response status and public source references to each of the nine illustrative interaction records. The KOL timeline and request register show both sides of each exchange, and the Mira research planner receives that response history as context. The prototype now has no left sidebar: drafting mode is on the main page, with API-key and model controls under OpenAI settings. The app remains local at http://localhost:8503; no public hosting was performed. Browser review confirmed the page loads and the sidebar is absent. The full test suite was not run for this update. See [local prototype status](workflows/local-prototype-update-2026-10-26.md).
