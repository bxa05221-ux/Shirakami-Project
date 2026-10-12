"""Authenticated human session replay boundary."""
from __future__ import annotations

from typing import Any, Mapping


class HumanAuthReplayError(ValueError):
    pass


def validate_human_auth_event(
    identity: Mapping[str, Any],
    *,
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
) -> None:
    principal = identity.get("principal_id")
    auth_id = identity.get("authentication_id")

    if not principal or not auth_id:
        raise HumanAuthReplayError("missing principal/authentication identity")
    if identity.get("actor_type") != "human":
        raise HumanAuthReplayError("authentication actor is not human")
    if identity.get("authenticated") is not True:
        raise HumanAuthReplayError("authentication is not established")
    if auth_id in seen_authentication_ids:
        raise HumanAuthReplayError("authentication replay detected")
    if auth_id in current_revoked_authentications:
        raise HumanAuthReplayError("revoked authentication cannot be reused")

    return


def validate_human_auth_for_decision(
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
    *,
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
) -> None:
    validate_human_auth_event(
        identity,
        current_revoked_authentications=current_revoked_authentications,
        seen_authentication_ids=seen_authentication_ids,
    )

    if decision.get("principal_id") != identity["principal_id"]:
        raise HumanAuthReplayError("principal substitution")
    if decision.get("authentication_id") != identity["authentication_id"]:
        raise HumanAuthReplayError("authentication substitution")
    if decision.get("human_approval") is not True:
        raise HumanAuthReplayError("missing human approval")
    if decision.get("runtime_authority") is True:
        raise HumanAuthReplayError("runtime authority forbidden")
