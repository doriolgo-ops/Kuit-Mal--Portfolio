"""Identity before data: decide whether a document is really about the school material.

Match classes (strongest first):
  EXACT_GRADE              official manufacturer doc + trade name + consistent CAS + grade modifiers satisfied
  EXACT_NAME_MANUFACTURER  trade name + manufacturer (official domain or explicit mention), no CAS contradiction
  EXACT_CAS_ONLY           CAS matches, trade name absent (chemical-level evidence only)
  LIKELY_MATCH             trade name / species match but manufacturer or CAS unconfirmed
  AMBIGUOUS                name matches but a different grade, a contradicting CAS or several candidates
  REJECTED                 neither name nor CAS (or clearly another product)
"""
import re

from .common import DOMAINS, norm_text

STRIP_TOKENS = {"toco", "tocopherol", "prg", "elincs", "firm", "giv", "tm", "ext", "lmr", "csm", "blo", "sfo",
                "for", "life", "tt", "pfg", "bht", "rd", "ei", "(elincs)", "(tt)", "new", "nat"}
STABILISER_TOKENS = {"toco", "tocopherol", "bht", "pfg"}
GRADE_WORDS = {"plus", "extra", "forte", "pure", "coeur", "heart", "crystals", "cryst", "decol", "decolorized",
               "super", "total", "supra", "mono", "ultra", "light", "dark", "absolute", "resinoid", "concrete",
               "co2", "md", "folded", "terpeneless", "fcf", "bergaptene-free"}
NATURAL_TYPES = {"oil": ["oil", "essential oil", "huile"], "abs": ["absolute", "abs"], "resoid": ["resinoid", "resin"],
                 "co2": ["co2", "supercritical"], "concrete": ["concrete"]}
ORIGINS = {"turkish": ["turkey", "turkish", "isparta"], "french": ["france", "french"], "haiti": ["haiti"],
           "java": ["java", "indonesia"], "india": ["india", "indian"], "guatemala": ["guatemala"],
           "bulgarian": ["bulgaria", "bulgarian"], "madag": ["madagascar"]}

# Aliases the chart abbreviations cannot express (documented, reviewable).
EXTRA_ALIASES = {
    "S-0366": ["calone 1951", "calone", "watermelon ketone", "methyl benzodioxepinone"],
    "S-0479": ["iso e super"],
    "S-0526": ["muscemor"],
    "N-0556": ["bergamot oil", "bergamot essential oil", "citrus bergamia"],
    "N-0728": ["tuberose absolute", "tuberose abs", "polianthes tuberosa", "agave amica"],
    "N-0632": ["cardamom oil", "cardamom essential oil", "cardamom seed oil"],
    "N-0623": ["clary sage oil", "clary sage essential oil", "salvia sclarea oil"],
    "N-0697": ["rose oil", "rose otto", "rosa damascena oil", "turkish rose oil"],
    "N-0775": ["vetiver oil", "vetiver essential oil", "vetiveria zizanioides oil", "chrysopogon zizanioides oil"],
}
EXPECTED_SPECIES = {
    "N-0775": ["chrysopogon zizanioides", "vetiveria zizanioides", "vetiveria zizanoides"],
    "N-0697": ["rosa damascena", "rosa x damascena", "rosa × damascena"],
    "N-0623": ["salvia sclarea"],
    "N-0632": ["elettaria cardamomum"],
    "N-0556": ["citrus bergamia", "citrus aurantium subsp. bergamia", "citrus aurantium ssp. bergamia", "citrus × bergamia"],
    "N-0728": ["polianthes tuberosa", "agave amica"],
}
CONFUSER_SPECIES = ["rosa centifolia", "rosa damascena", "polianthes tuberosa", "cymbopogon", "salvia officinalis",
                    "amomum", "citrus limon", "citrus aurantium", "chrysopogon nigritana", "pogostemon cablin",
                    "jasminum", "iris pallida", "vetiveria", "elettaria cardamomum"]


