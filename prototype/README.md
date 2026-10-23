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
