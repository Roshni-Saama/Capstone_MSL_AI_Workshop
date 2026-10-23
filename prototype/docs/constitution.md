# MSL Repeat-Meeting Assistant Constitution

## Mission

Demonstrate how a small, governed AI workflow can help an MSL prepare for and follow up on repeat KOL scientific engagements.

## Scope principles

1. Build one end-to-end repeat-meeting workflow using three fictional KOL records.
2. Keep exactly three bounded application agents: KOL Context Agent, Scientific Source Agent, and Follow-up Agent.
3. Use LangGraph to coordinate three deterministic Python agents. Do not call an LLM or external model service.
4. Keep identity selection, access limits, review gates, and task ownership deterministic.
5. Prefer the smallest demonstrable change; do not imply production readiness or live enterprise integration.

## Scientific and safety principles

1. Synthetic CRM history is interaction context, not scientific evidence.
2. Scientific claims require an explicitly supplied, reviewable source; absent sources require abstention.
3. Preserve the distinction between stakeholder observation and MSL interpretation.
4. Mark generated content as a draft requiring human review.
5. Do not use real HCP or patient data, provide patient-specific advice, send external communications, write to a CRM, or submit safety reports.
6. Potential safety information must be handled through the organization's established process; this prototype makes no reportability decision.
7. PubMed and ClinicalTrials.gov queries are user-triggered and read-only; send only the search terms to those public registries.

## Quality principles

1. Every requirement has an acceptance check.
2. Record lookup must be exact and must not mix KOL histories.
3. Model unavailability must fail closed and never invent a scientific summary.
4. API keys stay in environment variables and are never committed.

## Definition of done

A change is complete when relevant acceptance criteria pass, limitations are documented, and test results are reported accurately.