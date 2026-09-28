"""EXTRACTED CLAIM layer: turns a cached raw document into short, structured claims.

Only facts are kept (value + a context snippet of at most 200 characters) — never large
fragments of the source. Every claim keeps doc_id + URL (provenance).
"""
import re
from pathlib import Path

from bs4 import BeautifulSoup

from .common import ROOT, find_cas, short

# label (normalised) -> field
LABEL_FIELDS = [
    (r"\bcas\b|cas no|cas number|cas-no|cas #", "cas"),
    (r"einecs|\bec number|\bec no|elincs", "ec_number"),
    (r"^fema", "fema"),
    (r"vapou?r pressure", "vapour_pressure"),
    (r"log ?p(ow)?\b|log kow|partition coefficient", "logp"),
    (r"refractive index|refraction index|indice de r", "refractive_index"),
    (r"specific gravity|relative density|^density|densit", "density"),
    (r"flash ?point|point d.eclair", "flash_point"),
    (r"boiling point", "boiling_point"),
    (r"tenacity|longevity|odou?r life|substantivity on blotter|life on blotter", "tenacity"),
    (r"substantivity (damp|dry)|substantivity on (fabric|hair|skin)", "substantivity_application"),
    (r"^substantivity", "tenacity"),
    (r"use level|usage level|recommended (use|usage|level|dosage)|dosage|typical use|use rate|suggested use|level of use|max(imum)? use", "use_level"),
    (r"^odou?r (threshold|limit)", None),
    (r"description of the goods|un proper shipping|transport", None),
    (r"^odou?r|olfactive (description|profile)|odou?r (description|profile|type)|scent profile|odor notes|olfactory (description|notes)", "odour_description"),
    (r"olfactive (family|note)|odou?r family", "odour_family"),
    (r"appearance|physical state|^aspect|^form$", "physical_state"),
    (r"^colou?r", "colour"),
    (r"solubility|soluble in", "solubility"),
    (r"^stability|chemical stability", "stability_text"),
    (r"molecular weight|^mw$|mol\. weight", "molecular_weight"),
    (r"^formula|molecular formula", "molecular_formula"),
    (r"product code|item code|article (no|number)|material number|\bipc\b|product number|^code", "product_code"),
    (r"botanical name|latin name|inci name", "botanical_name"),
    (r"part used|plant part|parts? of plant", "plant_part"),
    (r"extraction|method of (production|extraction)|^process", "extraction_method"),
    (r"country of origin|^origin", "origin"),
    (r"chemical name|iupac", "chemical_name"),
    (r"burning effectiveness|bloom in", "performance_application"),
]
LABEL_RES = [(re.compile(p), f) for p, f in LABEL_FIELDS]

CLP_CLASS_RE = re.compile(r"\b(Flam\. ?Liq\.|Skin Irrit\.|Skin Sens\.|Skin Corr\.|Eye Irrit\.|Eye Dam\.|Aquatic Acute|"
                          r"Aquatic Chronic|Asp\. ?Tox\.|Acute Tox\.|Repr\.|STOT ?SE|STOT ?RE|Muta\.|Carc\.|Resp\. ?Sens\.)"
                          r"\s*(\d[A-C]?)", re.I)
H_RE = re.compile(r"\b(EUH\d{3}|H[234]\d{2}(?:[A-Za-z]{1,2})?)\b")
SIGNAL_RE = re.compile(r"signal word\s*[:\-]?\s*(danger|warning|none)", re.I)
ISO_RE = re.compile(r"\bISO\s?(\d{3,5})(?::\s?(\d{4}))?")
DOSE_RANGE_RE = re.compile(r"(?:use level|usage|use|dosage|recommended|level)[^.%\n]{0,50}?(?:up to|from|between|of|:)?\s*"
                           r"(\d+(?:[.,]\d+)?)\s*%?\s*(?:-|–|to|and)\s*(\d+(?:[.,]\d+)?)\s*%", re.I)
DOSE_UPTO_RE = re.compile(r"(?:use level|usage|use|dosage|recommended|level)[^.%\n]{0,50}?(?:up to|max(?:imum)?(?: of)?|<=?)\s*"
                          r"(\d+(?:[.,]\d+)?)\s*%", re.I)
