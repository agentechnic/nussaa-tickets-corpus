from corpus import phrases_ar, phrases_en, spec


# Banks keyed by theme. WORDPLAY is deliberately absent: it is a flat list,
# not a per-theme mapping.
THEMED_BANKS = (
    ("COLLOQUIAL", phrases_ar.COLLOQUIAL),
    ("FUSHA", phrases_ar.FUSHA),
    ("ENGLISH", phrases_en.ENGLISH),
    ("MIXED", phrases_en.MIXED),
)


def test_every_theme_has_colloquial_variants():
    for key in spec.THEMES:
        assert len(phrases_ar.COLLOQUIAL.get(key, [])) >= 4, (
            f"{key} needs at least 4 colloquial variants so the corpus does "
            "not read as copy-paste"
        )


def test_every_theme_has_fusha_variants():
    for key in spec.THEMES:
        assert len(phrases_ar.FUSHA.get(key, [])) >= 2, f"{key} needs fusha variants"


def test_phrases_are_actually_arabic():
    arabic_range = range(0x0600, 0x0700)
    for bank in (phrases_ar.COLLOQUIAL, phrases_ar.FUSHA):
        for key, variants in bank.items():
            for text in variants:
                assert any(ord(ch) in arabic_range for ch in text), (
                    f"{key}: {text!r} contains no Arabic characters"
                )


def test_wordplay_bank_exists_and_puns_on_the_name():
    assert len(phrases_ar.WORDPLAY) >= 6
    for text in phrases_ar.WORDPLAY:
        assert ("نص" in text) or ("نصف" in text) or ("nus" in text.lower()), (
            f"{text!r} does not play on the brand name"
        )


def test_wordplay_spans_arabic_and_english():
    joined = " ".join(phrases_ar.WORDPLAY)
    assert any(ch.isascii() and ch.isalpha() for ch in joined), (
        "at least one pun should land in English too"
    )


def test_every_theme_has_english_variants():
    for key in spec.THEMES:
        assert len(phrases_en.ENGLISH.get(key, [])) >= 3, f"{key} needs English variants"


def test_every_theme_has_mixed_variants():
    for key in spec.THEMES:
        assert len(phrases_en.MIXED.get(key, [])) >= 3, f"{key} needs code-switched variants"


def test_mixed_variants_contain_both_scripts():
    arabic_range = range(0x0600, 0x0700)
    for key, variants in phrases_en.MIXED.items():
        for text in variants:
            has_arabic = any(ord(ch) in arabic_range for ch in text)
            has_latin = any(ch.isascii() and ch.isalpha() for ch in text)
            assert has_arabic and has_latin, (
                f"{key}: {text!r} should mix Arabic and Latin script"
            )


def test_every_themed_bank_uses_only_spec_theme_keys():
    for name, bank in THEMED_BANKS:
        assert set(bank) == set(spec.THEMES), (
            f"{name} keys have drifted from spec.THEMES"
        )


def test_no_phrase_is_repeated_within_a_bank():
    banks = THEMED_BANKS + (("WORDPLAY", {"wordplay": phrases_ar.WORDPLAY}),)
    for name, bank in banks:
        seen = {}
        for key, variants in bank.items():
            for text in variants:
                assert text not in seen, (
                    f"{name}: {text!r} appears in both {seen[text]} and {key}; "
                    "duplicates weaken the per-theme clustering signal"
                )
                seen[text] = key


# --- divergence guard -------------------------------------------------
#
# The corpus's central difficulty is that a theme has to be recognised
# across three registers that share no vocabulary. A later task checks
# that a theme's Arabic, English and mixed forms cluster together. That
# check is only meaningful if the mixed form is a genuinely different
# utterance. If MIXED[theme][i] is COLLOQUIAL[theme][j] with two nouns
# flipped to English, a bag-of-words model clusters the pair on their
# shared Arabic tokens and the cross-register skill is never exercised —
# the suite goes green while the exercise quietly stops teaching
# anything. Nothing asserted this before, and the banks had drifted to a
# measured 0.90 overlap before anyone noticed.
#
# Threshold: the banks currently top out at 0.27. 0.35 leaves room for
# honest additions without letting a transliterated one through.

_MAX_ARABIC_OVERLAP = 0.35

_ARABIC = range(0x0600, 0x0700)

# Orthographic variants people do not distinguish when typing.
_FOLD = str.maketrans({
    "أ": "ا", "إ": "ا", "آ": "ا", "ٱ": "ا",
    "ة": "ه", "ى": "ي", "ؤ": "و", "ئ": "ي",
})

# Proclitics stranded when the English noun they attach to is stripped
# out (الـ app -> "ال"). They carry no theme information.
_ORPHAN_CLITICS = {"ال", "وال", "بال", "فال", "كال", "لل", "ولل", "ب", "ل", "و", "ف", "ك"}


def _arabic_tokens(text):
    """Set of normalised Arabic-script words in ``text``."""
    text = text.replace("ـ", "").translate(_FOLD)
    tokens, current = set(), []
    for ch in text:
        if ord(ch) in _ARABIC and ch.isalnum():
            current.append(ch)
        else:
            if current:
                tokens.add("".join(current))
            current = []
    if current:
        tokens.add("".join(current))
    return tokens - _ORPHAN_CLITICS


def _jaccard(left, right):
    if not left or not right:
        return 0.0
    return len(left & right) / len(left | right)


def test_mixed_entries_diverge_from_their_arabic_siblings():
    for key in spec.THEMES:
        colloquial = [(c, _arabic_tokens(c)) for c in phrases_ar.COLLOQUIAL[key]]
        for mixed in phrases_en.MIXED[key]:
            mixed_tokens = _arabic_tokens(mixed)
            for text, tokens in colloquial:
                score = _jaccard(mixed_tokens, tokens)
                assert score <= _MAX_ARABIC_OVERLAP, (
                    f"{key}: mixed entry shares {score:.2f} of its Arabic "
                    f"vocabulary with a colloquial entry.\n"
                    f"  MIXED:      {mixed}\n"
                    f"  COLLOQUIAL: {text}\n"
                    "This is transliteration, not code-switching: the Arabic "
                    "sentence survives and a noun or two flips script. A "
                    "bag-of-words model will cluster these two on shared "
                    "Arabic tokens rather than on theme, so the corpus stops "
                    "testing cross-register recognition — the one thing it "
                    "exists to test. Rewrite the mixed entry to say something "
                    "genuinely different about the same grievance: a "
                    "different detail, a different sentence shape."
                )
