# US History II · Weekly Agenda

The public, student-facing weekly agenda: https://nflores-cloud.github.io/us-history-agenda/

It opens to the current week automatically, with falling seasonal leaves, and students can move between weeks.

## How it updates

The agenda is planned in a private Claude dashboard. A nightly scheduled task copies the student fields from the dashboard into `index.html` and pushes it here; GitHub Pages publishes it within a few minutes.

- `template.html`: the page design, with a `__AGENDA_DATA__` placeholder.
- `build.py`: `python3 build.py DATA_DIR` fills the template from saved dashboard data and writes `index.html`. It keeps only student fields (topic, SWBAT, lesson focus, agenda, assignments, weekly focus and reminders, days off). Teacher notes never reach this repository.
- `index.html`: the published page. Do not edit by hand; it is rebuilt every night.

## Embedding in Google Sites

Insert → Embed → By URL → paste the page address above.
