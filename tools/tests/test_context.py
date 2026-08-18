import re
import statistics
from pathlib import Path

from corpus import spec

NUSSAA = Path(__file__).resolve().parents[2] / "nussaa"
CHANGELOG = NUSSAA / "context" / "changelog.md"
PRIOR = NUSSAA / "context" / "themes-2025-q4.md"

HEADING = re.compile(r"^## v(?P<version>\S+)\s+—\s+(?P<date>\d{4}-\d{2}-\d{2})\s*$")


def _entries(text):
    """Parse the changelog into {version: (date, body_word_count)}.

    The heading is excluded from the word count — it is identical in shape for
    every entry, so counting it only dilutes the comparison between bodies.
    """
    entries = {}
    for block in re.split(r"^(?=## )", text, flags=re.MULTILINE)[1:]:
        heading, _, body = block.partition("\n")
        match = HEADING.match(heading.strip())
        assert match, f"changelog heading not in 'v<version> — <date>' form: {heading!r}"
        entries[match["version"]] = (match["date"], len(body.split()))
    return entries


def test_changelog_lists_every_release():
    """Version and date must be paired, not merely both present somewhere."""
    entries = _entries(CHANGELOG.read_text(encoding="utf-8"))
    for release in spec.RELEASES:
        assert release.version in entries, f"changelog missing v{release.version}"
        stamped = entries[release.version][0]
        assert stamped == release.date, (
            f"v{release.version} is stamped {stamped} but spec says {release.date}"
        )


def test_changelog_does_not_flag_the_planted_release():
    """The correlation must be discoverable, not announced."""
    text = CHANGELOG.read_text(encoding="utf-8").lower()
    for giveaway in ("caused", "regression", "incident", "known issue", "spike"):
        assert giveaway not in text, (
            f"changelog says {giveaway!r} — that hands the answer to the room"
        )


def test_planted_release_entry_is_not_conspicuous():
    """v4.2 must not be the entry the eye lands on. Same shape as its neighbours."""
    entries = _entries(CHANGELOG.read_text(encoding="utf-8"))
    planted = entries[spec.PLANTED.release_version][1]
    others = [
        words
        for version, (_, words) in entries.items()
        if version != spec.PLANTED.release_version
    ]
    assert planted <= max(others), (
        f"v{spec.PLANTED.release_version} is the longest entry in the changelog "
        f"({planted} words vs {max(others)} for the next longest)"
    )
    cap = statistics.median(others) + 3
    assert planted <= cap, (
        f"v{spec.PLANTED.release_version} is written up in more detail than its "
        f"neighbours ({planted} words, cap {cap})"
    )


def test_prior_report_has_the_house_format_sections():
    text = PRIOR.read_text(encoding="utf-8")
    for heading in ("## Summary", "## Themes", "## Recommendations"):
        assert heading in text, f"prior report missing {heading}"


def test_prior_report_quantifies_each_theme():
    text = PRIOR.read_text(encoding="utf-8")
    assert "tickets" in text.lower()
    assert "%" in text, "themes should carry a share, so the new report copies that"


# Word-bounded so ordinary prose does not trip them: "addressed", "opinion" and
# "shipping" are fine, the nouns are not. The bare version number is guarded too
# — a themes report quoting "4.2" of anything reads as a release reference.
ANACHRONISMS = (
    r"v?4\.2\b",
    r"\baddress(es)?\b",
    r"\bmap pin\w*\b",
    r"\bpin\b",
    r"\blocation\b",
    r"\bgps\b",
    "العنوان",
    "الموقع",
)


def test_prior_report_predates_the_planted_release():
    """Q4 2025 is the 'before' picture — it cannot know about v4.2 or addresses."""
    text = PRIOR.read_text(encoding="utf-8").lower()
    for pattern in ANACHRONISMS:
        assert not re.search(pattern, text), (
            f"Q4 2025 report matches {pattern!r} — it predates that release"
        )
