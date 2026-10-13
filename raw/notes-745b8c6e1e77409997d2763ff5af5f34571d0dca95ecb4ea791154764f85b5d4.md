# MSL and KOL Engagement Capstone Notes and References

Collected discussion notes for the AI workshop capstone. Updated 13 October 2026.

The capstone starts with a business and workflow problem: helping Medical Science Liaisons prepare for and follow up on scientific engagements. It asks the team to design a useful AI solution with scientific accuracy, governance, and human oversight.

## The manager brief

The original brief is in [03_MSL_KOL_Engagement_Agent.docx](03_MSL_KOL_Engagement_Agent.docx).

The challenge is intentionally open-ended. The team should research current work, identify users and data sources, define a focused problem, develop an end-to-end workflow, design the experience, and explain where agents create value. Guardrails, transparency, governance, and human oversight form part of the solution.

Possible areas include KOL briefings, relevant scientific discussion topics, post-visit insight capture, routing questions or potential safety information, and identifying patterns across engagements. These are options, not a requirement to implement every feature.

The brief is business-led, with technical and governance deliverables. It does not prescribe an architecture, model, or platform. Its description of notebook-based work is a starting scenario, not evidence that every MSL team operates that way.

## The MSL role and value

A Medical Science Liaison (MSL) is a scientific professional within Medical Affairs. A Key Opinion Leader (KOL) is a clinician or researcher recognised for expertise in a field.

The exchange is two-way. MSLs explain scientific evidence and its limitations to healthcare professionals, and bring clinical questions, unmet needs, and evidence gaps back into the company. This supports scientific communication, medical education, research relationships, and medical strategy.

