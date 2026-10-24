# Prototype test use cases and scenarios

This folder records what was tested, how to reproduce it and what remains unverified. All demonstration inputs are fictional. Model and registry calls in the automated suite are mocked; no live API use is needed to rerun it.

## Start here

- [Use cases and demonstration steps](use_cases.md): three KOL stories, sample inputs and expected behavior.
- [Automated scenario catalog](scenario_catalog.csv): one row per executed test instance, including parameterized cases, exact test reference and actual result.
- [Local QA closeout](results/local_qa_summary.md): current results, scope and pending live review.
- [Latest execution report](results/latest_run.md): verified totals, command and limitations.
- [Machine-readable pytest results](results/automated_tests.xml): pass/fail evidence from the full run.
- [Live and manual checks](live_and_manual_checks.md): earlier observed checks versus checks still pending.
- [Copyable scenario inputs](fixtures/scenario_inputs.json): fictional text only, not scientific evidence.
- [Executable tests](../tests): actual Python assertions. Tests remain here so normal pytest discovery continues to work.
- [CRM dataset and CSV exports](../data/synthetic_crm/README.md).

## Reproduce

From the prototype folder, using its existing Python environment:

```powershell
.\.venv\Scripts\python.exe -B -m pytest -q -p no:cacheprovider --junitxml=test_scenarios/results/automated_tests.xml
.\.venv\Scripts\python.exe -B test_scenarios/build_report.py --date 2026-10-23
```

Use the current local report date with --date when rerunning. The second command builds the catalog/report from the XML produced by the first; it does not run tests or invent results. Review or archive the current report before overwriting it if a historical run is needed. The current folder contains the latest run; earlier verification statements are retained in [the wiki change log](../../wiki/log.md).

The automated catalog documents assertions actually exercised. Source inspection, live registry smoke checks, clinical review and real OpenAI completions are separate kinds of evidence. Matching a quote or passing a test does not establish scientific accuracy or business value.

## Dedicated agent harness

The [agent harness](../harness/README.md) adds fixed-case evaluation, named assertions, network guards, grader regression checks, provenance hashes and a single local-QA command. Its [16-case report](../harness/results/agent_evaluation.md) is separate from the unit/UI test count; the two overlap in tested behavior. [Specification development](../specs/README.md) remains a separate folder.

## Advanced search and browser evidence

[Source-specific filter specification](../specs/advanced-search-and-navigation.md), [live API acceptance](results/advanced_filters_live.json), [browser checks](results/advanced_filters_browser.json), [desktop PubMed preview](results/advanced_filters_desktop.png), [desktop trial preview](results/trial_filters_desktop.png), [mobile preview](results/advanced_filters_mobile.png). Earlier UI screenshots are historical; these previews show the three-workspace layout.

Neutral wording: [presentation-preservation tests](../tests/test_presentation.py), [browser check](results/neutral_wording_browser.json), [current screenshot](results/neutral_wording_desktop.png).

CRM profile cards: [browser check](results/crm_profile_browser.json), [desktop layout](results/crm_profile_desktop.png), [mobile layout](results/crm_profile_mobile.png).

Task/request and search alignment: [browser checks](results/aligned_layout_browser.json), [task cards](results/aligned_tasks_desktop.png), [request cards](results/aligned_requests_desktop.png), [PubMed filters](results/aligned_pubmed_filters_desktop.png), [trial filters](results/aligned_trials_filters_desktop.png).
