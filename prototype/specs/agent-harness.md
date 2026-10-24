# Agent harness specification

Status: software contract implemented for local mechanical QA; live model and evaluator acceptance remain pending. User requested local QA and an explicit agent harness on 24 October 2026. Hosting is on hold pending team confirmation.

## Scope

Keep exactly three production agents and existing Offline/OpenAI modes. Build a reproducible evaluation layer, not another autonomous agent. Existing runtime, unit, transport, retrieval and Streamlit tests remain the baseline. Fixed synthetic evaluations must run without secrets, network calls or usage charges. No model-based grading or clinical-quality claim is permitted from these mechanical checks.

## Acceptance contracts

| ID | Contract | Evidence |
| --- | --- | --- |
| H1 | The same synthetic dataset exercises all three KOLs in Offline and mocked LLM mode | harness/cases.json; harness/results/agent_evaluation.json |
| H2 | Exact identity and context isolation; no other KOL history | Named grading checks and deliberately corrupted identity/context tests |
| H3 | Expected role order, isolated payloads, maximum three calls | Mock request inspection and call-order mutation test |
| H4 | Missing evidence causes abstention; empty notes skip model follow-up | Fixed cases with explicit expected call sequences |
| H5 | Invalid identity/input, source IDs, quotes, malformed/refused responses fail closed | Expected error, attempted calls and absence of accepted result |
| H6 | Original sources/notes preserved; review labels and unassigned ownership retained | Output checks and deliberate note/source corruption tests |
| H7 | No network or real API key; strict schemas; credentials excluded from state/prompts/reports | Network guards, fake transport, credential mutation test |
| H8 | Reproducible machine-readable and readable reports, versions and provenance | JSON/Markdown reports, SHA-256 input hashes, Asia/Kolkata timestamp |
| H9 | One QA command works independently of the caller's current folder and fails when any stage fails | harness/run_local_qa.py; pytest.ini |

## Evaluation boundaries

The harness uses the real graph and production schema parser with a scripted transport. It verifies rejection behavior and data boundaries, not factual entailment, usefulness, live model prompt-injection resistance, safety-reportability decisions, clinical correctness or regulatory compliance. Human scoring uses [the existing evaluation protocol](evaluation-and-review.md); [the blank score sheet](../harness/reviewer_scores.csv) must not be populated automatically.

The existing registry parser and search UI tests use mocked public service responses. Real registry availability and live model quality require separately labeled checks and are not inferred from a passing harness. See [runner instructions](../harness/README.md) and [requirement matrix](requirement-test-matrix.md).
