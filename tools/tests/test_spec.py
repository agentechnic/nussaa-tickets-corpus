from datetime import date

from corpus import spec


def test_planted_signal_points_at_a_real_release():
    versions = {r.version for r in spec.RELEASES}
    assert spec.PLANTED.release_version in versions


def test_planted_signal_points_at_a_real_theme():
    assert spec.PLANTED.theme_key in spec.THEMES


def test_releases_are_chronological():
    dates = [date.fromisoformat(r.date) for r in spec.RELEASES]
    assert dates == sorted(dates), "releases must be listed oldest first"


def test_every_theme_has_both_labels():
    for key, theme in spec.THEMES.items():
        assert theme.label_en.strip(), f"{key} missing English label"
        assert theme.label_ar.strip(), f"{key} missing Arabic label"
