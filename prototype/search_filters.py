"""Validated, source-specific search filters. No local filtering of retrieved rows."""
from dataclasses import dataclass
from datetime import date
import re

PUBMED_TYPES = {
    "Clinical trial": '"Clinical Trial"[pt]',
    "Randomized controlled trial": '"Randomized Controlled Trial"[pt]',
    "Review": '"Review"[pt]', "Systematic review": 'systematic[sb]',
    "Meta-analysis": '"Meta-Analysis"[pt]', "Observational study": '"Observational Study"[pt]',
}
LANGUAGES = {"English": "english", "Hindi": "hindi", "French": "french", "German": "german", "Spanish": "spanish"}
STATUSES = {"Recruiting": "RECRUITING", "Not yet recruiting": "NOT_YET_RECRUITING", "Active, not recruiting": "ACTIVE_NOT_RECRUITING", "Completed": "COMPLETED", "Enrolling by invitation": "ENROLLING_BY_INVITATION", "Suspended": "SUSPENDED", "Terminated": "TERMINATED", "Withdrawn": "WITHDRAWN", "Unknown": "UNKNOWN"}
PHASES = {"Early phase 1": "EARLY_PHASE1", "Phase 1": "PHASE1", "Phase 2": "PHASE2", "Phase 3": "PHASE3", "Phase 4": "PHASE4", "Not applicable": "NA"}
STUDY_TYPES = {"Any": "", "Interventional": "INTERVENTIONAL", "Observational": "OBSERVATIONAL", "Expanded access": "EXPANDED_ACCESS"}
INTERVENTION_TYPES = {"Any": "", "Drug": "DRUG", "Biological": "BIOLOGICAL", "Device": "DEVICE", "Procedure": "PROCEDURE", "Radiation": "RADIATION", "Behavioral": "BEHAVIORAL", "Dietary supplement": "DIETARY_SUPPLEMENT", "Other": "OTHER"}
AGE_GROUPS = {"Any": "", "Child (under 18)": "CHILD", "Adult (18?64)": "ADULT", "Older adult (65+)": "OLDER_ADULT"}
SEXES = {"Any": "", "All": "ALL", "Female": "FEMALE", "Male": "MALE"}
DATE_FIELDS = {"Last update posted": "LastUpdatePostDate", "First posted": "StudyFirstPostDate", "Study start": "StartDate"}
PUBMED_SORT = {"Default": "", "Best match": "relevance", "Publication date": "pub_date"}
TRIAL_SORT = {"Default": "", "Best match": "@relevance", "Last updated": "LastUpdatePostDate:desc", "Newest registration": "StudyFirstPostDate:desc"}


def literal(value, name):
    if not isinstance(value, str) or len(value) > 120 or re.search(r'["\\\[\]{}\n\r]', value):
        raise ValueError(f"{name} must be at most 120 characters without quotes, brackets or line breaks.")
    return value.strip()


def option(value, allowed, name):
    if value not in allowed:
        raise ValueError(f"Choose a supported {name}.")
    return value


def options(values, allowed, name):
    if not isinstance(values, (tuple, list)) or len(values) > len(allowed):
        raise ValueError(f"Choose supported {name} values.")
    return [option(value, allowed, name) for value in values]


def dates(start, end):
    if any(value is not None and type(value) is not date for value in (start, end)):
        raise ValueError("Choose valid calendar dates.")
    if start and end and start > end:
        raise ValueError("The start date must be on or before the end date.")


@dataclass(frozen=True)
class PubMedFilters:
    start: date | None = None
    end: date | None = None
    article_types: tuple[str, ...] = ()
    languages: tuple[str, ...] = ()
    availability: str = "Any"
    species: str = "Any"
    therapy: str = ""
    affiliation: str = ""
    journal: str = ""
    sort: str = "Default"


@dataclass(frozen=True)
class TrialFilters:
    start: date | None = None
    end: date | None = None
    date_field: str = "Last update posted"
    statuses: tuple[str, ...] = ()
    phases: tuple[str, ...] = ()
    study_type: str = "Any"
    intervention_type: str = "Any"
    intervention: str = ""
    location: str = ""
    age: str = "Any"
    sex: str = "Any"
    sort: str = "Default"


def pubmed_parameters(query, filters=None):
    f = filters or PubMedFilters()
    dates(f.start, f.end)
    clauses = []
    if f.start or f.end:
        clauses.append(f'{(f.start or date(1000, 1, 1)):%Y/%m/%d}:{(f.end or date(3000, 12, 31)):%Y/%m/%d}[dp]')
    types = options(f.article_types, PUBMED_TYPES, "article type")
    if types:
        clauses.append("(" + " OR ".join(PUBMED_TYPES[value] for value in types) + ")")
    languages = options(f.languages, LANGUAGES, "language")
    if languages:
        clauses.append("(" + " OR ".join(LANGUAGES[value] + "[la]" for value in languages) + ")")
    availability = option(f.availability, ("Any", "Abstract available", "Free full text"), "text availability")
    if availability != "Any":
        clauses.append({"Abstract available": "hasabstract", "Free full text": "free full text[sb]"}[availability])
    species = option(f.species, ("Any", "Humans", "Other animals"), "species")
    if species != "Any":
        clauses.append("humans[mh]" if species == "Humans" else "(animals[mh] NOT humans[mh])")
    for value, name, tag in ((f.therapy, "Therapy keyword", "tiab"), (f.affiliation, "Author affiliation", "ad"), (f.journal, "Journal", "ta")):
        value = literal(value, name)
        if value:
            clauses.append(f'"{value}"[{tag}]')
    parameters = {"term": " AND ".join([f"({query})", *clauses]) if clauses else query}
    sort = PUBMED_SORT[option(f.sort, PUBMED_SORT, "PubMed sort order")]
    if sort:
        parameters["sort"] = sort
    return parameters


def trial_parameters(query, filters=None):
    f = filters or TrialFilters()
    dates(f.start, f.end)
    parameters = {"query.cond": query}
    for value, key, label in ((f.intervention, "query.intr", "Intervention"), (f.location, "query.locn", "Study location")):
        value = literal(value, label)
        if value:
            parameters[key] = f'"{value}"'
    statuses = options(f.statuses, STATUSES, "recruitment status")
    if statuses:
        parameters["filter.overallStatus"] = ",".join(STATUSES[value] for value in statuses)
    clauses = []
    phases = options(f.phases, PHASES, "phase")
    if phases:
        clauses.append("(" + " OR ".join(f"AREA[Phase]{PHASES[value]}" for value in phases) + ")")
    for value, mapping, area, label in ((f.study_type, STUDY_TYPES, "StudyType", "study type"), (f.intervention_type, INTERVENTION_TYPES, "InterventionType", "intervention type"), (f.age, AGE_GROUPS, "StdAge", "age group"), (f.sex, SEXES, "Sex", "sex")):
        code = mapping[option(value, mapping, label)]
        if code:
            clauses.append(f"AREA[{area}]{code}")
    date_field = DATE_FIELDS[option(f.date_field, DATE_FIELDS, "trial date field")]
    if f.start or f.end:
        clauses.append(f"AREA[{date_field}]RANGE[{f.start.isoformat() if f.start else 'MIN'},{f.end.isoformat() if f.end else 'MAX'}]")
    if clauses:
        parameters["filter.advanced"] = " AND ".join(clauses)
    sort = TRIAL_SORT[option(f.sort, TRIAL_SORT, "trial sort order")]
    if sort:
        parameters["sort"] = sort
    return parameters
