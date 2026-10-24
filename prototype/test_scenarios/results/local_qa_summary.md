# Local QA closeout ? 24 October 2026

Hosting is on hold pending team confirmation. No deployment or account setup was performed during local QA.

- Automated pytest/AppTest suite: **126 passed, 0 failed, 0 skipped**. [Execution report](latest_run.md), [JUnit evidence](automated_tests.xml), [scenario catalog](../scenario_catalog.csv).
- Fixed agent evaluation: **16 passed, 0 failed**. [Per-case checks and provenance](../../harness/results/agent_evaluation.json), [readable results](../../harness/results/agent_evaluation.md). These cases overlap with unit-test behavior and are not an independent model-quality sample.
- Grader regression tests reject deliberate corruption of identity, notes, sources, credential fields, role input, call order and other-KOL context.
- All local Markdown links under wiki and prototype resolve; all 9 canonical raw-source hashes match the manifest. The known original DOCX reference in raw is outside this link-check scope.
- Advanced filters: both live public API searches accepted combined criteria and returned records; see [live evidence](advanced_filters_live.json). Browser checks passed for filtered searches, three workspaces, Offline abstention, no visible exception and no page horizontal overflow at desktop/mobile sizes; see [browser evidence](advanced_filters_browser.json). Date controls allow 1900?2100; changed criteria invalidate stale evidence and drafts.
- No OpenAI completion, clinical assessment or evaluator scoring was performed. Reviewer score sheet remains blank.
- Next: record a real local OpenAI walkthrough, inspect each draft against its source, and complete evaluator scoring. Automated passes do not establish scientific correctness or business benefit.

See [advanced-search specification](../../specs/advanced-search-and-navigation.md), [single-command QA instructions](../../harness/README.md) and [specification directory](../../specs/README.md).

Neutral-wording update: original records, IDs and provenance remain intact; scientific sources and entered notes are preserved verbatim. Neutral labels and Offline draft text verified in the restarted local preview. See [browser evidence](neutral_wording_browser.json) and [updated preview](neutral_wording_desktop.png).

CRM profile layout: all fields retained in four cards; verified two columns at 1680px and one at 430px, with no page horizontal overflow or visible exception. [Browser evidence](crm_profile_browser.json), [desktop preview](crm_profile_desktop.png), [mobile preview](crm_profile_mobile.png).

Task/request and search realignment: responsive cards retain complete read-only registers; metadata rows align on desktop. Both search toolbars, grouped filters and summary cards verified using live public searches. [Browser evidence](aligned_layout_browser.json), [tasks](aligned_tasks_desktop.png), [requests](aligned_requests_desktop.png), [PubMed filters](aligned_pubmed_filters_desktop.png), [trial filters](aligned_trials_filters_desktop.png). No OpenAI call or hosting action performed.

Navy & Azure theme: 126 automated tests, 16 harness scenarios and eight refreshed layout/public-search browser checks passed. Actual computed colours match primary #2563EB, navy #102A43 and background #F4F7FC. [Theme verification](navy_azure_browser.json). Presentation HTML, PDF and walkthrough images were rebuilt; all 47 presentation checks passed.
