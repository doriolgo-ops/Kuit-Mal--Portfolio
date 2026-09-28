"""Formula research infrastructure (prepared in the pilot; bulk harvesting is a later phase).

Staging tables:
  formula_leads        candidate formula documents found by the search layer (URL, source type, status)
  formula_records      one formula version (source, application, total, dilution basis)
  formula_ingredients  one line per ingredient, with the palette link level from CONTROLLED VOCABULARY
                       (EXACT_TRADE_NAME, CHEMICAL, RELATED_GRADE, RELATED_NATURAL, TRADE_NAME, AMBIGUOUS,
                        CLOSE_MATERIAL, NO_PALETTE_MATCH, SOLVENT_CARRIER ...)

Source types: MANUFACTURER_DEMO, PATENT, PROFESSIONAL_PUBLIC, EDUCATIONAL, HISTORICAL.
Same rules as the material pipeline: raw document cached with hash, never written to the master,
ambiguous ingredient links are excluded from dose statistics.
"""
import re

from . import identity
from .common import canonical_url, domain_info, norm_text, now_iso

SCHEMA = """
CREATE TABLE IF NOT EXISTS formula_leads (
  canonical_url TEXT PRIMARY KEY, url TEXT, title TEXT, source_type TEXT, found_for TEXT, status TEXT DEFAULT 'NOT_STARTED', at TEXT);
CREATE TABLE IF NOT EXISTS formula_records (
  formula_id TEXT PRIMARY KEY, doc_id TEXT, url TEXT, source_type TEXT, name TEXT, application TEXT,
  total_parts REAL, dosage_in_product TEXT, license_class TEXT, notes TEXT);
CREATE TABLE IF NOT EXISTS formula_ingredients (
  formula_id TEXT, line_no INTEGER, name_as_printed TEXT, parts REAL, dilution_note TEXT,
  palette_id TEXT, link_level TEXT, link_reason TEXT, PRIMARY KEY(formula_id, line_no));
"""
FORMULA_HINT = re.compile(r"formula|formulation|demo|accord|recipe|brief|fragrance composition|example \d", re.I)


def source_type(url, title):
    tier = domain_info(url)["tier"]
    if tier == "OFFICIAL_MANUFACTURER":
        return "MANUFACTURER_DEMO"
    if tier == "PATENT" or "patent" in url:
        return "PATENT"
    if re.search(r"school|course|lesson|educat|university", (title or "") + url, re.I):
        return "EDUCATIONAL"
    if re.search(r"19[0-8]\d|vintage|histor", title or "", re.I):
        return "HISTORICAL"
    return "PROFESSIONAL_PUBLIC"


def harvest_leads(con):
    """Collect formula-like leads already returned by the search layer (no extra searching)."""
    con.executescript(SCHEMA)
    n = 0
    for r in con.execute("SELECT palette_id, url, title FROM leads").fetchall():
        if FORMULA_HINT.search((r["title"] or "") + " " + r["url"]) and (r["url"].lower().endswith(".pdf") or "patent" in r["url"]):
            con.execute("INSERT OR IGNORE INTO formula_leads(canonical_url, url, title, source_type, found_for, at) VALUES (?,?,?,?,?,?)",
                        (canonical_url(r["url"]), r["url"], r["title"], source_type(r["url"], r["title"]), r["palette_id"], now_iso()))
            n += 1
    con.commit()
    return n


def link_ingredient(name_as_printed, palette_masters):
    """Match one formula line to palette materials. Returns (palette_id|None, link_level, reason)."""
    n = norm_text(re.sub(r"\b\d+(\.\d+)?\s*%.*", "", name_as_printed))
    if re.search(r"\b(dpg|dipropylene glycol|ethanol|alcohol|ipm|isopropyl myristate|tec|triethyl citrate|benzyl benzoate)\b", n) \
            and len(n.split()) <= 3:
        return None, "SOLVENT_CARRIER", "solvent/carrier line"
    hits = []
    for m in palette_masters:
        variants, _, _ = identity.name_variants(m)
        if any(v == n or re.search(r"(?<![a-z0-9])" + re.escape(v) + r"(?![a-z0-9])", n) for v in variants):
            hits.append(m["palette_id"])
    if len(hits) == 1:
        return hits[0], "EXACT_TRADE_NAME", "trade/common name match"
    if len(hits) > 1:
        return None, "AMBIGUOUS", f"several palette candidates: {hits[:5]}"
    return None, "NO_PALETTE_MATCH", "no palette name matched"
