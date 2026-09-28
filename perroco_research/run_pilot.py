#!/usr/bin/env python3
"""Perroco Lab research pipeline — pilot runner.

    python run_pilot.py            # run (or resume) every stage for every pilot material
    python run_pilot.py --stage fetch --only S-0372
    python run_pilot.py --redo extract   # recompute one stage (keeps cache; no re-download)
    python run_pilot.py --status   # show material states

Resumable: completed stages are recorded per material in data/staging.sqlite and skipped
on the next run; downloaded documents are cached by content hash and never re-downloaded.
The master workbook is only read, never written.
"""
import argparse
import sys
import traceback

from perroco import db, formulas, pipeline, propose, report
from perroco.common import get_logger

STAGES = ["search", "fetch", "extract", "validate", "propose"]
log = get_logger("run")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=STAGES + ["report", "dedupe", "all"], default="all")
    ap.add_argument("--only", nargs="*", help="palette ids")
    ap.add_argument("--redo", choices=STAGES, help="force a stage (and the stages after it) to run again")
    ap.add_argument("--status", action="store_true")
    a = ap.parse_args()
    con = db.connect()
    pipeline.stage_init(con)
    ids = a.only or pipeline.pilot_ids()
    if a.status:
        for r in con.execute("SELECT palette_id, school_name, state, stage_done, state_note FROM materials ORDER BY palette_id"):
            print(f"{r['palette_id']:7} {r['state']:22} [{r['stage_done']}] {r['school_name']} — {r['state_note']}")
        return
    if a.redo:
        drop = STAGES[STAGES.index(a.redo):]
        for pid in ids:
            row = con.execute("SELECT stage_done FROM materials WHERE palette_id=?", (pid,)).fetchone()
            keep = [s for s in (row["stage_done"] or "").split(",") if s and s not in drop]
            con.execute("UPDATE materials SET stage_done=? WHERE palette_id=?", (",".join(keep), pid))
        con.commit()
    run = STAGES if a.stage == "all" else ([a.stage] if a.stage in STAGES else [])
    funcs = {"search": pipeline.stage_search, "fetch": pipeline.stage_fetch, "extract": pipeline.stage_extract,
             "validate": pipeline.stage_validate, "propose": propose.build}
    for stage in run:
        if stage == "validate":
            pipeline.stage_dedupe(con)
        for pid in ids:
            if db.stage_done(con, pid, stage):
                continue
            try:
                log.info("== %s %s", stage, pid)
                funcs[stage](con, pid)
            except Exception as exc:
                log.error("%s failed for %s: %s\n%s", stage, pid, exc, traceback.format_exc())
                db.set_state(con, pid, "ERROR", f"{stage}: {type(exc).__name__}: {exc}"[:300])
    if a.stage == "dedupe":
        pipeline.stage_dedupe(con)
    if a.stage in ("all", "propose", "report"):
        log.info("formula leads staged for a later phase: %d", formulas.harvest_leads(con))
        propose.export(con)
        report.write_all(con)
    return 0


if __name__ == "__main__":
    sys.exit(main())
