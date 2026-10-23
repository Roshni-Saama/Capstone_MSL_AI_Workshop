from __future__ import annotations

import json
from io import BytesIO
from urllib.parse import parse_qs, urlparse

import pytest

import pubmed


ARTICLE_XML = b"""<?xml version='1.0'?>
<PubmedArticleSet>
  <PubmedArticle>
    <MedlineCitation>
      <PMID>12345678</PMID>
      <Article>
        <ArticleTitle>Example title for a demo citation</ArticleTitle>
        <AuthorList>
          <Author><LastName>Example</LastName><ForeName>Ada</ForeName></Author>
          <Author><CollectiveName>Demo Research Group</CollectiveName></Author>
        </AuthorList>
        <Journal>
          <Title>Journal of Demonstration</Title>
          <JournalIssue><PubDate><Year>2025</Year></PubDate></JournalIssue>
        </Journal>
        <Abstract>
          <AbstractText Label='BACKGROUND'>First abstract section.</AbstractText>
          <AbstractText Label='CONCLUSION'>Second abstract section.</AbstractText>
        </Abstract>
      </Article>
    </MedlineCitation>
    <PubmedData><ArticleIdList>
      <ArticleId IdType='doi'>10.1000/demo.123</ArticleId>
    </ArticleIdList></PubmedData>
  </PubmedArticle>
</PubmedArticleSet>
"""


def test_search_pubmed_parses_citation_and_abstract(monkeypatch: pytest.MonkeyPatch) -> None:
    responses = [
        json.dumps({"esearchresult": {"idlist": ["12345678"]}}).encode(),
        ARTICLE_XML,
    ]
    requested_urls: list[str] = []

    def fake_request(url: str) -> bytes:
        requested_urls.append(url)
        return responses.pop(0)

    monkeypatch.setattr(pubmed, "_request_bytes", fake_request)

    results = pubmed.search_pubmed("fictional topic", retmax=3)

    assert len(results) == 1
    assert results[0]["pmid"] == "12345678"
    assert results[0]["title"] == "Example title for a demo citation"
    assert results[0]["authors"] == "Ada Example, Demo Research Group"
    assert results[0]["year"] == "2025"
    assert "BACKGROUND: First abstract section." in results[0]["abstract"]
    assert results[0]["doi"] == "10.1000/demo.123"
    assert results[0]["url"] == "https://pubmed.ncbi.nlm.nih.gov/12345678/"
    assert parse_qs(urlparse(requested_urls[0]).query)["db"] == ["pubmed"]
    assert parse_qs(urlparse(requested_urls[0]).query)["term"] == ["fictional topic"]
    assert parse_qs(urlparse(requested_urls[1]).query)["id"] == ["12345678"]


@pytest.mark.parametrize("query", ["", "   "])
def test_search_rejects_empty_query(query: str) -> None:
    with pytest.raises(ValueError, match="Enter search terms"):
        pubmed.search_pubmed(query)


def test_search_rejects_result_limit_outside_supported_range() -> None:
    with pytest.raises(ValueError, match="between 1 and 10"):
        pubmed.search_pubmed("topic", retmax=11)


def test_search_returns_empty_list_when_no_pmids(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(
        pubmed,
        "_request_bytes",
        lambda url: b'{"esearchresult":{"idlist":[]}}',
    )

    assert pubmed.search_pubmed("no matching demo term") == []