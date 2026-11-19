#!/usr/bin/env python3
"""Build index.html (the public student agenda) from dashboard data.

Usage: python3 build.py DATA_DIR
DATA_DIR holds config/main.json and weeks/<YYYY-MM-DD>.json, as saved by the
dashboard's database. Only student-facing fields are copied into the page;
teacher-only notes (lesson-plan sections, assessments, Atlas links) never leave
DATA_DIR. Keep DATA_DIR outside this repository so raw data is never committed.
"""
import glob, json, os, sys
from datetime import datetime
from zoneinfo import ZoneInfo

KEEP = ["id", "cls", "topic", "title", "obj", "lfocus", "act", "hw"]
here = os.path.dirname(os.path.abspath(__file__))

def load(path):
    d = json.load(open(path, encoding="utf-8"))
    return d.get("data", d) if isinstance(d.get("data"), dict) else d

def main(data_dir):
    cfg = load(os.path.join(data_dir, "config", "main.json"))
    weeks = {}
    for f in sorted(glob.glob(os.path.join(data_dir, "weeks", "*.json"))):
        key = os.path.basename(f)[:-5]
        d = load(f)
        days = {k: [{x: e.get(x, "") for x in KEEP} for e in v] for k, v in (d.get("days") or {}).items()}
        weeks[key] = {"focus": d.get("focus", ""), "reminders": d.get("reminders", ""), "off": d.get("off") or {}, "days": days}
    now = datetime.now(ZoneInfo("America/New_York"))
    data = {
        "config": {"classes": cfg.get("classes", []), "season": cfg.get("season", "auto"), "name": "", "canvas": {}, "atlasHome": ""},
        "weeks": weeks,
        "updated": now.strftime("%b %-d, %Y"),
    }
    js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
    assert tpl.count("__AGENDA_DATA__") == 1
    out = tpl.replace("__AGENDA_DATA__", js)
    open(os.path.join(here, "index.html"), "w", encoding="utf-8").write(out)
    print(f"index.html built with {len(weeks)} week(s)")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
