"""Polite, cached, robots-aware fetcher.

Rules enforced here (never bypassed):
  * robots.txt is honoured for our own user agent AND for Anthropic/Claude agent names;
    if any of them is disallowed the URL is not fetched -> MANUAL_RETRIEVAL_REQUIRED.
  * one request at a time, per-domain minimum interval (or Crawl-delay if larger).
  * 401/403/429 or a bot-challenge page -> the domain is marked blocked for the run and
    every further URL on it becomes MANUAL_RETRIEVAL_REQUIRED (no retries, no UA tricks).
  * login pages / paywalls are not handled: MANUAL_RETRIEVAL_REQUIRED.
Every fetched body is cached once under data/cache/<sha256>, keyed by content hash.
"""
import hashlib
import re
import time
from urllib.parse import urlsplit

import requests

from .common import CACHE, SETTINGS, canonical_url, domain_info, get_logger, now_iso, registered_domain

log = get_logger("fetch")
UA = SETTINGS["user_agent"]
_session = requests.Session()
_session.headers.update({"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/pdf,application/json;q=0.9,*/*;q=0.5",
                         "Accept-Language": "en,fr;q=0.8,es;q=0.6"})
_last_hit = {}
_robots_cache = {}

CHALLENGE_MARKERS = ("cf-chl", "challenge-platform", "Just a moment...", "Attention Required! | Cloudflare",
                     "captcha", "px-captcha", "Access Denied</title>")


# ---------------------------------------------------------------- robots.txt
def _parse_robots(text):
    groups, cur_agents, cur_rules, last_was_agent = [], [], [], False
    for raw in text.splitlines():
        line = raw.split("#", 1)[0].strip()
        if ":" not in line:
            continue
        k, v = [x.strip() for x in line.split(":", 1)]
        k = k.lower()
        if k == "user-agent":
            if not last_was_agent and cur_agents:
                groups.append((cur_agents, cur_rules))
                cur_agents, cur_rules = [], []
            cur_agents.append(v.lower())
            last_was_agent = True
        elif k in ("allow", "disallow", "crawl-delay"):
            cur_rules.append((k, v))
            last_was_agent = False
    if cur_agents:
        groups.append((cur_agents, cur_rules))
    return groups


def _rule_re(pattern):
    esc = re.escape(pattern).replace(r"\*", ".*")
    if esc.endswith(r"\$"):
        esc = esc[:-2] + "$"
    return re.compile(esc)


def _agent_rules(groups, agent):
    agent = agent.lower()
    specific = [rules for agents, rules in groups if any(a != "*" and a in agent for a in agents)]
    if specific:
        return [r for rules in specific for r in rules]
    return [r for agents, rules in groups if "*" in agents for r in rules]


def _allowed(rules, path):
    best_len, verdict = -1, True
    for k, v in rules:
        if k == "crawl-delay" or (k == "disallow" and v == ""):
            continue
        if _rule_re(v).match(path):
            ln = len(v)
            if ln > best_len or (ln == best_len and k == "allow"):
                best_len, verdict = ln, (k == "allow")
    return verdict


def robots_check(url):
    """Return (allowed: bool, crawl_delay: float|None, note)."""
    parts = urlsplit(url)
    base = f"{parts.scheme}://{parts.netloc}"
    if base not in _robots_cache:
        try:
            r = _session.get(base + "/robots.txt", timeout=SETTINGS["request_timeout_s"])
            if r.status_code == 200:
                _robots_cache[base] = ("OK", _parse_robots(r.text))
            elif r.status_code in (401, 403):
                _robots_cache[base] = ("ROBOTS_FORBIDDEN", [])
            else:
                _robots_cache[base] = ("NO_ROBOTS", [])
        except requests.RequestException as exc:
            _robots_cache[base] = ("UNREACHABLE", str(exc)[:200])
    status, groups = _robots_cache[base]
    if status == "UNREACHABLE":
        return None, None, f"robots.txt unreachable: {groups}"
    if status == "ROBOTS_FORBIDDEN":
        return False, None, "robots.txt itself returns 401/403 (site blocks automated clients)"
    if status == "NO_ROBOTS":
        return True, None, "no robots.txt"
    path = parts.path or "/"
    if parts.query:
        path += "?" + parts.query
    delay = None
    for agent in SETTINGS["robots_agents_checked"]:
        rules = _agent_rules(groups, agent)
        for k, v in rules:
            if k == "crawl-delay":
                try:
                    delay = max(delay or 0, float(v))
                except ValueError:
                    pass
        if not _allowed(rules, path):
            return False, delay, f"robots.txt disallows {agent} for {path}"
    return True, delay, "allowed by robots.txt"


