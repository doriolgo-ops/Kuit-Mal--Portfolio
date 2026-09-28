"""PROPOSED CHANGE layer. Produces reviewable changes against existing master sheets/columns only.

review_status:
  AUTO_ELIGIBLE     exact identity (EXACT_GRADE / EXACT_NAME_MANUFACTURER) from the official manufacturer,
                    no conflict. Still NOT applied in the pilot.
  NEEDS_REVIEW      distributor/retailer/secondary source, LIKELY_MATCH identity, parser output to spot-check.
  BLOCKED_CONFLICT  the value is part of a CONFLICT; both/all claims are kept, nothing is overwritten.
The master workbook is never modified by this module.
"""
import hashlib
import json
import re
from datetime import date

from . import db, identity
from .common import OUTPUT, find_cas, short

TODAY = date.today().isoformat()
PHYS_MAP = {  # field -> (property name in PHYSICOCHEMICAL DATA, unit template)
    "vapour_pressure": ("vapor_pressure_supplier", "Pa"),
    "logp": ("logP_supplier", "log10 (octanol/water)"),
    "density": ("density_20C", "g/mL"),
    "refractive_index": ("refractive_index_20C", "nD20"),
    "flash_point": ("flash_point", "C"),
    "boiling_point": ("boiling_point_normal", "degC"),
    "physical_state": ("physical_state", None),
    "solubility": ("solubility", None),
    "ec_number": ("EC_number", None),
    "fema": ("FEMA_number", None),
}
VALUE_TYPE = {"OFFICIAL_MANUFACTURER": "MANUFACTURER", "DISTRIBUTOR": "DISTRIBUTOR_SPECIFICATION",
              "RETAILER": "RETAILER (SECONDARY CLAIM)", "PEER_REVIEWED": "MEASURED_PUBLISHED"}
NEW_SOURCES = {
    "PEER_REVIEWED": ("SRC-PMC-OA-GCMS", "PMC open-access GC-MS articles (via NCBI E-utilities)", "Peer-reviewed literature",
                      "PRODUCTION_SAFE_WITH_CITATION"),
    "IDENTITY_DB": ("SRC-PUBCHEM-API", "PubChem PUG-REST / PUG-View (direct API)", "Reference identity",
                    "PRODUCTION_SAFE_WITH_ATTRIBUTION"),
    "PATENT": ("SRC-PATENTS", "Patent documents (Google Patents)", "Patent", "PRODUCTION_SAFE_WITH_CITATION"),
}
MASTER_SRC = {"OFFICIAL_MANUFACTURER": "SRC-SUPPLIER-PAGE", "DISTRIBUTOR": "SRC-DISTRIBUTOR-SPEC", "RETAILER": "SRC-RETAILER-PAGE",
              "SECONDARY_DB": "SRC-SCENTREE / PATENTS / DOI (legacy)", "PEER_REVIEWED": "SRC-PMC-OA-GCMS",
              "IDENTITY_DB": "SRC-PUBCHEM-API", "PATENT": "SRC-PATENTS"}


def _cid(pid, sheet, key):
    return "PC-" + hashlib.sha1(f"{pid}|{sheet}|{key}".encode()).hexdigest()[:10]


def _status(c, auto_ok):
    if c["validation"] == "CONFLICT":
        return "BLOCKED_CONFLICT"
    if not c.get("expected_mfr_ok"):
        return "NEEDS_REVIEW"
    if auto_ok and c["tier"] == "OFFICIAL_MANUFACTURER" and c["match_class"] in identity.GRADE_LEVEL_OK and c["validation"] == "VALID":
        return "AUTO_ELIGIBLE"
    return "NEEDS_REVIEW"


def _conf(c):
    if c["match_class"] == "EXACT_GRADE":
        return "HIGH"
    if c["match_class"] == "EXACT_NAME_MANUFACTURER":
        return "HIGH" if c["tier"] == "OFFICIAL_MANUFACTURER" else "MEDIUM"
    if c["match_class"] in ("EXACT_CAS_ONLY", "LIKELY_MATCH"):
        return "MEDIUM" if c["tier"] in ("OFFICIAL_MANUFACTURER", "PEER_REVIEWED", "IDENTITY_DB") else "LOW"
    return "LOW"


