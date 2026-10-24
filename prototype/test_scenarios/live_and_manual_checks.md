# Live and manual verification status

Status date: 24 October 2026. This distinguishes earlier observations, current automated checks and pending human work. Do not treat a mocked completion as a live model run.

| Check | Evidence/status | Limitation |
| --- | --- | --- |
| Full Python suite and Streamlit AppTest | Current XML, catalog and latest_run.md in results | Mocked models/registries; no scientific quality conclusion |
| Expanded CRM views and KOL switching | Automated CRM/UI assertions in current suite | Browser appearance still benefits from user review |
| Local Streamlit health | Checked separately when running the app; see wiki log for recorded observations | Health alone does not prove an end-to-end user session |
| PubMed topic search | Previously observed on 23 October: oncology returned 5 records; first PMID 42909464 | Earlier read-only smoke check; not scientific appraisal, not rerun for this CRM change |
| PubMed no-result query | Previously observed: capstonezzqnomatch20261023 returned 0 records | Search results can change |
| ClinicalTrials.gov topic search | Previously observed: breast cancer returned 5 records; first NCT00089973 | Earlier read-only smoke check; not scientific appraisal |
| ClinicalTrials.gov no-result query | Previously observed: same artificial query returned 0 records | Search results can change |
| Real OpenAI three-agent completion | Not independently verified; user is exploring the app and has not saved a report | Key is available locally; complete and save the guided run before output review |
| Scientific claim/quote entailment | Pending qualified review | Exact quote matching does not establish truth or entailment |
| Live prompt-injection resistance | Not established | Automated test checks system/data separation only |
| Workshop evaluator acceptance | Pending | Reviewer role identified; no acceptance decision recorded |
| Manual versus assisted timings | Not measured | No preparation-time saving or business benefit claimed |
| Real CRM connection, outgoing message or safety submission | Outside this prototype | Not performed or implied by fictional fixture data |

Earlier observations are documented in [evaluation-and-review.md](../specs/evaluation-and-review.md) and [wiki/log.md](../../wiki/log.md). The latest test report is generated from actual pytest XML, not from this narrative table.

Desktop and narrow-screen browser previews of the refreshed interface were checked on 24 October 2026 without model calls. No horizontal document overflow was observed at 1680px and 430px viewport widths. These checks establish layout behavior, not live scientific performance.

## Advanced filters and workspaces ? 24 October 2026

Read-only filtered PubMed and ClinicalTrials.gov calls both returned one record in connectivity checks; exact criteria and IDs are in [live evidence](results/advanced_filters_live.json). Fresh-browser checks exercised both filtered searches, Offline abstention with unselected sources, all three workspaces, no visible exception and no horizontal page overflow at 1680px and 430px; see [browser evidence](results/advanced_filters_browser.json). These are software/connectivity observations, not scientific appraisal or a live OpenAI evaluation.
