# Local QA closeout ? 24 October 2026

Hosting is on hold pending team confirmation. No deployment or account setup was performed during local QA.

- Automated pytest/AppTest suite: **121 passed, 0 failed, 0 skipped**. [Execution report](latest_run.md), [JUnit evidence](automated_tests.xml), [scenario catalog](../scenario_catalog.csv).
- Fixed agent evaluation: **16 passed, 0 failed**. [Per-case checks and provenance](../../harness/results/agent_evaluation.json), [readable results](../../harness/results/agent_evaluation.md). These cases overlap with unit-test behavior and are not an independent model-quality sample.
- Grader regression tests reject deliberate corruption of identity, notes, sources, credential fields, role input, call order and other-KOL context.
- All local Markdown links under wiki and prototype resolve; all 9 canonical raw-source hashes match the manifest. The known original DOCX reference in raw is outside this link-check scope.
- Advanced filters: both live public API searches accepted combined criteria and returned records; see [live evidence](advanced_filters_live.json). Browser checks passed for filtered searches, three workspaces, Offline abstention, no visible exception and no page horizontal overflow at desktop/mobile sizes; see [browser evidence](advanced_filters_browser.json). Date controls allow 1900?2100; changed criteria invalidate stale evidence and drafts.
- No OpenAI completion, clinical assessment or evaluator scoring was performed. Reviewer score sheet remains blank.
- Next: record a real local OpenAI walkthrough, inspect each draft against its source, and complete evaluator scoring. Automated passes do not establish scientific correctness or business benefit.

See [advanced-search specification](../../specs/advanced-search-and-navigation.md), [single-command QA instructions](../../harness/README.md) and [specification directory](../../specs/README.md).
