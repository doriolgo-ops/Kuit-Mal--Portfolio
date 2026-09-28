"""Resumable pipeline: each stage is idempotent and records completion per material.

Stages: init -> search -> fetch -> extract -> dedupe -> validate -> propose -> report
Material states: NOT_STARTED, SEARCHING, SOURCES_FOUND, EXTRACTED, NEEDS_REVIEW, VALIDATED,
NO_PUBLIC_DATA_FOUND, PUBLIC_RESEARCH_EXHAUSTED (never set in a pilot), ERROR.
"""
import hashlib
import json
import re
import traceback
from collections import Counter

from rapidfuzz import fuzz

from . import apis, db, extract, identity, normalize
from .common import (ADDITIVE_CAS, CONFIG, DOMAINS, INGEST, MANIFESTS, ROOT, SETTINGS, canonical_url, domain_info, find_cas, get_logger,
                     load_json, norm_text, now_iso, registered_domain, short)
from .fetch import fetch
from .master import load_snapshot, master_sha256, summarize, write_snapshot_file

log = get_logger("pipeline")
TIER_WEIGHT = {"OFFICIAL_MANUFACTURER": 10, "PATENT": 5, "PEER_REVIEWED": 6, "DISTRIBUTOR": 6, "IDENTITY_DB": 4,
               "REGULATORY": 4, "RETAILER": 4, "SECONDARY_DB": 2, "SECONDARY": 1, "STANDARDS_BODY": 2}
EVIDENCE_BY_TIER = {"OFFICIAL_MANUFACTURER": "MANUFACTURER", "DISTRIBUTOR": "DISTRIBUTOR_SPEC",
                    "RETAILER": "RETAILER (SECONDARY CLAIM)", "PEER_REVIEWED": "PUBLISHED", "PATENT": "PATENT",
                    "IDENTITY_DB": "REFERENCE_IDENTITY", "SECONDARY_DB": "SECONDARY_REFERENCE",
                    "REGULATORY": "REGULATORY", "STANDARDS_BODY": "STANDARD_METADATA", "SECONDARY": "SECONDARY_REFERENCE"}


def pilot():
    return load_json(CONFIG / "pilot_materials.json")


def pilot_ids():
    return [m["palette_id"] for m in pilot()["materials"]]


def expected_mfr(pid):
    return next((m.get("expected_manufacturer") for m in pilot()["materials"] if m["palette_id"] == pid), None)


# ============================================================================ init
def stage_init(con):
    ids = pilot_ids()
    per_mat, headers, registries = load_snapshot(ids)
    sha = master_sha256()
    snap = {"master_file": SETTINGS["master_path"], "master_sha256": sha, "taken_at": now_iso(),
            "materials": {p: summarize(p, per_mat[p]) for p in ids}, "headers": headers,
            "licensing_audit": registries["SOURCE LICENSING AUDIT"],
            "source_registry_ids": [r.get("source_id") for r in registries["SOURCE REGISTRY"]]}
    write_snapshot_file(MANIFESTS / "master_snapshot.json", snap)
    groups = {m["palette_id"]: m["group"] for m in pilot()["materials"]}
    for pid in ids:
        s = snap["materials"][pid]
        con.execute("INSERT INTO materials(palette_id, school_name, pilot_group, chart_kind, master_json, updated_at)"
                    " VALUES (?,?,?,?,?,?) ON CONFLICT(palette_id) DO UPDATE SET master_json=excluded.master_json",
                    (pid, s["school_name"], groups[pid], s["chart_kind"], json.dumps(s, default=str), now_iso()))
    con.commit()
    log.info("init: %d materials, master sha256 %s", len(ids), sha[:12])


# ============================================================================ search
def _lead_priority(lead, variants, cas=()):
    info = domain_info(lead["url"])
    p = TIER_WEIGHT.get(info["tier"], 1) + 1.0 / max(1, lead["rank"])
    t = norm_text(lead.get("title", ""))
    u = lead["url"].lower()
    if u.endswith(".pdf") or ".pdf?" in u:
        p += 1.5
    if re.search(r"sds|msds|safety data|fds", t + " " + u):
        p += 2.5
    if any(v in t or v.replace(" ", "-") in u for v in variants) or any(c in t for c in cas):
        p += 2
    elif info["tier"] != "OFFICIAL_MANUFACTURER":
        p -= 3
    return p, info["tier"]


