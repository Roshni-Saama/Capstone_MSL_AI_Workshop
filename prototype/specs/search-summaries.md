# Summary-first search results

Status: implemented 23 October 2026. Live model summary quality still requires configured credentials and reviewer assessment.

## User experience

1. Run PubMed or ClinicalTrials.gov search explicitly.
2. Open a result to see a concise summary/overview with its PMID/NCT ID and original link.
3. Expand supporting quotes for an AI summary, or View original details for the original abstract/registry fields.
4. Select sources explicitly for the briefing. The briefing receives the original records, not these generated summaries.

Offline mode produces compact previews without model calls: a PubMed abstract excerpt and a structured trial overview. OpenAI mode adds a single batch request per successful nonempty search, through the existing Scientific Source Agent. No new application agent is introduced. All returned public records with source text may be sent for summarization; CRM and meeting notes are excluded from this request.

## Summary contract

- Up to five records per search; one batch response in OpenAI mode.
- Two or three short plain-language points requested, no more than 90 words per record instructed; locally reject more than three points or more than 120 words.
- Each model point requires an exact quote from that record's abstract or registered fields. Unknown/duplicate IDs, omitted records and unsupported quotes reject the whole batch.
- PubMed abstracts do not establish full-text review. Missing abstracts skip scientific summarization for that record.
- Trial summaries describe registered design, population, intervention and planned outcomes without inventing results or efficacy.
- Structured output and matching quotes do not establish factual correctness or faithful interpretation; MSL review remains necessary.
- API failure or invalid output shows a visible summary warning and labeled offline previews. Retrieved source records remain available. No partial or stale AI summary is shown.
- Cached summaries clear for new search, identity change and drafting mode/model changes. Widget reruns do not trigger repeat model calls.

## Verification

[Executable tests](../tests/test_search_summaries.py) cover short offline previews, missing abstracts, source preservation, batched role-isolated model requests, invalid source IDs/quotes/lengths, summary-first UI, original-detail access, explicit selection, session caching and failure recovery. Model and registry services are mocked in tests. Live scientific quality and robustness against hostile source instructions are not established by these assertions.

[Current executed scenario report](../test_scenarios/results/latest_run.md)
