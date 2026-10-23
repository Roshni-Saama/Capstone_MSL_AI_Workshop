# MSL and KOL capstone wiki

Status: editable starter templates. Created 13 October 2026.

## Start here
- [Understanding the manager brief](manager-brief.md)
- [Working capstone notes](../MSL_KOL_Capstone_Notes_and_References.md)
- [MSL and KOL concepts](concepts/msl-kol.md)
- [KOL categories and expert directory](concepts/kol-directory.md)
- [Synthetic CRM demo data: three fictional KOL records](demo-data/synthetic-crm/index.md)
- [Expanded application CRM and CSV exports](../prototype/data/synthetic_crm/README.md)
- [Test use cases, all executed scenarios and results](../prototype/test_scenarios/README.md)
- [Engagement workflow](workflows/engagement.md)
- [Prototype scope, demonstration storyline, and delivery plan](../prototype/specs/scope-and-delivery.md)
- [OpenAI LLM agents: setup and acceptance criteria](../prototype/specs/llm-agents.md)
- [Human oversight and guardrails](governance/oversight.md)
- [Evaluation cases and workshop reviewer pack](../prototype/specs/evaluation-and-review.md)
- [Workshop presentation and walkthrough](../prototype/docs/workshop-walkthrough.md)
- [Wiki change log](log.md)
- [Codex instructions](../AGENTS.md)

## Source evidence
- [Original notes snapshot](../raw/notes-745b8c6e1e77409997d2763ff5af5f34571d0dca95ecb4ea791154764f85b5d4.md): preserved byte-for-byte on 13 October 2026. This is a copy of the project notes, not independent verification of their external references.
- The manager brief referenced in the notes is not yet stored in this repository.
- A targeted review of the MSL role and reporting guidance is recorded in the [MSL evidence note](../raw/msl-role-evidence.md). A targeted review of training and the MAPS insights process is recorded in the [supporting concepts research note](../raw/msl-concepts-evidence.md). Other linked papers remain unreviewed for these templates; full copies of those papers have not been downloaded.

- [KOL directory research notes](../raw/kol-directory-evidence.md): links expert selection and directory capabilities to reviewed source passages. The KOL page also links saved WHO HTML and Veeva PDF references.

- [Current readable capstone notes](../raw/Capstone_notes.md), with a [preserved snapshot](../raw/notes-aa7e638dd48c1f9f9b0aac118e9cba2f100efb8a4cabcc06230a3c095a0e6db2.md). Readable source aliases are maintained alongside the original evidence versions.

## How to edit
1. Open this repository folder in VS Code or as an Obsidian vault.
2. Fill in the templates below, distinguishing evidence from assumptions.
3. Add source evidence to raw/ using new filenames; preserve earlier versions.
4. Link each new wiki page here and append its change to the log.
5. Review, stage, commit, and push changes to GitHub.

## Project decisions to complete

Status: draft populated from discussion notes on 13 October 2026. Proposed scope and evaluation require stakeholder review; no company process or policy is approved.

### Focused business problem

Draft problem: For repeat KOL meetings, MSLs need to reconstruct relevant scientific context, prior discussions, and outstanding commitments from interaction history, then accurately document new questions and complete follow-up. The prototype will use clearly labeled, fully synthetic CRM-shaped records to demonstrate this continuity. The intended outcome is a source-backed briefing and a reviewed follow-up record with clear owners and status.

Basis: [Original notes, Operational and technical challenges](../raw/Capstone_notes.md#operational-and-technical-challenges). These are candidate problems, not validated findings about a particular company.

### Users and stakeholder reviewer

- Primary user: the MSL preparing for and following up on a scientific engagement.
- External stakeholder: the KOL receiving scientific information and raising evidence questions.
- Supporting roles in the illustrative example: medical-information colleagues reviewing responses and the medical team reviewing potential insights.
- Proposed stakeholder reviewer: an MSL or Medical Affairs manager who can validate the workflow. Scope reviewer role: workshop evaluator (user-confirmed on 23 October 2026); name and review date: [To complete]. Specialist reviewers for privacy, compliance, and safety routing: [To complete with the company].

Basis: [Original notes, The MSL role and value](../raw/Capstone_notes.md#the-msl-role-and-value) and [the fictional engagement example](../raw/Capstone_notes.md#an-illustrative-engagement-from-preparation-through-follow-up).

### Selected use case and exclusions

Proposed first use case: an MSL preparation and follow-up assistant for repeat KOL meetings. Final selection remains pending review.

- Preparation: assemble relevant scientific sources, synthetic prior interaction context, and unresolved questions into a briefing.
- Documentation: draft a structured record separating KOL statements, MSL interpretations, and follow-up tasks.
- Follow-up: carry prior commitments into the next meeting and track task owners, reviewed responses, and unresolved questions.
- Demo data: use fictional KOLs, organizations, interactions, and follow-up records with enterprise-like identifiers and relationships. Do not connect to or imply access to a live CRM.
- Human review: the MSL reviews briefings, interpretations, and outgoing responses.

### Agent and runtime decision

Current decision (user-authorized 23 October 2026): three LangGraph-coordinated agents with Offline default and explicit OpenAI LLM mode. KOL Context Agent retrieves exact-ID fictional history and drafts meeting priorities; Scientific Source Agent retrieves selected public sources and drafts quote-backed findings/questions/limitations; Follow-up Agent preserves notes and extracts draft requests/questions. Model output requires schema, source-ID and quote checks plus human review. Selected fictional context, sources and notes are sent to OpenAI only on explicit LLM preparation. Credentials and live completion verification remain pending; see the [LLM specification](../prototype/specs/llm-agents.md).

Proposed exclusions for the initial prototype: autonomous external messaging, patient treatment recommendations, sales targeting, promises of funding or research, live meeting recording, and company-wide strategy automation. Potential safety information must be flagged for the required company process; the prototype must not make final safety-reporting decisions. These are proposed boundaries, not approved company policy.

Basis: [Original notes, Possible AI scope for the capstone](../raw/Capstone_notes.md#possible-ai-scope-for-the-capstone). Prototype exclusions are design proposals added here for review.

### Success measures and evaluation plan

Proposed measures:

- Preparation effort: compare time to produce a reviewer-accepted briefing with and without assistance.
- Scientific reliability: assess source support, unsupported statements, and correct presentation of evidence limitations.
- Capture quality: check whether the record preserves the KOL question and distinguishes statements from interpretations.
- Follow-up completeness: check whether every task has an owner, status, and evidence of closure when completed.
- Human oversight and usefulness: verify review before release and obtain MSL feedback on relevance and required corrections.

Proposed evaluation: use fictional or authorised de-identified engagements, compare manual and assisted outputs against the same source pack, and have an MSL or Medical Affairs reviewer assess them. Include missing evidence, conflicting sources, an unsolicited off-label question, and potential safety information as review cases. Measure task handling and flags, not clinical outcomes or sales.

Baseline, numeric targets, test dataset, acceptance criteria, evaluator, and review date: [To complete after stakeholder validation]. These measures and test cases are new design proposals, not measured results. Their rationale is the accuracy, traceability, privacy, and oversight requirements in [Original notes, Possible AI scope](../raw/Capstone_notes.md#possible-ai-scope-for-the-capstone).
