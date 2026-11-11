"""Decision-to-execution binding boundary for Shirakami.

A human approval is valid only for the exact decision scope it approved:
context, evidence, protocol, and proposal. Runtime output never becomes
authority merely by satisfying these bindings.
"""
from __future__ import annotations

from typing import Any, Mapping


class DecisionBindingError(ValueError):
    """Raised when an approval is used outside its approved scope."""


REQUIRED_BINDINGS = (
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
)


def validate_decision_binding(
    approval: Mapping[str, Any],
    execution: Mapping[str, Any],
) -> None:
    """Fail closed unless execution exactly matches the approved scope."""
    approval_id = approval.get("approval_id")
    if not approval_id:
        raise DecisionBindingError("approval_id is required")

    for field in REQUIRED_BINDINGS:
        approved = approval.get(field)
        attempted = execution.get(field)
        if approved is None:
            raise DecisionBindingError(f"approval missing binding: {field}")
        if attempted is None:
            raise DecisionBindingError(f"execution missing binding: {field}")
        if attempted != approved:
            raise DecisionBindingError(
                f"decision binding mismatch: {field} for approval {approval_id}"
            )

    if execution.get("approval_id") != approval_id:
        raise DecisionBindingError(
            f"execution uses different approval_id: {execution.get('approval_id')}"
        )

    if execution.get("runtime_authority") is True:
        raise DecisionBindingError("runtime authority claim is forbidden")
