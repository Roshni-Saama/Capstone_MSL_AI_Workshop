# OpenAI LLM agents specification

Status: implementation authorized by the user on 23 October 2026. Provider: OpenAI API. Workshop evaluator acceptance, live model verification and specialist review remain pending.

## Three-agent contract

| Agent | Authoritative input | LLM output | Deterministic checks |
| --- | --- | --- | --- |
| KOL Context Agent | Exact-ID synthetic CRM record | Meeting priorities and unresolved requests | Identity resolved before any model call; each item quotes retrieved context |
| Scientific Source Agent | Explicitly selected sources, numbered S1, S2, etc. | Findings, neutral discussion questions, limitations | Missing source skips model and abstains; source IDs must exist and quotes must occur in that source |
| Follow-up Agent | Fictional notes | Observations, follow-up requests and open questions | Quotes must occur in notes; preserve originals and keep owners/dates unassigned |

See [agents.py](../agents.py), [workflow.py](../workflow.py) and [llm.py](../llm.py). The graph has fixed coordination and bounded model drafting, without autonomous tool selection or looping.

## Request and credential contract

- Explicit OpenAI mode and Prepare action; Offline remains the default and makes no model requests.
- One response per non-skipped agent, maximum three calls, 45-second timeout per HTTP call and no automatic retries.
- OpenAI Responses API with strict JSON schema, `store=false` and an output-token cap. Endpoint is fixed to api.openai.com; redirects are rejected.
- Default model is configurable `gpt-4.1-mini`, documented to support Structured Outputs. Availability is not assumed for every API project.
- Selected fictional context, selected source text and notes may leave the machine in OpenAI mode. No other KOL records, API keys or raw error bodies enter prompts or graph state.
- API key comes from the session password field or OPENAI_API_KEY environment variable. It is not saved by this app. Streamlit session memory is not a secret vault.
- Input size is bounded before requests. Generated payloads follow local Pydantic schemas; API refusals/incomplete responses and failed validation reject the workflow.

## Acceptance criteria

1. Unknown identity, missing key and oversized input fail without a model request.
2. Three bounded LLM roles run in graph order when context, scientific source and notes are present.
3. No scientific source means no scientific model call; no notes means no follow-up model call.
4. Invalid source IDs and evidence quotes are rejected. All original sources/identifiers remain available for review.
5. API errors are sanitized. No stale or partial result remains after a failed preparation.
6. Mode/model changes clear the previous result; identity changes clear the meeting workspace.
7. Model inputs are data, never executable instructions; no autonomous external actions exist.
8. Drafts and agent run details distinguish model output from offline formatting. A matching quote is not proof of entailment or medical accuracy.

Automated tests: [test_llm.py](../tests/test_llm.py), [test_app.py](../tests/test_app.py). Mock tests cannot establish live API access, prompt-injection resistance or scientific quality.

## Live verification still required

Open the app, select OpenAI LLM, configure a key locally, provide a permitted source and fictional notes, then Prepare. Verify that all three agent entries appear, citations match, notes are preserved, and no task owner/date is invented. Test missing sources, conflicting material and misleading instructions with reviewer supervision. Do not mark this complete until a real request and human assessment have occurred.

No API key was configured during implementation. No live OpenAI completion or model-quality evaluation has been claimed.

## Official references

- [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs): JSON schema constrains response structure; schema validity does not establish factual truth.
- [GPT-4.1 mini](https://developers.openai.com/api/docs/models/gpt-4.1-mini): selected configurable model and structured-output support.
