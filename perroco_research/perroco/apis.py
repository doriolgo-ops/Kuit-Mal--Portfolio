"""Documented public APIs used as deterministic (non-search-engine) sources.

* PubChem PUG-REST / PUG-View (NIH): identity, synonyms, substance-level GHS (C&L notifications).
* NCBI E-utilities (PMC open-access subset): peer-reviewed GC-MS papers for naturals.

Every API response is stored as a raw document (sha256, cache file) exactly like a web page,
so provenance and de-duplication work the same way.
"""
import hashlib
import json
import re
import xml.etree.ElementTree as ET

from .common import CACHE, ROOT, SETTINGS, canonical_url, get_logger, now_iso, find_cas
from .fetch import api_get

log = get_logger("apis")
PUG = "https://pubchem.ncbi.nlm.nih.gov/rest/pug"
PUGVIEW = "https://pubchem.ncbi.nlm.nih.gov/rest/pug_view"
EUTILS = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"

# constituents used to read GC-MS tables (markers, not a full profile)
MARKERS = {
    "N-0775": ["khusimol", "vetiselinenol", "isovalencenol", "alpha-vetivone", "α-vetivone", "beta-vetivone", "β-vetivone",
               "zizanoic acid", "khusenic acid", "prezizaene", "beta-vetispirene", "β-vetispirene", "cyclocopacamphenol"],
    "N-0697": ["citronellol", "geraniol", "nerol", "2-phenylethyl alcohol", "phenylethyl alcohol", "phenyl ethyl alcohol",
               "methyl eugenol", "eugenol", "nonadecane", "heneicosane", "geranyl acetate", "linalool"],
    "N-0623": ["linalyl acetate", "linalool", "germacrene d", "sclareol", "alpha-terpineol", "α-terpineol",
               "geranyl acetate", "neryl acetate", "beta-caryophyllene", "β-caryophyllene", "caryophyllene"],
    "N-0632": ["1,8-cineole", "alpha-terpinyl acetate", "α-terpinyl acetate", "linalool", "linalyl acetate",
               "limonene", "sabinene", "alpha-terpineol", "α-terpineol", "geraniol"],
    "N-0556": ["limonene", "linalyl acetate", "linalool", "gamma-terpinene", "γ-terpinene", "beta-pinene", "β-pinene",
               "bergapten", "bergamottin", "sabinene"],
    "N-0728": ["methyl benzoate", "methyl anthranilate", "benzyl benzoate", "methyl salicylate", "indole",
               "eugenol", "geraniol", "1,8-cineole", "benzyl alcohol", "farnesol"],
}
PMC_QUERIES = {
    "N-0775": '(vetiver[Title] OR "Chrysopogon zizanioides"[Title] OR "Vetiveria zizanioides"[Title]) AND (GC-MS OR "gas chromatography") AND oil',
    "N-0697": '("Rosa damascena"[Title] OR "rose oil"[Title]) AND (GC-MS OR "gas chromatography") AND (oil OR otto)',
    "N-0623": '("Salvia sclarea"[Title] OR "clary sage"[Title]) AND (GC-MS OR "gas chromatography") AND "essential oil"',
    "N-0632": '("Elettaria cardamomum"[Title] OR cardamom[Title]) AND (GC-MS OR "gas chromatography") AND "essential oil"',
    "N-0556": '(bergamot[Title] OR "Citrus bergamia"[Title]) AND (GC-MS OR "gas chromatography" OR composition) AND oil',
    "N-0728": '("Polianthes tuberosa"[Title] OR tuberose[Title]) AND (GC-MS OR "gas chromatography" OR volatile)',
}


def store_api_doc(con, url, body, kind, tier, license_class, title):
    doc_id = hashlib.sha256(body).hexdigest()
    path = CACHE / doc_id[:2] / f"{doc_id}.{kind}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(body)
    canon = canonical_url(url)
    con.execute("INSERT OR IGNORE INTO documents(doc_id, first_url, canonical_url, domain, tier, manufacturer, license_class,"
                " content_type, doc_kind, title, raw_path, bytes, fetched_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (doc_id, url, canon, re.sub(r"https?://([^/]+)/.*", r"\1", url), tier, None, license_class, kind,
                 "API", title[:200], str(path.relative_to(ROOT)), len(body), now_iso()))
    con.execute("INSERT OR IGNORE INTO doc_urls(doc_id, canonical_url) VALUES (?,?)", (doc_id, canon))
    con.execute("INSERT OR REPLACE INTO fetch_log(canonical_url,url,final_url,domain,status,http_status,doc_id,note,at)"
                " VALUES (?,?,?,?,?,?,?,?,?)", (canon, url, url, "api", "FETCHED", 200, doc_id, "public API", now_iso()))
    con.commit()
    return doc_id


