"""Pilot report: per-material and global audit of what the pipeline found."""
import csv
import html
import json
from collections import Counter, defaultdict

from . import db, identity
from .common import DATA, MANIFESTS, OUTPUT, load_json, now_iso, short


def master_sha():
    try:
        return load_json(MANIFESTS / "master_snapshot.json")["master_sha256"]
    except Exception:
        return "?"
from .pipeline import pilot

W = {"identity_coverage": 20, "sensory_coverage": 15, "sensory_quantification_coverage": 10, "dose_coverage": 20,
     "formula_coverage": 15, "interaction_coverage": 5, "performance_coverage": 5, "regulatory_coverage": 10}
TIER_COV = {"A": 3, "B": 2, "C": 1, "D": 0}


def _score(cov, tier):
    s = sum(w * (cov.get(k) or 0) / 3 for k, w in W.items())
    if (tier or "D").startswith("D"):
        s = min(s, 20)
    if not cov.get("dose_coverage") and not cov.get("formula_coverage"):
        s = min(s, 40)
    return s


def _cls(s):
    return "READY_WITH_CAVEATS" if s >= 70 else ("PARTIAL" if s >= 45 else "NOT_READY")


def simulate_readiness(master, changes, include_review):
    """Estimate readiness after applying proposals, using the master's documented weights/caps.
    Residual between the documented formula and the stored score is carried over unchanged."""
    cov = {k: (master.get("coverage") or {}).get(k) or 0 for k in W}
    tier = master.get("identity_tier") or "D"
    old = _score(cov, tier)
    offset = (master.get("readiness_score") or 0) - old
    ok = {"AUTO_ELIGIBLE"} | ({"NEEDS_REVIEW"} if include_review else set())
    new = dict(cov)
    new_tier = tier
    for ch in changes:
        if ch["review_status"] not in ok:
            continue
        p = ch["payload"]
        if ch["target_sheet"] == "MATERIAL IDENTITY" and p.get("column") == "identity_tier":
            new_tier = p["new_value"]
            new["identity_coverage"] = max(new["identity_coverage"], TIER_COV[new_tier[0]])
        if ch["target_sheet"] == "MATERIAL IDENTITY" and p.get("column") == "resolved_cas" and new_tier.startswith("D"):
            new_tier = "B_EXACT_CHEMICAL_VIA_TRADE_NAME_LINK"
            new["identity_coverage"] = max(new["identity_coverage"], 2)
        if ch["target_sheet"] == "DOSE EVIDENCE STRUCTURED":
            new["dose_coverage"] = max(new["dose_coverage"], 3 if p["dose_type"] == "SUPPLIER_RECOMMENDATION" else 1)
        if ch["target_sheet"] in ("PERFORMANCE EVIDENCE",) or (ch["target_sheet"] == "PHYSICOCHEMICAL DATA" and p.get("property") == "vapor_pressure_supplier"):
            manu = any(e["tier"] == "OFFICIAL_MANUFACTURER" for e in ch["evidence"])
            new["performance_coverage"] = max(new["performance_coverage"], 2 if manu else 1)
    s = max(0, min(100, _score(new, new_tier) + offset))
    return round(s), _cls(s)


def _md_table(headers, rows):
    out = ["| " + " | ".join(headers) + " |", "|" + "---|" * len(headers)]
    for r in rows:
        out.append("| " + " | ".join(str(x if x is not None else "").replace("|", "/").replace("\n", " ") for x in r) + " |")
    return "\n".join(out)


