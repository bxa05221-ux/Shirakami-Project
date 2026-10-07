"""Human signing-key trust boundary (abstract/test contract)."""
from __future__ import annotations

from typing import Any, Mapping


class HumanKeyTrustError(ValueError):
    pass


def validate_human_key_trust(
    decision: Mapping[str, Any],
    *,
    trusted_principals: frozenset[str],
    revoked_keys: frozenset[str] = frozenset(),
) -> None:
    principal = decision.get("principal_id")
    key_id = decision.get("key_id")

    if not principal or not key_id:
        raise HumanKeyTrustError("missing human principal or key")
    if principal not in trusted_principals:
        raise HumanKeyTrustError("human principal is not trusted")
    if key_id in revoked_keys:
        raise HumanKeyTrustError("human signing key is revoked")
    if decision.get("actor_type") != "human":
        raise HumanKeyTrustError("decision actor is not human")
    if decision.get("human_approval") is not True:
        raise HumanKeyTrustError("missing human approval")
    if decision.get("runtime_authority") is True:
        raise HumanKeyTrustError("runtime authority forbidden")

    return
