"""The attendee-facing files, and the answer key that must not reach them."""

from pathlib import Path

from corpus import spec

ROOT = Path(__file__).resolve().parents[2]
NUSSAA = ROOT / "nussaa"
KEY = ROOT / "facilitator" / "nussaa-answer-key.md"


def test_agents_md_states_the_report_format_rule():
    text = (NUSSAA / "AGENTS.md").read_text(encoding="utf-8")
    assert "themes-2025-q4.md" in text, (
        "AGENTS.md must point at the prior report; it is the house format"
    )


def test_agents_md_does_not_leak_the_answer():
    text = (NUSSAA / "AGENTS.md").read_text(encoding="utf-8").lower()
    assert "4.2" not in text
    assert "address picker" not in text
    assert "map pin" not in text


def test_readme_does_not_leak_the_answer():
    text = (NUSSAA / "README.md").read_text(encoding="utf-8").lower()
    assert "4.2" not in text
    assert "address picker" not in text
    assert "map pin" not in text


def test_readme_says_nussaa_is_fictional():
    """Attendees should never wonder whether they are reading real customers."""
    text = (NUSSAA / "README.md").read_text(encoding="utf-8").lower()
    assert "fictional" in text


def test_answer_key_names_the_release_and_the_counts():
    text = KEY.read_text(encoding="utf-8")
    assert spec.PLANTED.release_version in text
    for figure in ("36", "26", "32"):
        assert figure in text, f"answer key is missing the figure {figure}"


def test_answer_key_is_not_inside_the_attendee_folder():
    assert not (NUSSAA / "expected").exists(), (
        "the answer key must not ship inside the folder attendees open"
    )
    assert not list(NUSSAA.rglob("*answer*")), (
        "nothing under nussaa/ may look like an answer key"
    )


def test_every_seed_file_is_actually_committed():
    """Existing on disk is not the same as reaching an attendee's clone.

    The root .gitignore excludes AGENTS.md, which silently swallowed
    nussaa/AGENTS.md the first time it was committed. Everything an
    attendee needs must be tracked, and a filesystem check cannot see that.
    """
    import subprocess

    tracked = subprocess.run(
        ["git", "ls-files", "nussaa"],
        cwd=ROOT, capture_output=True, text=True, check=True,
    ).stdout.split()
    tracked_paths = {ROOT / p for p in tracked}

    IGNORED = {".DS_Store", "Thumbs.db"}
    for path in NUSSAA.rglob("*"):
        if path.name in IGNORED or path.name.startswith("."):
            continue  # OS clutter; correctly untracked, and excluded from the zip
        if path.is_file() and "__pycache__" not in path.parts:
            assert path in tracked_paths, (
                f"{path.relative_to(ROOT)} exists but is not tracked — it will "
                "not be in the repo attendees clone. Check .gitignore."
            )


def test_answer_key_explains_both_discovery_routes():
    """The Q4 table's omission is load-bearing; a facilitator must know."""
    text = KEY.read_text(encoding="utf-8").lower()
    assert "changelog" in text and "q4" in text, (
        "the answer key must name both routes to the discovery"
    )


def test_rules_file_ships_under_both_names():
    """One corpus, two agent CLIs, and neither reads the other's filename.

    Claude Code reads CLAUDE.md and not AGENTS.md; the Antigravity CLI reads
    AGENTS.md. So the corpus ships both, and a workshop opens whichever its
    tool actually loads. Shipping two files is only safe if they cannot drift.
    """
    agents = (NUSSAA / "AGENTS.md").read_text(encoding="utf-8").splitlines()
    claude = (NUSSAA / "CLAUDE.md").read_text(encoding="utf-8").splitlines()

    assert agents[0] == "# AGENTS.md — Nussaa support analysis"
    assert claude[0] == "# CLAUDE.md — Nussaa support analysis"
    assert agents[1:] == claude[1:], (
        "AGENTS.md and CLAUDE.md must be identical below the title line. "
        "Edit one and copy it to the other, or a workshop teaches from a "
        "rules file the other workshop does not have."
    )


def test_claude_md_does_not_leak_the_answer():
    text = (NUSSAA / "CLAUDE.md").read_text(encoding="utf-8").lower()
    assert "4.2" not in text
    assert "address picker" not in text
    assert "map pin" not in text
