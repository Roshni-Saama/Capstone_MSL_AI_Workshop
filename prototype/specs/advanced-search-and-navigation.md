# Advanced search and workspace navigation

Status: implemented locally on 24 October 2026. Hosting remains on hold. No new application agent is introduced; the Scientific Source Agent continues to own public retrieval.

## Upstream review and mapping

Reviewed the official [PubMed User Guide](https://pubmed.ncbi.nlm.nih.gov/help/), [ClinicalTrials.gov API documentation](https://clinicaltrials.gov/data-api/api), its [OpenAPI specification](https://clinicaltrials.gov/api/oas/v2), [search areas](https://clinicaltrials.gov/data-api/about-api/search-areas), and [complex query syntax](https://clinicaltrials.gov/find-studies/constructing-complex-search-queries). This implements a focused subset of their search options, not complete website parity.

| PubMed control | Server-side mapping |
| --- | --- |
| Publication date from/to | Date of publication range [dp]; either bound can be omitted |
| Article types | Clinical trial, RCT, review, systematic review, meta-analysis, observational study; [pt], except systematic[sb] uses the documented systematic-review strategy |
| Languages | English, Hindi, French, German, Spanish [la] |
| Text availability | Any, abstract available (hasabstract), free full text (free full text[sb]) |
| Species | Any, humans [mh], other animals (animals[mh] NOT humans[mh]) |
| Therapy/intervention keyword | Title/abstract [tiab]; text search rather than an inferred therapy ontology |
| Author affiliation location | [ad]; country/city/institution text in affiliations, not the study location or journal country |
| Journal and sorting | [ta]; default, best match or publication date |

PubMed indexing-dependent filters may omit relevant recent or unindexed records. The free-full-text filter does not change retrieval: this app still obtains metadata/abstracts, not publisher full text.

| ClinicalTrials.gov control | Server-side mapping |
| --- | --- |
| Condition | query.cond |
| Intervention/treatment name | query.intr |
| Location terms | query.locn; country/state/city/facility terms, not radius or guaranteed site recruitment |
| Recruitment statuses | filter.overallStatus |
| Phases | filter.advanced with AREA[Phase] clauses |
| Study and intervention type | AREA[StudyType], AREA[InterventionType] |
| Age group and sex | AREA[StdAge], AREA[Sex]; registered eligibility, not patient matching |
| Date range and date field | AREA[LastUpdatePostDate], AREA[StudyFirstPostDate] or AREA[StartDate] with RANGE; these are not publication dates |
| Sort | Default, relevance, latest update or newest registration |

Options within an article-type, language, status or phase category use OR; categories use AND. All filters are sent before the API chooses the returned records. No client-side filtering of the first five results is presented as an exhaustive registry search. The UI retains the five-record cap to keep the existing model-summary batch bounded; it labels returned counts as a sample, not total matches.

## State and failure behavior

Searches remain explicit. Editing controls makes no registry or model call. A changed query or filter clears that source's results, selected IDs, summaries, applied criteria and previous draft. A new explicit search also clears the old draft. Reset controls restore that source's defaults. Changing KOL resets all filter controls and both sources' search state. Tab navigation retains notes and selected sources. The Drafts tab shows selected record counts.

Date pickers allow 1900?2100, including historical literature and future planned study dates. Validate dates, options and literal filter fields before requests. Reversed dates or unsupported values produce a visible error. Literal fields reject quotes, brackets, backslashes and line breaks that could alter the generated expression. The main query retains the existing source-specific length limit and supports the source's ordinary query syntax. API failures retain visible errors and no fabricated records.

## Navigation

Three full-width workspaces replace the uneven CRM/evidence columns: 01 KOL context; 02 Evidence search; 03 Drafts & follow-up. Evidence has PubMed and ClinicalTrials.gov tabs. These are Streamlit tabs rather than separate URL pages; keeping the widgets mounted preserves existing session-only keys, selections and notes without extra model calls. The header is smaller and filters are grouped in expandable three-column panels that stack on narrow screens.

## Verification

[Filter tests](../tests/test_search_filters.py) exercise Boolean grouping, request encoding, validation before network, state invalidation, reset, navigation and visible date errors. Existing source selection, source-preservation, summary-cache and failure-recovery tests still run. See [latest automated evidence](../test_scenarios/results/latest_run.md), [live filter checks](../test_scenarios/results/advanced_filters_live.json) and [browser checks](../test_scenarios/results/advanced_filters_browser.json). Live checks validate connectivity and query acceptance, not medical relevance or completeness; no OpenAI call was made during this change.
