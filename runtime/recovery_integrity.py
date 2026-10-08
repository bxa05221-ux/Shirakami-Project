"""Fail-closed recovery boundary for Shirakami.

An interrupted execution never gains authority merely because an approval
was persisted before or around a crash. Recovery must prove that the
approval is still bound to the same execution scope and that the previous
transition reached a known durable state.
"""
from __future__ import annotations

from typing import Any, Mapping


class RecoveryIntegrityError(ValueError):
    """Raised when recovery cannot establish a safe, authoritative state."""


KNOWN_DURABLE_STATES = {"approved", "candidate_created", "verified", "committed"}
QUARANTINE_STATES = {
    "unknown",
    "apply_started",
    "execution_applied",
    "crashed",
    "incomplete",
}


def validate_recovery(
    approval: Mapping[str, Any],
    persisted: Mapping[str, Any],
) -> None:
    """Fail closed unless persisted state is complete and approval-bound."""
    state = persisted.get("state")
    if state in QUARANTINE_STATES or state not in KNOWN_DURABLE_STATES:
        raise RecoveryIntegrityError(
            f"recovery requires quarantine for non-durable state: {state}"
        )

    if persisted.get("approval_id") != approval.get("approval_id"):
        raise RecoveryIntegrityError("recovery approval mismatch")

    for field in ("context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        if persisted.get(field) != approval.get(field):
            raise RecoveryIntegrityError(f"recovery binding mismatch: {field}")

    if persisted.get("runtime_authority") is True:
        raise RecoveryIntegrityError("runtime authority claim is forbidden")


def recovery_action(persisted: Mapping[str, Any]) -> str:
    """Return the only safe recovery action for a persisted state."""
    state = persisted.get("state")
    if state in QUARANTINE_STATES:
        return "quarantine_and_reverify"
    if state == "approved":
        return "resume_after_integrity_check"
    if state == "candidate_created":
        return "reconcile_candidate"
    if state == "verified":
        return "reconcile_verified"
    if state == "committed":
        return "reconcile_committed"
    return "quarantine_and_reverify"
