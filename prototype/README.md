# MSL Repeat-Meeting Assistant

Streamlit workshop prototype for repeat MSL-KOL preparation and follow-up. It uses three fictional CRM-shaped records and exactly three LangGraph-coordinated agents. No live CRM is connected.

## Two drafting modes

- **Offline** (default): deterministic retrieval, source preservation and generic note/follow-up formatting; no model requests.
- **OpenAI LLM**: explicit preparation invokes bounded OpenAI Responses calls. KOL Context Agent extracts meeting priorities and unresolved requests from the selected synthetic history; Scientific Source Agent drafts findings, neutral discussion questions and limitations from selected sources only; Follow-up Agent extracts observations, requests and open questions from fictional notes.

Identity lookup stays exact and deterministic. Missing scientific sources cause abstention and skip the scientific model call. Empty notes skip the follow-up model call. Maximum three model calls per preparation, no automatic retries, no autonomous tool loop, no CRM writes or external messages. This is a bounded LLM workflow, not a general autonomous assistant.

## Run locally

From this folder:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m streamlit run app.py
```

Use the sidebar to select **OpenAI LLM**, enter an API key in the password field and choose a model. The default is `gpt-4.1-mini`; access depends on your API project. Alternatively configure `OPENAI_API_KEY` and optionally `OPENAI_MODEL` in the server environment, then restart Streamlit. `.env` files are not loaded automatically. Do not paste keys into chat, code, source text or meeting notes. No key is bundled with the project.

The password field remains in the current Streamlit session memory; do not use a shared browser session for secrets. The application does not save credentials to disk or graph state. Secret files are excluded by `.gitignore`.

When you click **Prepare selected sources and notes** in OpenAI mode, the selected fictional history, selected source text and fictional notes are sent to OpenAI. API usage may incur charges. The app uses `store=false` on requests; this is not a claim of zero provider retention. Review applicable provider data controls before any real deployment. Registry queries remain separate, explicit read-only requests to PubMed/ClinicalTrials.gov.

## Walkthrough

1. Select a fictional KOL and inspect the CRM profile, interaction timeline, current tasks and medical-information requests. The fixed 23 October 2026 snapshot contains 3 profiles, 9 interactions, 9 tasks and 6 requests.
2. Choose Offline or OpenAI LLM in the sidebar.
3. Search a registry, inspect and explicitly select records, or supply permitted source text.
4. Enter fictional meeting notes and click Prepare.
5. Review meeting priorities (LLM mode), scientific draft/abstention, original source appendix and note/follow-up draft. Source IDs and exact supporting quotes aid review.
6. Changing KOL clears the current meeting workspace. Changing mode/model clears the prior result. Regenerating clears the old draft before attempting a new run.

## Evidence and failure behavior

Every model response is constrained to a JSON schema and validated locally with Pydantic. Draft items require a nonempty exact quote from the designated input, and scientific items require a selected source ID. Invalid source IDs, mismatched quotes, malformed responses, refusals, incomplete output and API errors reject the run. The UI shows an error without displaying partial or older results; it never silently calls an offline draft an LLM result.

Quote matching does not prove that a paraphrase follows from its source. Model text can still be misleading, incomplete or scientifically wrong. MSL review remains mandatory. Original sources/notes stay visible; task owners and due dates remain unassigned; no approval or closure action is performed. Potential safety information must follow the established organizational process; the prototype does not detect reportability or submit reports.

## Verification

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

Tests use mocked model/registry responses and Streamlit AppTest; running tests incurs no OpenAI usage. Real model quality requires a separately configured key and reviewer evaluation. The integration was built without a configured API key, so a live OpenAI completion has not yet been verified.

## Project references

- [Scope and delivery plan](specs/scope-and-delivery.md)
- [LLM acceptance criteria and verification](specs/llm-agents.md)
- [Requirement-test matrix](specs/requirement-test-matrix.md)
- [Evaluation and reviewer pack](specs/evaluation-and-review.md)
- [Workshop walkthrough](docs/workshop-walkthrough.md)
- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs)
- [GPT-4.1 mini model documentation](https://developers.openai.com/api/docs/models/gpt-4.1-mini)

## Synthetic CRM and test scenarios

- [CRM data and CSV exports](data/synthetic_crm/README.md): profiles, interactions, tasks and medical-information requests; the app reads data/kol_records.json.
- [Dedicated test use cases and scenarios](test_scenarios/README.md): all executed test instances, reproducible fictional inputs, XML evidence, latest results and separate live/manual status.

CRM task updates and request responses remain read-only fixture history. New drafts do not modify these records. Overdue is calculated at the fixture snapshot, not against the computer clock.
## Restart after updating backend code

If an existing browser session reports `run_workflow() got an unexpected keyword argument 'use_llm'` after updating the application, stop the old Streamlit server and start it again from this prototype folder with `./.venv/Scripts/python.exe -B -m streamlit run app.py`. Then refresh the browser. A fresh process loads the updated workflow signature; a browser refresh alone may retain an older imported function. Restarting clears the session, so re-enter the API key locally and restore any unsaved fictional notes.

## Summary-first scientific search

Opening a PubMed or ClinicalTrials.gov result now shows a short overview before the original details. Links and source identifiers remain visible. Expand **View original details** for the abstract or registered fields; PubMed retrieval is abstract-based and does not fetch full article text.

- Offline: PubMed shows a bounded abstract excerpt, explicitly labeled as an excerpt rather than an AI summary. Trials show a compact overview of design/status, population/interventions and planned outcomes. Missing abstracts are disclosed.
- OpenAI LLM: clicking a search generates one batch of short, source-checked summaries for up to five returned records through the existing Scientific Source Agent. These are additional API calls beyond preparation; retrieved public source text is sent to OpenAI. Draft summaries require MSL review.
- Summaries are session-only and reused on ordinary UI reruns. A new search, KOL change or mode/model change clears the affected summaries. Model failures show a warning and explicitly labeled offline previews, never an old AI summary.
- Source selection remains explicit. Preparing a briefing uses original selected records, not generated search summaries. Registry planned outcomes are not represented as study results.

See the [search-summary specification](specs/search-summaries.md) and [executed test scenarios](test_scenarios/README.md).

## Guided live walkthrough and refreshed interface

The workspace uses a navy/teal palette, system typography, a clear heading scale, aligned CRM/evidence columns, readable metrics and distinct review cards. Original source appendices are collapsed in review drafts and remain accessible. Desktop and narrow-screen browser checks were performed on 24 October 2026.

Open **Live OpenAI walkthrough - Dr Mira Sen** and click **Load Dr Mira Sen walkthrough**. This selects KOL-DEMO-001, switches to OpenAI mode and fills a public topic query plus fictional notes. Loading inputs makes no API request. Enter the key locally, run the PubMed search, inspect and select an article, then Prepare. Check all three entries under Agent run details and review the generated claims against sources.

After successful generation, **Download walkthrough record** exports a JSON report. **Save walkthrough record locally** explicitly writes the report to `prototype/test_scenarios/results/live_openai_walkthrough.json`. Reports include drafts and agent status, exclude credential fields, and retain a human-review-pending label. No live result is claimed until a real key-configured run has completed. Original CRM fixture data remains read-only.

## Public hosting

See [deployment setup and hosted verification](docs/deployment.md). The root `streamlit_app.py` is the public entrypoint: visitors supply their own API keys and download reports; server-side keys and local report saves are disabled. Deployment is pending authenticated publication.

## Local QA and agent harness

Run `./prototype/.venv/Scripts/python.exe -B prototype/harness/run_local_qa.py` from the repository root. It executes tests, regenerates the scenario catalog and runs the fixed agent evaluation pack. See [harness instructions and reports](harness/README.md) and [specification directory](specs/README.md). Hosting is on hold pending team confirmation.

## Advanced search and cleaner navigation

Use **KOL context**, **Evidence search** and **Drafts & follow-up** for the three full-width workspaces. Evidence search has separate PubMed and ClinicalTrials.gov tabs, each with expandable advanced filters. PubMed supports publication dates, article types/languages, availability, species, therapy keywords, affiliation location and journal. Trials support intervention name/type, study location, recruitment, phase, study type, age/sex eligibility and registry dates. Changing criteria clears old results and drafts; click Search to retrieve again. See [filter semantics and verification](specs/advanced-search-and-navigation.md). The verified fresh local preview for this update runs at http://localhost:8502.
