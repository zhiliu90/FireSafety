#!/usr/bin/env python3
"""Deliver the latest fire-safety weekly report produced by fire_safety_weekly_scan.py."""
from __future__ import annotations

import datetime as dt
import json
import os
from pathlib import Path
import sys

TZ = dt.timezone(dt.timedelta(hours=8), name="Asia/Shanghai")
HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes")).expanduser()
BASE_DIR = Path(
    os.environ.get(
        "FIRE_SAFETY_MONITOR_DIR",
        HERMES_HOME / "data" / "fire_safety_paper_monitor",
    )
).expanduser()
STATE_JSON = BASE_DIR / "state.json"
LATEST_REPORT = BASE_DIR / "latest_report.md"


def parse_dt(s: str):
    try:
        return dt.datetime.fromisoformat(s).astimezone(TZ)
    except Exception:
        return None


def main() -> int:
    if not STATE_JSON.exists() or not LATEST_REPORT.exists():
        print("Fire-safety paper digest failed: the local 13:00 collector report was not found.")
        return 0
    try:
        state = json.loads(STATE_JSON.read_text(encoding="utf-8"))
    except Exception:
        state = {}
    last_run = parse_dt(state.get("last_run_at", ""))
    now = dt.datetime.now(TZ)
    if not last_run or now - last_run > dt.timedelta(hours=8):
        print("Fire-safety paper digest failed: the 13:00 collector result is missing or stale.")
        return 0
    text = LATEST_REPORT.read_text(encoding="utf-8").strip()
    if not text:
        print("Fire-safety paper digest failed: the local report is empty.")
        return 0
    print(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