def stage_search(con, pid):
    master = db.master_record(con, pid)
    db.set_state(con, pid, "SEARCHING", "ingesting search results + API lookups")
    # links are rebuilt by search/fetch; PubChem links are kept (API results are not re-requested)
    con.execute("DELETE FROM doc_material WHERE palette_id=? AND doc_id NOT IN (SELECT doc_id FROM documents WHERE tier='IDENTITY_DB')", (pid,))
    variants, _, _ = identity.name_variants(master)
    f = INGEST / f"{pid}.json"
    if f.exists():
        data = load_json(f)
        for q in data.get("queries", []):
            cur = con.execute("INSERT OR IGNORE INTO queries(palette_id, query, purpose, provider, executed_at, n_results, provider_summary)"
                              " VALUES (?,?,?,?,?,?,?)", (pid, q["query"], q.get("purpose"), q.get("provider", "claude_websearch"),
                                                          q.get("executed_at"), len(q.get("results", [])), q.get("provider_summary", "")))
            qid = cur.lastrowid or con.execute("SELECT id FROM queries WHERE palette_id=? AND provider=? AND query=?",
                                               (pid, q.get("provider", "claude_websearch"), q["query"])).fetchone()["id"]
            for r in q.get("results", []):
                if not r.get("url", "").startswith("http"):
                    continue
                pr, tier = _lead_priority(r, variants, master.get("master_cas_set") or [])
                con.execute("INSERT INTO leads(palette_id, query_id, rank, url, canonical_url, title, domain, tier, priority)"
                            " VALUES (?,?,?,?,?,?,?,?,?) ON CONFLICT(palette_id, query_id, canonical_url) DO UPDATE SET"
                            " priority=excluded.priority, tier=excluded.tier", (pid, qid, r.get("rank"), r["url"], canonical_url(r["url"]),
                                                            r.get("title", ""), registered_domain(r["url"]), tier, pr))
    else:
        log.warning("%s: no search ingest file (search layer not yet run)", pid)
    con.commit()
    api_errors = _api_searches(con, pid, master, variants)
    # select leads: best priority per canonical URL, all official-manufacturer leads, top-N overall
    rows = con.execute("SELECT canonical_url, MAX(priority) p, tier FROM leads WHERE palette_id=? GROUP BY canonical_url"
                       " ORDER BY p DESC", (pid,)).fetchall()
    chosen = [r["canonical_url"] for r in rows if r["tier"] == "OFFICIAL_MANUFACTURER"]
    for r in rows:
        if len(chosen) >= SETTINGS["max_leads_fetched_per_material"]:
            break
        if r["canonical_url"] not in chosen:
            chosen.append(r["canonical_url"])
    con.execute("UPDATE leads SET selected=0 WHERE palette_id=?", (pid,))
    for c in chosen:
        con.execute("UPDATE leads SET selected=1 WHERE palette_id=? AND canonical_url=?", (pid, c))
    con.commit()
    n = con.execute("SELECT COUNT(DISTINCT canonical_url) n FROM leads WHERE palette_id=?", (pid,)).fetchone()["n"]
    if api_errors:
        log.warning("%s: %d API lookups failed; search stage left open for resume", pid, api_errors)
    else:
        db.mark_stage(con, pid, "search")
    log.info("%s: %d distinct leads, %d selected for fetch", pid, n, len(chosen))


def _add_api_query(con, pid, provider, query, purpose, n):
    con.execute("INSERT OR IGNORE INTO queries(palette_id, query, purpose, provider, executed_at, n_results) VALUES (?,?,?,?,?,?)",
                (pid, query, purpose, provider, now_iso(), n))
    con.commit()


def _link_api_doc(con, pid, doc_id, note):
    con.execute("INSERT OR IGNORE INTO doc_material(doc_id, palette_id, match_class, reasons, accepted) VALUES (?,?,?,?,?)",
                (doc_id, pid, None, note, None))
    con.commit()


def _api_searches(con, pid, master, variants):
    # PubChem: by each master CAS (synthetics) or by trade-name variants when CAS is missing
    lookups = []
    if master.get("chart_kind") == "Synthetic":
        lookups = [("cas", c) for c in (master.get("master_cas_set") or [])[:3]]
        if not lookups:
            lookups = [("name", v) for v in variants[:4]]
    api_errors = 0
    done = {r["query"] for r in con.execute("SELECT query FROM queries WHERE palette_id=? AND provider='pubchem_api'", (pid,))}
    for how, q in lookups:
        if f"{how}:{q}" in done:
            continue
        res = apis.pubchem_lookup(con, q)
        if res == "API_ERROR":
            api_errors += 1
            continue
        _add_api_query(con, pid, "pubchem_api", f"{how}:{q}", "identity", 1 if res else 0)
        if res:
            for d in res["doc_ids"] + ([res["ghs"]["doc_id"]] if res["ghs"]["doc_id"] else []):
                _link_api_doc(con, pid, d, json.dumps({"pubchem_query": q, "by": how, "cid": res["cid"], "n_cids": res["n_cids"]}))
    # NCBI PMC (open access) for naturals
    term = apis.PMC_QUERIES.get(pid)
    if term:
        ids = apis.pmc_search(term)
        summ = apis.pmc_summaries(ids)
        _add_api_query(con, pid, "ncbi_pmc_api", term, "natural_gcms", len(ids))
        genus_terms = [s.split()[0] for s in identity.EXPECTED_SPECIES.get(pid, [])] + \
                      [a.split()[0] for a in identity.EXTRA_ALIASES.get(pid, [])]
        picked = 0
        for i in ids:
            t = summ.get(i, {}).get("title", "")
            if picked >= SETTINGS["ncbi_max_articles_per_natural"]:
                break
            if not any(g.lower() in t.lower() for g in genus_terms):
                continue
            if not re.search(r"(?i)essential oil|absolute|composition|constituent|volatile|gc|chemical|chemotype|headspace|oil", t) \
                    or re.search(r"(?i)virus|genom|transcriptom|hydrosol|antibacterial activity of essential oils from", t):
                continue
            title = f"{t} ({summ[i].get('journal')}, {summ[i].get('pubdate')}) doi:{summ[i].get('doi')} PMC{i}"
            try:
                d = apis.pmc_fetch_xml(con, i, title)
                _link_api_doc(con, pid, d, json.dumps({"pmcid": i, "doi": summ[i].get("doi")}))
                picked += 1
            except Exception as exc:
                log.warning("PMC fetch %s failed: %s", i, exc)
                api_errors += 1
    return api_errors


# ============================================================================ fetch
PMC_RE = re.compile(r"(?:ncbi\.nlm\.nih\.gov/pmc/articles|pmc\.ncbi\.nlm\.nih\.gov/articles)/PMC(\d+)", re.I)
DOI_RE = re.compile(r"(?:doi\.org/|/doi/(?:abs/|full/|pdf/)?)(10\.\d{4,9}/[^\s?#]+)", re.I)
MDPI_RE = re.compile(r"mdpi\.com/(\d{4}-\d{4})/(\d+)/(\d+)/(\d+)")


