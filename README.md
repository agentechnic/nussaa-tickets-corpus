# Nussaa tickets corpus

The fixture behind Agentechnic's agent workshops: a quarter of bilingual
customer support tickets for a fictional Riyadh food delivery company, with a
cause planted in the data and a second quarter that tells a different story on
purpose.

Attendees analyse it. Facilitators mark nothing against it. Workshops consume
it as a versioned download.

**Nussaa does not exist.** Its restaurants, riders, customers and complaints
were written for a workshop. The company's own site — also invented — is at
[agentechnic.github.io/nussaa](https://agentechnic.github.io/nussaa/).

## Get the corpus

Attendees download the packaged folder from a **release**, not from this repo:

**[Latest release](https://github.com/agentechnic/nussaa-tickets-corpus/releases/latest)** → `nussaa.zip`

Workshops pin an explicit version so a corpus change never silently rewrites a
workshop's answer key. Whatever version a workshop names in its README is the
version its numbers were calibrated against.

## What is in it

```
nussaa/
  tickets-q1/    200 support tickets, one per file
  tickets-q2/    120 more, from the quarter after
  context/
    changelog.md         what shipped, and when
    themes-2025-q4.md    the previous quarter's report — the house format
  AGENTS.md      the conventions the agent works to
  CLAUDE.md      the same file under the name Claude Code reads
  README.md      what this is
```

### Two names, one rules file

`AGENTS.md` and `CLAUDE.md` ship together and are byte-identical below their
title lines. This is not redundancy for its own sake: Claude Code
[reads `CLAUDE.md` and not `AGENTS.md`](https://code.claude.com/docs/en/memory),
while the Antigravity CLI reads `AGENTS.md`. A workshop opens whichever file
its tool actually loads, and the folder works with either.

A test enforces that they stay identical. Edit one, copy it to the other.

About 38KB of ticket text in Q1. Worth knowing, because people assume the
constraint in a workshop is the model's memory. It is not.

### Why it is messy

Deliberately, and in the specific ways a real support queue is messy.

**Three registers, often in one ticket.** Colloquial Saudi Arabic as people
actually type it — inconsistent spelling, missing hamzas, no diacritics — fusha
in the longer formal complaints, English of varying fluency, and code-switching
as the common case. The same complaint appears in all three. Grouping by
language instead of by meaning manufactures fake themes and hides a real one.

**Some tickets are useless.** One line, no detail. **Some are duplicates.**
Someone hit send twice. **A few are jokes** — the company is called "half an
hour" and the food took two. Real complaints and jokes at once, which is also
what a real queue looks like.

### The planted signal

Q1 contains a spike with a knowable cause, discoverable by two independent
routes, and Q2 shifts to a different dominant theme so that a procedure which
quietly hardcoded Q1's answer produces a confidently wrong report.

The exact numbers, both routes, and how to run the moment are in
[`facilitator/nussaa-answer-key.md`](facilitator/nussaa-answer-key.md).
**Facilitators only.** It is in this repository rather than in a workshop's,
because its figures are assertions in `tools/tests/`, not prose — separate them
and they drift the first time the spec is touched.

## Maintaining it

The tickets are generated, not hand-written. Seeded at `20260815`, so the
corpus reproduces byte-identically.

```bash
cd tools
uv run python -m corpus.generate    # regenerate the corpus
uv run pytest                       # 113 property tests over it
```

Nothing else here needs Python, and attendees never touch this.

### The rule that matters

**Change `tools/corpus/spec.py` and every number in the answer key stops being
true.** In order:

1. Regenerate.
2. Re-run the tests.
3. Update `facilitator/nussaa-answer-key.md`.
4. `bash scripts/build-download.sh` and cut a new **minor or major** release.
5. Tell the workshops, so they can re-pin and re-check their facilitator notes.

A corpus change is a breaking change for every workshop built on it. Version it
like one.

### Cutting a release

```bash
bash scripts/build-download.sh          # verifies counts, refuses to ship answers
gh release create v1.1.0 nussaa.zip     # attach the built zip
```

`build-download.sh` fails if the ticket counts are wrong, if a seed file is
missing, or if anything resembling facilitator material has found its way into
the folder. That last check is the one that matters — it is the only thing
standing between a spec change and handing the room its answer.

## Who uses it

- [getting-real-with-antigravity](https://github.com/agentechnic/getting-real-with-antigravity)
- getting-real-with-claude-code

## Licence

MIT. Take it, change the company, run your own workshop.
