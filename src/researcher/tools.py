"""Research tools: OpenAlex metadata search, Crossref DOI lookup, and local PDF retrieval."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import httpx
from agents import function_tool

from .config import CHROMA_PATH, OPENALEX_MAX_RESULTS


def _clean(value: Any) -> str:
    return str(value or "").strip()


@function_tool
async def search_openalex(query: str, max_results: int = OPENALEX_MAX_RESULTS) -> str:
    """Search OpenAlex for scholarly works. Returns titles, authors, years, DOI and landing URLs."""
    params = {
        "search": query,
        "per-page": max(1, min(int(max_results), 20)),
        "sort": "relevance_score:desc",
        "select": "id,doi,title,publication_year,authorships,primary_location,cited_by_count,type",
    }
    async with httpx.AsyncClient(timeout=30) as client:
        response = await client.get("https://api.openalex.org/works", params=params)
        response.raise_for_status()
        payload = response.json()

    rows = []
    for item in payload.get("results", []):
        authors = []
        for authorship in (item.get("authorships") or [])[:5]:
            author = (authorship.get("author") or {}).get("display_name")
            if author:
                authors.append(author)
        location = item.get("primary_location") or {}
        source = (location.get("source") or {}).get("display_name")
        rows.append({
            "title": item.get("title"),
            "year": item.get("publication_year"),
            "authors": authors,
            "doi": item.get("doi"),
            "url": (location.get("landing_page_url") or item.get("doi") or item.get("id")),
            "venue": source,
            "cited_by_count": item.get("cited_by_count"),
            "type": item.get("type"),
        })
    return str(rows) if rows else "No OpenAlex works found for this query."


@function_tool
async def lookup_crossref_doi(doi: str) -> str:
    """Look up DOI metadata in Crossref. Use to validate bibliographic metadata, not paper conclusions."""
    doi = doi.strip().replace("https://doi.org/", "").replace("http://doi.org/", "")
    async with httpx.AsyncClient(timeout=25) as client:
        response = await client.get(f"https://api.crossref.org/works/{doi}")
        response.raise_for_status()
        item = response.json().get("message", {})
    return str({
        "DOI": item.get("DOI"),
        "title": item.get("title"),
        "author": item.get("author"),
        "published": item.get("published-print") or item.get("published-online") or item.get("created"),
        "container-title": item.get("container-title"),
        "publisher": item.get("publisher"),
        "type": item.get("type"),
        "URL": item.get("URL"),
    })


@function_tool
def search_local_research_library(query: str, n_results: int = 5) -> str:
    """Search PDFs previously indexed into the local Chroma research library."""
    try:
        import chromadb
        client = chromadb.PersistentClient(path=CHROMA_PATH)
        collection = client.get_or_create_collection("research_papers")
        if collection.count() == 0:
            return "The local research library is empty. Add PDFs with the ingest command."
        result = collection.query(query_texts=[query], n_results=max(1, min(n_results, 10)))
        docs = result.get("documents", [[]])[0]
        metas = result.get("metadatas", [[]])[0]
        out = []
        for doc, meta in zip(docs, metas):
            out.append({"source": meta.get("source"), "page": meta.get("page"), "text": doc})
        return str(out) if out else "No matching passages found in the local library."
    except Exception as exc:
        return f"Local library search unavailable: {type(exc).__name__}: {exc}"


@function_tool
def list_supported_domains() -> str:
    """Return the specialist research domains supported by this assistant."""
    return (
        "Chemical engineering: separations, reaction engineering, catalysis, process systems, "
        "adsorption, membranes, process safety, scale-up. Sustainability: LCA, carbon accounting, "
        "circularity, EPD, industrial decarbonization. Environmental science: water/wastewater, "
        "air pollution, remediation, waste management, environmental monitoring. Industrial AI: "
        "predictive maintenance, optimization, digital twins, process analytics, computer vision, "
        "industrial agents and deployment."
    )