def collect(con):
    mats = []
    for m in pilot()["materials"]:
        pid = m["palette_id"]
        row = con.execute("SELECT * FROM materials WHERE palette_id=?", (pid,)).fetchone()
        master = db.master_record(con, pid)
        queries = [dict(r) for r in con.execute("SELECT provider, query, purpose, n_results FROM queries WHERE palette_id=? ORDER BY id", (pid,))]
        n_leads = con.execute("SELECT COUNT(DISTINCT canonical_url) n FROM leads WHERE palette_id=?", (pid,)).fetchone()["n"]
        fetches = [dict(r) for r in con.execute(
            "SELECT DISTINCT f.url, f.status, f.http_status, f.note, f.domain FROM leads l JOIN fetch_log f ON f.canonical_url=l.canonical_url"
            " WHERE l.palette_id=? AND l.selected=1", (pid,))]
        docs = [dict(r) for r in con.execute(
            "SELECT dm.match_class, dm.match_score, dm.reasons, dm.accepted, dm.reject_reason, d.* FROM doc_material dm"
            " JOIN documents d ON d.doc_id=dm.doc_id WHERE dm.palette_id=? ORDER BY dm.accepted DESC, dm.match_score DESC", (pid,))]
        claims = [dict(r) for r in con.execute("SELECT * FROM claims WHERE palette_id=? AND match_class NOT IN ('REJECTED','ERROR')", (pid,))]
        conflicts = [dict(r) for r in con.execute("SELECT * FROM conflicts WHERE palette_id=?", (pid,))]
        changes = [dict(r) | {"payload": json.loads(r["payload"]), "evidence": json.loads(r["evidence"])}
                   for r in con.execute("SELECT * FROM proposed_changes WHERE palette_id=?", (pid,))]
        mats.append({"cfg": m, "row": dict(row), "master": master, "queries": queries, "n_leads": n_leads, "fetches": fetches,
                     "docs": docs, "claims": claims, "conflicts": conflicts, "changes": changes,
                     "ready_auto": simulate_readiness(master, changes, False), "ready_all": simulate_readiness(master, changes, True)})
    return mats


KEY_FIELDS = ["cas", "use_level", "vapour_pressure", "logp", "tenacity", "substantivity_application", "density", "refractive_index",
              "flash_point", "boiling_point", "physical_state", "solubility", "odour_description", "odour_family", "product_code",
              "ec_number", "fema", "botanical_name", "plant_part", "extraction_method", "origin", "iso_standard", "clp_class",
              "h_statement", "signal_word", "sds_product_name", "sds_component_cas", "storage", "stability_text", "gcms_study",
              "synonym_trade_name", "molecular_formula", "molecular_weight", "logp_computed", "h_statement_substance"]


