"""Full-system authority chain composing temporal, verification, trust, and human gate boundaries."""
from __future__ import annotations
from typing import Any, Mapping

from runtime.cross_layer_authority_chain import validate_cross_layer_authority_chain
from runtime.full_human_gate import validate_full_human_gate

class FullSystemAuthorityError(ValueError):
    pass


def _event_time(event: Mapping[str, Any]):
    from datetime import datetime
    value = str(event.get("occurred_at", ""))
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FullSystemAuthorityError(f"invalid system event timestamp: {value}") from exc


def _validate_system_temporal_binding(events, verification, decision, approval, execution) -> None:
    verification_id = verification.get("verification_id")
    decision_id = decision.get("decision_id")
    approval_id = approval.get("approval_id")
    if not verification_id or not decision_id or not approval_id:
        raise FullSystemAuthorityError("system temporal binding identifiers are required")
    verification_events = [e for e in events if e.get("event_type") == "verification" and e.get("verification_id") == verification_id]
    decision_events = [e for e in events if e.get("event_type") == "human_decision" and e.get("decision_id") == decision_id]
    approval_events = [e for e in events if e.get("event_type") == "human_approval" and e.get("approval_id") == approval_id]
    execution_events = [e for e in events if e.get("event_type") == "execution" and e.get("approval_id") == approval_id]
    if not all((verification_events, decision_events, approval_events, execution_events)):
        raise FullSystemAuthorityError("system temporal artifacts are incomplete")
    verification_event = verification_events[0]
    decision_event = decision_events[0]
    approval_event = approval_events[0]
    execution_event = execution_events[0]
    if verification_event.get("verification_id") != verification_id:
        raise FullSystemAuthorityError("verification event binding mismatch")
    if decision_event.get("decision_id") != decision_id:
        raise FullSystemAuthorityError("decision event binding mismatch")
    for field in ("approval_id", "context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        if approval_event.get(field) != approval.get(field):
            raise FullSystemAuthorityError(f"approval event {field} mismatch")
    for field in ("approval_id", "context_version"):
        if execution_event.get(field) != execution.get(field):
            raise FullSystemAuthorityError(f"execution event {field} mismatch")
    vt, dt, at, xt = map(_event_time, (verification_event, decision_event, approval_event, execution_event))
    if not (vt <= dt <= at <= xt):
        raise FullSystemAuthorityError("system temporal order violation")

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
    trusted_verifiers: frozenset[str],
    trusted_keys: frozenset[str],
    trusted_from: str,
    trusted_until: str | None = None,
    revoked_at: str | None = None,
    verifier_revoked_at: frozenset[str] = frozenset(),
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
    current_revoked_keys: frozenset[str] = frozenset(),
    seen_decision_ids: frozenset[str] = frozenset(),
) -> None:
    try:
        validate_cross_layer_authority_chain(
            events, approval, execution, verification, verification_digest,
            persisted, trusted_at=trusted_verifiers, revoked_at=verifier_revoked_at,
            current_revoked_verifiers=verifier_revoked_at,
        )
        _validate_system_temporal_binding(events, verification, decision, approval, execution)
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
