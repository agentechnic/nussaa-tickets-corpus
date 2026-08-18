"""The properties the workshop actually depends on.

If any of these fail, the corpus is internally consistent and still cannot
teach the session. Adjust the corpus; never weaken the test.
"""

from collections import Counter
from datetime import date, timedelta

from corpus import generate, spec

TICKETS = generate.build_tickets("q1")


def _release(version: str) -> date:
    return date.fromisoformat(
        next(r for r in spec.RELEASES if r.version == version).date
    )


def test_planted_cluster_exists_in_the_window_after_the_release():
    start = _release(spec.PLANTED.release_version)
    end = start + timedelta(days=spec.PLANTED.window_days)

    in_window = [
        t for t in TICKETS
        if t.theme_key == spec.PLANTED.theme_key
        and start <= date.fromisoformat(t.date) <= end
    ]
    assert len(in_window) >= spec.PLANTED.count, (
        f"expected at least {spec.PLANTED.count} planted tickets in the "
        f"{spec.PLANTED.window_days} days after v{spec.PLANTED.release_version}, "
        f"found {len(in_window)} — the workshop's central discovery does not exist"
    )


def test_planted_theme_is_rare_before_the_release():
    start = _release(spec.PLANTED.release_version)
    before = [t for t in TICKETS
              if t.theme_key == spec.PLANTED.theme_key
              and date.fromisoformat(t.date) < start]
    after = [t for t in TICKETS
             if t.theme_key == spec.PLANTED.theme_key
             and date.fromisoformat(t.date) >= start]
    assert len(after) > 2 * len(before), (
        "the spike must stand out against its own baseline, or there is "
        f"nothing to notice ({len(before)} before, {len(after)} after)"
    )


def test_language_mix_is_in_band():
    counts = Counter(t.language for t in TICKETS)
    total = len(TICKETS)
    assert 0.45 <= counts["ar"] / total <= 0.65, counts
    assert 0.15 <= counts["en"] / total <= 0.35, counts
    assert 0.10 <= counts["mixed"] / total <= 0.30, counts


def test_the_planted_theme_appears_in_all_three_registers():
    languages = {t.language for t in TICKETS
                 if t.theme_key == spec.PLANTED.theme_key}
    assert languages == {"ar", "en", "mixed"}, (
        "the cluster must span Arabic, English and code-switched tickets, or "
        f"grouping it is trivial — found {languages}"
    )


def test_corpus_contains_near_empty_tickets():
    stubs = [t for t in TICKETS if len(t.body) <= 30]
    assert stubs, "a real queue contains useless one-liners; this one does not"


def test_corpus_contains_duplicates():
    bodies = Counter(t.body for t in TICKETS)
    assert any(count > 1 for count in bodies.values()), "no duplicate tickets"


def test_theme_is_never_written_into_the_ticket():
    """No ticket may carry a machine-readable classification.

    Deriving the theme is the exercise. If a ticket file said what its theme
    was, clustering would collapse into reading one header and the whole task
    would evaporate.

    What this checks is the snake_case keys — `driver_lost`, `payment_failed`
    — and the absence of any classification header field.

    What it deliberately does NOT check is the human-readable labels, in
    either language, because matching those reports the corpus rather than a
    risk. The labels were written as plain descriptions of ordinary
    complaints, so ordinary complaints contain them:

      - `rude_driver` is labelled `تعامل الكابتن`, and
        "تعامل الكابتن ما كان مناسب ابدا" is simply how that complaint opens.
      - `late` is labelled "Late delivery", and a customer writes
        "third late delivery this month".
      - the key `late` is itself an English word, appearing in "الطلب late".

    In each case the body echoing its own label is the customer's own
    phrasing, not a tag. A guard that fires on those is measuring the fact
    that the labels are good, which is not a defect.
    """
    classification_fields = ("Theme:", "Category:", "Classification:", "Label:")
    distinctive_keys = {k for k in spec.THEMES if "_" in k}

    for ticket in TICKETS:
        rendered = generate.render(ticket)
        for key in distinctive_keys:
            assert key not in rendered, (
                f"NUS-{ticket.number:05d} leaks the theme key {key!r}"
            )
        for field in classification_fields:
            assert field not in rendered, (
                f"NUS-{ticket.number:05d} carries a {field!r} header — "
                "deriving the theme is the task, so it cannot be handed over"
            )


def test_the_wordplay_tickets_made_it_into_the_corpus():
    """The facilitator reads these aloud; if they vanish, the room is quieter."""
    from corpus import phrases_ar

    bodies = {t.body for t in TICKETS}
    landed = bodies & set(phrases_ar.WORDPLAY)
    assert len(landed) >= 4, (
        f"only {len(landed)} brand-wordplay tickets reached the corpus"
    )


def test_subjects_are_not_all_identical_within_a_theme():
    """Varied subjects, or the header still gives the grouping away."""
    planted = [t for t in TICKETS if t.theme_key == spec.PLANTED.theme_key]
    assert len({t.subject for t in planted}) >= 4, (
        "the planted cluster's subjects are too uniform to be realistic"
    )


def test_tickets_span_the_whole_quarter():
    months = {t.date[:7] for t in TICKETS}
    assert months == {"2026-01", "2026-02", "2026-03"}, (
        f"Q1 tickets should cover all three months, found {sorted(months)}"
    )
