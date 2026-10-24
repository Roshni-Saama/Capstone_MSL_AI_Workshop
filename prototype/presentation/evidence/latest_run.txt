# Latest automated test execution

Report date: 2026-10-24 (Asia/Kolkata).

Executed cases: **126**. Passed: **126**. Failed: **0**. Skipped: **0**.

Results are derived from [the pytest JUnit XML](automated_tests.xml); this report does not infer pass status from file presence or earlier runs.

| Area | Executed cases |
| --- | --- |
| Advanced registry filters and navigation | 16 |
| Agent contracts | 6 |
| Agent evaluation harness and grader | 8 |
| ClinicalTrials.gov parsing and prompts | 6 |
| Guided walkthrough and run evidence | 4 |
| Neutral interface wording and preservation | 3 |
| OpenAI integration contracts | 25 |
| Prepared public runtime protections | 2 |
| PubMed parsing and validation | 5 |
| Scientific search summaries | 16 |
| Synthetic CRM data and UI | 19 |
| UI and LLM failure recovery | 9 |
| Workflow and evidence boundaries | 7 |

Run from the prototype folder:

```powershell
./.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --junitxml=test_scenarios/results/automated_tests.xml
./.venv/Scripts/python.exe -B test_scenarios/build_report.py --date 2026-10-24
```

The suite uses fictional CRM fixtures and mocked model/registry responses; no live OpenAI completion or medical accuracy was verified by this test run.

Additional evidence: [scenario catalog](../scenario_catalog.csv), [use cases](../use_cases.md), [live/manual checks](../live_and_manual_checks.md).

Test code is maintained in [prototype/tests](../../tests). The report describes the latest run, not a complete archive of all historical runs.