# ---------------------------------------------------------------- fetch
def _wait(domain, delay, base=None):
    gap = max(SETTINGS["default_min_interval_s"] if base is None else base, delay or 0)
    last = _last_hit.get(domain)
    if last is not None:
        sleep = gap - (time.time() - last)
        if sleep > 0:
            time.sleep(sleep)
    _last_hit[domain] = time.time()


def _kind(content_type, body):
    ct = (content_type or "").lower()
    if body[:5] == b"%PDF-" or "pdf" in ct:
        return "pdf"
    if "json" in ct:
        return "json"
    if "html" in ct or body.lstrip()[:15].lower().startswith((b"<!doctype", b"<html")):
        return "html"
    if "xml" in ct:
        return "xml"
    return "other"


def fetch(con, url, *, force=False):
    """Fetch url once (cached). Returns dict(status, doc_id, http_status, note, final_url).

    status in: FETCHED, CACHED, MANUAL_RETRIEVAL_REQUIRED, ROBOTS_DISALLOWED, ENV_UNREACHABLE,
               HTTP_ERROR, UNSUPPORTED_CONTENT, TOO_LARGE
    """
    canon = canonical_url(url)
    row = con.execute("SELECT * FROM fetch_log WHERE canonical_url=?", (canon,)).fetchone()
    if row and not force and row["status"] in ("FETCHED", "CACHED", "MANUAL_RETRIEVAL_REQUIRED", "ROBOTS_DISALLOWED",
                                               "UNSUPPORTED_CONTENT", "TOO_LARGE", "HTTP_ERROR"):
        return dict(row) | {"status": "CACHED" if row["status"] == "FETCHED" else row["status"]}
    domain = registered_domain(url)

    def record(status, http_status=None, doc_id=None, note="", final_url=None):
        con.execute("INSERT OR REPLACE INTO fetch_log(canonical_url,url,final_url,domain,status,http_status,doc_id,note,at)"
                    " VALUES (?,?,?,?,?,?,?,?,?)", (canon, url, final_url, domain, status, http_status, doc_id, note, now_iso()))
        con.commit()
        return {"status": status, "http_status": http_status, "doc_id": doc_id, "note": note, "final_url": final_url,
                "canonical_url": canon, "url": url, "domain": domain}

    dstat = con.execute("SELECT status, note FROM domain_status WHERE domain=?", (domain,)).fetchone()
    if domain == "doi.org":
        dstat = None
    if dstat and dstat["status"] in ("BLOCKED", "UNREACHABLE"):
        st = "MANUAL_RETRIEVAL_REQUIRED" if dstat["status"] == "BLOCKED" else "ENV_UNREACHABLE"
        return record(st, note=f"domain {dstat['status'].lower()} earlier in run: {dstat['note']}")

    allowed, delay, rnote = robots_check(url)
    if allowed is None:
        _mark_domain(con, domain, "UNREACHABLE", rnote)
        return record("ENV_UNREACHABLE", note=rnote)
    if not allowed:
        return record("ROBOTS_DISALLOWED", note=rnote + " -> MANUAL_RETRIEVAL_REQUIRED")

    _wait(domain, delay)
    try:
        r = _session.get(url, timeout=SETTINGS["request_timeout_s"], allow_redirects=True, stream=True)
        body = b""
        for chunk in r.iter_content(65536):
            body += chunk
            if len(body) > SETTINGS["max_bytes"]:
                return record("TOO_LARGE", r.status_code, note="exceeds max_bytes")
    except requests.RequestException as exc:
        note = f"{type(exc).__name__}: {str(exc)[:160]}"
        _mark_domain(con, domain, "UNREACHABLE", note)
        return record("ENV_UNREACHABLE", note=note)

    head = body[:6000].decode("utf-8", "ignore")
    if r.status_code in (401, 403, 429) or (r.status_code >= 400 and any(m in head for m in CHALLENGE_MARKERS)):
        note = f"HTTP {r.status_code} (site refuses automated access; not bypassed)"
        # block the domain that actually refused (redirectors such as doi.org stay usable)
        _mark_domain(con, registered_domain(r.url), "BLOCKED", note)
        return record("MANUAL_RETRIEVAL_REQUIRED", r.status_code, note=note, final_url=r.url)
    if r.status_code >= 400:
        return record("HTTP_ERROR", r.status_code, note=f"HTTP {r.status_code}", final_url=r.url)
    title_m = re.search(r"<title>([^<]{0,120})", head, re.I)
    ptitle = title_m.group(1) if title_m else ""
    # Cloudflare injects '/cdn-cgi/challenge-platform/' scripts into normal pages too: only a real
    # interstitial (challenge title, or a tiny page carrying cf-chl) counts as a block.
    if re.search(r"just a moment|attention required|access denied|verify you are human", ptitle, re.I) or \
            ("cf-chl" in head and len(body) < 20000) or \
            (len(body) < 30000 and re.search(r"captcha|are you a robot|unusual traffic|bot detection", head, re.I)):
        _mark_domain(con, domain, "BLOCKED", "bot challenge page")
        return record("MANUAL_RETRIEVAL_REQUIRED", r.status_code, note="bot challenge page served", final_url=r.url)

    kind = _kind(r.headers.get("Content-Type"), body)
    if kind == "other":
        return record("UNSUPPORTED_CONTENT", r.status_code, note=r.headers.get("Content-Type", ""), final_url=r.url)
    doc_id = hashlib.sha256(body).hexdigest()
    ext = {"pdf": "pdf", "html": "html", "json": "json", "xml": "xml"}[kind]
    path = CACHE / doc_id[:2] / f"{doc_id}.{ext}"
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_bytes(body)
    info = domain_info(r.url)
    existing = con.execute("SELECT doc_id FROM documents WHERE doc_id=?", (doc_id,)).fetchone()
    if not existing:
        con.execute("INSERT INTO documents(doc_id, first_url, canonical_url, domain, tier, manufacturer, license_class,"
                    " content_type, doc_kind, raw_path, bytes, fetched_at) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                    (doc_id, url, canonical_url(r.url), registered_domain(r.url), info["tier"], info.get("manufacturer"),
                     info["license"], kind, None, str(path.relative_to(CACHE.parent.parent)), len(body), now_iso()))
    con.execute("INSERT OR IGNORE INTO doc_urls(doc_id, canonical_url) VALUES (?,?)", (doc_id, canon))
    con.execute("INSERT OR IGNORE INTO doc_urls(doc_id, canonical_url) VALUES (?,?)", (doc_id, canonical_url(r.url)))
    con.commit()
    note = "exact duplicate of an already cached document (same sha256)" if existing else ""
    return record("FETCHED", r.status_code, doc_id, note, r.url)