def build(con, pid):
    master = db.master_record(con, pid)
    con.execute("DELETE FROM proposed_changes WHERE palette_id=?", (pid,))
    claims = [dict(c) for c in con.execute(
        "SELECT c.*, d.title doc_title, d.duplicate_of, d.derived_from, d.manufacturer, dm.reasons FROM claims c JOIN documents d ON d.doc_id=c.doc_id"
        " JOIN doc_material dm ON dm.doc_id=c.doc_id AND dm.palette_id=c.palette_id"
        " WHERE c.palette_id=? AND c.match_class NOT IN ('REJECTED','ERROR') AND c.validation != 'REJECTED'", (pid,)).fetchall()]
    from .pipeline import expected_mfr
    exp = expected_mfr(pid)
    aliases = [a.lower() for a in identity.manufacturer_aliases(exp)] if exp else []
    for c in claims:
        # a manufacturer page can only be auto-eligible if the school bottle's manufacturer is known and is that one
        c["expected_mfr_ok"] = bool(exp) and any(a in (c.get("manufacturer") or "").lower() for a in aliases)
    changes = []

    def add(sheet, op, payload, c_or_list, rationale, status=None, conf=None):
        cl = c_or_list if isinstance(c_or_list, list) else [c_or_list]
        st = status or _status(cl[0], True)
        key = json.dumps(payload, sort_keys=True, default=str)
        changes.append({
            "change_id": _cid(pid, sheet, key), "palette_id": pid, "school_name_exact": master.get("school_name"),
            "target_sheet": sheet, "operation": op, "payload": payload, "review_status": st,
            "confidence": conf or _conf(cl[0]), "rationale": rationale,
            "evidence": [{"claim_id": c["claim_id"], "url": c["url"], "doc_sha256": c["doc_id"], "tier": c["tier"],
                          "evidence_level": c["evidence_level"], "match_class": c["match_class"], "license_class": c["license_class"],
                          "raw_value": c["raw_value"], "context": c["context"]} for c in cl],
        })

    def independent(cs):
        """One claim per independent source; prefer the root document (not its duplicate) and parsed values."""
        best = {}
        for c in cs:
            g = c["independent_group"] or c["doc_id"]
            key = (c["doc_id"] == g, c["norm_value"] is not None or c["norm_max"] is not None)
            if g not in best or key > best[g][0]:
                best[g] = (key, c)
        return [v[1] for v in best.values()]

    # ---- dose
    master_dose_urls = {str(r.get("source_detail")) for r in master.get("dose_rows", [])}
    for c in independent([c for c in claims if c["field"] == "use_level"]):
        if c["url"] in master_dose_urls:
            continue
        manu = c["tier"] == "OFFICIAL_MANUFACTURER"
        row = {"palette_id": pid, "school_name_exact": master.get("school_name"),
               "dose_type": "SUPPLIER_RECOMMENDATION" if manu else "SECONDARY_REFERENCE_MAX_USE",
               "value_min": c["norm_min"], "value_max": c["norm_max"] if c["norm_max"] is not None else c["norm_value"],
               "value_text": c["raw_value"], "unit": "%", "denominator": "NOT STATED by source",
               "application": "not specified (general perfumery)", "active_basis": "as supplied",
               "identity_scope": c["scope"], "source_id": MASTER_SRC.get(c["tier"], "SRC-DISTRIBUTOR-SPEC"),
               "source_detail": c["url"], "evidence_class": c["evidence_level"]}
        add("DOSE EVIDENCE STRUCTURED", "APPEND_ROW", row, c,
            f"{'Manufacturer' if manu else c['tier'].title()} use level; identity {c['match_class']}")
    # ---- physico-chemical
    master_phys = {(r.get("property"), str(r.get("value"))) for r in master.get("physchem_rows", [])}
    for field, (prop, unit) in PHYS_MAP.items():
        for c in independent([c for c in claims if c["field"] == field]):
            if c["match_class"] == "AMBIGUOUS" or c["tier"] in ("IDENTITY_DB", "RETAILER", "SECONDARY", "SECONDARY_DB"):
                continue  # retailer/secondary physico-chemical values stay in staging (reported, not proposed)
            val = c["norm_value"] if c["norm_value"] is not None else c["norm_text"]
            bnd = re.search(r"BOUND ([<>])", c["norm_note"] or "")
            if bnd and c["norm_value"] is not None:
                val = f"{bnd.group(1)}{c['norm_value']}"
            if (prop, str(val)) in master_phys:
                continue
            u = c["norm_unit"] or unit
            if field == "vapour_pressure":
                u = f"Pa ({c['norm_note']})"
            row = {"palette_id": pid, "school_name_exact": master.get("school_name"),
                   "matched_cas": master.get("resolved_cas"), "property": prop, "value": val, "unit": u,
                   "value_type": VALUE_TYPE.get(c["tier"], "SECONDARY_REFERENCE"), "method": f"{c['extractor']}; raw '{short(c['raw_value'], 80)}'",
                   "source_id": MASTER_SRC.get(c["tier"], "SRC-DISTRIBUTOR-SPEC"), "identity_tier": master.get("identity_tier"),
                   "_source_url": c["url"]}
            add("PHYSICOCHEMICAL DATA", "APPEND_ROW", row, c, f"{prop} from {c['tier']} ({c['match_class']})")
    # ---- performance
    for c in independent([c for c in claims if c["field"] in ("tenacity", "substantivity_application")]):
        if c["match_class"] == "AMBIGUOUS":
            continue
        is_ten = c["field"] == "tenacity"
        row = {"palette_id": pid, "school_name_exact": master.get("school_name"),
               "property": "tenacity_on_blotter_supplier" if is_ten else "substantivity_application_supplier",
               "value": (("%s%s" % (re.search(r"BOUND ([<>])", c["norm_note"] or "").group(1), c["norm_value"]))
                         if re.search(r"BOUND ([<>])", c["norm_note"] or "") and c["norm_value"] is not None
                         else (c["norm_value"] if c["norm_value"] is not None else c["raw_value"])),
               "unit": c["norm_unit"] or "text", "substrate": "blotter (as stated by source)" if is_ten else short(c["context"], 60),
               "concentration": "not stated", "source_id": MASTER_SRC.get(c["tier"], "SRC-DISTRIBUTOR-SPEC"), "source_detail": c["url"],
               "matched_cas": master.get("resolved_cas"), "identity_tier": master.get("identity_tier"),
               "value_type": VALUE_TYPE.get(c["tier"], "SECONDARY_REFERENCE")}
        add("PERFORMANCE EVIDENCE", "APPEND_ROW", row, c, f"{row['property']} from {c['tier']}")
    # ---- olfactory description (kept short; manufacturer only)
    for c in independent([c for c in claims if c["field"] == "odour_description" and c["tier"] == "OFFICIAL_MANUFACTURER"]):
        add("INDIVIDUAL RESEARCH LOG", "NOTE_ONLY", {"palette_id": pid, "odour_description_manufacturer": short(c["raw_value"], 200),
                                                      "source_url": c["url"]}, c,
            "Manufacturer odour description captured (short fact; for OLFACTORY EVIDENCE facet coding by a reviewer)",
            status="NEEDS_REVIEW")
    # ---- identity
    ident_claims = [c for c in claims if c["field"] == "cas" and c["match_class"] in identity.ACCEPTED and c["tier"] != "IDENTITY_DB"]
    mset = set(master.get("master_cas_set") or [])
    best_docs = sorted({(c["doc_id"], c["tier"], c["match_class"], c["url"], c["doc_title"]) for c in claims
                        if c["match_class"] in identity.GRADE_LEVEL_OK and c["field"] != "formula_document"},
                       key=lambda x: (x[1] != "OFFICIAL_MANUFACTURER", x[2] != "EXACT_GRADE"))
    if not mset and ident_claims:
        cas_vals = sorted({c["norm_text"] for c in ident_claims})
        conflict = len(cas_vals) > 1 or any(c["validation"] == "CONFLICT" for c in ident_claims)
        add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "resolved_cas", "old_value": None,
                                                 "new_value": " | ".join(cas_vals)}, ident_claims,
            f"CAS resolved from {len(independent(ident_claims))} independent source(s)",
            status="BLOCKED_CONFLICT" if conflict else _status(ident_claims[0], True))
    if not mset and not ident_claims:
        # no labelled CAS anywhere: accept a CAS printed on >=2 independent pages that carry the trade name in their title
        ment = [c for c in claims if c["field"] == "cas_mentioned" and c["match_class"] in identity.ACCEPTED
                and "in title" in (c.get("reasons") or "")]
        groups = {}
        for c in ment:
            groups.setdefault(c["norm_text"], {}).setdefault(c["independent_group"] or c["doc_id"], c)
        ranked = sorted(groups.items(), key=lambda kv: -len(kv[1]))
        if ranked and len(ranked[0][1]) >= 2 and (len(ranked) == 1 or len(ranked[1][1]) < len(ranked[0][1])):
            cas, srcs = ranked[0]
            ident_claims = list(srcs.values())
            add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "resolved_cas", "old_value": None, "new_value": cas},
                ident_claims, f"CAS printed on {len(srcs)} independent pages naming the material in their title "
                              f"(other CAS seen: {[k for k, _ in ranked[1:4]]})", status="NEEDS_REVIEW", conf="MEDIUM")
    tier_now = master.get("identity_tier") or ""
    if not best_docs and ident_claims and tier_now.startswith(("C", "D")) and not mset:
        add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "identity_tier", "old_value": tier_now,
                                                 "new_value": "B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK"}, ident_claims[:1],
            "Trade name linked to a CAS by source(s) whose grade/manufacturer is not confirmed", status="NEEDS_REVIEW")
    if best_docs:
        d = best_docs[0]
        dc = [c for c in claims if c["doc_id"] == d[0]][:1]
        if d[1] == "OFFICIAL_MANUFACTURER" and not tier_now.startswith("A"):
            has_conf = con.execute("SELECT COUNT(*) n FROM conflicts WHERE palette_id=? AND field IN ('cas','botanical_species')", (pid,)).fetchone()["n"]
            add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "identity_tier", "old_value": tier_now,
                                                     "new_value": "A_EXACT_COMMERCIAL_GRADE"}, dc,
                f"Traceable manufacturer grade document ({d[2]}): {d[3]}", status="BLOCKED_CONFLICT" if has_conf else None)
        elif d[1] != "OFFICIAL_MANUFACTURER" and tier_now.startswith(("C", "D")) and ident_claims:
            add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "identity_tier", "old_value": tier_now,
                                                     "new_value": "B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK"}, dc,
                "Trade name linked to a CAS by a non-manufacturer source", status="NEEDS_REVIEW")
        if d[1] == "OFFICIAL_MANUFACTURER" and not master.get("supplier_grade_url"):
            add("MATERIAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "supplier_grade_url", "old_value": None,
                                                     "new_value": d[3]}, dc, "Official manufacturer grade page/document")
    # ---- SDS / CLP (only SDS of this product or a same-name grade; never substance-level PubChem GHS)
    by_doc = {}
    for c in claims:
        if c["field"] in ("clp_class", "h_statement", "signal_word", "sds_product_name") and c["match_class"] in identity.ACCEPTED \
                and c["tier"] != "IDENTITY_DB":
            by_doc.setdefault(c["doc_id"], []).append(c)
    for doc_id, cs in by_doc.items():
        classes = sorted({c["raw_value"] for c in cs if c["field"] == "clp_class"})
        hs = sorted({c["raw_value"] for c in cs if c["field"] == "h_statement"})
        if not (classes or hs):
            continue
        pname = next((c["raw_value"] for c in cs if c["field"] == "sds_product_name"), "")
        grade_ok = cs[0]["match_class"] in identity.GRADE_LEVEL_OK
        row = {"palette_id": pid, "school_name_exact": master.get("school_name"),
               "hazard_classes": "; ".join(classes) + (" | H: " + ", ".join(hs) if hs else ""),
               "source": f"{cs[0]['evidence_level']} '{short(pname or cs[0]['doc_title'], 80)}' ({cs[0]['url'].split('/')[2]})",
               "source_url": cs[0]["url"], "evidence_class": cs[0]["evidence_level"], "accessed": TODAY,
               "note": "Raw-material hazard classification (CLP/GHS) as printed on this SDS; identity "
                       f"{cs[0]['match_class']}{'' if grade_ok else ' - NOT confirmed as the school grade'}; not a finished-product classification."}
        st = "BLOCKED_CONFLICT" if any(c["validation"] == "CONFLICT" for c in cs) else \
            ("AUTO_ELIGIBLE" if grade_ok and cs[0]["tier"] == "OFFICIAL_MANUFACTURER" else "NEEDS_REVIEW")
        add("CLP HAZARDS", "APPEND_ROW", row, cs, "SDS hazard section parsed", status=st)
    # ---- naturals: botanical identity + reference composition
    for cf in con.execute("SELECT * FROM conflicts WHERE palette_id=? AND field='botanical_species'", (pid,)).fetchall():
        vals = json.loads(cf["values_json"])
        new = next((v["value"] for v in vals if v["claim_id"] != "MASTER"), None)
        cs = [c for c in claims if c["claim_id"] in json.loads(cf["claim_ids"])]
        add("NATURAL IDENTITY", "UPDATE_CELL", {"palette_id": pid, "column": "botanical_species",
                                                "old_value": master.get("botanical_species"), "new_value": new}, cs or claims[:1],
            cf["detail"] + " -> CORRECTIONS LOG entry required", status="BLOCKED_CONFLICT", conf="HIGH" if len(cs) >= 2 else "MEDIUM")
    for c in claims:
        if c["field"].startswith("composition:") and c["tier"] == "PEER_REVIEWED" and c["match_class"] == "LIKELY_MATCH":
            sp = (identity.EXPECTED_SPECIES.get(pid) or [""])[0]
            row = {"Reference family": f"{master.get('school_name')} reference sample(s)", "Research sample ID": short(c["doc_title"], 50) + " | cols: " + short((re.search(r"columns: ([^;]*)", c["norm_note"] or "") or [None, ""])[1], 60),
                   "Species as published": sp, "Analyte": c["field"].split(":", 1)[1], "Sample relative peak area %": c["raw_value"],
                   "Primary study URL": c["url"], "Related palette IDs (reference only; research sample is NOT the school bottle) [added 2026-09-28]": pid,
                   "_label": "REFERENCE_COMPOSITION"}
            add("NATURAL GCMS STUDIES", "APPEND_ROW", row, c, "Parsed from a GC-MS table (automatic; spot-check before import)",
                status="NEEDS_REVIEW")
    # ---- research log row (always)
    n_acc = con.execute("SELECT COUNT(*) n FROM doc_material WHERE palette_id=? AND accepted=1", (pid,)).fetchone()["n"]
    useful = [ch for ch in changes if ch["target_sheet"] != "INDIVIDUAL RESEARCH LOG"]
    outcome = "FOUND" if any(ch["review_status"] == "AUTO_ELIGIBLE" for ch in useful) else ("PARTIAL" if useful else "SEARCHED_NO_USABLE_DATA")
    top = best_docs[0] if best_docs else None
    mfr = next((c["manufacturer"] for c in claims if c["tier"] == "OFFICIAL_MANUFACTURER" and c["match_class"] in identity.GRADE_LEVEL_OK and c.get("manufacturer")), None) \
        or next((c["evidence_level"].split("(")[-1].rstrip(")") + " (per SDS)" for c in claims if c["evidence_level"].startswith("MANUFACTURER_SDS_VIA")), None)
    cas_out = master.get("resolved_cas") or " | ".join(sorted({c["norm_text"] for c in ident_claims})) or None
    ev = top[1] if top else None
    add("INDIVIDUAL RESEARCH LOG", "APPEND_ROW", {
        "palette_id": pid, "school_name_exact": master.get("school_name"), "manufacturer": mfr,
        "cas": cas_out, "identity_tier_after": next((ch["payload"]["new_value"] for ch in changes if ch["payload"].get("column") == "identity_tier"), master.get("identity_tier")),
        "evidence_class": {"OFFICIAL_MANUFACTURER": "MANUFACTURER", "DISTRIBUTOR": "DISTRIBUTOR_SPEC", "RETAILER": "RETAILER"}.get(ev, ev or "SEARCHED_NO_USABLE_DATA"),
        "source_title": short(top[4], 120) if top else None, "source_url": top[3] if top else None,
        "notes": f"Pilot {TODAY}: {n_acc} accepted documents; {len(useful)} proposed data changes; see output/materials/{pid}.md",
        "accessed": TODAY, "search_outcome": outcome, "public_research_status": "TARGETED_SEARCH_DONE (not yet exhausted)"},
        claims[:1] if claims else [], "One row per researched material (single source of 'individually researched')",
        status="NEEDS_REVIEW", conf="MEDIUM")
    if not claims:
        changes[-1]["evidence"] = []
    for ch in changes:
        con.execute("INSERT OR REPLACE INTO proposed_changes(change_id, palette_id, target_sheet, operation, payload, review_status,"
                    " confidence, rationale, evidence) VALUES (?,?,?,?,?,?,?,?,?)",
                    (ch["change_id"], pid, ch["target_sheet"], ch["operation"], json.dumps(ch["payload"], default=str),
                     ch["review_status"], ch["confidence"], ch["rationale"], json.dumps(ch["evidence"], default=str)))
    con.commit()
    # final material state
    n_conf = con.execute("SELECT COUNT(*) n FROM conflicts WHERE palette_id=?", (pid,)).fetchone()["n"]
    if not useful:
        db.set_state(con, pid, "NO_PUBLIC_DATA_FOUND", "no usable public data in this targeted pass (not exhaustive)")
    elif n_conf or any(ch["review_status"] != "AUTO_ELIGIBLE" for ch in useful):
        db.set_state(con, pid, "NEEDS_REVIEW", f"{n_conf} conflicts; {sum(ch['review_status'] != 'AUTO_ELIGIBLE' for ch in useful)} changes need review")
    else:
        db.set_state(con, pid, "VALIDATED", "all proposed changes auto-eligible, no conflicts")
    db.mark_stage(con, pid, "propose")
    return changes


