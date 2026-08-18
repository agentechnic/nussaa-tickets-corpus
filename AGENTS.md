# AGENTS.md — nussaa-tickets-corpus

Context for any agent working on this repository.

## What this is

The shared fixture behind Agentechnic's agent workshops: a generated corpus of
bilingual support tickets with a planted signal, plus the generator, the tests
that hold its shape, and the facilitator answer key.

Workshops consume it as a versioned release artifact. They do not vendor it.

## The coupling that governs everything here

`tools/corpus/spec.py` → the generated tickets → the numbers in
`facilitator/nussaa-answer-key.md` → the facilitator notes in every workshop
built on this corpus.

Touch the first and all four have to move together. There is no automated
check across repository boundaries, so the discipline is the release version:
a corpus change is a breaking change for every workshop, and gets a version
bump and a note to the workshops that pin it.

## Conventions

- **Never hand-edit files under `nussaa/tickets-q1/` or `tickets-q2/`.** They
  are output. Change the spec, regenerate, re-run the tests.
- The seed is `20260815` and regeneration must stay byte-identical. If a change
  makes the corpus non-reproducible, that is a bug, not a new baseline.
- `nussaa/AGENTS.md` is attendee-facing — it is the rules file the workshop
  teaches with. It must never mention the planted release, the address picker,
  or anything else that hands over the answer. There is a test for this.
- The answer key stays out of `nussaa/`. There is a test for this too, and
  `scripts/build-download.sh` refuses to package if it finds one.
- Messiness in the corpus is curriculum, not sloppiness. Do not "clean up"
  duplicate, near-empty or joke tickets.

## Before any release

```bash
cd tools && uv run pytest            # 113 tests
cd .. && bash scripts/build-download.sh
```

Then `gh release create vX.Y.Z nussaa.zip`, and tell the workshops.
