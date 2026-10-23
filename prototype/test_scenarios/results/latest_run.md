# Latest automated test execution

Report date: 2026-10-23 (Asia/Kolkata).

Executed cases: **75**. Passed: **75**. Failed: **0**. Skipped: **0**.

Results are derived from [the pytest JUnit XML](automated_tests.xml); this report does not infer pass status from file presence or earlier runs.

| Area | Executed cases |
| --- | --- |
| Agent contracts | 6 |
| ClinicalTrials.gov parsing and prompts | 6 |
| OpenAI integration contracts | 25 |
| PubMed parsing and validation | 5 |
| Synthetic CRM data and UI | 17 |
| UI and LLM failure recovery | 9 |
| Workflow and evidence boundaries | 7 |

Run from the prototype folder:

```powershell
./.venv/Scripts/python.exe -B -m pytest -q -p no:cacheprovider --junitxml=test_scenarios/results/automated_tests.xml
./.venv/Scripts/python.exe -B test_scenarios/build_report.py --date 2026-10-23
```

The suite uses fictional CRM fixtures and mocked model/registry responses; no live OpenAI completion or medical accuracy was verified by this test run.

Additional evidence: [scenario catalog](../scenario_catalog.csv), [use cases](../use_cases.md), [live/manual checks](../live_and_manual_checks.md).

Test code is maintained in [prototype/tests](../../tests). The report describes the latest run, not a complete archive of all historical runs.