Professional guidance recommends scientific independence, reporting into Medical Affairs, and no sales targets for MSLs. See [the joint MSL best-practices position statement](https://ifapp.org/wp-content/uploads/2021/08/Theron2021_Article_PromotingBestPracticesForMedic.pdf).

## Operational and technical challenges

The following are candidate problems to validate with an MSL or manager. Company practices and systems vary.

| Stage | Operational challenge | Technical challenge |
| --- | --- | --- |
| Preparation | Finding relevant evidence and remembering unresolved questions takes time | Publications, CRM history, email, and reviewed content may be in separate systems |
| Scientific exchange | Limited meeting time and changing questions require attentive listening | Capture and summaries must preserve context and avoid unsupported statements |
| Documentation | Converting notes into accurate records and useful insights requires judgment | Unstructured notes and inconsistent terminology complicate analysis |
| Follow-up | Tasks can be delayed when ownership and closure are unclear | Medical information, CRM, and safety workflows require reliable handoffs |
| Medical strategy | Teams must distinguish recurring concerns from isolated opinions | Aggregation needs traceability, context, and protection against misleading patterns |

MAPS describes fragmented medical-insight practices and the need for clear processes, responsibilities, and suitable technology. See [Building Medical Insights Capabilities](https://medicalaffairs.org/wp-content/uploads/2022/05/00-MAPS-WP-Building-Medical-Insights-V01-1.pdf).

Recent survey papers address MSL performance measurement and AI adoption. Survey results should be interpreted in light of their sampling, geography, and data-collection dates; a publication date does not make a survey a live industry census. See references 3 and 4 below.

## An illustrative engagement from preparation through follow up

This is a fictional example, not a record of an actual company meeting. Timing and processes depend on company procedures.

Priya, an oncology MSL, meets Dr Mehta, an oncologist and researcher. At their previous meeting, he asked whether a clinical trial adequately represented older patients.

### Preparation

Priya reviews his publications, prior CRM notes, the relevant trial and supplementary material, current company-reviewed scientific content, and the status of the earlier information request. She prepares a brief with a meeting objective, evidence sources, limitations, and open questions.

### Confirming the need

Priya asks whether the representation of older patients is still his main concern. Dr Mehta clarifies that he means older patients with several coexisting conditions. This changes the focus: age alone does not address his question.

### Scientific discussion

Priya explains the study population and available evidence, including its limitations. She asks which aspects are hardest to interpret in his clinical setting. He requests additional published evidence relevant to patients with multiple conditions.

Priya records the request and agrees to check the evidence. She does not promise research funding or a new study. Scientific exchanges and any unsolicited off-label requests must follow applicable local rules and company procedures. See [MSL best practices](https://ifapp.org/wp-content/uploads/2021/08/Theron2021_Article_PromotingBestPracticesForMedic.pdf).

### Documentation

| Record type | Example |
| --- | --- |
| Discussion record | Reviewed trial eligibility and evidence concerning older patients |
| KOL observation | Dr Mehta said coexisting conditions make the trial findings harder to apply to his patients |
| Potential insight | Limited evidence in patients with multiple conditions may create uncertainty when interpreting the study |
| Follow-up task | Check relevant publications and provide a reviewed response |
| Open question | Is this concern shared by other clinicians or specific to this setting? |

The potential insight is an interpretation requiring review. One comment does not establish a broad pattern. MAPS distinguishes observations from actionable insights and stresses the role of scientific expertise. See [Insights Management Pain Points](https://medicalaffairs.org/wp-content/uploads/2023/10/MAPS-Within3-Insights-Pain-Points-V3.pdf).

Potential adverse-event information must enter the required company safety-reporting process, separately from routine insight analysis.

### External follow up

Priya works with the appropriate medical-information colleagues to check the evidence. After required review, she sends a focused response with sources and limitations. She records what was sent and what remains unresolved. If evidence is unavailable, the response acknowledges the gap.

### Internal review and closure

The medical team compares this observation with other field feedback. Recurring concerns may inform educational content or assessment of an evidence-generation need. The team gives Priya feedback on how her observation was used. See [The Value and Strategic Implementation of Insights Management](https://medicalaffairs.org/wp-content/uploads/2023/02/The-Value-and-Strategic-Implementation-of-Insights-Management.pdf).

## Possible AI scope for the capstone

A focused first project could support preparation and follow-up:

- Assemble a briefing with verifiable sources and unresolved questions.
- Draft structured notes that distinguish statements from interpretations.
- Track questions, owners, responses, and outstanding tasks.

The MSL reviews briefings, interpretations, and outgoing responses. Scientific accuracy, privacy, source traceability, current content, and human oversight are design requirements. These are proposed choices to validate, not a selected implementation.

## Reading list

1. **Theron et al. (2021): Promoting Best Practices for Medical Science Liaisons, Position Statement from the APPA, IFAPP, MAPS and MSLS.** Start here for the role, scientific independence, and engagement boundaries. [PDF](https://ifapp.org/wp-content/uploads/2021/08/Theron2021_Article_PromotingBestPracticesForMedic.pdf) | [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC8492581/) | [DOI](https://doi.org/10.1007/s43441-021-00310-y)

2. **MAPS: Building Medical Insights Capabilities in Medical Affairs Organizations.** Explains collection, review, analysis, organisational responsibilities, and technology. [PDF](https://medicalaffairs.org/wp-content/uploads/2022/05/00-MAPS-WP-Building-Medical-Insights-V01-1.pdf)

3. **Dyer et al. (2026): Measuring the Impact of Medical Science Liaisons: A Global Cross-Sectional Survey of Evaluation Practices and Perceptions.** Explores measuring quality and strategic value beyond activity counts. Published 12 March 2026; survey conducted in 2024. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13081017/) | [DOI](https://doi.org/10.7759/cureus.105099)

4. **Dyer et al. (2026): Perceptions, Utilization, and Impact of Artificial Intelligence on Medical Science Liaisons: A Global Cross-Sectional Survey of Medical Affairs Professionals.** Covers AI use, perceptions, and governance concerns. Published 16 April 2026. The sample was predominantly US-based, limiting direct generalisation to Indian practice. [PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC13179699/) | [DOI](https://doi.org/10.7759/cureus.107157)

5. **MAPS (2023): Identifying and Addressing Pain Points in the Insights Management Process.** Useful for distinguishing information, observations, and actionable insights. [PDF](https://medicalaffairs.org/wp-content/uploads/2023/10/MAPS-Within3-Insights-Pain-Points-V3.pdf)

6. **MAPS: The Value and Strategic Implementation of Insights Management.** Explains how medical insights inform decisions and why validation and internal communication matter. [PDF](https://medicalaffairs.org/wp-content/uploads/2023/02/The-Value-and-Strategic-Implementation-of-Insights-Management.pdf)

The references above are web links; the linked papers are not stored as local PDF copies.
