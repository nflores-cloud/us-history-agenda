#!/usr/bin/env python3
"""Build the public student agenda pages from dashboard data.

Usage: python3 build.py DATA_DIR
DATA_DIR holds config/main.json and weeks/<YYYY-MM-DD>.json, as saved by the
dashboard's database. One page is built per class in the dashboard:
US History II -> index.html, every other class -> <slug>/index.html
(for example Sociology -> sociology/index.html).
Only student-facing fields are copied into the pages; teacher-only notes
(lesson-plan sections, assessments, Atlas links) never leave DATA_DIR. Keep
DATA_DIR outside this repository so raw data is never committed.
"""
import glob, json, os, re, sys
from datetime import datetime
from zoneinfo import ZoneInfo

KEEP = ["id", "cls", "topic", "title", "obj", "lfocus", "act", "hw"]
ROOT_CLASS = "US History II"
here = os.path.dirname(os.path.abspath(__file__))

def load(path):
    d = json.load(open(path, encoding="utf-8"))
    return d["data"] if isinstance(d.get("data"), dict) else d

def slug(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "class"

def page_path(cls):
    return "index.html" if cls == ROOT_CLASS else f"{slug(cls)}/index.html"

def focus_for(week, cls, first):
    cf = (week.get("classFocus") or {}).get(cls)
    if cf:
        return cf.get("focus", ""), cf.get("reminders", "")
    if cls == first:
        return week.get("focus", ""), week.get("reminders", "")
    return "", ""

def main(data_dir):
    cfg = load(os.path.join(data_dir, "config", "main.json"))
    classes = cfg.get("classes") or [ROOT_CLASS]
    raw = {os.path.basename(f)[:-5]: load(f) for f in sorted(glob.glob(os.path.join(data_dir, "weeks", "*.json")))}
    tpl = open(os.path.join(here, "template.html"), encoding="utf-8").read()
    assert tpl.count("__AGENDA_DATA__") == 1 and tpl.count("__TITLE__") == 1
    updated = datetime.now(ZoneInfo("America/New_York")).strftime("%b %-d, %Y")
    for cls in classes:
        weeks = {}
        for key, d in raw.items():
            days = {k: [{x: e.get(x, "") for x in KEEP} for e in v if e.get("cls") == cls] for k, v in (d.get("days") or {}).items()}
            focus, reminders = focus_for(d, cls, classes[0])
            weeks[key] = {"focus": focus, "reminders": reminders, "off": d.get("off") or {}, "days": days}
        data = {"config": {"classes": [cls], "season": cfg.get("season", "auto"), "name": "", "canvas": {}, "atlasHome": ""},
                "weeks": weeks, "updated": updated}
        js = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
        title = f"{cls} · Weekly Agenda".replace("<", "").replace("&", "and")
        out = tpl.replace("__AGENDA_DATA__", js).replace("__TITLE__", title)
        path = os.path.join(here, page_path(cls))
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").write(out)
        print(f"{cls}: {page_path(cls)} ({len(weeks)} week(s))")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
