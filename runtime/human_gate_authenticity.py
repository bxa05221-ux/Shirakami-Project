"""Human Gate authenticity boundary.

A record that merely claims human approval is not sufficient authority.
The gate requires an explicit human decision event and exact bindings.
"""
from __future__ import annotations

from typing import Any, Mapping


class HumanGateAuthenticityError(ValueError):
    pass


REQUIRED_BINDINGS = (
    "approval_id",
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
)


def validate_human_gate_authenticity(
    decision: Mapping[str, Any],
    approval: Mapping[str, Any],
) -> None:
    if decision.get("actor_type") != "human":
        raise HumanGateAuthenticityError("decision actor is not human")
    if decision.get("decision") not in {"approve", "reject", "revise"}:
        raise HumanGateAuthenticityError("invalid human decision")
    if decision.get("runtime_authority") is True:
        raise HumanGateAuthenticityError("runtime cannot impersonate human authority")
    if decision.get("human_approval") is not True:
        raise HumanGateAuthenticityError("human approval is not explicitly recorded")

    for field in REQUIRED_BINDINGS:
        if decision.get(field) in (None, "") or approval.get(field) in (None, ""):
            raise HumanGateAuthenticityError(f"missing binding: {field}")
        if decision[field] != approval[field]:
            raise HumanGateAuthenticityError(f"decision binding mismatch: {field}")

    if approval.get("human_approval") is not True:
        raise HumanGateAuthenticityError("approval lacks explicit human approval")

    # This validator authenticates the shape/provenance boundary only.
    # It does not infer that a UI claim or runtime output is a real person.
    return
