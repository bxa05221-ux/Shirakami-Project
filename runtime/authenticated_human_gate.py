"""End-to-end authenticated Human Gate boundary composition."""
from __future__ import annotations
from typing import Any, Mapping

from runtime.human_gate_authenticity import validate_human_gate_authenticity
from runtime.human_identity_auth import validate_authenticated_human_decision
from runtime.human_auth_replay import validate_human_auth_for_decision
from runtime.human_decision_signature import validate_human_decision_signature
from runtime.human_key_trust import validate_human_key_trust
from runtime.human_key_temporal import validate_key_at_decision_time
from runtime.human_key_rotation_recovery import validate_key_rotation_recovery

class AuthenticatedHumanGateError(ValueError):
    pass

def validate_authenticated_human_gate(
    *,
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
    approval: Mapping[str, Any],
    signature: str,
    secret: bytes,
    persisted: Mapping[str, Any],
    decision_time: str,
    trusted_principals: frozenset[str],
    trusted_keys: frozenset[str],
    trusted_from: str,
    trusted_until: str | None = None,
    revoked_at: str | None = None,
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
    current_revoked_keys: frozenset[str] = frozenset(),
) -> None:
    try:
        validate_human_gate_authenticity(decision, approval)
        validate_authenticated_human_decision(identity, decision)
        validate_human_auth_for_decision(
            identity, decision,
            current_revoked_authentications=current_revoked_authentications,
            seen_authentication_ids=seen_authentication_ids,
        )
        validate_human_decision_signature(decision, signature, secret)
        validate_human_key_trust(
            decision,
            trusted_principals=trusted_principals,
            trusted_keys=trusted_keys,
            revoked_keys=current_revoked_keys,
        )
        validate_key_at_decision_time(
            decision,
            decision_time=decision_time,
            trusted_from=trusted_from,
            trusted_until=trusted_until,
            revoked_at=revoked_at,
        )
        validate_key_rotation_recovery(
            decision, persisted,
            current_revoked_keys=current_revoked_keys,
            trusted_keys=trusted_keys,
        )
    except Exception as exc:
        raise AuthenticatedHumanGateError(str(exc)) from exc
    return
