"""Temporal validity of verifier trust.

A verification event is evaluated against the trust state effective at its
event time. Revocation does not retroactively rewrite history, but a revoked
verifier cannot be accepted for a later event.
"""
from __future__ import annotations

from datetime import datetime
from typing import FrozenSet


class TrustRootTemporalError(ValueError):
    pass


def _parse(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except (TypeError, ValueError) as exc:
        raise TrustRootTemporalError("invalid timestamp") from exc


def validate_trust_at_event_time(
    *,
    verifier: str,
    event_time: str,
    trusted_at: FrozenSet[str],
    revoked_at: FrozenSet[str],
) -> None:
    if not verifier:
        raise TrustRootTemporalError("missing verifier")

    if verifier in revoked_at:
        raise TrustRootTemporalError("verifier revoked")

    if verifier not in trusted_at:
        raise TrustRootTemporalError("verifier not trusted at event time")

    _parse(event_time)


def reject_revoked_replay(
    *,
    verifier: str,
    verification_time: str,
    current_revoked: FrozenSet[str],
) -> None:
    _parse(verification_time)
    if verifier in current_revoked:
        raise TrustRootTemporalError("revoked verifier replay rejected")
