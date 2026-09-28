"""Shared paths, configuration, logging and small helpers."""
import json
import logging
import re
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

ROOT = Path(__file__).resolve().parent.parent
CONFIG = ROOT / "config"
DATA = ROOT / "data"
CACHE = DATA / "cache"
INGEST = DATA / "search_ingest"
MANIFESTS = DATA / "manifests"
LOGS = ROOT / "logs"
OUTPUT = ROOT / "output"
DB_PATH = DATA / "staging.sqlite"

for _p in (CACHE, INGEST, MANIFESTS, LOGS, OUTPUT):
    _p.mkdir(parents=True, exist_ok=True)


def load_json(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


SETTINGS = load_json(CONFIG / "settings.json")
DOMAINS = load_json(CONFIG / "domains.json")


def now_iso():
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def get_logger(name="perroco"):
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        fmt = logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s")
        fh = logging.FileHandler(LOGS / "pipeline.log", encoding="utf-8")
        fh.setFormatter(fmt)
        sh = logging.StreamHandler()
        sh.setFormatter(fmt)
        logger.addHandler(fh)
        logger.addHandler(sh)
    return logger


TRACKING_PARAMS = re.compile(r"^(utm_.*|gclid|fbclid|srsltid|mc_cid|mc_eid|_ga|ref|source)$", re.I)


def canonical_url(url):
    """Canonical form used for de-duplication: lower-case scheme/host, no www., no
    fragment, no tracking parameters, sorted query, no trailing slash (except root)."""
    url = url.strip()
    parts = urlsplit(url)
    scheme = "https" if parts.scheme in ("http", "https") else parts.scheme
    host = parts.netloc.lower()
    if host.startswith("www."):
        host = host[4:]
    path = re.sub(r"/{2,}", "/", parts.path or "/")
    if len(path) > 1 and path.endswith("/"):
        path = path[:-1]
    query = urlencode(sorted((k, v) for k, v in parse_qsl(parts.query, keep_blank_values=True)
                             if not TRACKING_PARAMS.match(k)))
    return urlunsplit((scheme, host, path, query, ""))


def registered_domain(url):
    host = urlsplit(url).netloc.lower().split(":")[0]
    if host.startswith("www."):
        host = host[4:]
    return host


def domain_info(url):
    """Look up the domain registry, matching on the longest registered suffix."""
    host = registered_domain(url)
    best = None
    for dom, info in DOMAINS["domains"].items():
        if host == dom or host.endswith("." + dom):
            if best is None or len(dom) > len(best[0]):
                best = (dom, info)
    if best:
        return dict(best[1], domain_key=best[0])
    return {"tier": "SECONDARY", "license": "UNKNOWN_LICENSE", "domain_key": host}


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm_text(s):
    # drop trademark signs BEFORE accent stripping (NFKD turns the TM sign into the letters 'TM')
    s = str(s or "").replace("™", " ").replace("®", " ").replace("©", " ")
    s = strip_accents(s).lower()
    s = re.sub(r"[^a-z0-9%.,+\-/ ]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()


CAS_RE = re.compile(r"(?<![\d-])(\d{2,7})-(\d{2})-(\d)(?![\d-])")


def cas_checksum_ok(cas):
    m = re.fullmatch(r"(\d{2,7})-(\d{2})-(\d)", cas)
    if not m:
        return False
    digits = (m.group(1) + m.group(2))[::-1]
    return sum((i + 1) * int(d) for i, d in enumerate(digits)) % 10 == int(m.group(3))


def find_cas(text):
    out = []
    for m in CAS_RE.finditer(text or ""):
        cas = m.group(0)
        if cas_checksum_ok(cas) and cas not in out:
            out.append(cas)
    return out


# stabilisers / carriers that appear as SDS components of commercial grades (not identity CAS)
ADDITIVE_CAS = {"10191-41-0": "DL-alpha-tocopherol", "59-02-9": "alpha-tocopherol", "128-37-0": "BHT",
                "25265-71-8": "dipropylene glycol", "110-27-0": "isopropyl myristate", "77-93-0": "triethyl citrate",
                "120-51-4": "benzyl benzoate", "64-17-5": "ethanol", "57-55-6": "propylene glycol",
                "1406-18-4": "vitamin E", "7695-91-2": "tocopheryl acetate"}


def short(s, n=200):
    s = re.sub(r"\s+", " ", str(s or "")).strip()
    return s if len(s) <= n else s[: n - 1] + "…"
