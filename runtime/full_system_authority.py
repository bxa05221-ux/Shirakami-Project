"""Full-system authority chain composing temporal, verification, trust, and human gate boundaries."""
from __future__ import annotations
from typing import Any, Mapping

from runtime.cross_layer_authority_chain import validate_cross_layer_authority_chain
from runtime.full_human_gate import validate_full_human_gate

class FullSystemAuthorityError(ValueError):
    pass

def validate_full_system_authority(
    *,
    events,
    approval: Mapping[str, Any],
    execution: Mapping[str, Any],
    verification: Mapping[str, Any],
    verification_digest: str,
    persisted: Mapping[str, Any],
    ui_event: Mapping[str, Any],
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
    signature: str,
    secret: bytes,
    decision_time: str,
    trusted_principals: frozenset[str],
    trusted_keys: frozenset[str],
    trusted_from: str,
    trusted_until: str | None = None,
    revoked_at: str | None = None,
    current_revoked_verifiers: set[str] = set(),
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
    current_revoked_keys: frozenset[str] = frozenset(),
    seen_decision_ids: frozenset[str] = frozenset(),
) -> None:
    try:
        validate_cross_layer_authority_chain(
            events, approval, execution, verification, verification_digest,
            persisted, trusted_at=trusted_from, revoked_at=revoked_at,
            current_revoked_verifiers=current_revoked_verifiers,
        )
        validate_full_human_gate(
            ui_event=ui_event, identity=identity, decision=decision,
            approval=approval, execution=execution, signature=signature,
            secret=secret, persisted=persisted, decision_time=decision_time,
            trusted_principals=trusted_principals, trusted_keys=trusted_keys,
            trusted_from=trusted_from, trusted_until=trusted_until,
            revoked_at=revoked_at,
            current_revoked_authentications=current_revoked_authentications,
            seen_authentication_ids=seen_authentication_ids,
            current_revoked_keys=current_revoked_keys,
            seen_decision_ids=seen_decision_ids,
        )
        if decision.get("approval_id") != approval.get("approval_id"):
            raise FullSystemAuthorityError("human decision approval mismatch")
        if decision.get("context_version") != approval.get("context_version"):
            raise FullSystemAuthorityError("human decision context mismatch")
        if decision.get("evidence_hash") != approval.get("evidence_hash"):
            raise FullSystemAuthorityError("human decision evidence mismatch")
        if decision.get("protocol_hash") != approval.get("protocol_hash"):
            raise FullSystemAuthorityError("human decision protocol mismatch")
        if decision.get("proposal_id") != approval.get("proposal_id"):
            raise FullSystemAuthorityError("human decision proposal mismatch")
    except Exception as exc:
        if isinstance(exc, FullSystemAuthorityError):
            raise
        raise FullSystemAuthorityError(str(exc)) from exc