# ----------------------------------------------------------------------------- PubChem
def pubchem_lookup(con, query, by="name"):
    """Return dict(cid, doc_ids, props, synonyms, cas_in_synonyms, ghs) or None."""
    try:
        res = api_get(f"{PUG}/compound/name/{query}/cids/JSON", min_interval=1.0)
    except Exception as exc:
        log.warning("pubchem cid lookup failed for %s: %s", query, exc)
        return "API_ERROR"
    if not res or "IdentifierList" not in res:
        return None
    cids = res["IdentifierList"]["CID"]
    cid = cids[0]
    out = {"cid": cid, "n_cids": len(cids), "doc_ids": []}
    url = f"{PUG}/compound/cid/{cid}/property/MolecularFormula,MolecularWeight,IUPACName,XLogP/JSON"
    props = api_get(url, min_interval=1.0)
    out["doc_ids"].append(store_api_doc(con, url, json.dumps(props).encode(), "json", "IDENTITY_DB",
                                        "PRODUCTION_SAFE_WITH_ATTRIBUTION", f"PubChem CID {cid} properties"))
    out["props"] = props["PropertyTable"]["Properties"][0]
    url = f"{PUG}/compound/cid/{cid}/synonyms/JSON"
    syn = api_get(url, min_interval=1.0) or {}
    out["doc_ids"].append(store_api_doc(con, url, json.dumps(syn).encode(), "json", "IDENTITY_DB",
                                        "PRODUCTION_SAFE_WITH_ATTRIBUTION", f"PubChem CID {cid} synonyms"))
    syns = (syn.get("InformationList", {}).get("Information") or [{}])[0].get("Synonym", [])
    out["synonyms"] = syns
    out["cas_in_synonyms"] = [s for s in syns if find_cas(s) == [s]]
    url = f"{PUGVIEW}/data/compound/{cid}/JSON?heading=GHS+Classification"
    try:
        ghs = api_get(url, min_interval=1.0)
    except Exception:
        ghs = None
    out["ghs"] = {"h": [], "signal": None, "doc_id": None}
    if ghs:
        out["ghs"]["doc_id"] = store_api_doc(con, url, json.dumps(ghs).encode(), "json", "IDENTITY_DB",
                                             "PRODUCTION_SAFE_WITH_ATTRIBUTION", f"PubChem CID {cid} GHS classification")
        blob = json.dumps(ghs)
        out["ghs"]["h"] = sorted(set(re.findall(r"\b(H[234]\d{2})\b", blob)))
        m = re.search(r'"String": "(Danger|Warning)"', blob)
        out["ghs"]["signal"] = m.group(1) if m else None
    return out


# ----------------------------------------------------------------------------- NCBI PMC
def pmc_search(term, retmax=12):
    res = api_get(f"{EUTILS}/esearch.fcgi", params={"db": "pmc", "term": term + " AND open access[filter]",
                                                    "retmode": "json", "retmax": retmax, "sort": "relevance"},
                  min_interval=SETTINGS["ncbi_min_interval_s"])
    return res.get("esearchresult", {}).get("idlist", [])


def pmc_summaries(ids):
    if not ids:
        return {}
    res = api_get(f"{EUTILS}/esummary.fcgi", params={"db": "pmc", "id": ",".join(ids), "retmode": "json"},
                  min_interval=SETTINGS["ncbi_min_interval_s"])
    out = {}
    for i in ids:
        r = res.get("result", {}).get(i, {})
        doi = next((a["value"] for a in r.get("articleids", []) if a.get("idtype") == "doi"), None)
        out[i] = {"title": r.get("title", ""), "journal": r.get("fulljournalname", ""), "pubdate": r.get("pubdate", ""), "doi": doi}
    return out


def pmc_fetch_xml(con, pmcid, title):
    url = f"{EUTILS}/efetch.fcgi?db=pmc&id={pmcid}&rettype=xml"
    body = api_get(f"{EUTILS}/efetch.fcgi", params={"db": "pmc", "id": pmcid, "rettype": "xml"},
                   min_interval=SETTINGS["ncbi_min_interval_s"], as_json=False)
    return store_api_doc(con, url, body, "xml", "PEER_REVIEWED", "PRODUCTION_SAFE_WITH_CITATION", title)


def doi_to_pmcid(doi):
    try:
        res = api_get("https://www.ncbi.nlm.nih.gov/pmc/utils/idconv/v1.0/", params={"ids": doi, "format": "json"},
                      min_interval=SETTINGS["ncbi_min_interval_s"])
        rec = (res or {}).get("records", [{}])[0]
        return rec.get("pmcid", "").replace("PMC", "") or None
    except Exception:
        return None


