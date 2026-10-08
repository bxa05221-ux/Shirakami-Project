"""Human identity authentication boundary.

This is an abstract contract test: the gate accepts only an explicitly
authenticated human principal whose authentication context is bound to the
decision. It does not implement a production identity provider.
"""
from __future__ import annotations

from typing import Any, Mapping


class HumanIdentityAuthError(ValueError):
    pass


BOUND_FIELDS = (
    "decision_id",
    "approval_id",
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
)


def validate_authenticated_human_decision(
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> None:
    principal = identity.get("principal_id")
    auth_id = identity.get("authentication_id")

    if not principal or not auth_id:
        raise HumanIdentityAuthError("missing authenticated human identity")

    if identity.get("actor_type") != "human":
        raise HumanIdentityAuthError("identity is not a human principal")

    if identity.get("authenticated") is not True:
        raise HumanIdentityAuthError("human authentication is not established")

    if identity.get("authentication_method") in (None, ""):
        raise HumanIdentityAuthError("missing authentication method")

    if decision.get("actor_type") != "human":
        raise HumanIdentityAuthError("decision actor is not human")

    if decision.get("human_approval") is not True:
        raise HumanIdentityAuthError("decision lacks human approval")

    if decision.get("principal_id") != principal:
        raise HumanIdentityAuthError("decision principal mismatch")

    if decision.get("authentication_id") != auth_id:
        raise HumanIdentityAuthError("decision authentication mismatch")

    for field in BOUND_FIELDS:
        if identity.get(field) != decision.get(field):
            raise HumanIdentityAuthError(f"identity/decision binding mismatch: {field}")

    if decision.get("runtime_authority") is True:
        raise HumanIdentityAuthError("runtime cannot become human authority")

    return
