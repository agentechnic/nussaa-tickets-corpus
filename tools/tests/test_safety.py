"""No real company may appear anywhere in the corpus.

Two hundred fabricated complaints attached to a real business is
defamatory content, and this repository is public.

This list is not paranoia. The project's first chosen brand name — Sufra —
turned out to be a live Saudi food-delivery service, and so did the next
three candidates. The check below scans for other companies; nothing can
scan for the one we picked, which is why the plan requires a name to be
verified against the web, both app stores, and domain availability before
it enters a file.
"""

from pathlib import Path

import pytest

# Only names distinctive enough to scan for. Many Gulf brands ARE ordinary
# vocabulary — جاهز is "ready", طلبات is "orders", نون is the letter noon,
# كريم is "generous", زين is "good" in Najdi, صحتين is "bon appétit", and
# `mada` sits inside "Ramadan". Scanning for those reports the corpus rather
# than the risk, so they are deliberately excluded. See AMBIGUOUS below.
REAL_BRANDS = [
    # Food delivery in the Gulf
    "hungerstation", "hunger station", "jahez", "talabat", "mrsool", "مرسول",
    "the chefz", "chefz", "deliveroo", "ديليفرو", "uber eats", "uber", "أوبر",
    "careem", "sufra", "loqma", "toyou", "burgerizzr", "dailymealz", "keeta",
    # Names checked and rejected while naming this project; never resurface
    "wasel", "kartona", "كرتونة", "sahtain",
    # Retail and marketplaces
    "amazon", "أمازون", "jarir", "جرير", "othaim", "العثيم", "danube",
    "tamimi", "التميمي",
    # Telecom, banks, payment
    "mobily", "موبايلي", "rajhi", "الراجحي", "alinma", "الإنماء",
    "riyad bank", "بنك الرياض", "stc pay", "tamara", "tabby", "paypal",
    "بايبال", "mastercard",
    # Restaurants
    "al baik", "albaik", "البيك", "kudu", "herfy", "هرفي", "starbucks",
    "ستاربكس", "mcdonald", "ماكدونالدز", "shawarmer", "شاورمر",
]

# Real brands whose names are also ordinary words. These CANNOT be scanned
# for without flooding the suite with false positives, so they are listed
# here as a reviewer's checklist rather than an assertion. If one of these
# ever needs to be excluded, it has to be done by reading, not by grep.
AMBIGUOUS = {
    "جاهز": "jahez — but also simply 'ready'",
    "طلبات": "talabat — but also simply 'orders'",
    "نون": "noon — but also the Arabic letter and 'noon'",
    "كريم": "careem — but also 'generous' and 'cream'",
    "زين": "zain — but also 'good' in Najdi",
    "صحتين": "sahtain — but also 'bon appétit'",
    "سفرة": "sufra — but also 'a spread laid for a meal'",
    "لقمة": "loqma — but also 'a mouthful'",
    "مدى": "mada — and `mada` is a substring of 'Ramadan'",
    "بنده": "panda — but also the animal",
    "زاد": "zaad — but also 'provisions'",
}

NUSSAA = Path(__file__).resolve().parents[2] / "nussaa"


def _all_text_files():
    return sorted(NUSSAA.rglob("*.txt")) + sorted(NUSSAA.rglob("*.md"))


@pytest.mark.parametrize("brand", REAL_BRANDS)
def test_no_real_brand_appears_in_the_corpus(brand):
    for path in _all_text_files():
        text = path.read_text(encoding="utf-8").lower()
        assert brand not in text, f"{path.name} names a real company: {brand!r}"


def test_the_corpus_actually_has_files_to_check():
    assert len(_all_text_files()) > 300, "safety scan found almost nothing to scan"


def test_ambiguous_brand_list_is_documented_not_asserted():
    """A reviewer's checklist, deliberately not a grep.

    Present so the reasoning survives: these are real companies whose names
    are ordinary Arabic words, and asserting on them would fail on innocent
    prose. Anyone tightening this file should read the list before assuming
    the omissions were an oversight.
    """
    assert AMBIGUOUS, "the ambiguous-brand rationale must not be silently dropped"
    for name, why in AMBIGUOUS.items():
        assert "—" in why or "but also" in why, (
            f"{name} needs a note saying why it cannot be scanned for"
        )


def test_phrase_banks_are_scanned_too():
    """The corpus is generated from the banks; a leak there reaches every file."""
    from corpus import phrases_ar, phrases_en

    everything = " ".join(
        phrase
        for bank in (phrases_ar.COLLOQUIAL, phrases_ar.FUSHA,
                     phrases_en.ENGLISH, phrases_en.MIXED)
        for variants in bank.values()
        for phrase in variants
    ).lower()
    everything += " " + " ".join(phrases_ar.WORDPLAY).lower()

    for brand in REAL_BRANDS:
        assert brand not in everything, f"phrase banks name a real company: {brand!r}"
