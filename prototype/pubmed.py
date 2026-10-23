"""Read-only PubMed search using NCBI E-utilities."""

from __future__ import annotations

import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

import truststore


EUTILS_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
USER_AGENT = "MSLRepeatMeetingPrototype/0.1 (educational capstone)"


class PubMedError(RuntimeError):
    """Raised when PubMed cannot provide a valid search response."""


def _request_bytes(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        context = truststore.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        with urllib.request.urlopen(request, timeout=15, context=context) as response:
            return response.read()
    except (urllib.error.URLError, TimeoutError, OSError) as error:
        raise PubMedError("PubMed could not be reached. Check the connection and retry.") from error


def _text(element: ET.Element | None) -> str:
    if element is None:
        return ""
    return "".join(element.itertext()).strip()


def _article_from_xml(article: ET.Element) -> dict[str, str]:
    citation = article.find("./MedlineCitation")
    if citation is None:
        return {}
    article_data = citation.find("./Article")
    if article_data is None:
        return {}

    pmid = _text(citation.find("./PMID"))
    title = _text(article_data.find("./ArticleTitle")) or "Title unavailable"
    journal = _text(article_data.find("./Journal/Title"))
    pub_date = article_data.find("./Journal/JournalIssue/PubDate")
    year = _text(pub_date.find("./Year")) if pub_date is not None else ""
    if not year and pub_date is not None:
        medline_date = _text(pub_date.find("./MedlineDate"))
        year_match = re.search(r"\b\d{4}\b", medline_date)
        year = year_match.group(0) if year_match else ""

    authors = []
    for author in article_data.findall("./AuthorList/Author"):
        collective = _text(author.find("./CollectiveName"))
        last_name = _text(author.find("./LastName"))
        fore_name = _text(author.find("./ForeName"))
        name = collective or " ".join(part for part in (fore_name, last_name) if part)
        if name:
            authors.append(name)

    abstract_parts = []
    abstract = article_data.find("./Abstract")
    if abstract is not None:
        for section in abstract.findall("./AbstractText"):
            value = _text(section)
            label = section.attrib.get("Label") or section.attrib.get("NlmCategory")
            if value:
                abstract_parts.append(f"{label}: {value}" if label else value)

    doi = ""
    for article_id in article.findall("./PubmedData/ArticleIdList/ArticleId"):
        if article_id.attrib.get("IdType") == "doi":
            doi = _text(article_id)
            break

    return {
        "pmid": pmid,
        "title": title,
        "authors": ", ".join(authors),
        "journal": journal,
        "year": year,
        "abstract": "\n\n".join(abstract_parts),
        "doi": doi,
        "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/" if pmid else "",
    }


def search_pubmed(query: str, retmax: int = 5) -> list[dict[str, str]]:
    """Search PubMed and fetch up to ten structured citations and abstracts."""
    search_term = query.strip()
    if not search_term:
        raise ValueError("Enter search terms for PubMed.")
    if len(search_term) > 300:
        raise ValueError("PubMed search text must be 300 characters or fewer.")
    if not 1 <= retmax <= 10:
        raise ValueError("PubMed result count must be between 1 and 10.")

    search_params = urllib.parse.urlencode(
        {"db": "pubmed", "term": search_term, "retmode": "json", "retmax": retmax}
    )
    search_url = f"{EUTILS_BASE}/esearch.fcgi?{search_params}"
    try:
        search_payload = json.loads(_request_bytes(search_url))
        ids = search_payload["esearchresult"]["idlist"]
    except (json.JSONDecodeError, KeyError, TypeError) as error:
        raise PubMedError("PubMed returned an unreadable search response.") from error

    if not ids:
        return []

    fetch_params = urllib.parse.urlencode(
        {"db": "pubmed", "id": ",".join(ids), "retmode": "xml"}
    )
    fetch_url = f"{EUTILS_BASE}/efetch.fcgi?{fetch_params}"
    try:
        root = ET.fromstring(_request_bytes(fetch_url))
    except ET.ParseError as error:
        raise PubMedError("PubMed returned unreadable article data.") from error

    return [
        result
        for result in (_article_from_xml(article) for article in root.findall("./PubmedArticle"))
        if result.get("pmid")
    ]