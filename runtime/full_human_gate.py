"""Full Human Gate composition across UI, decision, identity, auth, signature, trust, time, and recovery."""
from __future__ import annotations
from typing import Any, Mapping
from runtime.ui_adapter_gate import validate_ui_adapter_decision
from runtime.human_decision_replay import validate_human_decision_event
from runtime.decision_binding import validate_decision_binding
from runtime.authenticated_human_gate import validate_authenticated_human_gate
class FullHumanGateError(ValueError):
    pass
def validate_full_human_gate(*, ui_event: Mapping[str, Any], identity: Mapping[str, Any], decision: Mapping[str, Any], approval: Mapping[str, Any], execution: Mapping[str, Any], signature: str, secret: bytes, persisted: Mapping[str, Any], decision_time: str, trusted_principals: frozenset[str], trusted_keys: frozenset[str], trusted_from: str, trusted_until: str | None = None, revoked_at: str | None = None, current_revoked_authentications: frozenset[str] = frozenset(), seen_authentication_ids: frozenset[str] = frozenset(), current_revoked_keys: frozenset[str] = frozenset(), seen_decision_ids: frozenset[str] = frozenset()) -> None:
    try:
        validate_ui_adapter_decision(ui_event, decision)
        validate_human_decision_event(decision, seen_decision_ids=seen_decision_ids)
        validate_decision_binding(approval, execution)
        validate_authenticated_human_gate(identity=identity, decision=decision, approval=approval, signature=signature, secret=secret, persisted=persisted, decision_time=decision_time, trusted_principals=trusted_principals, trusted_keys=trusted_keys, trusted_from=trusted_from, trusted_until=trusted_until, revoked_at=revoked_at, current_revoked_authentications=current_revoked_authentications, seen_authentication_ids=seen_authentication_ids, current_revoked_keys=current_revoked_keys)
    except Exception as exc:
        raise FullHumanGateError(str(exc)) from exc