def material_md(M):
    m, master = M["cfg"], M["master"]
    pid = m["palette_id"]
    acc = [d for d in M["docs"] if d["accepted"] == 1]
    amb = [d for d in M["docs"] if d["match_class"] == "AMBIGUOUS"]
    rej = [d for d in M["docs"] if d["match_class"] in ("REJECTED", "ERROR")]
    best = max(acc, key=lambda d: (d["match_score"] or 0), default=None)
    L = [f"## {pid} — {master.get('school_name')}", "",
         f"*Grupo piloto:* {m['group']} · *Qué prueba:* {', '.join(m['test_purpose'])}",
         f"*Estado final:* **{M['row']['state']}** — {M['row']['state_note']}",
         f"*Master antes:* tier `{master.get('identity_tier')}`, CAS `{master.get('resolved_cas')}`, readiness {master.get('readiness_score')} ({master.get('readiness_class')})",
         f"*Readiness estimado después:* solo AUTO_ELIGIBLE → {M['ready_auto'][0]} ({M['ready_auto'][1]}); si se aprueban también los NEEDS_REVIEW → {M['ready_all'][0]} ({M['ready_all'][1]})", ""]
    L += ["**Queries realizadas**", ""]
    L += [f"- `{q['provider']}` · {q['query']} → {q['n_results']} resultados" for q in M["queries"]]
    st = Counter(f["status"] for f in M["fetches"])
    L += ["", f"**Fuentes encontradas:** {M['n_leads']} URLs distintas; {len(M['fetches'])} seleccionadas para descarga "
          f"({', '.join(f'{k}: {v}' for k, v in st.items())}); {len(M['docs'])} documentos analizados (incluye APIs PubChem/PMC).", ""]
    blocked = [f for f in M["fetches"] if f["status"] in ("MANUAL_RETRIEVAL_REQUIRED", "ROBOTS_DISALLOWED", "ENV_UNREACHABLE")]
    if blocked:
        L += ["**Requieren recuperación manual (no se evadió ningún bloqueo):**", ""]
        L += [f"- {f['url']} — {f['status']} ({short(f['note'], 90)})" for f in blocked]
        L += [""]
    L += ["**Fuentes aceptadas**", ""]
    if acc:
        L += [_md_table(["match", "tipo", "licencia", "documento", "motivos"],
                        [(d["match_class"], d["tier"], d["license_class"], f"[{short(d['title'] or d['first_url'], 60)}]({d['first_url']})",
                          short(d["reasons"], 160)) for d in acc])]
    else:
        L += ["_Ninguna._"]
    if amb:
        L += ["", "**Fuentes ambiguas (retenidas para revisión, no usadas automáticamente)**", ""]
        L += [f"- [{short(d['title'] or d['first_url'], 70)}]({d['first_url']}) — {short(d['reasons'], 160)}" for d in amb]
    if rej:
        L += ["", f"**Fuentes rechazadas:** {len(rej)}", ""]
        L += [f"- {short(d['title'] or d['first_url'], 70)} — {short(d['reject_reason'] or d['reasons'], 110)}" for d in rej[:12]]
        if len(rej) > 12:
            L += [f"- … y {len(rej) - 12} más"]
    conf_txt = "%s (score %.2f)" % (best["match_class"], best["match_score"] or 0) if best else "sin fuente aceptada"
    L += ["", f"**Confianza de identidad:** {conf_txt}", ""]
    rows = []
    for c in sorted(M["claims"], key=lambda c: (KEY_FIELDS.index(c["field"]) if c["field"] in KEY_FIELDS else 99, c["field"])):
        if c["field"] in ("cas_mentioned", "doc_is_sds", "performance_application", "chemical_name", "colour") :
            continue
        norm = c["norm_value"] if c["norm_value"] is not None else (f"{c['norm_min']}–{c['norm_max']}" if c["norm_max"] is not None else "")
        rows.append((c["field"], short(c["raw_value"], 70), f"{norm} {c['norm_unit'] or ''}".strip(), c["evidence_level"], c["match_class"],
                     c["validation"], c["url"].split("/")[2]))
    L += ["**Campos descubiertos (claims)**", ""]
    L += [_md_table(["campo", "valor bruto", "normalizado", "evidencia", "identidad", "validación", "dominio"], rows[:60]) if rows else "_Ninguno._"]
    if len(rows) > 60:
        L += [f"_… {len(rows) - 60} claims más en data/staging.sqlite_"]
    dose = [c for c in M["claims"] if c["field"] == "use_level"]
    perf = [c for c in M["claims"] if c["field"] in ("tenacity", "substantivity_application", "vapour_pressure")]
    sds = [c for c in M["claims"] if c["field"] in ("clp_class", "h_statement", "signal_word") and c["match_class"] in identity.ACCEPTED]
    L += ["", f"**Evidencia de dosis:** " + ("; ".join(f"{c['raw_value']} ({c['evidence_level']}, {c['url'].split('/')[2]}, {c['validation']})" for c in dose) or "ninguna encontrada"),
          f"**Evidencia de performance:** " + ("; ".join(f"{c['field']}={short(c['raw_value'], 30)} ({c['evidence_level']}, {c['validation']})" for c in perf) or "ninguna encontrada"),
          f"**SDS/CLP (por SDS, sin mezclar):** " + (" · ".join(
              f"{u}: " + ", ".join(sorted({c['raw_value'] for c in sds if c['url'].split('/')[2] == u}))
              for u in sorted({c['url'].split('/')[2] for c in sds})) if sds else "ningún SDS del producto analizado"), ""]
    if M["conflicts"]:
        L += ["**Conflictos (ningún valor sobrescrito; todos los claims conservados)**", ""]
        for cf in M["conflicts"]:
            vals = json.loads(cf["values_json"])
            L += [f"- `{cf['field']}`: {cf['detail']} — valores: " + "; ".join(f"{short(v['value'], 40)} [{v['tier']}]" for v in vals[:8])]
        L += [""]
    ch = Counter(c["review_status"] for c in M["changes"])
    L += [f"**Cambios propuestos:** {len(M['changes'])} ({', '.join(f'{k}: {v}' for k, v in ch.items())})", ""]
    L += [f"- `{c['review_status']}` · {c['target_sheet']} · {c['operation']} · {short(_payload_brief(c['payload']), 140)}" for c in M["changes"]]
    L += ["", "**Preguntas abiertas**", ""] + [f"- {q}" for q in unresolved(M)] + [""]
    return "\n".join(L)