SKIP_URL_RE = re.compile(r"^https?://[^/]+/?$|/sitemap|/search\?|/cart|/login|/account", re.I)


def stage_fetch(con, pid):
    """Walk leads by priority until the budget of successfully retrieved documents is reached.
    Leads on domains already known to block automated access are logged (MANUAL_RETRIEVAL_REQUIRED)
    without sending a request, so they do not consume the budget."""
    leads = con.execute("SELECT canonical_url, MIN(url) url, MAX(title) title, MAX(priority) p FROM leads WHERE palette_id=?"
                        " GROUP BY canonical_url ORDER BY p DESC", (pid,)).fetchall()
    budget, fetched, attempts = SETTINGS["max_leads_fetched_per_material"], 0, 0
    con.execute("UPDATE leads SET selected=0 WHERE palette_id=?", (pid,))
    for ld in leads:
        if fetched >= budget or attempts >= 2.5 * budget:
            break
        url = ld["url"]
        if SKIP_URL_RE.search(url):
            continue
        con.execute("UPDATE leads SET selected=1 WHERE palette_id=? AND canonical_url=?", (pid, ld["canonical_url"]))
        attempts += 1
        # open-access articles: use the official PMC API instead of scraping publisher pages
        m = PMC_RE.search(url)
        if m:
            try:
                d = apis.pmc_fetch_xml(con, m.group(1), ld["title"] or f"PMC{m.group(1)}")
                _link_api_doc(con, pid, d, json.dumps({"pmcid": m.group(1), "via": "lead"}))
                fetched += 1
            except Exception as exc:
                log.warning("PMC API failed for %s: %s", url, exc)
            continue
        res = fetch(con, url)
        if res.get("doc_id"):
            fetched += 1
            _link_api_doc(con, pid, res["doc_id"], json.dumps({"lead_url": url}))
        elif res["status"] in ("MANUAL_RETRIEVAL_REQUIRED", "ROBOTS_DISALLOWED", "HTTP_ERROR", "ENV_UNREACHABLE"):
            # a blocked publisher article may exist in the PMC open-access archive (same article, official route)
            doi = DOI_RE.search(url)
            if doi:
                try:
                    pmcid = apis.doi_to_pmcid(doi.group(1))
                    if pmcid:
                        d = apis.pmc_fetch_xml(con, pmcid, (ld["title"] or "") + f" doi:{doi.group(1)} PMC{pmcid}")
                        _link_api_doc(con, pid, d, json.dumps({"pmcid": pmcid, "doi": doi.group(1), "via": "idconv"}))
                        fetched += 1
                except Exception as exc:
                    log.warning("PMC idconv failed for %s: %s", url, exc)
    con.commit()
    n_docs = con.execute("SELECT COUNT(*) n FROM doc_material WHERE palette_id=?", (pid,)).fetchone()["n"]
    db.set_state(con, pid, "SOURCES_FOUND" if n_docs else "SEARCHING",
                 f"{n_docs} documents retrieved ({fetched} this run)" if n_docs else "no document retrievable")
    db.mark_stage(con, pid, "fetch")


# ============================================================================ extract + identity
def _claim_id(pid, doc_id, field, value):
    return hashlib.sha1(f"{pid}|{doc_id}|{field}|{value}".encode()).hexdigest()[:16]