def name_variants(master):
    pid = master["palette_id"]
    school = master.get("school_name") or ""
    tokens = [t for t in re.split(r"[\s\"]+", school.lower()) if t]
    core = [t for t in tokens if t.strip("()") not in STRIP_TOKENS and not re.fullmatch(r"\d+(pct|%)?", t)]
    variants = set()
    base = norm_text(" ".join(core))
    if base:
        variants.add(base)
    if core and core[0] == "ald":
        rest = norm_text(" ".join(core[1:]))
        rest_nonum = norm_text(" ".join(t for t in core[1:] if not re.match(r"c-?\d+", t)))
        for r in (rest, rest_nonum):
            if r:
                variants.update({f"{r} aldehyde", f"aldehyde {r}", r})
    for k in ("iff_grade_name", "supplier_grade_name"):
        if master.get(k):
            variants.add(norm_text(master[k]))
    for a in EXTRA_ALIASES.get(pid, []):
        variants.add(norm_text(a))
    variants = {v for v in variants if len(v) >= 4}
    grade_mods = {t for t in core if t in GRADE_WORDS}
    return sorted(variants, key=len, reverse=True), grade_mods, {t for t in tokens if t in STABILISER_TOKENS}


def manufacturer_aliases(name):
    if not name:
        return []
    for key, aliases in DOMAINS["manufacturer_aliases"].items():
        if key.lower() in name.lower() or any(a.lower() in name.lower() for a in aliases):
            return [key] + aliases
    return [name]


def _word_in(needle, hay):
    return re.search(r"(?<![a-z0-9])" + re.escape(needle) + r"(?![a-z0-9])", hay) is not None