def _num(s):
    s = s.replace(",", ".").strip()
    m = re.fullmatch(r"(\d{1,3}(?:\.\d+)?)", s)
    return float(m.group(1)) if m else None


GOOD_COL = re.compile(r"(?i)%|area|rel\.?|relative|content|abundance|amount|conc|sample|oil|\beo\b|mean|average|value|peak")
BAD_COL = re.compile(r"(?i)\brt\b|r\.t|retention|\bri\b|\bki\b|\blri\b|\bai\b|index|mg|µg|ug/|intake|lod|loq|recover|rsd|\bsd\b|"
                     r"std|cas|formula|mw|identif|method|class|match|similar|odou?r|ion|m/z|exposure|margin|noael|group|fl-?\s?no|flavis|\bno\.?$|number")
BAD_TABLE = re.compile(r"(?i)gas(eous)? phase|vapou?r phase|headspace|air sample|emission|validation|calibration|intake|exposure|"
                       r"margin|recover|linearity|limit of|antimicrob|mic\b|inhibition|docking|binding")


def _norm_marker(x):
    x = x.lower().replace("α", "alpha-").replace("β", "beta-").replace("γ", "gamma-").replace("δ", "delta-")
    return re.sub(r"-+", "-", x).strip()


def parse_pmc_tables(xml_bytes, markers):
    """Extract marker constituents from GC-MS composition tables of a JATS article.

    Only columns whose header reads as a relative amount (%, area, content, sample/oil name...) are
    read; retention time/index, mg/kg, intake, validation or headspace tables are skipped. A table
    without a recognisable amount column is skipped entirely. Values must be 0-100.
    Returns list of dict(marker, values, table_label, columns, context).
    """
    out = []
    try:
        root = ET.fromstring(xml_bytes)
    except ET.ParseError:
        return out
    marks = [(mk, _norm_marker(mk)) for mk in markers]
    for tw in root.iter("table-wrap"):
        cap = tw.find("caption")
        label = " ".join((tw.findtext("label") or "", "".join(cap.itertext()) if cap is not None else ""))
        label = re.sub(r"\s+", " ", label).strip()
        if not re.search(r"(?i)composition|constituent|compound|gc|chemical|volatile|component|profile", label) or BAD_TABLE.search(label):
            continue
        header_rows = [tr for th in tw.iter("thead") for tr in th.iter("tr")]
        heads = []
        for tr in header_rows:
            cells = ["".join(c.itertext()).strip() for c in tr if c.tag in ("td", "th")]
            if len(cells) > len(heads):
                heads = cells
        if not heads:
            continue
        good = [j for j, h in enumerate(heads) if j > 0 and GOOD_COL.search(h) and not BAD_COL.search(h)]
        if not good:
            # headers are only sample codes (e.g. 'S1', 'Clone 3'): accept them when no column is clearly non-amount
            good = [j for j, h in enumerate(heads) if j > 0 and h and not BAD_COL.search(h) and len(h) <= 25]
            if not good or len(good) == len(heads) - 1 and len(heads) <= 2:
                continue
        body = [tr for tb in tw.iter("tbody") for tr in tb.iter("tr")] or list(tw.iter("tr"))[len(header_rows):]
        for tr in body:
            cells = ["".join(td.itertext()).strip() for td in tr if td.tag in ("td", "th")]
            if len(cells) < 2:
                continue
            name_idx = next((j for j, c in enumerate(cells[:3]) if re.search(r"[A-Za-zα-ω]{4,}", c)), None)
            if name_idx is None:
                continue
            nm = _norm_marker(cells[name_idx])
            nm = re.sub(r"^\(?[ez]\)?-", "", nm).strip()
            for mk, mkn in marks:
                if nm == mkn or re.fullmatch(re.escape(mkn) + r"\s*(\(.*\))?\s*[a-z*,†‡§]{0,3}", nm):
                    vals, cols = [], []
                    for j in good:
                        if j < len(cells) and j != name_idx:
                            m = re.match(r"\s*(\d{1,3}(?:[.,]\d+)?)", cells[j])
                            if m:
                                v = float(m.group(1).replace(",", "."))
                                if v <= 100:
                                    vals.append(v)
                                    cols.append(heads[j][:20])
                    if vals:
                        out.append({"marker": mk, "values": vals, "table_label": label[:150], "columns": cols,
                                    "context": f"{label[:70]} | {cells[name_idx][:30]}: " +
                                               ", ".join(f"{c}={v}" for c, v in list(zip(cols, vals))[:6])})
                    break
    return out
