# Weekly Agendas

Public, student-facing weekly agendas, one page per class:

- US History II: https://nflores-cloud.github.io/us-history-agenda/
- Sociology: https://nflores-cloud.github.io/us-history-agenda/sociology/
- AP World Modern: https://nflores-cloud.github.io/us-history-agenda/ap-world-modern/

It opens to the current week automatically, with falling seasonal leaves, and students can move between weeks.

## How it updates

The agenda is planned in a private Claude dashboard. A nightly scheduled task copies the student fields from the dashboard into `index.html` and pushes it here; GitHub Pages publishes it within a few minutes.

- `template.html`: the page design, with a `__AGENDA_DATA__` placeholder.
- `build.py`: `python3 build.py DATA_DIR` fills the template from saved dashboard data and writes one page per class (`index.html` for US History II, `<class-slug>/index.html` for the others). It keeps only student fields (topic, SWBAT, lesson focus, agenda, assignments, weekly focus and reminders, days off). Teacher notes never reach this repository.
- `index.html`, `sociology/index.html`, `ap-world-modern/index.html`: the published pages. Do not edit by hand; they are rebuilt every night.

## Embedding in Google Sites

Insert → Embed → By URL → paste the page address for that class.
