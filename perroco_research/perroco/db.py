"""SQLite staging layer. Every stage writes here; nothing is ever written to the master.

Pipeline layers (never skipped):
  RAW SOURCE (documents, fetch_log, data/cache)  ->  EXTRACTED CLAIM (claims)
  -> NORMALISED CLAIM (claims.norm_*)  ->  VALIDATION (claims.validation, conflicts)
  -> PROPOSED CHANGE (proposed_changes; exported to output/proposed_changes.jsonl)
"""
import json
import sqlite3

from .common import DB_PATH, now_iso

STATES = [
    "NOT_STARTED", "SEARCHING", "SOURCES_FOUND", "EXTRACTED", "NEEDS_REVIEW", "VALIDATED",
    "NO_PUBLIC_DATA_FOUND", "PUBLIC_RESEARCH_EXHAUSTED", "ERROR",
]

SCHEMA = """
CREATE TABLE IF NOT EXISTS materials (
  palette_id TEXT PRIMARY KEY, school_name TEXT, pilot_group TEXT, chart_kind TEXT,
  state TEXT NOT NULL DEFAULT 'NOT_STARTED', state_note TEXT, stage_done TEXT DEFAULT '',
  master_json TEXT, updated_at TEXT);
CREATE TABLE IF NOT EXISTS state_history (
  id INTEGER PRIMARY KEY AUTOINCREMENT, palette_id TEXT, from_state TEXT, to_state TEXT,
  note TEXT, at TEXT);
CREATE TABLE IF NOT EXISTS queries (
  id INTEGER PRIMARY KEY AUTOINCREMENT, palette_id TEXT, query TEXT, purpose TEXT,
  provider TEXT, executed_at TEXT, n_results INTEGER, provider_summary TEXT,
  UNIQUE(palette_id, provider, query));
CREATE TABLE IF NOT EXISTS leads (
  id INTEGER PRIMARY KEY AUTOINCREMENT, palette_id TEXT, query_id INTEGER, rank INTEGER,
  url TEXT, canonical_url TEXT, title TEXT, domain TEXT, tier TEXT, priority REAL,
  selected INTEGER DEFAULT 0, UNIQUE(palette_id, query_id, canonical_url));
CREATE TABLE IF NOT EXISTS fetch_log (
  canonical_url TEXT PRIMARY KEY, url TEXT, final_url TEXT, domain TEXT, status TEXT,
  http_status INTEGER, doc_id TEXT, note TEXT, at TEXT);
CREATE TABLE IF NOT EXISTS documents (
  doc_id TEXT PRIMARY KEY, first_url TEXT, canonical_url TEXT, domain TEXT, tier TEXT,
  manufacturer TEXT, license_class TEXT, content_type TEXT, doc_kind TEXT, title TEXT,
  raw_path TEXT, text_path TEXT, bytes INTEGER, fetched_at TEXT, duplicate_of TEXT,
  duplicate_basis TEXT, derived_from TEXT);
CREATE TABLE IF NOT EXISTS doc_urls (
  doc_id TEXT, canonical_url TEXT, PRIMARY KEY(doc_id, canonical_url));
CREATE TABLE IF NOT EXISTS doc_material (
  doc_id TEXT, palette_id TEXT, match_class TEXT, match_score REAL, reasons TEXT,
  accepted INTEGER, reject_reason TEXT, PRIMARY KEY(doc_id, palette_id));
CREATE TABLE IF NOT EXISTS claims (
  claim_id TEXT PRIMARY KEY, palette_id TEXT, doc_id TEXT, url TEXT, field TEXT,
  raw_value TEXT, context TEXT, extractor TEXT, evidence_level TEXT, tier TEXT,
  license_class TEXT, match_class TEXT, scope TEXT,
  norm_value REAL, norm_min REAL, norm_max REAL, norm_unit TEXT, norm_text TEXT, norm_note TEXT,
  validation TEXT, validation_note TEXT, independent_group TEXT, created_at TEXT);
CREATE TABLE IF NOT EXISTS conflicts (
  conflict_id TEXT PRIMARY KEY, palette_id TEXT, field TEXT, claim_ids TEXT, values_json TEXT,
  includes_master INTEGER, detail TEXT);
CREATE TABLE IF NOT EXISTS proposed_changes (
  change_id TEXT PRIMARY KEY, palette_id TEXT, target_sheet TEXT, operation TEXT,
  payload TEXT, review_status TEXT, confidence TEXT, rationale TEXT, evidence TEXT);
CREATE TABLE IF NOT EXISTS domain_status (
  domain TEXT PRIMARY KEY, status TEXT, note TEXT, at TEXT);
"""


def connect():
    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    con.executescript(SCHEMA)
    return con


def set_state(con, palette_id, state, note=""):
    assert state in STATES, state
    row = con.execute("SELECT state FROM materials WHERE palette_id=?", (palette_id,)).fetchone()
    old = row["state"] if row else None
    if old != state:
        con.execute("INSERT INTO state_history(palette_id, from_state, to_state, note, at) VALUES (?,?,?,?,?)",
                    (palette_id, old, state, note, now_iso()))
    con.execute("UPDATE materials SET state=?, state_note=?, updated_at=? WHERE palette_id=?",
                (state, note, now_iso(), palette_id))
    con.commit()


def mark_stage(con, palette_id, stage):
    row = con.execute("SELECT stage_done FROM materials WHERE palette_id=?", (palette_id,)).fetchone()
    done = set(filter(None, (row["stage_done"] or "").split(",")))
    done.add(stage)
    con.execute("UPDATE materials SET stage_done=? WHERE palette_id=?", (",".join(sorted(done)), palette_id))
    con.commit()


def stage_done(con, palette_id, stage):
    row = con.execute("SELECT stage_done FROM materials WHERE palette_id=?", (palette_id,)).fetchone()
    return stage in set((row["stage_done"] or "").split(",")) if row else False


def master_record(con, palette_id):
    row = con.execute("SELECT master_json FROM materials WHERE palette_id=?", (palette_id,)).fetchone()
    return json.loads(row["master_json"]) if row and row["master_json"] else {}
