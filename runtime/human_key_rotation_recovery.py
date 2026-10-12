"""Human signing-key rotation, revocation, replay, and recovery boundary."""
from __future__ import annotations
from typing import Any, Mapping

class HumanKeyRotationError(ValueError):
    pass

BINDINGS=("decision_id","approval_id","context_version","evidence_hash","protocol_hash","proposal_id","principal_id","authentication_id","key_id")

def validate_key_rotation_recovery(
    decision: Mapping[str, Any],
    persisted: Mapping[str, Any],
    *,
    current_revoked_keys: frozenset[str]=frozenset(),
    trusted_keys: frozenset[str]=frozenset(),
) -> None:
    key_id=decision.get("key_id")
    if not key_id or key_id not in trusted_keys:
        raise HumanKeyRotationError("decision key is not currently trusted")
    if key_id in current_revoked_keys:
        raise HumanKeyRotationError("decision key is revoked")
    if decision.get("human_approval") is not True:
        raise HumanKeyRotationError("missing human approval")
    if decision.get("runtime_authority") is True or persisted.get("runtime_authority") is True:
        raise HumanKeyRotationError("runtime authority forbidden")
    if persisted.get("human_approval") is not True:
        raise HumanKeyRotationError("persisted state lacks human approval")
    for field in BINDINGS:
        if not decision.get(field) or not persisted.get(field):
            raise HumanKeyRotationError(f"missing binding: {field}")
        if decision[field] != persisted[field]:
            raise HumanKeyRotationError(f"binding mismatch: {field}")
    return