VP_RE = re.compile(r"vapou?r pressure[^0-9\n]{0,40}?(\d+(?:[.,]\d+)?(?:\s*[eE]\s*-?\d+)?)\s*(hpa|kpa|pa|mm ?hg|mmhg|torr)"
                   r"(?:[^0-9\n]{0,15}(\d{1,3})\s*°?\s*c)?", re.I)
FP_RE = re.compile(r"flash ?point[^0-9<>\n]{0,40}?([<>]=?)?\s*(\d+(?:[.,]\d+)?)\s*°?\s*([CF])\b", re.I)
DENS_RE = re.compile(r"(specific gravity|relative density|density)[^0-9\n]{0,40}?([01][.,]\d{2,4})(?:\s*(?:-|–|to)\s*([01][.,]\d{2,4}))?", re.I)
RI_RE = re.compile(r"refractive index[^0-9\n]{0,40}?(1[.,]\d{3,4})(?:\s*(?:-|–|to)\s*(1[.,]\d{3,4}))?", re.I)
LOGP_RE = re.compile(r"\blog\s?(?:p|pow|kow)\b[^0-9\n]{0,15}?(-?\d+(?:[.,]\d+)?)", re.I)
TEN_RE = re.compile(r"(tenacity|substantivity|longevity)(?: on (?:blotter|strip|paper))?[^0-9<>\n]{0,30}?([<>]\s*)?(\d+(?:[.,]\d+)?)\s*(hours?|hrs?|h\b|days?|weeks?)", re.I)
BP_RE = re.compile(r"boiling point[^0-9\n]{0,40}?(\d{2,3}(?:[.,]\d+)?)\s*°?\s*C", re.I)


def load_text(doc_row):
    """Return (title, full_text, label_value_pairs) for a cached document."""
    path = ROOT / doc_row["raw_path"]
    kind = doc_row["content_type"]
    if kind == "pdf":
        return _pdf_text(path)
    if kind in ("html", "xml"):
        return _html_text(path.read_bytes())
    return "", "", []


def _pdf_text(path):
    import pdfplumber
    texts = []
    try:
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages[:40]:
                texts.append(page.extract_text() or "")
    except Exception as exc:  # corrupt / encrypted PDFs are reported, not fatal
        return "", f"[PDF_PARSE_ERROR {type(exc).__name__}]", []
    text = "\n".join(texts)
    title = next((ln.strip() for ln in text.splitlines() if len(ln.strip()) > 3), "")[:200]
    pairs = []
    for ln in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z ()/.\-°]{2,45}?)\s*[:：]\s*(.+)$", ln)
        if m:
            pairs.append((m.group(1).strip(), m.group(2).strip(), "pdf_line"))
    return title, text, pairs


def _html_text(body):
    soup = BeautifulSoup(body, "lxml")
    title = (soup.title.get_text(" ", strip=True) if soup.title else "")[:200]
    for t in soup(["script", "style", "noscript", "svg"]):
        t.decompose()
    pairs = []
    # (1) Givaudan-style: <span class="property field-X">Label</span> ... <span class="property-value field-X">
    labels = {}
    for sp in soup.select("span.property"):
        cls = [c for c in sp.get("class", []) if c.startswith("field-")]
        if cls and "property-value" not in sp.get("class", []):
            labels.setdefault(cls[0], sp.get_text(" ", strip=True))
    for sp in soup.select("span.property-value"):
        cls = [c for c in sp.get("class", []) if c.startswith("field-")]
        if cls and cls[0] in labels:
            val = sp.get_text(" ", strip=True)
            if "star" in sp.get("class", []):
                val = f"{val.count(chr(9733))}/5 stars"
            pairs.append((labels[cls[0]], val, "html_property"))
    # (2) two-cell table rows, definition lists
    for tr in soup.find_all("tr"):
        cells = tr.find_all(["th", "td"])
        if len(cells) == 2:
            a, b = (c.get_text(" ", strip=True) for c in cells)
            if a and b and len(a) < 60:
                pairs.append((a, b, "html_table"))
    for dt in soup.find_all("dt"):
        dd = dt.find_next_sibling("dd")
        if dd:
            pairs.append((dt.get_text(" ", strip=True), dd.get_text(" ", strip=True), "html_dl"))
    # (3) intro / description paragraphs
    intro = soup.select_one("p.ingredient-intro")
    if intro:
        pairs.append(("Odour description", intro.get_text(" ", strip=True), "html_intro"))
    for meta in soup.find_all("meta", attrs={"name": "description"}):
        if meta.get("content"):
            pairs.append(("meta description", meta["content"], "html_meta"))
    text = soup.get_text("\n")
    text = re.sub(r"\n\s*\n+", "\n", text)
    for ln in text.splitlines():
        m = re.match(r"^\s*([A-Za-z][A-Za-z ()/.\-°]{2,45}?)\s*[:：]\s*(.{1,300})$", ln)
        if m:
            pairs.append((m.group(1).strip(), m.group(2).strip(), "text_line"))
    return title, text, pairs