def stage_extract(con, pid):
    master = db.master_record(con, pid)
    exp = expected_mfr(pid)
    exp_sp = identity.EXPECTED_SPECIES.get(pid, [])
    species_terms = exp_sp + ([s for s in identity.CONFUSER_SPECIES if not any(e.startswith(s) or s.startswith(e) for e in exp_sp)]
                              if master.get("chart_kind") == "Natural" else [])
    markers = apis.MARKERS.get(pid, [])
    con.execute("DELETE FROM claims WHERE palette_id=?", (pid,))
    links = con.execute("SELECT dm.doc_id, dm.reasons, d.* FROM doc_material dm JOIN documents d ON d.doc_id=dm.doc_id"
                        " WHERE dm.palette_id=?", (pid,)).fetchall()
    for doc in links:
        try:
            if doc["doc_kind"] == "API" and doc["content_type"] == "json":
                _extract_pubchem(con, pid, master, doc)
                continue
            if doc["content_type"] == "xml" and doc["tier"] == "PEER_REVIEWED":
                _extract_pmc(con, pid, master, doc, markers)
                continue
            title, text, pairs = extract.load_text(doc)
            if title and not doc["title"]:
                con.execute("UPDATE documents SET title=? WHERE doc_id=?", (title, doc["doc_id"]))
            text, pairs, content_note = _strip_boilerplate(con, doc, text, pairs)
            kind = "SDS" if extract.is_sds(text) else ("PDF" if doc["content_type"] == "pdf" else "HTML")
            if FORMULA_DOC_RE.search(doc["first_url"] + " " + (title or "")) and kind != "SDS":
                kind = "FORMULA"
            if content_note:
                kind = "NO_CONTENT"
            con.execute("UPDATE documents SET doc_kind=? WHERE doc_id=?", (kind, doc["doc_id"]))
            text_path = ROOT / "data" / "text" / f"{doc['doc_id']}.txt"
            text_path.parent.mkdir(parents=True, exist_ok=True)
            text_path.write_text(text, encoding="utf-8")
            con.execute("UPDATE documents SET text_path=? WHERE doc_id=?", (str(text_path.relative_to(ROOT)), doc["doc_id"]))
            raw = [] if kind in ("FORMULA", "NO_CONTENT") else \
                extract.extract_claims(title, text, pairs, species_terms=species_terms, marker_terms=markers)
            for c in raw:
                if c["field"] in ("cas", "cas_mentioned", "sds_component_cas") and c["raw_value"] in ADDITIVE_CAS:
                    c["field"] = "additive_cas"
                    c["context"] = short(f"{ADDITIVE_CAS[c['raw_value']]}: " + c["context"], 200)
            raw = [c for c in raw if not (c["field"] in normalize.NUMERIC_FIELDS and not re.search(r"\d|trace", c["raw_value"], re.I))]
            raw = [c for c in raw if not (c["field"] == "use_level" and (not re.search(r"%|ppm|trace", c["raw_value"], re.I)
                                                                        or re.search(r"mg\s*/\s*kg", c["raw_value"], re.I)))]
            third_party_mfr = None
            if kind == "SDS" and doc["tier"] != "OFFICIAL_MANUFACTURER":
                s1 = norm_text(extract.sds_sections(text).get(1, text[:3000])[:3000])
                for key, aliases in DOMAINS["manufacturer_aliases"].items():
                    if any(re.search(r"(?<![a-z])" + re.escape(norm_text(a)) + r"(?![a-z])", s1) for a in aliases if len(a) > 3):
                        third_party_mfr = key
                        break
            if kind == "FORMULA":
                raw = [{"field": "formula_document", "raw_value": short(title or doc["first_url"], 120),
                        "context": "manufacturer/other formula document mentioning the material (routed to formula pipeline)",
                        "extractor": "formula_router"}]
            cas_lab = [c["raw_value"] for c in raw if c["field"] == "cas"]
            cas_any = [c["raw_value"] for c in raw if c["field"] in ("cas_mentioned", "sds_component_cas")]
            mclass, score, reasons = identity.classify(master, exp, doc, (title or doc["title"] or "") + " " + doc["first_url"],
                                                       text, cas_lab, cas_any)
            accepted = mclass in identity.ACCEPTED
            if content_note:
                reasons.append(content_note)
            if third_party_mfr:
                reasons.append(f"SDS issued by {third_party_mfr} (section 1), hosted by a third party")
            if kind == "FORMULA":
                reasons.append("formula document -> formula pipeline (no material claims)")
            con.execute("UPDATE doc_material SET match_class=?, match_score=?, reasons=?, accepted=?, reject_reason=? WHERE doc_id=? AND palette_id=?",
                        (mclass, score, "; ".join(reasons), 1 if accepted else 0,
                         None if accepted else "; ".join(reasons[-2:]), doc["doc_id"], pid))
            if mclass == "REJECTED":
                continue
            for c in raw:
                ev = None
                if third_party_mfr and third_party_mfr in (exp or third_party_mfr):
                    ev = f"MANUFACTURER_SDS_VIA_THIRD_PARTY ({third_party_mfr})"
                _insert_claim(con, pid, doc, c, mclass, kind, evidence_level=ev)
        except Exception as exc:
            log.error("%s extract failed on %s: %s\n%s", pid, doc["doc_id"][:12], exc, traceback.format_exc())
            con.execute("UPDATE doc_material SET match_class='ERROR', reasons=? WHERE doc_id=? AND palette_id=?",
                        (f"extract error: {exc}", doc["doc_id"], pid))
    con.commit()
    db.set_state(con, pid, "EXTRACTED", f"{con.execute('SELECT COUNT(*) n FROM claims WHERE palette_id=?', (pid,)).fetchone()['n']} claims")
    db.mark_stage(con, pid, "extract")


FORMULA_DOC_RE = re.compile(r"(?i)_formula\.pdf|demo[ -]?formula|/formulas?/|formulation examples?")
_BOILER = {}


def _strip_boilerplate(con, doc, text, pairs):
    """Remove lines shared by several documents of the same domain (menus, footers, cookie banners).
    Pages whose remaining content is tiny (JavaScript-rendered shops) are flagged NO_CONTENT."""
    if doc["content_type"] != "html":
        return text, pairs, None
    dom = doc["domain"]
    if dom not in _BOILER:
        others = con.execute("SELECT doc_id, raw_path FROM documents WHERE domain=? AND content_type='html'", (dom,)).fetchall()
        counts, mats = Counter(), {}
        if len(others) >= 2:
            for o in others:
                _, t, _ = extract.load_text(dict(o) | {"content_type": "html"})
                pids = {r["palette_id"] for r in con.execute("SELECT palette_id FROM doc_material WHERE doc_id=?", (o["doc_id"],))}
                for ln in {ln.strip() for ln in t.splitlines() if ln.strip()}:
                    counts[ln] += 1
                    mats.setdefault(ln, set()).update(pids)
        # a line is template only if it recurs on pages about different materials (or on many pages);
        # two copies of the same product page (e.g. page + print view) must not erase the product itself
        _BOILER[dom] = {ln for ln, n in counts.items()
                        if (n >= 2 and len(mats.get(ln, ())) >= 2 and n >= 0.5 * len(others)) or n >= max(4, 0.6 * len(others))}
    bp = _BOILER[dom]
    if not bp:
        return text, pairs, None
    kept = [ln for ln in text.splitlines() if ln.strip() and ln.strip() not in bp]
    content = "\n".join(kept)
    pairs = [p for p in pairs if p[2] in ("html_property", "html_intro") or f"{p[0]}: {p[1]}".strip() not in bp and p[1].strip() not in bp]
    if len(content) < 150:
        return content, [], f"NO_CONTENT: only site template after removing {len(bp)} shared lines (page likely rendered by JavaScript)"
    return content, pairs, None