def _payload_brief(p):
    if "column" in p:
        return f"{p['column']}: {p.get('old_value')} → {p.get('new_value')}"
    keys = ["property", "dose_type", "value_text", "value", "unit", "hazard_classes", "Analyte", "Sample relative peak area %",
            "search_outcome", "odour_description_manufacturer"]
    return ", ".join(f"{k}={p[k]}" for k in keys if k in p and p[k] is not None)


def unresolved(M):
    q = []
    master = M["master"]
    fields = {c["field"] for c in M["claims"] if c["match_class"] in identity.ACCEPTED}
    for f in M["fetches"]:
        if f["status"] in ("MANUAL_RETRIEVAL_REQUIRED", "ROBOTS_DISALLOWED") and f["domain"] in ("iff.com", "studio.dsm-firmenich.com"):
            q.append(f"Página oficial bloqueada a acceso automatizado ({f['url']}): recuperar manualmente y re-ejecutar la extracción.")
            break
    if "use_level" not in fields:
        q.append("Sin dosis publicada localizada: buscar en compendio del fabricante (manual) o planificar serie de dilución interna.")
    if not {"clp_class", "h_statement"} & fields:
        q.append("Sin SDS del producto analizable: pedir SDS al proveedor/escuela.")
    for cf in M["conflicts"]:
        q.append(f"Resolver conflicto en `{cf['field']}`: {short(cf['detail'], 140)}")
    amb = [d for d in M["docs"] if d["match_class"] == "AMBIGUOUS"]
    if amb:
        q.append(f"{len(amb)} documento(s) de identidad ambigua esperan revisión humana.")
    if master.get("chart_kind") == "Natural":
        q.append("La composición GC-MS publicada es REFERENCE_COMPOSITION (muestras de investigación), nunca la botella ISIPCA; falta CoA/especificación del lote.")
    return q


def write_all(con):
    mats = collect(con)
    (OUTPUT / "materials").mkdir(exist_ok=True)
    for M in mats:
        (OUTPUT / "materials" / f"{M['cfg']['palette_id']}.md").write_text(material_md(M), encoding="utf-8")
    write_manifests(con)
    g = global_stats(con, mats)
    md = global_md(g, mats)
    (OUTPUT / "pilot_report.md").write_text(md, encoding="utf-8")
    (OUTPUT / "global_stats.json").write_text(json.dumps(g, indent=1, default=str), encoding="utf-8")
    with open(OUTPUT / "pilot_summary.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["palette_id", "school_name", "group", "state", "queries", "distinct_urls", "docs_accepted", "docs_ambiguous",
                    "docs_rejected", "best_identity", "claims", "conflicts", "changes_auto", "changes_review", "changes_blocked",
                    "readiness_before", "class_before", "readiness_after_auto", "class_after_auto", "readiness_after_all", "class_after_all"])
        for M in mats:
            ch = Counter(c["review_status"] for c in M["changes"])
            acc = [d for d in M["docs"] if d["accepted"] == 1]
            best = max(acc, key=lambda d: d["match_score"] or 0, default=None)
            w.writerow([M["cfg"]["palette_id"], M["master"].get("school_name"), M["cfg"]["group"], M["row"]["state"], len(M["queries"]),
                        M["n_leads"], len(acc), sum(d["match_class"] == "AMBIGUOUS" for d in M["docs"]),
                        sum(d["match_class"] == "REJECTED" for d in M["docs"]), best["match_class"] if best else "",
                        len(M["claims"]), len(M["conflicts"]), ch["AUTO_ELIGIBLE"], ch["NEEDS_REVIEW"], ch["BLOCKED_CONFLICT"],
                        M["master"].get("readiness_score"), M["master"].get("readiness_class"), *M["ready_auto"], *M["ready_all"]])
    return g


