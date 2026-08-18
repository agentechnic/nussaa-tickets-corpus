"""Q2 must tell a different story from Q1.

If both quarters share a dominant theme, a Skill that quietly hardcoded
Q1's finding would sail through the cold run and prove nothing — which is
the one thing the cold run exists to catch.
"""

from collections import Counter

from corpus import generate

Q1 = generate.build_tickets("q1")
Q2 = generate.build_tickets("q2")


def _dominant(tickets):
    return Counter(t.theme_key for t in tickets).most_common(1)[0][0]


def test_q2_dominant_theme_differs_from_q1():
    assert _dominant(Q2) != _dominant(Q1), (
        "if both quarters share a dominant theme, a Skill that hardcoded "
        "Q1's finding would pass the cold run and prove nothing"
    )


def test_q2_is_dominated_by_payment_problems():
    assert _dominant(Q2) == "payment_failed"


def test_q2_has_no_planted_driver_spike():
    counts = Counter(t.theme_key for t in Q2)
    assert counts["driver_lost"] < counts["payment_failed"] / 3, (
        "Q2 must not repeat Q1's signal"
    )


def test_q2_falls_entirely_inside_the_second_quarter():
    months = {t.date[:7] for t in Q2}
    assert months <= {"2026-04", "2026-05", "2026-06"}, (
        f"Q2 tickets strayed outside the quarter: {sorted(months)}"
    )


def test_q2_carries_no_brand_wordplay():
    """The jokes are a Q1 flourish; Q2 is the cold, unfamiliar batch."""
    from corpus import phrases_ar

    assert not ({t.body for t in Q2} & set(phrases_ar.WORDPLAY))