def _scope(mclass, tier, field, kind):
    if tier == "PEER_REVIEWED":
        return "REFERENCE_COMPOSITION" if field.startswith("composition:") else "PUBLISHED_REFERENCE"
    if tier == "IDENTITY_DB":
        return "SUBSTANCE_LEVEL (not the commercial grade)"
    if mclass in identity.GRADE_LEVEL_OK:
        return "COMMERCIAL_GRADE" + (" (SDS of this product)" if kind == "SDS" else "")
    if mclass == "EXACT_CAS_ONLY":
        return "CHEMICAL_LEVEL (grade unconfirmed)"
    return "UNCONFIRMED_IDENTITY"


def _insert_claim(con, pid, doc, c, mclass, kind, evidence_level=None, extra_note=""):
    n = normalize.normalize(c["field"], c["raw_value"])
    ev = evidence_level or EVIDENCE_BY_TIER.get(doc["tier"], "SECONDARY_REFERENCE")
    if n.get("implausible"):
        extra_note = (extra_note + "; IMPLAUSIBLE value (parser or unit problem) -> excluded").strip("; ")
    if n.get("bound"):
        extra_note = (extra_note + f"; BOUND {n['bound']}").strip("; ")
    if kind == "SDS" and not evidence_level:
        ev = {"MANUFACTURER": "MANUFACTURER_SDS", "DISTRIBUTOR_SPEC": "DISTRIBUTOR_SDS"}.get(ev, ev + " SDS")
    con.execute("INSERT OR REPLACE INTO claims(claim_id, palette_id, doc_id, url, field, raw_value, context, extractor,"
                " evidence_level, tier, license_class, match_class, scope, norm_value, norm_min, norm_max, norm_unit,"
                " norm_text, norm_note, validation, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (_claim_id(pid, doc["doc_id"], c["field"], c["raw_value"]), pid, doc["doc_id"], doc["first_url"], c["field"],
                 c["raw_value"], c["context"], c["extractor"], ev, doc["tier"], doc["license_class"], mclass,
                 _scope(mclass, doc["tier"], c["field"], kind), n["norm_value"], n["norm_min"], n["norm_max"], n["norm_unit"],
                 n["norm_text"], (n["norm_note"] + ("; " + extra_note if extra_note else "")).strip("; "), None, now_iso()))


def _extract_pubchem(con, pid, master, doc):
    data = json.loads((ROOT / doc["raw_path"]).read_text())
    meta = json.loads(con.execute("SELECT reasons FROM doc_material WHERE doc_id=? AND palette_id=?",
                                  (doc["doc_id"], pid)).fetchone()["reasons"] or "{}") if True else {}
    by = meta.get("by", "cas") if isinstance(meta, dict) else "cas"
    mclass = "EXACT_CAS_ONLY" if by == "cas" else "LIKELY_MATCH"
    reasons = f"PubChem lookup by {by} '{meta.get('pubchem_query')}' -> CID {meta.get('cid')} ({meta.get('n_cids')} CIDs)"
    claims = []
    if "PropertyTable" in data:
        p = data["PropertyTable"]["Properties"][0]
        for f, k in (("molecular_formula", "MolecularFormula"), ("molecular_weight", "MolecularWeight"),
                     ("chemical_name", "IUPACName"), ("logp_computed", "XLogP")):
            if p.get(k) is not None:
                claims.append({"field": f, "raw_value": str(p[k]), "context": f"PubChem CID {p.get('CID')} {k}", "extractor": "pubchem_props"})
    elif "InformationList" in data:
        syns = (data["InformationList"].get("Information") or [{}])[0].get("Synonym", [])
        variants, _, _ = identity.name_variants(master)
        trade = [s for s in syns if norm_text(s) in variants or any(v == norm_text(s).replace(" r ", " ") for v in variants)]
        for s in trade[:3]:
            claims.append({"field": "synonym_trade_name", "raw_value": s, "context": f"PubChem synonym list of CID {meta.get('cid')}", "extractor": "pubchem_synonyms"})
        cas_syn = [s for s in syns if find_cas(s) == [s]]
        for s in cas_syn[:4]:
            claims.append({"field": "cas", "raw_value": s, "context": f"PubChem synonym list of CID {meta.get('cid')} (CAS-format synonyms: {len(cas_syn)})", "extractor": "pubchem_synonyms"})
        if by == "name" and not trade:
            mclass = "AMBIGUOUS"
            reasons += "; trade name not confirmed in synonyms"
        elif by == "name" and trade:
            mclass = "LIKELY_MATCH"
            reasons += f"; trade name '{trade[0]}' present in PubChem synonyms (depositor-supplied, unverified)"
    elif "Record" in data:
        blob = json.dumps(data)
        for h in sorted(set(re.findall(r"\b(H[234]\d{2})\b", blob))):
            claims.append({"field": "h_statement_substance", "raw_value": h, "context": "PubChem GHS classification (aggregated C&L notifications; pure substance, NOT the commercial grade)", "extractor": "pubchem_ghs"})
        m = re.search(r'"String": "(Danger|Warning)"', blob)
        if m:
            claims.append({"field": "signal_word_substance", "raw_value": m.group(1), "context": "PubChem GHS signal word (substance level)", "extractor": "pubchem_ghs"})
    con.execute("UPDATE doc_material SET match_class=?, match_score=?, reasons=?, accepted=? WHERE doc_id=? AND palette_id=?",
                (mclass, 0.6 if mclass == "EXACT_CAS_ONLY" else 0.5, reasons, 1 if mclass in identity.ACCEPTED else 0, doc["doc_id"], pid))
    for c in claims:
        _insert_claim(con, pid, doc, c, mclass, "API")


