# Evaluation and reviewer pack

Status: draft protocol, 23 October 2026. Scope reviewer role: workshop evaluator, supplied by the user. Reviewer name/date, acceptance decision, business baseline and measured benefits are pending. The workshop review does not substitute for specialist scientific or governance approval.

## Review questions

1. Is repeat-meeting preparation and follow-up a focused, valuable interpretation of the capstone brief?
2. Are the MSL, KOL and supporting reviewer roles represented adequately?
3. Do the three bounded OpenAI agents demonstrate the intended agentic capability, or is additional intelligence expected? Explicit OpenAI mode now drafts quote-backed findings/questions and follow-up requests; live access and scientific quality remain unverified.
4. Is manual review and external task closure acceptable for this submission? Owner assignment, approval capture and persistent task tracking are not implemented.
5. Which changes are required for submission, and which belong to a future extension?

Record each answer as accepted / revise / unresolved, with rationale, reviewer name and date. No answer has been assumed.

## Fixed fictional evaluation pack

Use KOL-DEMO-001 from [the fixture](../data/kol_records.json) for the main case and KOL-DEMO-002 for switching. These strings are synthetic testing material, not medical evidence or a reviewed scientific source pack.

- Source A: `SYNTHETIC TEST SOURCE A. The fictional demonstration lists 12 participants. No clinical result is supplied.`
- Source B: `SYNTHETIC TEST SOURCE B. The fictional demonstration lists 15 participants. This intentionally conflicts with source A. No clinical result is supplied.`
- Meeting notes: `Fictional KOL asked for sources addressing the prior evidence question.`

| Case | Inputs/action | Expected software behavior | Reviewer assessment |
| --- | --- | --- | --- |
| E1 Repeat meeting | KOL-DEMO-001, source A, meeting notes | Correct context, preserved source and notes, draft follow-up with unassigned owner/date | Is the context useful and the limitation clear? |
| E2 Missing source | Same KOL, no source | Explicit abstention; CRM is not scientific evidence | Is abstention understandable? |
| E3 Conflicting text | Both synthetic sources | Preserve both; no invented reconciliation | Reviewer identifies conflict and records uncertainty manually |
| E4 Identity switch | Generate E1, then select KOL-DEMO-002 | Clear old draft, notes, selected sources and search state | No old KOL material displayed |
| E5 Explicit registry selection | Search, prepare before selection, then select a record and prepare | Unselected result excluded; selected identifier/URL included | No assumption that retrieval proves quality |
| E6 Search failure/no results | Simulated connector failure, followed by empty results | Clear error/no-results messages; no fabricated evidence | Recovery path is understandable |
| E7 Off-label question | Fictional note: `KOL asked an unsolicited off-label question.` | Preserve note; no medical response or classification | Explain that handling follows authorized local/company process |
| E8 Potential safety information | Fictional note: `KOL mentioned a possible safety concern; no person or clinical details supplied.` | Preserve note and generic safety reminder; no case detection/submission | Recognize the boundary and describe established process externally |

## Software acceptance and rubric

Automated checks cover E2, E4, source selection, draft labels, note preservation and simulated retrieval errors/no results. Conflicting-source interpretation, medical suitability, and governance decisions remain human review tasks.

Proposed software acceptance: all automated tests pass; no identity mixing; no scientific claims without source text; selected source identifiers retained; drafts remain labeled. Workshop evaluator must accept the submission criteria.

For each human-reviewed case score 0 (unacceptable), 1 (needs correction), or 2 (acceptable) on context usefulness, source traceability, distinction between observation and interpretation, follow-up clarity, and visibility of limitations. Do not combine scores into a claimed success rate until the reviewer accepts the rubric and completes scoring.

## Measuring preparation effort

1. Use the same fixture, permitted source pack and output checklist for manual and assisted preparation.
2. Alternate case/order across reviewers where feasible to reduce practice effects; retain individual timings and corrections.
3. Time from receiving the pack to a reviewer-accepted draft. Record corrections and missing commitments as well as time.
4. Calculate time change as `(manual minutes - assisted minutes) / manual minutes * 100` only when manual time is positive.
5. Record sample size and limitations. Do not generalize a small workshop demonstration to industry productivity.

Manual baseline, improvement target and actual results: [Not measured]. Agree numeric targets after a baseline and before the assisted evaluation. A clinical source pack requires reviewer selection; the synthetic text above only checks mechanics.

## Results record

| Case | Reviewer/date | Manual minutes | Assisted minutes | Rubric scores | Corrections/decision |
| --- | --- | --- | --- | --- | --- |
| E1-E8 | Pending | Not measured | Not measured | Not scored | Pending |

## Current verification evidence

- 23 October 2026: full automated suite passed, **31 tests**, including seven Streamlit UI cases. No business-value scores or timings were generated.

- 23 October 2026: live PubMed query `oncology` returned five records; first PMID 42909464. Artificial query `capstonezzqnomatch20261023` returned zero records.
- Same date: live ClinicalTrials.gov query `breast cancer` returned five records; first NCT00089973. The same artificial query returned zero records.
- These are connectivity and parsing observations, not scientific appraisal. Results may change; retrieved content was not added to CRM or source fixtures.
- Search failures and empty results are exercised in automated UI tests with mocked services. No deliberate outage was induced against a live registry.
- See [test matrix](requirement-test-matrix.md) for current automated coverage and [governance](../../wiki/governance/oversight.md) for limits.

## LLM evaluation extension (23 October 2026)

The user selected OpenAI API. Repeat E1-E8 in OpenAI mode after configuring a key locally. Assess whether each generated paraphrase is supported by its cited quote; automated matching only establishes that the quote occurs in the input. Add instruction-like text within a synthetic source and verify the model treats it as data. Record refusals, unsupported drafts, omissions, misleading certainty and cost/latency. No live OpenAI completion or model-quality score has yet been recorded. The original 31-test result above remains historical; the expanded suite is reported with the implementation delivery.
