# Search protocol (search layer of the pipeline)

Automated search engines are NOT usable from the container (Google/Bing robots.txt
disallow /search; DuckDuckGo connection is dropped by the egress proxy; no search-API
key is configured). The search layer is therefore executed by the operator agent with
its WebSearch tool, and every query + raw result list is stored verbatim in
`data/search_ingest/<palette_id>.json`. The pipeline code then fetches, caches,
classifies and extracts from the returned URLs itself (respecting robots.txt).

Search results are LEADS, never evidence. The `provider_summary` text is kept only as a
hint (evidence_level = SEARCH_SUMMARY, never auto-eligible).

## File format
{
  "palette_id": "S-0372",
  "school_name_exact": "FLORHYDRAL TOCO (ELINCS)",
  "searched_by": "operator-agent (WebSearch tool)",
  "queries": [
    {"query": "Florhydral Givaudan", "purpose": "manufacturer_page",
     "executed_at": "2026-09-28T11:00:00Z", "provider": "claude_websearch",
     "results": [{"rank": 1, "title": "...", "url": "https://..."}],
     "provider_summary": "verbatim summary text returned by the tool (hint only)"}
  ]
}

## Query plan per material (6-9 queries)
Synthetics: `<trade name> <manufacturer>`; `<trade name> CAS`; `<trade name> safety data sheet`;
`<trade name> use level` ; `<trade name> <manufacturer> pdf`; `<trade name> odor vapor pressure`;
optional `<trade name> patent`.
Naturals: `<name> <supplier>`; `<species> <part> essential oil GC-MS composition`;
`<material> ISO standard`; `<material> safety data sheet`; `<material> chemotype origin`;
`<material> use level perfumery`.
Difficult: name variants (drop grade suffixes TOCO/PRG/EXT/TM/ELINCS), `<name> IFF`, `<name> CAS`.
