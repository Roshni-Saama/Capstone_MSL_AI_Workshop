# Agent harness execution

Run: 2026-10-24T15:03:53+05:30

Cases: 16; passed: 16; failed: 0.

Offline/scripted transport only. No live model quality, clinical correctness or business benefit was evaluated.

| Case | Mode | Result | Failed checks |
| --- | --- | --- | --- |
| offline-kol-001 | offline | Passed | None |
| mock-kol-001 | mock | Passed | None |
| offline-kol-002 | offline | Passed | None |
| mock-kol-002 | mock | Passed | None |
| offline-kol-003 | offline | Passed | None |
| mock-kol-003 | mock | Passed | None |
| missing-source-abstention | mock | Passed | None |
| empty-notes-no-follow-up | mock | Passed | None |
| unknown-identity-rejected | mock | Passed | None |
| oversized-input-rejected | mock | Passed | None |
| unselected-citation-rejected | mock | Passed | None |
| invented-quote-rejected | mock | Passed | None |
| malformed-output-rejected | mock | Passed | None |
| refusal-rejected | mock | Passed | None |
| conflicting-sources-preserved | mock | Passed | None |
| instruction-like-source-remains-data | mock | Passed | None |

Expected rejection cases pass only when the expected error and call sequence occur and no result is accepted.

See [machine-readable checks and provenance](agent_evaluation.json) and [harness instructions](../README.md).
