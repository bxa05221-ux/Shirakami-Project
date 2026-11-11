"""Cross-layer authority chain: verification -> decision -> recovery.

Historical verification provenance does not itself grant present execution
authority. Every boundary must pass before recovery can be accepted.
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.decision_binding import validate_decision_binding
from runtime.revocation_decision_recovery import (
    validate_decision_recovery_after_revocation,
)
from runtime.temporal_integrity import validate_event_graph
from runtime.trust_root_temporal import validate_trust_at_event_time
from runtime.verification_forgery import validate_verification_integrity


class CrossLayerAuthorityError(ValueError):
    pass


def validate_cross_layer_authority_chain(
    events,
    approval: Mapping[str, Any],
    execution: Mapping[str, Any],
    verification: Mapping[str, Any],
    verification_digest: str,
    persisted: Mapping[str, Any],
    *,
    trusted_at,
    revoked_at,
    current_revoked_verifiers: set[str],
) -> None:
    try:
        validate_event_graph(events)
        validate_verification_integrity(verification, verification_digest)
        verifier = verification.get("verifier")
        verification_time = verification.get("verification_time")
        validate_trust_at_event_time(
            verifier=verifier,
            event_time=verification_time,
            trusted_at=trusted_at,
            revoked_at=revoked_at,
        )
        validate_decision_binding(approval, execution)
        validate_decision_recovery_after_revocation(
            approval,
            persisted,
            current_revoked_verifiers=current_revoked_verifiers,
        )
        if approval.get("verifier") != verifier:
            raise CrossLayerAuthorityError("approval verifier mismatch")
    except Exception as exc:
        if isinstance(exc, CrossLayerAuthorityError):
            raise
        raise CrossLayerAuthorityError(str(exc)) from exc
