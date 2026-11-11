"""Prevent revoked verifier state from resurrecting authority during recovery."""
from __future__ import annotations

from typing import Any, Mapping


class RevocationDecisionRecoveryError(ValueError):
    pass


def validate_decision_recovery_after_revocation(
    approval: Mapping[str, Any],
    persisted: Mapping[str, Any],
    *,
    current_revoked_verifiers: set[str],
) -> None:
    verifier = approval.get("verifier")
    if not verifier:
        raise RevocationDecisionRecoveryError("missing verifier provenance")

    if verifier in current_revoked_verifiers:
        raise RevocationDecisionRecoveryError(
            "revoked verifier cannot resurrect persisted authority"
        )

    required = ("approval_id", "context_version", "evidence_hash", "protocol_hash", "proposal_id")
    for field in required:
        if approval.get(field) in (None, ""):
            raise RevocationDecisionRecoveryError(
                f"missing approval binding: {field}"
            )
        if persisted.get(field) in (None, ""):
            raise RevocationDecisionRecoveryError(
                f"missing persisted binding: {field}"
            )
        if approval.get(field) != persisted.get(field):
            raise RevocationDecisionRecoveryError(
                f"recovery binding mismatch: {field}"
            )

    if persisted.get("human_approval") is not True:
        raise RevocationDecisionRecoveryError(
            "persisted state does not contain explicit human approval"
        )

    if persisted.get("runtime_authority") is True:
        raise RevocationDecisionRecoveryError(
            "runtime authority cannot be restored by recovery"
        )