def _mark_domain(con, domain, status, note):
    con.execute("INSERT OR REPLACE INTO domain_status(domain, status, note, at) VALUES (?,?,?,?)",
                (domain, status, note, now_iso()))
    con.commit()
    log.warning("domain %s marked %s: %s", domain, status, note)


_api_down = {}


def api_get(url, *, params=None, min_interval=1.0, as_json=True):
    """For documented public APIs (PubChem PUG, NCBI E-utilities). Rate limited, no caching of errors.
    Circuit breaker: after 2 calls that end rate-limited, the API is treated as unavailable for this run."""
    domain = registered_domain(url)
    if _api_down.get(domain, 0) >= 2:
        raise requests.HTTPError(f"{domain} unavailable for this run (repeated 429/503; not retried)")
    for attempt in range(3):
        _wait(domain, None, base=min_interval)
        r = _session.get(url, params=params, timeout=SETTINGS["request_timeout_s"])
        if r.status_code not in (429, 503):
            break
        # documented API rate limit: back off (Retry-After if given) and try at most twice more
        pause = float(r.headers.get("Retry-After") or 0) or (10 * (attempt + 1) ** 2)
        log.warning("429 from %s, backing off %.0fs (attempt %d)", domain, pause, attempt + 1)
        time.sleep(pause)
    if r.status_code in (429, 503):
        _api_down[domain] = _api_down.get(domain, 0) + 1
    if r.status_code == 404:
        return None
    r.raise_for_status()
    return r.json() if as_json else r.content