def global_stats(con, mats):
    g = {}
    data_changes = lambda M: [c for c in M["changes"] if c["target_sheet"] != "INDIVIDUAL RESEARCH LOG"]
    g["materials_with_new_data"] = [M["cfg"]["palette_id"] for M in mats if data_changes(M)]
    g["materials_without_useful_results"] = [M["cfg"]["palette_id"] for M in mats if not data_changes(M)]
    g["documents_downloaded"] = con.execute("SELECT COUNT(*) n FROM documents WHERE doc_kind!='API' OR doc_kind IS NULL").fetchone()["n"]
    g["api_documents"] = con.execute("SELECT COUNT(*) n FROM documents WHERE doc_kind='API'").fetchone()["n"]
    g["documents_by_kind"] = dict(Counter(r["content_type"] for r in con.execute("SELECT content_type FROM documents")))
    g["urls_attempted"] = con.execute("SELECT COUNT(*) n FROM fetch_log WHERE domain!='api'").fetchone()["n"]
    g["fetch_status"] = dict(Counter(r["status"] for r in con.execute("SELECT status FROM fetch_log WHERE domain!='api'")))
    g["exact_duplicate_urls"] = con.execute("SELECT COUNT(*) n FROM (SELECT doc_id FROM doc_urls GROUP BY doc_id HAVING COUNT(*)>1)").fetchone()["n"]
    g["near_duplicates"] = [dict(r) for r in con.execute("SELECT doc_id, first_url, duplicate_of, duplicate_basis FROM documents WHERE duplicate_of IS NOT NULL")]
    g["derived_copies"] = [dict(r) for r in con.execute("SELECT doc_id, first_url, derived_from FROM documents WHERE derived_from IS NOT NULL")]
    g["conflicts"] = [dict(r) for r in con.execute("SELECT palette_id, field, detail, includes_master FROM conflicts")]
    allch = [c for M in mats for c in M["changes"]]
    def cnt(pred):
        return sum(1 for c in allch if pred(c))
    g["new_manufacturer_dose_records"] = {s: cnt(lambda c: c["target_sheet"] == "DOSE EVIDENCE STRUCTURED" and c["payload"]["dose_type"] == "SUPPLIER_RECOMMENDATION" and c["review_status"] == s) for s in ("AUTO_ELIGIBLE", "NEEDS_REVIEW", "BLOCKED_CONFLICT")}
    g["new_secondary_dose_records"] = cnt(lambda c: c["target_sheet"] == "DOSE EVIDENCE STRUCTURED" and c["payload"]["dose_type"] != "SUPPLIER_RECOMMENDATION")
    g["new_vp_records"] = {s: cnt(lambda c: c["target_sheet"] == "PHYSICOCHEMICAL DATA" and c["payload"].get("property") == "vapor_pressure_supplier" and c["review_status"] == s) for s in ("AUTO_ELIGIBLE", "NEEDS_REVIEW", "BLOCKED_CONFLICT")}
    g["new_physchem_records"] = cnt(lambda c: c["target_sheet"] == "PHYSICOCHEMICAL DATA")
    g["new_performance_records"] = {s: cnt(lambda c: c["target_sheet"] == "PERFORMANCE EVIDENCE" and c["review_status"] == s) for s in ("AUTO_ELIGIBLE", "NEEDS_REVIEW", "BLOCKED_CONFLICT")}
    g["identity_improvements"] = [(c["palette_id"], c["payload"]["column"], c["payload"].get("old_value"), c["payload"]["new_value"], c["review_status"])
                                  for c in allch if c["target_sheet"] in ("MATERIAL IDENTITY", "NATURAL IDENTITY")]
    g["new_sds_clp"] = [(c["palette_id"], c["payload"]["hazard_classes"], c["payload"]["source_url"], c["review_status"]) for c in allch if c["target_sheet"] == "CLP HAZARDS"]
    g["new_gcms_reference_rows"] = cnt(lambda c: c["target_sheet"] == "NATURAL GCMS STUDIES")
    g["gcms_studies"] = sorted({c["url"] for M in mats for c in M["claims"] if c["field"] == "gcms_study" and c["match_class"] == "LIKELY_MATCH"})
    g["changes_by_status"] = dict(Counter(c["review_status"] for c in allch))
    g["changes_by_sheet"] = dict(Counter(c["target_sheet"] for c in allch))
    inacc = defaultdict(set)
    for r in con.execute("SELECT domain, status, note FROM fetch_log WHERE status IN ('MANUAL_RETRIEVAL_REQUIRED','ROBOTS_DISALLOWED','ENV_UNREACHABLE')"):
        inacc[(r["domain"], r["status"])].add(short(r["note"], 90))
    g["inaccessible_domains"] = sorted([(d, s, len(n), sorted(n)[0]) for (d, s), n in inacc.items()], key=lambda x: -x[2])
    g["errors"] = [dict(r) for r in con.execute("SELECT palette_id, state_note FROM materials WHERE state='ERROR'")] + \
                  [dict(r) for r in con.execute("SELECT palette_id, doc_id, reasons FROM doc_material WHERE match_class='ERROR'")]
    g["states"] = dict(Counter(M["row"]["state"] for M in mats))
    before = Counter(M["master"].get("readiness_class") for M in mats)
    g["readiness_before"] = dict(before)
    g["readiness_after_auto"] = dict(Counter(M["ready_auto"][1] for M in mats))
    g["readiness_after_all"] = dict(Counter(M["ready_all"][1] for M in mats))
    g["readiness_moves"] = [(M["cfg"]["palette_id"], M["master"].get("readiness_score"), M["master"].get("readiness_class"), *M["ready_auto"], *M["ready_all"])
                            for M in mats if M["ready_all"][1] != M["master"].get("readiness_class") or M["ready_all"][0] != M["master"].get("readiness_score")]
    audit = DATA / "audit" / "audit_verdicts.json"
    if audit.exists():
        a = load_json(audit)
        g["audit"] = a.get("summary", {})
    g["queries_total"] = sum(len(M["queries"]) for M in mats)
    g["queries_by_provider"] = dict(Counter(q["provider"] for M in mats for q in M["queries"]))
    g["distinct_urls_found"] = con.execute("SELECT COUNT(DISTINCT canonical_url) n FROM leads").fetchone()["n"]
    return g