def classify(master, expected_mfr, doc, title, text, doc_cas_labelled, doc_cas_any):
    """Return (match_class, score 0-1, reasons list)."""
    reasons = []
    pid = master["palette_id"]
    natural = (master.get("chart_kind") == "Natural")
    variants, grade_mods, _ = name_variants(master)
    t_title, t_text = norm_text(title), norm_text(text[:400000])
    in_title = [v for v in variants if _word_in(v, t_title)]
    in_text = [v for v in variants if _word_in(v, t_text)]
    master_cas = set(master.get("master_cas_set") or [])
    cas_hit = sorted(master_cas & (set(doc_cas_labelled) | set(doc_cas_any)))
    cas_conflict = sorted(set(doc_cas_labelled) - master_cas) if master_cas and doc_cas_labelled and not (master_cas & set(doc_cas_labelled)) else []
    official = doc["tier"] == "OFFICIAL_MANUFACTURER"
    exp_aliases = manufacturer_aliases(expected_mfr)
    doc_mfr = doc["manufacturer"] or ""
    mfr_official_ok = official and (not expected_mfr or any(a.lower() in doc_mfr.lower() for a in exp_aliases)
                                    or doc_mfr.lower() in (expected_mfr or "").lower())
    mfr_mention = any(_word_in(norm_text(a), t_text) for a in exp_aliases) if expected_mfr else False
    if in_title:
        reasons.append(f"trade/common name in title: '{in_title[0]}'")
    elif in_text:
        reasons.append(f"trade/common name in text: '{in_text[0]}'")
    if cas_hit:
        reasons.append(f"CAS match {cas_hit}")
    if cas_conflict:
        reasons.append(f"labelled CAS {cas_conflict} not in master set {sorted(master_cas)}")
    if official:
        reasons.append(f"official manufacturer domain ({doc_mfr})")
    if mfr_mention:
        reasons.append(f"expected manufacturer '{expected_mfr}' mentioned")

    # a different grade of the same trade name in the title (e.g. 'Iso E Super Plus')
    other_grade = None
    for v in in_title:
        m = re.search(re.escape(v) + r"\s+([a-z0-9]+)", t_title)
        if m and m.group(1) in GRADE_WORDS and m.group(1) not in grade_mods and m.group(1) not in v.split():
            other_grade = m.group(1)
    subst = re.search(r"\b(substitute|replacer|replacement|alternative|imitation|analogue|analog|dupe|type|reconstitution)\b", t_title)
    if subst and in_title and subst.group(1) not in " ".join(variants):
        other_grade = other_grade or subst.group(1)
        reasons.append(f"title describes a different product ('{subst.group(1)}')")
    if other_grade:
        reasons.append(f"title names another grade ('{other_grade}')")
    other_trade = None
    if not in_title:
        tm = re.search(r"([A-Za-z][\w\- ]{2,30}?)\s*[\u00ae\u2122]", title or "")
        if tm and not any(_word_in(v, norm_text(tm.group(1))) for v in variants):
            other_trade = tm.group(1).strip()
            reasons.append(f"page is about another trade product ('{other_trade}')")

    if natural:
        species = EXPECTED_SPECIES.get(pid, [])
        sp_hit = [s for s in species if s in t_text]
        conf = [s for s in CONFUSER_SPECIES if s in t_text and not any(s in x or x in s for x in species)]
        if sp_hit:
            reasons.append(f"species match {sp_hit[0]}")
        if not in_text and not sp_hit and not cas_hit:
            return "REJECTED", 0.0, reasons + ["no name, species or CAS match"]
        if subst and in_title:
            return "AMBIGUOUS", 0.35, reasons
        if (in_title or in_text) and official and mfr_official_ok:
            return "EXACT_NAME_MANUFACTURER", 0.85, reasons
        if sp_hit or in_title:
            if conf and not sp_hit:
                return "AMBIGUOUS", 0.4, reasons + [f"other species present: {conf[:3]}"]
            return "LIKELY_MATCH", 0.7 if sp_hit else 0.55, reasons + ["reference for the natural type (not the school bottle)"]
        if cas_hit:
            return "EXACT_CAS_ONLY", 0.5, reasons + ["generic NCS CAS only"]
        return "AMBIGUOUS", 0.35, reasons + ["common name only in body text"]

    if not in_text and not cas_hit:
        return "REJECTED", 0.0, reasons + ["neither trade name nor CAS found"]
    if other_trade:
        return "AMBIGUOUS", 0.35, reasons + ["same CAS/name mention but a different commercial product -> chemical-level at most"]
    if other_grade:
        return "AMBIGUOUS", 0.4, reasons
    if in_text and cas_conflict:
        return "AMBIGUOUS", 0.4, reasons + ["name matches but CAS contradicts master -> CONFLICT review"]
    if (in_title or in_text) and official and not expected_mfr:
        return "LIKELY_MATCH", 0.75, reasons + [f"official {doc_mfr} document, but the manufacturer of the school bottle is not "
                                                "established -> not treated as the school grade"]
    if (in_title or in_text) and official and mfr_official_ok:
        mods_ok = all(_word_in(m, t_text) for m in grade_mods)
        if in_title and mods_ok and (cas_hit or not master_cas):
            return "EXACT_GRADE", 0.95, reasons + ([f"grade modifiers {sorted(grade_mods)} found"] if grade_mods else [])
        return "EXACT_NAME_MANUFACTURER", 0.85, reasons
    if in_text and mfr_mention and not cas_conflict:
        return "EXACT_NAME_MANUFACTURER", 0.8 if (in_title or cas_hit) else 0.7, reasons + ["manufacturer stated by a third party"]
    if cas_hit and not in_text:
        return "EXACT_CAS_ONLY", 0.6, reasons
    if in_title or (in_text and cas_hit):
        return "LIKELY_MATCH", 0.65, reasons
    return "AMBIGUOUS", 0.35, reasons + ["name only in body text"]


ACCEPTED = {"EXACT_GRADE", "EXACT_NAME_MANUFACTURER", "EXACT_CAS_ONLY", "LIKELY_MATCH"}
GRADE_LEVEL_OK = {"EXACT_GRADE", "EXACT_NAME_MANUFACTURER"}