def _extract_pmc(con, pid, master, doc, markers):
    xml = (ROOT / doc["raw_path"]).read_bytes()
    rows = apis.parse_pmc_tables(xml, markers)
    text = re.sub(r"<[^>]+>", " ", xml.decode("utf-8", "ignore"))
    species = identity.EXPECTED_SPECIES.get(pid, [])
    low = text.lower()
    sp_hit = [s for s in species if s in low]
    mclass = "LIKELY_MATCH" if sp_hit or any(a.split()[0] in (doc["title"] or "").lower() for a in identity.EXTRA_ALIASES.get(pid, [])) else "AMBIGUOUS"
    reasons = f"peer-reviewed article; species {'found: ' + sp_hit[0] if sp_hit else 'NOT found'}; REFERENCE_COMPOSITION only (research sample, not the school bottle)"
    con.execute("UPDATE doc_material SET match_class=?, match_score=?, reasons=?, accepted=? WHERE doc_id=? AND palette_id=?",
                (mclass, 0.7 if sp_hit else 0.4, reasons, 1 if mclass in identity.ACCEPTED else 0, doc["doc_id"], pid))
    doi = re.search(r"doi:(\S+)", doc["title"] or "")
    _insert_claim(con, pid, doc, {"field": "gcms_study", "raw_value": short(doc["title"], 250), "context": f"{len(rows)} marker rows parsed from composition tables",
                                  "extractor": "pmc_meta"}, mclass, "XML")
    best = {}
    for r in rows:
        key = r["marker"].replace("α", "alpha-").replace("β", "beta-").replace("γ", "gamma-").replace("--", "-")
        vals = best.setdefault(key, {"values": [], "ctx": r["context"], "cols": []})
        vals["values"].extend(r["values"])
        vals["cols"].extend(r.get("columns", []))
    for mk, v in best.items():
        vals = v["values"]
        raw = f"{min(vals)}-{max(vals)}" if len(set(vals)) > 1 else f"{vals[0]}"
        _insert_claim(con, pid, doc, {"field": f"composition:{mk}", "raw_value": raw, "context": v["ctx"], "extractor": "pmc_table"},
                      mclass, "XML", extra_note=f"n_values={len(vals)}; columns: {'; '.join(dict.fromkeys(v['cols']))[:120]}; "
                                                "relative GC peak area % unless paper states otherwise")
    for s in sp_hit[:1]:
        _insert_claim(con, pid, doc, {"field": "botanical_name", "raw_value": s, "context": "species named in article", "extractor": "pmc_species"}, mclass, "XML")
    for m in set(re.findall(r"\bISO\s?(\d{3,5})(?::\s?(\d{4}))?", text)):
        if m[0] in ("4716", "9842", "7609", "4733", "3520", "3063", "3515", "3757", "3518"):
            _insert_claim(con, pid, doc, {"field": "iso_standard", "raw_value": f"ISO {m[0]}" + (f":{m[1]}" if m[1] else ""),
                                          "context": "ISO standard cited in article", "extractor": "pmc_iso"}, mclass, "XML")


# ============================================================================ dedupe
def stage_dedupe(con):
    """Exact duplicates are already merged by sha256. Here: near-duplicates (same document served
    by several URLs/mirrors) and derived copies (distributor text reproducing manufacturer text)."""
    docs = con.execute("SELECT * FROM documents WHERE text_path IS NOT NULL AND doc_kind NOT IN ('NO_CONTENT','API')"
                       " ORDER BY CASE tier WHEN 'OFFICIAL_MANUFACTURER' THEN 0"
                       " WHEN 'DISTRIBUTOR' THEN 1 ELSE 2 END, fetched_at").fetchall()
    texts = {d["doc_id"]: (ROOT / d["text_path"]).read_text(encoding="utf-8")[:30000] for d in docs}
    docs = [d for d in docs if len(texts[d["doc_id"]]) >= 300]   # boilerplate already removed at extraction
    con.execute("UPDATE documents SET duplicate_of=NULL, duplicate_basis=NULL, derived_from=NULL")
    for i, a in enumerate(docs):
        for b in docs[i + 1:]:
            if b["duplicate_of"]:
                continue
            ta, tb = texts[a["doc_id"]], texts[b["doc_id"]]
            if not ta or not tb:
                continue
            same_title = a["title"] and norm_text(a["title"]) == norm_text(b["title"] or "") and a["domain"] != b["domain"]
            ratio = fuzz.ratio(ta[:8000], tb[:8000]) if abs(len(ta) - len(tb)) < 0.3 * max(len(ta), len(tb)) else 0
            if ratio >= 93 or (same_title and ratio >= 88):
                con.execute("UPDATE documents SET duplicate_of=?, duplicate_basis=? WHERE doc_id=?",
                            (a["doc_id"], f"text similarity {ratio:.0f}%" + ("; same title" if same_title else ""), b["doc_id"]))
    # derived descriptions: identical odour description text on two domains
    rows = con.execute("SELECT claim_id, palette_id, doc_id, tier, norm_text FROM claims WHERE field='odour_description'").fetchall()
    for i, a in enumerate(rows):
        for b in rows[i + 1:]:
            if a["palette_id"] == b["palette_id"] and a["doc_id"] != b["doc_id"] and \
                    fuzz.token_set_ratio(a["norm_text"], b["norm_text"]) >= 90:
                src, cop = (a, b) if a["tier"] == "OFFICIAL_MANUFACTURER" or b["tier"] != "OFFICIAL_MANUFACTURER" else (b, a)
                con.execute("UPDATE documents SET derived_from=? WHERE doc_id=? AND derived_from IS NULL", (src["doc_id"], cop["doc_id"]))
    # independent groups: root document of every claim
    for c in con.execute("SELECT claim_id, doc_id FROM claims").fetchall():
        root, seen = c["doc_id"], set()
        while root not in seen:
            seen.add(root)
            d = con.execute("SELECT duplicate_of, derived_from FROM documents WHERE doc_id=?", (root,)).fetchone()
            nxt = d and (d["duplicate_of"] or d["derived_from"])
            if not nxt:
                break
            root = nxt
        con.execute("UPDATE claims SET independent_group=? WHERE claim_id=?", (root, c["claim_id"]))
    con.commit()


