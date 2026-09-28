"""Read-only access to the research master. This module never writes to the workbook."""
import hashlib
import json

import openpyxl

from .common import ROOT, SETTINGS, find_cas

SHEETS_WITH_MATERIAL_ROWS = [
    "MATERIALS", "MATERIAL IDENTITY", "FORMULATION READINESS", "COVERAGE BY DIMENSION",
    "UNCERTAINTY", "NATURAL IDENTITY", "DOSE EVIDENCE STRUCTURED", "PHYSICOCHEMICAL DATA",
    "PERFORMANCE EVIDENCE", "PERFORMANCE PROFILE", "CLP HAZARDS", "VOLATILITY MODEL",
    "INDIVIDUAL RESEARCH LOG", "RESEARCH QUEUE", "REFERENCE COMPOSITION", "STABILITY",
    "EMPIRICAL DOSE STATS", "SENSORY PROFILE",
]
PID_HEADERS = {"palette_id", "Palette ID"}


def master_path():
    return ROOT / SETTINGS["master_path"]


def master_sha256():
    h = hashlib.sha256()
    with open(master_path(), "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _header_row(rows):
    for i, r in enumerate(rows[:4]):
        if any(c in PID_HEADERS for c in r):
            return i
    return 0


def _clean(v):
    if v is None:
        return None
    if isinstance(v, (int, float, str, bool)):
        return v
    return str(v)


def load_snapshot(palette_ids):
    """Return ({palette_id: {sheet: [row dicts]}}, {sheet: headers}, registries)."""
    wb = openpyxl.load_workbook(master_path(), read_only=True, data_only=True)
    wanted = set(palette_ids)
    per_mat = {p: {} for p in palette_ids}
    headers = {}
    for name in SHEETS_WITH_MATERIAL_ROWS:
        rows = list(wb[name].iter_rows(values_only=True))
        hi = _header_row(rows)
        hdr = [str(h) if h is not None else f"col{j}" for j, h in enumerate(rows[hi])]
        headers[name] = hdr
        pcol = next((j for j, h in enumerate(hdr) if h in PID_HEADERS), None)
        for r in rows[hi + 1:]:
            if pcol is None:
                continue
            ids = str(r[pcol] or "")
            for pid in wanted:
                if pid == ids or (name == "REFERENCE COMPOSITION" and pid in ids):
                    per_mat[pid].setdefault(name, []).append({hdr[j]: _clean(v) for j, v in enumerate(r) if v is not None})
    registries = {}
    for name in ("SOURCE REGISTRY", "SOURCE LICENSING AUDIT", "CONTROLLED VOCABULARY"):
        rows = list(wb[name].iter_rows(values_only=True))
        hi = 1 if name == "SOURCE LICENSING AUDIT" else 0
        hdr = [str(h) for h in rows[hi]]
        registries[name] = [{hdr[j]: _clean(v) for j, v in enumerate(r) if v is not None} for r in rows[hi + 1:]]
        headers[name] = hdr
    # extra headers for sheets we may propose rows to
    for name in ("NATURAL GCMS STUDIES", "CORRECTIONS LOG", "SOURCE REGISTRY"):
        rows = list(wb[name].iter_rows(max_row=3, values_only=True))
        headers[name] = [str(h) for h in rows[_header_row(rows)] if h is not None]
    wb.close()
    return per_mat, headers, registries


def summarize(pid, sheets):
    """Flatten the master rows of one material into the fields the pipeline compares against."""
    mat = (sheets.get("MATERIALS") or [{}])[0]
    ident = (sheets.get("MATERIAL IDENTITY") or [{}])[0]
    fr = (sheets.get("FORMULATION READINESS") or [{}])[0]
    nat = (sheets.get("NATURAL IDENTITY") or [{}])[0]
    cov = (sheets.get("COVERAGE BY DIMENSION") or [{}])[0]
    cas_text = " | ".join(str(x) for x in [ident.get("resolved_cas"), mat.get("Supplier grade CAS as printed"),
                                           mat.get("Parent CAS candidate"), nat.get("glossary_cas")] if x)
    s = {
        "palette_id": pid,
        "school_name": ident.get("school_name_exact") or mat.get("School name EXACT"),
        "chart_kind": ident.get("chart_kind") or mat.get("Chart kind"),
        "school_family": ident.get("school_family"),
        "identity_tier": ident.get("identity_tier"),
        "resolved_cas": ident.get("resolved_cas"),
        "master_cas_set": find_cas(cas_text),
        "normalized_identity": ident.get("normalized_identity"),
        "supplier_codes": ident.get("supplier_codes"),
        "supplier_grade_url": ident.get("supplier_grade_url"),
        "supplier_grade_name": ident.get("supplier_grade_name"),
        "iff_grade_name": mat.get("IFF grade name"),
        "botanical_species": nat.get("botanical_species") or ident.get("botanical_source"),
        "plant_part": nat.get("plant_part") or ident.get("plant_part"),
        "extraction": nat.get("extraction_from_chart"),
        "origin": nat.get("geographic_origin_from_chart") or ident.get("origin_on_chart"),
        "vp_pa": mat.get("Vapor pressure Pa used [added 2026-09-28]"),
        "vp_basis": mat.get("Vapor pressure basis [added 2026-09-28]"),
        "iff_vp_text": mat.get("IFF vapor pressure (original units)"),
        "iff_logp": mat.get("IFF LogP (published)"),
        "published_use_level": mat.get("Published supplier use level"),
        "published_tenacity": mat.get("Published tenacity"),
        "readiness_score": fr.get("formulation_readiness_0_100"),
        "readiness_class": fr.get("readiness_class"),
        "limiting_factors": fr.get("limiting_factors"),
        "coverage": {k: cov.get(k) for k in ("identity_coverage", "supplier_grade_coverage", "sensory_coverage",
                                             "sensory_quantification_coverage", "dose_coverage", "formula_coverage",
                                             "interaction_coverage", "physchem_coverage", "performance_coverage",
                                             "regulatory_coverage", "natural_composition_coverage",
                                             "has_manufacturer_dose", "has_formula_observed_dose")},
        "dose_rows": sheets.get("DOSE EVIDENCE STRUCTURED", []),
        "physchem_rows": sheets.get("PHYSICOCHEMICAL DATA", []),
        "performance_rows": sheets.get("PERFORMANCE EVIDENCE", []),
        "clp_rows": sheets.get("CLP HAZARDS", []),
        "research_log_rows": sheets.get("INDIVIDUAL RESEARCH LOG", []),
        "reference_composition_n": len(sheets.get("REFERENCE COMPOSITION", [])),
    }
    return s


def write_snapshot_file(path, snapshot):
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(snapshot, fh, ensure_ascii=False, indent=1, default=str)