def source_registry_changes(con):
    """New source classes introduced by this pilot (SOURCE REGISTRY + SOURCE LICENSING AUDIT)."""
    tiers = {r["tier"] for r in con.execute("SELECT DISTINCT tier FROM documents d JOIN doc_material m ON m.doc_id=d.doc_id WHERE m.accepted=1")}
    out = []
    for t in sorted(tiers):
        if t in NEW_SOURCES:
            sid, title, cls, lic = NEW_SOURCES[t]
            for sheet, row in (("SOURCE REGISTRY", {"source_id": sid, "title": title, "source_class": cls,
                                                    "url_or_identifier_and_access": "per row URL; accessed " + TODAY,
                                                    "accessed_date": TODAY, "license_class": lic}),
                               ("SOURCE LICENSING AUDIT", {"source_id": sid, "license_class": lic,
                                                           "use_allowed_in_this_educational_project": "Y (facts + citation; no text reproduced)"})):
                out.append({"change_id": _cid("GLOBAL", sheet, sid), "palette_id": None, "target_sheet": sheet, "operation": "APPEND_ROW",
                            "payload": row, "review_status": "NEEDS_REVIEW", "confidence": "MEDIUM",
                            "rationale": f"New source class used by the pilot ({t})", "evidence": []})
    return out


def export(con):
    rows = []
    for r in con.execute("SELECT * FROM proposed_changes ORDER BY palette_id, target_sheet, change_id"):
        rows.append({"change_id": r["change_id"], "palette_id": r["palette_id"], "target_sheet": r["target_sheet"],
                     "operation": r["operation"], "payload": json.loads(r["payload"]), "review_status": r["review_status"],
                     "confidence": r["confidence"], "rationale": r["rationale"], "evidence": json.loads(r["evidence"])})
    rows += source_registry_changes(con)
    with open(OUTPUT / "proposed_changes.jsonl", "w", encoding="utf-8") as fh:
        for r in rows:
            fh.write(json.dumps(r, ensure_ascii=False, default=str) + "\n")
    return rows