# ============================================================================ validate
TOL = {"vapour_pressure": ("rel", 0.30), "density": ("abs", 0.012), "refractive_index": ("abs", 0.004),
       "flash_point": ("abs", 6), "logp": ("abs", 0.6), "tenacity": ("rel", 0.5), "boiling_point": ("abs", 8),
       "molecular_weight": ("abs", 0.6)}


def _val(c):
    for k in ("norm_value", "norm_max", "norm_min"):
        if c[k] is not None:
            return c[k]
    return None


def _differs(field, a, b):
    kind, tol = TOL[field]
    if kind == "abs":
        return abs(a - b) > tol
    return abs(a - b) > tol * max(abs(a), abs(b), 1e-12)


TIER_RANK = {"OFFICIAL_MANUFACTURER": 3, "DISTRIBUTOR": 2, "PEER_REVIEWED": 2, "PATENT": 2, "REGULATORY": 2,
             "IDENTITY_DB": 1, "RETAILER": 1, "SECONDARY_DB": 1, "SECONDARY": 1, "STANDARDS_BODY": 1}


def _rank(c):
    r = TIER_RANK.get(c["tier"], 1)
    if (c["evidence_level"] or "").startswith("MANUFACTURER_SDS_VIA_THIRD_PARTY"):
        r = 2  # manufacturer document, but not retrieved from the manufacturer: never promoted to rank 3
    return r


def _bound(c):
    m = re.search(r"BOUND ([<>])", c["norm_note"] or "")
    return m.group(1) if m else None


def _disagree(field, a, b):
    va, vb = _val(a), _val(b)
    if field in ("density", "refractive_index") and a["norm_min"] is not None and b["norm_min"] is not None:
        tol = TOL[field][1]   # specification ranges agree when they overlap (within tolerance)
        return a["norm_min"] - tol > b["norm_max"] or b["norm_min"] - tol > a["norm_max"]
    ba, bb = _bound(a), _bound(b)
    if ba == ">" and bb == ">" or ba == "<" and bb == "<":
        return False
    if ba == ">":
        return vb < va - (TOL[field][1] if TOL[field][0] == "abs" else 0)
    if bb == ">":
        return va < vb - (TOL[field][1] if TOL[field][0] == "abs" else 0)
    if ba == "<":
        return vb > va * 1.05
    if bb == "<":
        return va > vb * 1.05
    return _differs(field, va, vb)