def label_field(label):
    lab = re.sub(r"\s+", " ", label.lower()).strip(" :")
    for rx, field in LABEL_RES:
        if rx.search(lab):
            return field   # may be None for explicitly excluded labels
    return None


NOISE_VALUE_RE = re.compile(r"^\W*(not (determined|available|applicable|established|relevant|known)|no data( available)?|n\.?\s?/?\s?a\.?|"
                            r"conforms?( to (standard|reference))?|complies|characteristic( odou?r)?|typical|none|unknown|-+|"
                            r"0(?:[.,]0+)?)\W*$", re.I)


def is_noise(value):
    return bool(NOISE_VALUE_RE.match(value.strip()))


def is_sds(text):
    t = text[:20000].lower()
    return ("safety data sheet" in t or "fiche de données de sécurité" in t or "material safety data" in t) and \
           ("hazard" in t or "section 2" in t)


def sds_sections(text):
    """Split an SDS into {section_number: text} using 'SECTION n' / 'n. ' headings."""
    secs = {}
    marks = list(re.finditer(r"(?im)^\s*(?:section|rubrique)\s*(\d{1,2})\b|^\s*(\d{1,2})\.?\s+(?=[A-Z][a-z])", text))
    for i, m in enumerate(marks):
        n = int(m.group(1) or m.group(2))
        if not 1 <= n <= 16:
            continue
        end = marks[i + 1].start() if i + 1 < len(marks) else len(text)
        secs.setdefault(n, "")
        secs[n] += text[m.start():end]
    return secs


def _ctx(text, start, end):
    return short(text[max(0, start - 60): end + 80], 200)


