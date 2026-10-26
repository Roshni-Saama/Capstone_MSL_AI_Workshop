# Prototype specifications

This is the specification-development folder. Documents define behavior, acceptance criteria and proposed evaluation before or alongside implementation. They are project specifications, not approved company policy.

| Specification | Purpose |
| --- | --- |
| [Scope and delivery](scope-and-delivery.md) | Problem, scope, delivery artifacts, decisions and remaining work |
| [Repeat-meeting workflow](repeat-meeting.md) | Fictional repeat-meeting behavior and boundaries |
| [LLM agents](llm-agents.md) | Three roles, permitted inputs, structured outputs and failure behavior |
| [Search summaries](search-summaries.md) | Summary-first records, original evidence and explicit selection |
| [Advanced search and navigation](advanced-search-and-navigation.md) | Source-specific filters, query state and three full-width workspaces |
| [Mira guided research workflow](mira-research-workflow.md) | Context-led dual-source oncology search and reviewed next-step drafts |
| [Agent harness](agent-harness.md) | Network-free evaluation contract and pass/fail evidence |
| [Requirement-to-test matrix](requirement-test-matrix.md) | Traceability from requirements to executable checks |
| [Evaluation and review](evaluation-and-review.md) | E1-E8 scenarios, human rubric and reviewer acceptance |

Workflow: update the relevant behavior contract, map acceptance checks in the matrix, implement focused changes, run [local QA](../harness/README.md), then review the saved evidence. Live OpenAI quality and evaluator sign-off remain separate from automated acceptance. Hosting is on hold pending team confirmation.
