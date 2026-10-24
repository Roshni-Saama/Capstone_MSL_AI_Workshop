# Agent evaluation harness

This folder adds repeatable, network-free regression evaluation around the three production agents. It complements the existing pytest/AppTest harness and runtime orchestration; it does not add a fourth agent or a model judge.

## Run all local QA

From the repository root:

```powershell
./prototype/.venv/Scripts/python.exe -B prototype/harness/run_local_qa.py
```

From the prototype folder:

```powershell
./.venv/Scripts/python.exe -B harness/run_local_qa.py
```

The runner uses its own absolute folder to run pytest, rebuild the scenario catalog from actual JUnit XML, and execute the fixed-case agent evaluation. Any failing stage gives a nonzero exit code. The runner makes no live service requests and uses the current Asia/Kolkata date. Root pytest.ini also permits normal pytest discovery from the repository root.

To run only the agent pack:

```powershell
./prototype/.venv/Scripts/python.exe -B prototype/harness/evaluate.py
```

## What was built

1. Fixed [synthetic cases](cases.json): Offline and mocked LLM runs for all three KOLs; missing sources; empty notes; invalid identity; oversized input; unselected citations; invented quotes; malformed output; refusal; conflicting sources; instruction-like source text.
2. A local fake transport exercises production request construction, Pydantic parsing, LangGraph orchestration and quote/source checks. All model text is scripted, not a real completion. Socket connections, DNS resolution and direct URL requests are blocked during evaluation.
3. Named checks verify exact identity, isolation from other KOLs, ordered calls and three-call budget, role-specific payloads, untrusted-data placement, preserved sources/notes, explicit abstention, review labels and unassigned follow-up ownership.
4. Negative cases pass only when the expected error occurs with the expected attempted agent sequence and no partial result is accepted. Grader regression tests deliberately corrupt identity, notes, sources, credentials, role inputs, call order and other-KOL context; the grader must fail them.
5. [JSON results](results/agent_evaluation.json) contain each assertion, mocked call count, local runtime, dependency versions and SHA-256 hashes of the case pack and key production files. [Readable results](results/agent_evaluation.md) show case status. Output includes no raw drafts, keys, prompts or exception messages. Files are latest-run snapshots, not a historical archive.
6. [Human review sheet](reviewer_scores.csv) remains blank until a reviewer evaluates actual outputs using the existing [rubric](../specs/evaluation-and-review.md). Blank scores are pending, not zero or passed.

## Runtime harness already present

[workflow.py](../workflow.py) routes exactly KOL Context Agent ? Scientific Source Agent ? Follow-up Agent. It resolves identity before model calls, limits input size, skips scientific generation without sources and skips follow-up generation without notes. [llm.py](../llm.py) bounds output and request timeout, constrains schemas, disables provider-side response storage in the request, sanitizes errors and validates exact quotes. These controls and the [UI tests](../tests/test_app.py) are part of the existing harness.

## Evidence limits

The 16 evaluation cases overlap with some unit-test behaviors; their count is not an additional independent quality sample. Pass rates measure software mechanics only. Conflicting text is checked for preservation, not medically correct interpretation. The injection case checks data placement and scripted execution, not live resistance to prompt injection. No live registry or OpenAI call, clinical assessment, business-value measurement, deployment or hosting action occurs. Human review and a separately recorded real OpenAI walkthrough remain pending.

[Harness specification](../specs/agent-harness.md) | [All QA scenarios](../test_scenarios/README.md)
