# Nussaa corpus — facilitator answer key

**Do not show this page to attendees.** It is the answer to the question that
makes the session land.

## The planted signal

`tickets-q1/` contains **36 tickets** about drivers being unable to find the
customer's address. **26 of them** fall in the **21 days after v4.2 shipped on
2026-02-11**. v4.2 replaced free-text address entry with a map pin.

The shape of it:

| | Before v4.2 | On or after v4.2 |
|---|---|---|
| driver-address tickets | **4** | **32** |

An eight-fold jump. Visible once you look, invisible until you do.

The correlation is the discovery. Individually the tickets read as ordinary
complaints — a lost driver is unremarkable. Only reading them against
`context/changelog.md` shows that a release caused them.

## Q1 theme distribution

| Theme | Tickets | Share |
|---|---|---|
| Late delivery | 55 | 27.5% |
| Wrong or missing items | 38 | 19.0% |
| **Driver could not find the address** | **36** | **18.0%** |
| Food arrived cold | 23 | 11.5% |
| Refund not received | 17 | 8.5% |
| Payment failed or double charged | 14 | 7.0% |
| App crashes | 10 | 5.0% |
| Driver conduct | 7 | 3.5% |

Note that driver-address is only the **third** largest theme. A report that
ranks by volume alone and stops there will lead with late delivery and bury
the one theme that has a knowable cause. That is the difference between
counting and analysing, and it is worth saying out loud when it happens.

## Two routes to the discovery

Attendees find this one of two ways. Both are legitimate; know which one you
are watching.

1. **The changelog route.** Notice the driver-address tickets cluster in
   February, look at what shipped on 2026-02-11.
2. **The comparison route.** Notice that driver-address is not in last
   quarter's report *at all*. A theme at 18% that did not exist in Q4 is a
   new problem, and new problems have causes.

Route 2 is faster and several people will take it. It is why the Q4 theme
table deliberately omits the theme — do not "complete" that table.

## The counts below are a reference, not a marking scheme

A dry run produced 34 for the driver-address theme where the generator says
36, 53 for late delivery where the generator says 55, and split out a
service-fee theme the generator has no concept of. That is clustering being a
judgement call, and a second analyst would differ again.

**Do not "correct" an attendee's counts against this page.** What matters is
whether the report finds the theme, states a count it can defend, and connects
it to v4.2 by date. A report saying 34 is not wrong.

Each workshop keeps its own dry-run record, in its own repository,
showing what a real run of that tool produced against this corpus.

## What a good report does

- Names driver-address problems as a distinct theme rather than folding them
  into "late delivery".
- States the count.
- Connects the cluster to v4.2 **by date**, and says so in the
  recommendations.
- Groups Arabic, English and code-switched tickets describing the same
  problem into one theme.

## What a weak report does

- Reports "delivery issues" as one large generic theme.
- Gives no counts, or estimates them.
- Never opens `context/changelog.md`.
- Treats Arabic and English tickets as separate themes.
- Ranks purely by volume and never asks why anything changed.

## How to run the moment

Do not announce the signal. When the first reports appear, ask the room:

> *"Anything in here that looks like a cause rather than a symptom?"*

Wait. Someone will connect the dates. If nobody does after a minute, narrow
it: *"When did the driver complaints start? What happened that week?"*

Whoever finds it should say it, not you.

## The wordplay tickets

Six tickets pun on the company being called "half an hour". They are filed
under late delivery, spread across the quarter. Worth reading one aloud when
the room needs a lift — they are real complaints and jokes at once, which is
what a real queue is like.

Ticket **NUS-00061** (2026-02-03) is the cleanest:

> اسمكم نص ساعة والطلب صار له ساعتين، غيروا الاسم
> *"Your name is 'half an hour' and my order has taken two. Change the name."*

## Q2 — the cold-run batch

`tickets-q2/` is a different story on purpose:

| Theme | Tickets | Share |
|---|---|---|
| Payment failed or double charged | 35 | 29.2% |
| Refund not received | 25 | 20.8% |
| Late delivery | 20 | 16.7% |
| Driver could not find the address | 7 | 5.8% |

Payment problems dominate, following the v4.5 payment provider migration on
2026-04-14. Driver-address has fallen back to 5.8%.

This is what makes the cold run a real test. A Skill that quietly hardcoded
"drivers can't find addresses" will produce a confidently wrong report on Q2,
which is exactly what the subagent run is meant to expose. If every attendee's
Skill passes the cold run first time, be suspicious — ask to see the Skill,
not the report.

## Regenerating

```bash
cd tools && uv run python -m corpus.generate
```

Seeded at `20260815`, so it reproduces byte-identically. Nothing else in this
repository needs Python — the generator is a maintainer tool and attendees
never touch it.

The property tests assert the counts this page states:

```bash
cd tools && uv run pytest        # 115 tests
```

Two consequences worth knowing:

- **Every number on this page is the generator's ground truth**, not a
  transcript of any particular run. Each workshop's own dry-run record shows
  what a real run produced against this corpus, and why the two differ.
- **If you change anything in `tools/corpus/spec.py`, every number on this
  page stops being true.** Re-run the tests, update the tables here, and
  rebuild the attendee download with `bash scripts/build-download.sh` — or the
  zip and the repo disagree and half the room works from different material.
