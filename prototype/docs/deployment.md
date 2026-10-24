# Public workshop deployment

User decision, 24 October 2026: public link; sign-in email roshni.srivastava@saama.com. Hosting target: Streamlit Community Cloud. Publication and hosted smoke checks remain pending until authenticated deployment succeeds.

## Deploy from GitHub

1. Sign in at https://share.streamlit.io/ using the confirmed account. Connect the GitHub account that can access Roshni-Saama/Capstone_MSL_AI_Workshop. Complete any organization authorization required by GitHub.
2. Create app from existing repository. Repository: `Roshni-Saama/Capstone_MSL_AI_Workshop`; branch: `main`; main file: `streamlit_app.py`; Python: `3.12` in Advanced settings.
3. Leave API secrets empty. The public entrypoint forces visitor-provided keys and ignores server-side OPENAI_API_KEY. Do not add a shared API key to this public demo.
4. Deploy, then set app Sharing to public (anyone with the link). Repository visibility does not need to change.
5. Open the deployed URL in a separate browser session. Confirm Offline preparation, all three synthetic KOLs, theme, PubMed and ClinicalTrials searches, and report download. Enter a visitor key only in the app password field for a separately recorded OpenAI walkthrough; never in chat or GitHub.
6. Record the actual URL and results below only after verification.

## Public runtime behavior

`streamlit_app.py` sets MSL_PUBLIC_DEMO=1 and runs the prototype from an absolute path. Root configuration loads the theme from the repository root. Root requirements delegate to prototype requirements. No CRM or patient data is connected.

Public mode hides server-side report saving; use Download walkthrough record. Keys and drafts remain in the browser's Streamlit session on the server and are not durable storage. A session is not an identity system. Do not enter real HCP, patient or confidential information. Hosted filesystem storage is not a report archive. Server logs and hosting are still managed by the platform.

Run `streamlit run prototype/app.py` locally to retain the explicit local Save button and optional environment key. Run `streamlit run streamlit_app.py` from the repository root to exercise public behavior locally.

## Hosting choices

Streamlit is the app framework. Community Cloud is a GitHub-connected managed host; it is the recommended initial target for this synthetic workshop demo. Snowflake can host Streamlit near Snowflake data with platform roles, compute billing and configured external network access. Render is another managed web-service host, with more runtime configuration. No company platform approval is implied.

Official references: [Community Cloud file organization](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/file-organization), [deploy settings](https://docs.streamlit.io/deploy/streamlit-community-cloud/deploy-your-app/deploy), [public sharing](https://docs.streamlit.io/deploy/streamlit-community-cloud/share-your-app), [Snowflake external access](https://docs.snowflake.com/en/developer-guide/streamlit/features/external-access), [Render web services](https://render.com/docs/web-services).

## Deployment evidence

- Account sign-in: pending user completion.
- Public URL: pending deployment; no URL is claimed.
- Hosted registry smoke tests: pending.
- Live OpenAI draft validation and evaluator review: pending.

## Hosting hold ? 24 October 2026

The user stopped all hosting work pending team confirmation. Community Cloud sign-in was reported organization-blocked; the Snowflake trial Offline proposal was declined. No account creation or deployment is claimed. Preserve the prepared local cloud files for a future decision; current priority is local QA and agent evaluation.
