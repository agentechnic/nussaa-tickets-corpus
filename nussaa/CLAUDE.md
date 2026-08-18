# CLAUDE.md — Nussaa support analysis

## What this is

A quarter of customer support tickets for Nussaa, a food delivery app in
Riyadh, plus the product changelog and last quarter's themes report. The job
is to work out what this quarter's themes are and write them up.

## The material

- `tickets-q1/` — one ticket per file. Header fields, then whatever the
  customer actually wrote.
- `tickets-q2/` — a later batch. Leave it alone unless asked.
- `context/changelog.md` — what shipped, and when.
- `context/themes-2025-q4.md` — last quarter's report.

## Language

Tickets arrive in Arabic, English, and a mix of both. The Arabic is mostly
colloquial Saudi as people type it — inconsistent spelling, missing hamzas,
no diacritics — with fusha in the longer formal complaints.

The same complaint appears in all three registers. Group by what the customer
means, never by the language they wrote it in. "ما لقى العنوان", "driver
couldn't find building" and "الـ pin ودى الكابتن لحي ثاني" are one theme.

## Report format

Match `context/themes-2025-q4.md` exactly: a `## Summary`, a `## Themes`
table with ticket counts and share percentages, a short prose section per
significant theme, and `## Recommendations`. Same headings, same order.

## Conventions

- Counts must be exact. Count tickets; do not estimate or sample.
- A ticket raising several issues is assigned to its dominant one, as last
  quarter's method section describes.
- Quote real ticket text when it illustrates a theme, in its original
  language. Do not translate quotes into English.
- Do not modify anything under `tickets-q1/` or `tickets-q2/`.

## What to ask me about, never assume

- Any theme that is not in last quarter's report — say why it is new.
- Anything that looks like a cause rather than a symptom.
