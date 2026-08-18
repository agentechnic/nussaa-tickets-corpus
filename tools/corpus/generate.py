"""Deterministic generator for the Nussaa ticket corpus.

Seeded so the corpus regenerates byte-identically. The facilitator answer
key states exact counts, so drift here silently invalidates the workshop.

Messiness is deliberate: near-empty tickets, duplicates, and inconsistent
formatting all appear, because a clean corpus would not teach anything.

Sampling is per-theme throughout. The phrase banks are intentionally uneven
in size (driver_lost is the largest, matching its role as the planted
signal), so drawing from a flattened pool would give it a second, unplanned
boost on top of PLANTED.count.
"""

import random
from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

from . import phrases_ar, phrases_en, spec

CHANNELS = ["in-app", "email", "phone-callback", "whatsapp"]

# Baseline theme weights, before the planted signal is layered on.
Q1_WEIGHTS = {
    "late": 30, "wrong_items": 18, "cold_food": 14, "payment_failed": 10,
    "refund_delay": 8, "app_crash": 7, "rude_driver": 6, "driver_lost": 7,
}
# Q2 shifts hard to payment: a Skill that hardcoded Q1's answer fails here.
Q2_WEIGHTS = {
    "payment_failed": 34, "refund_delay": 20, "late": 14, "wrong_items": 10,
    "cold_food": 8, "app_crash": 6, "driver_lost": 5, "rude_driver": 3,
}

QUARTER_WINDOWS = {
    "q1": (date(2026, 1, 1), date(2026, 3, 31)),
    "q2": (date(2026, 4, 1), date(2026, 6, 30)),
}


@dataclass(frozen=True)
class Ticket:
    number: int
    date: str
    channel: str
    language: str
    theme_key: str
    subject: str
    body: str


def _pick_language(rng: random.Random) -> str:
    roll = rng.random()
    if roll < 0.55:
        return "ar"
    if roll < 0.80:
        return "en"
    return "mixed"


def _body_for(rng: random.Random, theme_key: str, language: str) -> str:
    if language == "ar":
        # Fusha shows up in the longer, more formal escalations.
        if rng.random() < 0.25:
            return rng.choice(phrases_ar.FUSHA[theme_key])
        return rng.choice(phrases_ar.COLLOQUIAL[theme_key])
    if language == "en":
        return rng.choice(phrases_en.ENGLISH[theme_key])
    return rng.choice(phrases_en.MIXED[theme_key])


def _subject_from(body: str) -> str:
    """A support tool's auto-filled subject: the customer's own first words.

    Never the theme label. The whole task is deriving the theme, and a
    canonical label in the header would hand it over.
    """
    lines = [line for line in body.strip().splitlines() if line.strip()]
    if not lines:
        return "(no subject)"
    words = lines[0].split()
    subject = " ".join(words[:6])
    if not subject:
        return "(no subject)"
    return subject if len(subject) <= 60 else subject[:57].rstrip() + "..."


def _weighted_theme(rng: random.Random, weights: dict[str, int]) -> str:
    keys = list(weights)
    return rng.choices(keys, weights=[weights[k] for k in keys], k=1)[0]


def _planted_dates(rng: random.Random) -> list[date]:
    """Dates for the planted cluster: inside the window after the release."""
    release = next(r for r in spec.RELEASES
                   if r.version == spec.PLANTED.release_version)
    start = date.fromisoformat(release.date)
    return [start + timedelta(days=rng.randint(0, spec.PLANTED.window_days))
            for _ in range(spec.PLANTED.count)]


def build_tickets(quarter: str) -> list[Ticket]:
    rng = random.Random(f"{spec.CORPUS_SEED}-{quarter}")
    weights = Q1_WEIGHTS if quarter == "q1" else Q2_WEIGHTS
    total = spec.Q1_TICKET_COUNT if quarter == "q1" else spec.Q2_TICKET_COUNT
    window_start, window_end = QUARTER_WINDOWS[quarter]
    span = (window_end - window_start).days

    plan: list[tuple[date, str]] = []

    if quarter == "q1":
        for when in _planted_dates(rng):
            plan.append((when, spec.PLANTED.theme_key))

    while len(plan) < total:
        when = window_start + timedelta(days=rng.randint(0, span))
        plan.append((when, _weighted_theme(rng, weights)))

    plan.sort(key=lambda pair: pair[0])

    # A few customers pun on the brand name. Spread across the quarter, all
    # filed under `late` because that is what provokes the joke.
    wordplay_slots: set[int] = set()
    if quarter == "q1":
        late_positions = [i for i, (_, theme) in enumerate(plan) if theme == "late"]
        wordplay_slots = set(rng.sample(
            late_positions, k=min(len(phrases_ar.WORDPLAY), 6, len(late_positions))
        ))
    wordplay_pool = list(phrases_ar.WORDPLAY)
    rng.shuffle(wordplay_pool)
    wordplay_used = 0

    tickets: list[Ticket] = []
    for index, (when, theme_key) in enumerate(plan, start=1):
        language = _pick_language(rng)
        body = _body_for(rng, theme_key, language)

        if (index - 1) in wordplay_slots:
            body = wordplay_pool[wordplay_used % len(wordplay_pool)]
            wordplay_used += 1
            has_latin = any(c.isascii() and c.isalpha() for c in body)
            language = "mixed" if has_latin else "ar"
        else:
            # Messiness. Roughly 1 in 12 tickets is near-empty, and 1 in 20 is
            # a verbatim resend of the previous one, because real queues
            # contain both. Wordplay tickets are exempt — they are the ones
            # read aloud, and truncating them would kill the joke.
            if rng.random() < 0.08:
                body = body.split("،")[0].split(",")[0][:28].strip()
            elif rng.random() < 0.05 and tickets:
                body = tickets[-1].body

        tickets.append(Ticket(
            number=index,
            date=when.isoformat(),
            channel=rng.choice(CHANNELS),
            language=language,
            theme_key=theme_key,
            subject=_subject_from(body),
            body=body,
        ))
    return tickets


def render(ticket: Ticket) -> str:
    """One ticket as a support-tool export. Header fields, then free text.

    The theme is NOT written into the file — deriving it is the exercise.
    """
    return (
        f"Ticket: NUS-{ticket.number:05d}\n"
        f"Date: {ticket.date}\n"
        f"Channel: {ticket.channel}\n"
        f"Subject: {ticket.subject}\n"
        f"\n"
        f"{ticket.body}\n"
    )


def write_corpus(quarter: str, out_dir: Path) -> int:
    out_dir.mkdir(parents=True, exist_ok=True)
    for stale in out_dir.glob("ticket-*.txt"):
        stale.unlink()
    tickets = build_tickets(quarter)
    for ticket in tickets:
        path = out_dir / f"ticket-{ticket.number:04d}.txt"
        path.write_text(render(ticket), encoding="utf-8")
    return len(tickets)


if __name__ == "__main__":
    root = Path(__file__).resolve().parents[2] / "nussaa"
    for quarter, folder in (("q1", "tickets-q1"), ("q2", "tickets-q2")):
        count = write_corpus(quarter, root / folder)
        print(f"wrote {count} tickets to {folder}")