def stage_validate(con, pid):
    """Conflicts are detected between INDEPENDENT sources only (duplicates/derived copies collapse to one).
    - disagreement among the highest-rank sources present -> CONFLICT (value blocked, all claims kept)
    - lower-rank source contradicting a higher-rank one     -> conflict recorded; higher-rank claims become
      VALID_DISPUTED (proposable, but only for human review), dissenting claims CONFLICT.
    Nothing is ever overwritten."""
    master = db.master_record(con, pid)
    con.execute("DELETE FROM conflicts WHERE palette_id=?", (pid,))
    claims = [dict(c) for c in con.execute("SELECT * FROM claims WHERE palette_id=?", (pid,)).fetchall()]
    for c in claims:
        if "IMPLAUSIBLE" in (c["norm_note"] or ""):
            c["validation"], c["validation_note"] = "REJECTED", "implausible value (parser/unit problem)"
        elif c["match_class"] == "AMBIGUOUS":
            c["validation"], c["validation_note"] = "NEEDS_REVIEW", "identity ambiguous"
        elif c["license_class"] == "UNKNOWN_LICENSE" and c["tier"] != "OFFICIAL_MANUFACTURER":
            c["validation"], c["validation_note"] = "NEEDS_REVIEW", "licence unknown"
        else:
            c["validation"], c["validation_note"] = "VALID", ""
    conflicts = []
    usable = [c for c in claims if c["match_class"] in identity.ACCEPTED and c["validation"] != "REJECTED"]

    def record(field, members, detail, includes_master=False, master_value=None, blocking=True):
        cid = f"CF-{pid}-{field}".replace(":", "_")[:60]
        vals = [{"claim_id": m["claim_id"], "value": m["raw_value"], "url": m["url"], "tier": m["tier"]} for m in members]
        if includes_master:
            vals.append({"claim_id": "MASTER", "value": master_value, "url": "Perroco_Lab_Research_Master_v2.xlsx", "tier": "MASTER"})
        conflicts.append((cid, field, vals, includes_master, detail + ("" if blocking else " [lower-tier dissent only]")))

    def ranked_conflict(field, members, disagree, detail):
        roots = {}
        for c in members:
            roots.setdefault(c["independent_group"] or c["doc_id"], c)
        reps = list(roots.values())
        pairs = [(a, b) for i, a in enumerate(reps) for b in reps[i + 1:] if disagree(a, b)]
        if not pairs:
            return
        top = max(_rank(c) for c in reps)
        blocking = any(_rank(a) == top and _rank(b) == top for a, b in pairs)
        dissent_roots = {x["independent_group"] or x["doc_id"] for a, b in pairs for x in (a, b) if _rank(x) < top}
        for c in members:
            g = c["independent_group"] or c["doc_id"]
            if blocking:
                c["validation"], c["validation_note"] = "CONFLICT", detail
            elif g in dissent_roots:
                c["validation"], c["validation_note"] = "CONFLICT", detail + " (dissents from higher-rank source)"
            elif _rank(c) == top and c["validation"] in ("VALID", "NEEDS_REVIEW"):
                c["validation"], c["validation_note"] = "VALID_DISPUTED", detail + " (a lower-rank source disagrees)"
        record(field, members, detail, blocking=blocking)

    for field in TOL:
        grp = [c for c in usable if c["field"] == field and _val(c) is not None]
        ranked_conflict(field, grp, lambda a, b, f=field: _disagree(f, a, b), f"{field}: independent sources disagree beyond tolerance {TOL[field]}")
        if field == "vapour_pressure" and master.get("vp_pa") and master.get("vp_basis") == "SUPPLIER_PUBLISHED":
            off = [c for c in grp if c["tier"] == "OFFICIAL_MANUFACTURER" and _differs(field, _val(c), float(master["vp_pa"]))]
            if off:
                for c in off:
                    c["validation"], c["validation_note"] = "CONFLICT", "manufacturer VP differs from master supplier VP"
                record(field, off, "manufacturer VP differs from master supplier VP", True, master["vp_pa"])

    def dose_disagree(a, b):
        amax = a["norm_max"] if a["norm_max"] is not None else a["norm_value"]
        bmax = b["norm_max"] if b["norm_max"] is not None else b["norm_value"]
        amin, bmin = a["norm_min"] or 0, b["norm_min"] or 0
        if amax is None or bmax is None:
            return False
        return amin > bmax * 1.25 or bmin > amax * 1.25 or (min(amax, bmax) > 0 and max(amax, bmax) > 2.5 * min(amax, bmax))
    doses = [c for c in usable if c["field"] == "use_level" and (c["norm_max"] is not None or c["norm_value"] is not None)]
    ranked_conflict("use_level", doses, dose_disagree, "recommended use levels from independent sources do not agree")
    master_dose = [r for r in master.get("dose_rows", []) if r.get("dose_type") == "SUPPLIER_RECOMMENDATION"]
    for r in master_dose:
        mv = r.get("value_max")
        for c in doses:
            cv = c["norm_max"] if c["norm_max"] is not None else c["norm_value"]
            if mv and cv and c["tier"] == "OFFICIAL_MANUFACTURER" and max(mv, cv) > 2.5 * min(mv, cv):
                record("use_level", [c], "manufacturer dose differs from master supplier dose", True, r.get("value_text"))

    # CAS: labelled identity CAS vs master set (additives already separated)
    mset = set(master.get("master_cas_set") or [])
    lab = [c for c in usable if c["field"] == "cas" and c["tier"] != "IDENTITY_DB"]
    if mset:
        off = [c for c in lab if c["norm_text"] not in mset]
        if off:
            top = max(_rank(c) for c in lab)
            blocking = any(_rank(c) == top for c in off)
            for c in off:
                c["validation"], c["validation_note"] = "CONFLICT", "CAS not in master CAS set"
            record("cas", off + [c for c in lab if c["norm_text"] in mset], "source CAS not in master CAS set", True,
                   " | ".join(sorted(mset)), blocking=blocking)
    else:
        distinct = {c["norm_text"] for c in lab}
        if len(distinct) > 1:
            for c in lab:
                c["validation"], c["validation_note"] = "CONFLICT", f"sources give different CAS {sorted(distinct)}"
            record("cas", lab, f"sources give different CAS numbers {sorted(distinct)} (master has none)")
    # botanical identity vs master
    if master.get("chart_kind") == "Natural":
        exp = identity.EXPECTED_SPECIES.get(pid, [])
        bots = [c for c in usable if c["field"] == "botanical_name"]
        mb = (master.get("botanical_species") or "").lower()
        if exp and mb and not any(e.split()[0] in mb for e in exp):
            support = [c for c in bots if c["norm_text"].lower() in exp]
            if support:
                record("botanical_species", support, f"sources identify {support[0]['norm_text']}; master says '{master.get('botanical_species')}'",
                       True, master.get("botanical_species"))
    # H statements: different SDS (different suppliers/grades) are reported, never merged
    sds_h = {}
    for c in usable:
        if c["field"] == "h_statement":
            sds_h.setdefault(c["independent_group"] or c["doc_id"], set()).add(c["norm_text"])
    sets = list(sds_h.values())
    if len(sets) > 1 and any(x != sets[0] for x in sets[1:]):
        record("h_statement", [c for c in usable if c["field"] == "h_statement"],
               "SDS from different suppliers/grades list different H statements (reported per SDS; not merged)", blocking=False)
    for c in claims:
        con.execute("UPDATE claims SET validation=?, validation_note=? WHERE claim_id=?", (c["validation"], c["validation_note"], c["claim_id"]))
    for cid, field, vals, im, detail in conflicts:
        cid = cid + ("-M" if im else "")
        con.execute("INSERT OR REPLACE INTO conflicts(conflict_id, palette_id, field, claim_ids, values_json, includes_master, detail)"
                    " VALUES (?,?,?,?,?,?,?)", (cid, pid, field, json.dumps([v["claim_id"] for v in vals]), json.dumps(vals), int(im), detail))
    con.commit()
    db.mark_stage(con, pid, "validate")
