from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
import math

SHANGHAI = timezone(timedelta(hours=8), "Asia/Shanghai")


def parse_instant(value) -> datetime | None:
    if value is None or value == "":
        return None
    try:
        result = value if isinstance(value, datetime) else datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        return result.replace(tzinfo=timezone.utc) if result.tzinfo is None else result
    except (ValueError, TypeError):
        return None


def date_header(value) -> datetime | None:
    try:
        result = parsedate_to_datetime(value or "")
        return result if result.tzinfo else result.replace(tzinfo=timezone.utc)
    except (TypeError, ValueError, IndexError, OverflowError):
        return None


def round_hours(value: float) -> int:
    # Match JavaScript Math.round used by the existing source adapter.
    return math.floor(value + 0.5)


def detect_fallback_skew(samples: list[dict]) -> int:
    offsets = []
    for row in samples:
        internal, header = parse_instant(row.get("internal_date")), date_header(row.get("date_header"))
        if internal and header:
            offsets.append(round_hours((internal - header).total_seconds() / 3600))
    if not offsets:
        return 0
    value, count = Counter(offsets).most_common(1)[0]
    return value if value > 0 and count / len(offsets) >= 0.8 else 0


def received_at(raw: dict, fallback_skew: int = 0) -> tuple[datetime | None, int]:
    internal = parse_instant(raw.get("internal_date"))
    if internal is None:
        return parse_instant(raw.get("first_seen_at")), 0
    header = date_header(raw.get("date_header"))
    hours = round_hours((internal - header).total_seconds() / 3600) if header else fallback_skew
    shift = hours if (1 <= hours <= 14 if header else hours > 0) else 0
    return (internal - timedelta(hours=shift)).astimezone(timezone.utc), shift