def global_md(g, mats):
    L = ["# Perroco Lab — Piloto de investigación automatizada (20 materiales)", "",
         "Resultado del pipeline RAW SOURCE → EXTRACTED CLAIM → NORMALISED CLAIM → VALIDATION → PROPOSED CHANGE. "
         "**El master no se ha modificado.** Todas las propuestas están en `output/proposed_changes.jsonl`.", "",
         f"Fecha de ejecución: {now_iso()[:10]} · master analizado (sha256): `{master_sha()[:16]}…` · "
         "estados posibles por material: NOT_STARTED → SEARCHING → SOURCES_FOUND → EXTRACTED → NEEDS_REVIEW / VALIDATED / NO_PUBLIC_DATA_FOUND / ERROR.", "",
         "## Resumen global", ""]
    rows = [
        ("Queries realizadas", f"{g['queries_total']} ({', '.join(f'{k}: {v}' for k, v in g['queries_by_provider'].items())})"),
        ("URLs distintas encontradas", g["distinct_urls_found"]),
        ("URLs cuya descarga se intentó", f"{g['urls_attempted']} ({', '.join(f'{k}: {v}' for k, v in g['fetch_status'].items())})"),
        ("Documentos descargados (web)", f"{g['documents_downloaded']} ({', '.join(f'{k}: {v}' for k, v in g['documents_by_kind'].items())} incl. API)"),
        ("Respuestas de API guardadas (PubChem/PMC)", g["api_documents"]),
        ("Materiales con datos nuevos", f"{len(g['materials_with_new_data'])}: {', '.join(g['materials_with_new_data'])}"),
        ("Materiales sin resultados útiles", f"{len(g['materials_without_useful_results'])}: {', '.join(g['materials_without_useful_results']) or '—'}"),
        ("Duplicados exactos (mismo hash, varias URLs)", g["exact_duplicate_urls"]),
        ("Casi-duplicados / copias derivadas", f"{len(g['near_duplicates'])} / {len(g['derived_copies'])}"),
        ("Conflictos detectados", len(g["conflicts"])),
        ("Nuevos registros de dosis de fabricante", g["new_manufacturer_dose_records"]),
        ("Nuevos registros de dosis secundaria (distribuidor/retailer)", g["new_secondary_dose_records"]),
        ("Nuevos registros de presión de vapor", g["new_vp_records"]),
        ("Nuevos registros físico-químicos (total)", g["new_physchem_records"]),
        ("Nuevos registros de performance", g["new_performance_records"]),
        ("Mejoras de identidad propuestas", len(g["identity_improvements"])),
        ("Nuevos SDS/CLP", len(g["new_sds_clp"])),
        ("Filas de composición de referencia GC-MS", f"{g['new_gcms_reference_rows']} filas (de {len(g['gcms_studies'])} estudios localizados)"),
        ("Cambios propuestos por estado", g["changes_by_status"]),
        ("Estados finales de materiales", g["states"]),
    ]
    L += [_md_table(["Indicador", "Valor"], rows), ""]
    if g.get("audit"):
        a = g["audit"]
        L += ["## Estimación de precisión (auditoría manual de una muestra)", "", a.get("text", ""), ""]
    L += ["## ¿Qué cambiaría en READY / PARTIAL / NOT_READY? (estimación)", "",
          "Recalculado con los pesos y topes documentados en FORMULATION READINESS; es una estimación, no el recálculo del workbook.", "",
          _md_table(["Clase", "Antes (master)", "Solo AUTO_ELIGIBLE", "Si se aprueban también NEEDS_REVIEW"],
                    [(k, g["readiness_before"].get(k, 0), g["readiness_after_auto"].get(k, 0), g["readiness_after_all"].get(k, 0))
                     for k in ("READY_WITH_CAVEATS", "PARTIAL", "NOT_READY")]), ""]
    if g["readiness_moves"]:
        L += [_md_table(["Material", "Antes", "Clase", "Tras AUTO", "Clase", "Tras todo", "Clase"], g["readiness_moves"]), ""]
    L += ["## Dominios inaccesibles (no se evadió ningún bloqueo)", "",
          _md_table(["Dominio", "Estado", "URLs", "Motivo"], g["inaccessible_domains"]), ""]
    L += ["## Conflictos", "", _md_table(["Material", "Campo", "Detalle", "¿Contra el master?"],
                                          [(c["palette_id"], c["field"], short(c["detail"], 120), "sí" if c["includes_master"] else "no") for c in g["conflicts"]]), ""]
    L += ["## Mejoras de identidad propuestas", "", _md_table(["Material", "Columna", "Antes", "Propuesto", "Estado"], g["identity_improvements"]), ""]
    L += ["## SDS / CLP", "", _md_table(["Material", "Clasificación", "Fuente", "Estado"], g["new_sds_clp"]) if g["new_sds_clp"] else "_Ninguno._", ""]
    L += ["## Errores", ""] + ([f"- {e}" for e in g["errors"]] or ["_Ninguno._"]) + [""]
    L += ["## Tabla por material", "",
          _md_table(["ID", "Material", "Estado", "Docs aceptados", "Identidad", "Conflictos", "Cambios auto/revisión/bloq.", "Readiness antes→después(auto)"],
                    [(M["cfg"]["palette_id"], M["master"].get("school_name"), M["row"]["state"], sum(d["accepted"] == 1 for d in M["docs"]),
                      max((d for d in M["docs"] if d["accepted"] == 1), key=lambda d: d["match_score"] or 0, default={"match_class": "—"})["match_class"],
                      len(M["conflicts"]),
                      "/".join(str(sum(c["review_status"] == s for c in M["changes"])) for s in ("AUTO_ELIGIBLE", "NEEDS_REVIEW", "BLOCKED_CONFLICT")),
                      f"{M['master'].get('readiness_score')} → {M['ready_auto'][0]}") for M in mats]), ""]
    L += ["## Limitaciones reales del entorno y alternativas", "",
          "- **Buscadores web**: no utilizables por script (robots.txt de Google/Bing prohíbe /search; DuckDuckGo cortado por el proxy; "
          "sin clave de API). Las búsquedas las hizo el agente operador con su herramienta de búsqueda y quedaron registradas tal cual "
          "(`data/search_ingest/`). Alternativa para escalar: una API de búsqueda con clave (Brave Search API, SerpAPI) escribiendo el mismo formato.",
          "- **IFF (iff.com, incluido el compendio LMR) y dsm-firmenich Studio** responden 403 a cualquier acceso automatizado; "
          "**Givaudan** sirvió CAPTCHA tras varias peticiones; **TGSC y ScenTree** prohíben explícitamente a los agentes de Anthropic en robots.txt. "
          "Todo ello quedó como MANUAL_RETRIEVAL_REQUIRED. Alternativa: descargar a mano (navegador) las fichas/PDF listados en cada material "
          "y dejarlos en una carpeta; el pipeline puede procesar archivos locales con la misma extracción y trazabilidad.",
          "- **PubChem** limitó la tasa de peticiones (429/503) durante el piloto; el pipeline se detuvo (cortacircuitos) y dejó esas consultas pendientes de reanudar.",
          "- La composición GC-MS publicada es siempre REFERENCE_COMPOSITION de muestras de investigación, nunca la botella ISIPCA.",
          "- Nada se ha escrito en el master. Aplicar cambios requiere una fase explícita de aprobación.", "",
          "## Detalle por material", ""]
    for M in mats:
        L += [material_md(M), "---", ""]
    return "\n".join(L)