def extract_claims(title, text, pairs, *, doc_kind_hint=None, species_terms=(), marker_terms=()):
    """Return a list of raw claims: dict(field, raw_value, context, extractor)."""
    claims = []

    def add(field, value, context, extractor):
        value = short(value, 300)
        if value and not any(c["field"] == field and c["raw_value"] == value for c in claims):
            claims.append({"field": field, "raw_value": value, "context": short(context, 200), "extractor": extractor})

    # --- label/value pairs (most reliable)
    for label, value, how in pairs:
        f = label_field(label)
        if not f or not value or is_noise(value):
            continue
        if f == "cas":
            for cas in find_cas(value):
                add("cas", cas, f"{label}: {value}", how)
            continue
        if f in ("odour_description",) and len(value) < 8:
            continue
        add(f, value, f"{label}: {value}", how)

    # --- free-text regexes
    for m in VP_RE.finditer(text):
        add("vapour_pressure", " ".join(x for x in m.groups() if x), _ctx(text, m.start(), m.end()), "regex_vp")
    for m in FP_RE.finditer(text):
        add("flash_point", f"{m.group(1) or ''}{m.group(2)} {m.group(3).upper()}", _ctx(text, m.start(), m.end()), "regex_fp")
    for m in DENS_RE.finditer(text):
        add("density", m.group(2) + (f"-{m.group(3)}" if m.group(3) else ""), _ctx(text, m.start(), m.end()), "regex_density")
    for m in RI_RE.finditer(text):
        add("refractive_index", m.group(1) + (f"-{m.group(2)}" if m.group(2) else ""), _ctx(text, m.start(), m.end()), "regex_ri")
    for m in LOGP_RE.finditer(text):
        add("logp", m.group(1), _ctx(text, m.start(), m.end()), "regex_logp")
    for m in TEN_RE.finditer(text):
        add("tenacity", f"{(m.group(2) or '').strip()}{m.group(3)} {m.group(4)}", _ctx(text, m.start(), m.end()), "regex_tenacity")
    for m in BP_RE.finditer(text):
        add("boiling_point", f"{m.group(1)} C", _ctx(text, m.start(), m.end()), "regex_bp")
    for m in DOSE_RANGE_RE.finditer(text):
        add("use_level", f"{m.group(1)}-{m.group(2)}%", _ctx(text, m.start(), m.end()), "regex_dose_range")
    for m in DOSE_UPTO_RE.finditer(text):
        add("use_level", f"up to {m.group(1)}%", _ctx(text, m.start(), m.end()), "regex_dose_upto")
    for m in ISO_RE.finditer(text):
        add("iso_standard", f"ISO {m.group(1)}" + (f":{m.group(2)}" if m.group(2) else ""), _ctx(text, m.start(), m.end()), "regex_iso")
    for cas in find_cas(text):
        i = text.find(cas)
        add("cas_mentioned", cas, _ctx(text, i, i + len(cas)), "regex_cas_anywhere")

    # --- species / botanical terms (naturals)
    low = text.lower()
    for sp in species_terms:
        m = re.search(r"(?<![a-z])" + re.escape(sp.lower()) + r"(?![a-z])", low)
        if m:
            add("botanical_name", sp, _ctx(text, m.start(), m.end()), "species_match")

    # --- GC-MS marker constituents with a percentage nearby (reference composition)
    sds_doc = doc_kind_hint == "SDS" or is_sds(text)
    for mk in ([] if sds_doc else marker_terms):
        for m in re.finditer(r"(?<![a-z])" + re.escape(mk) + r"(?![a-z])", text, re.I):
            window = text[m.end(): m.end() + 45]
            # free text: a percentage must be printed explicitly (e.g. 'linalyl acetate 30-45%')
            num = re.match(r"[^0-9\n%]{0,15}?(\d{1,2}(?:[.,]\d{1,2})?)\s*(?:(?:-|–|to)\s*(\d{1,2}(?:[.,]\d{1,2})?)\s*)?%", window)
            if num:
                add(f"composition:{mk}", num.group(1) + (f"-{num.group(2)}" if num.group(2) else "") + "%",
                    _ctx(text, m.start(), m.end() + num.end()), "marker_pct")
                break

    # --- SDS / CLP
    if sds_doc:
        secs = sds_sections(text)
        s1 = secs.get(1, text[:3000])
        m = re.search(r"(?i)(product name|trade name|product identifier|commercial name|name of the product)\s*[:\-]?\s*(.{2,80})", s1)
        if m:
            add("sds_product_name", m.group(2).strip(), _ctx(s1, m.start(), m.end()), "sds_s1")
        s2 = secs.get(2, "")
        if not s2:
            # headings such as '02 Hazard(s) identification': classification window = from the hazards heading
            # to the composition section (component H-codes of section 3 and the section-16 list are excluded)
            st = re.search(r"(?i)hazards?\(?s?\)?\s+identification|classification of the (substance|mixture)", text)
            if st:
                en = re.search(r"(?i)composition\s*/\s*information|information on ingredients|\n\s*(?:section\s*)?0?3[\s.:]+", text[st.end():])
                s2 = text[st.start(): st.end() + (en.start() if en else 4000)]
        scope = s2 or text[:6000]
        for m in CLP_CLASS_RE.finditer(scope):
            add("clp_class", f"{m.group(1)} {m.group(2)}", _ctx(scope, m.start(), m.end()), "sds_s2" if s2 else "sds_anywhere")
        for m in H_RE.finditer(scope):
            add("h_statement", m.group(1)[:4] if not m.group(1).startswith("EUH") else m.group(1), _ctx(scope, m.start(), m.end()),
                "sds_s2" if s2 else "sds_anywhere")
        m = SIGNAL_RE.search(scope)
        if m:
            add("signal_word", m.group(1).capitalize(), _ctx(scope, m.start(), m.end()), "sds_s2")
        s3 = secs.get(3, "")
        for cas in find_cas(s3):
            i = s3.find(cas)
            add("sds_component_cas", cas, _ctx(s3, i, i + len(cas)), "sds_s3")
        for n, field in ((7, "storage"), (10, "stability_text")):
            sec = secs.get(n, "")
            if sec:
                body = re.sub(r"\s+", " ", sec)[:600]
                key = re.search(r"(?i)(store[^.]{5,160}\.|stable[^.]{5,160}\.)", body)
                if key:
                    add(field, key.group(1), key.group(1), f"sds_s{n}")
        add("doc_is_sds", "yes", title, "sds_detect")
    return claims
