"""Temporal validity boundary for human signing keys."""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Mapping


class HumanKeyTemporalError(ValueError):
    pass


def _parse(value: Any) -> datetime:
    if not isinstance(value, str):
        raise HumanKeyTemporalError("invalid timestamp")
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise HumanKeyTemporalError("invalid timestamp") from exc
    if dt.tzinfo is None:
        raise HumanKeyTemporalError("timestamp must be timezone-aware")
    return dt.astimezone(timezone.utc)


def validate_key_at_decision_time(
    decision: Mapping[str, Any],
    *,
    decision_time: str,
    trusted_from: str,
    trusted_until: str | None = None,
    revoked_at: str | None = None,
) -> None:
    key_id = decision.get("key_id")
    if not key_id:
        raise HumanKeyTemporalError("missing key_id")

    t = _parse(decision_time)
    start = _parse(trusted_from)

    if t < start:
        raise HumanKeyTemporalError("key was not trusted at decision time")

    if trusted_until is not None and t >= _parse(trusted_until):
        raise HumanKeyTemporalError("key trust had expired at decision time")

    if revoked_at is not None and t >= _parse(revoked_at):
        raise HumanKeyTemporalError("key was revoked at decision time")

    return