def write_manifests(con):
    """Provenance manifests (committed): every document with hash, URLs, class and licence; every fetch attempt."""
    from .common import MANIFESTS
    with open(MANIFESTS / "sources_manifest.jsonl", "w", encoding="utf-8") as fh:
        for d in con.execute("SELECT * FROM documents ORDER BY fetched_at"):
            urls = [r["canonical_url"] for r in con.execute("SELECT canonical_url FROM doc_urls WHERE doc_id=?", (d["doc_id"],))]
            mats = [dict(r) for r in con.execute("SELECT palette_id, match_class, accepted FROM doc_material WHERE doc_id=?", (d["doc_id"],))]
            fh.write(json.dumps({k: d[k] for k in d.keys() if k not in ("text_path",)} | {"urls": urls, "materials": mats},
                                ensure_ascii=False) + "\n")
    with open(MANIFESTS / "fetch_log.jsonl", "w", encoding="utf-8") as fh:
        for r in con.execute("SELECT * FROM fetch_log ORDER BY at"):
            fh.write(json.dumps(dict(r), ensure_ascii=False) + "\n")
    with open(MANIFESTS / "state_history.jsonl", "w", encoding="utf-8") as fh:
        for r in con.execute("SELECT * FROM state_history ORDER BY id"):
            fh.write(json.dumps(dict(r), ensure_ascii=False) + "\n")
