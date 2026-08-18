"""The corpus's single source of truth.

The generator builds from this and the tests verify against it, so the
planted signal is defined exactly once. Changing anything here changes
what the facilitator answer key must say.
"""

from dataclasses import dataclass


CORPUS_SEED = 20260815

Q1_TICKET_COUNT = 200
Q2_TICKET_COUNT = 120


@dataclass(frozen=True)
class Release:
    version: str
    date: str  # YYYY-MM-DD
    summary: str


@dataclass(frozen=True)
class Theme:
    key: str
    label_en: str
    label_ar: str


@dataclass(frozen=True)
class PlantedSignal:
    theme_key: str
    release_version: str
    count: int
    window_days: int


# The v4.2 address picker is the cause the workshop is built around. Every
# other release is ordinary noise, present so the correlation has to be
# found rather than guessed.
RELEASES = [
    Release("4.0", "2026-01-08", "Ramadan pre-order scheduling."),
    Release("4.1", "2026-01-27", "Restaurant search ranking rebuilt."),
    Release("4.2", "2026-02-11", "New address picker with map pinning; "
                                 "replaces free-text address entry."),
    Release("4.3", "2026-03-04", "Loyalty points shown at checkout."),
    Release("4.4", "2026-03-23", "Order tracking screen refresh."),
    # Q2 territory — the payment migration is Q2's dominant cause.
    Release("4.5", "2026-04-14", "Payment provider migration."),
    Release("4.6", "2026-05-06", "Group orders."),
]

THEMES = {
    "driver_lost": Theme("driver_lost", "Driver could not find the address",
                         "الكابتن ما لقى العنوان"),
    "late": Theme("late", "Late delivery", "تأخير التوصيل"),
    "wrong_items": Theme("wrong_items", "Wrong or missing items",
                         "طلب خاطئ أو ناقص"),
    "cold_food": Theme("cold_food", "Food arrived cold", "الأكل وصل بارد"),
    "payment_failed": Theme("payment_failed", "Payment failed or double charged",
                            "مشكلة في الدفع أو خصم مزدوج"),
    "refund_delay": Theme("refund_delay", "Refund not received",
                          "تأخر استرداد المبلغ"),
    "app_crash": Theme("app_crash", "App crashes or will not open",
                       "التطبيق يطفي أو ما يفتح"),
    "rude_driver": Theme("rude_driver", "Driver conduct", "تعامل الكابتن"),
}

PLANTED = PlantedSignal(
    theme_key="driver_lost",
    release_version="4.2",
    count=23,
    window_days=21,
)
