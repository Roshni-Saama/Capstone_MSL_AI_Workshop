# Human oversight and guardrails

Status: proposed capstone controls, 23 October 2026; not approved company policy. Workshop evaluator is the scope reviewer identified by the user. Named reviewer and review date remain pending. Role assignments below are proposals, not confirmed appointments.

## Basis and implementation evidence

The [project notes, Possible AI scope and fictional engagement](../../raw/Capstone_notes.md) propose source traceability, privacy and MSL review. Current software behavior is evidenced by [agents.py](../../prototype/agents.py), [app.py](../../prototype/app.py), and the [acceptance matrix](../../prototype/specs/requirement-test-matrix.md). The manager brief is still outside this repository in the parent workspace. This page describes design controls and implementation limits, not legal advice or approved reporting procedures.

## Controls and responsibility

| Area | Implemented control or limit | Proposed reviewer | Validation and remaining gap |
| --- | --- | --- | --- |
| Scientific accuracy and citations | Selected records retain PMID/NCT ID and URL; OpenAI mode drafts findings/questions/limitations with source IDs and checked quotes; missing sources cause abstention | MSL or Medical Affairs reviewer | Automated preservation/abstention checks; relevance, accuracy, source currency and interpretation require human assessment |
| Human review | Outputs carry draft labels; interpretations, owners and due dates remain for the MSL | MSL | UI labels tested; no approval capture or enforced release gate exists. Real release remains outside the demonstrator |
| Privacy and access | Explicit OpenAI mode discloses transmission of selected fictional inputs; session/environment credentials are excluded from prompts and graph state; fictional fixture, exact-ID lookup, warnings against real personal/confidential input; changing KOL clears the meeting workspace | Prototype maintainer; privacy reviewer for any future deployment | Isolation and reset tested; no authentication, authorization or production privacy controls |
| Safety and off-label information | Notes may be processed by the model in OpenAI mode; generic reminder to use established organizational processes; no reportability decision, case submission or automatic routing | Authorized safety/medical-information specialist, if applicable | Reviewer scenario only; no reporting deadline or company process is invented |
| Transparency and audit | Mode labels and visible source identifiers distinguish offline formatting and model drafts from source material | Prototype maintainer and workshop evaluator | Automated draft-label checks; session state is temporary and there is no durable approval/audit trail |
| Missing, stale or conflicting evidence | Abstain when no source exists; display available metadata and preserve selected text; LLM limitations remain unverified drafts and no conflict resolution is accepted automatically | MSL | Missing-source test exists; stale/conflicting evidence requires manual review |
| External actions | Registry connectors are read-only; workflow has no CRM connector, messaging or safety-submission integration | Prototype maintainer | Source review plus tests of local draft flow, unchanged fixture and absence of search calls during drafting; not a general security certification |

## Failure handling

| Trigger | Current behavior / proposed reviewer action | Proposed owner |
| --- | --- | --- |
| Unknown KOL ID or invalid fixture | Reject lookup/fixture; maintainer corrects synthetic data before retrying | Prototype maintainer |
| User selects a different KOL | Clear notes, selected sources, queries, search results and prior draft | Application; tested by maintainer |
| Empty query, failed search or no matches | Display validation/error/no-results message; reviewer may retry or supply permitted source text | MSL/demo operator |
| No source text | Show explicit abstention; do not infer clinical claims from CRM notes | Application; MSL reviews |
| Suspected stale/conflicting sources | MSL checks original records and records uncertainty manually; no automated conflict resolution | MSL/Medical Affairs reviewer |
| Potential safety information or off-label question | Demo operator acknowledges the limitation and refers to the established process; prototype makes no final decision | Authorized company specialist outside the demo |

## Decisions still open

- Workshop evaluator name, review date and scope decision: [To complete].
- Medical, privacy and safety specialist review if required by the intended use: [Not obtained].
- Approved company policies, operational owners, access controls and release gates: [Not supplied; required before any real deployment].
- Accepted risks, requested changes and next review date: [To record after review].

## Related pages

- [Engagement workflow](../workflows/engagement.md)
- [Evaluation and reviewer pack](../../prototype/specs/evaluation-and-review.md)
- [Wiki home](../index.md)

## OpenAI runtime change

The user authorized OpenAI agents on 23 October 2026, superseding the former local-only drafting rule. See the [LLM contract](../../prototype/specs/llm-agents.md). Strict schema and matching quotes do not prove factual accuracy, entailment or resistance to prompt injection. Inputs remain untrusted; no model tools or action permissions are supplied. Requests use store=false, which is not a zero-retention guarantee. Specialist data-handling review and a live model evaluation are outstanding.
