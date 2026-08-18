#!/usr/bin/env bash
# build-download.sh — build nussaa.zip, the single download attendees get.
#
# Refuses to build if the ticket counts are wrong or if facilitator material,
# dry-run output, or a harvested Skill has leaked into the corpus. Attendees
# must not receive the answers.
#
# Usage: bash scripts/build-download.sh

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

fail() { echo "FAIL: $*" >&2; exit 1; }

[[ -d nussaa ]] || fail "no nussaa/ folder at $ROOT"

q1=$(find nussaa/tickets-q1 -type f | wc -l | tr -d ' ')
q2=$(find nussaa/tickets-q2 -type f | wc -l | tr -d ' ')
[[ "$q1" == "200" ]] || fail "tickets-q1 has $q1 files, expected 200"
[[ "$q2" == "120" ]] || fail "tickets-q2 has $q2 files, expected 120"

for f in nussaa/AGENTS.md nussaa/CLAUDE.md nussaa/README.md nussaa/context/changelog.md nussaa/context/themes-2025-q4.md; do
  [[ -f "$f" ]] || fail "missing $f"
done

# Nothing that gives the game away.
leaked=$(find nussaa -name 'themes-2026-*.md' -o -name 'SKILL.md' -o -name 'nussaa-answer-key.md' | head -5)
[[ -z "$leaked" ]] || fail "answer material inside the corpus:"$'\n'"$leaked"

# The rules file ships under both names and must not have drifted.
if ! diff -q <(tail -n +2 nussaa/AGENTS.md) <(tail -n +2 nussaa/CLAUDE.md) >/dev/null; then
  fail "AGENTS.md and CLAUDE.md differ below the title line"
fi

rm -f nussaa.zip
zip -rq nussaa.zip nussaa -x '*.DS_Store'

echo "built nussaa.zip — $(du -h nussaa.zip | cut -f1), $q1 + $q2 tickets"
