"""Cross-layer boundary: verifier quorum cannot mint decision or recovery authority."""
from __future__ import annotations

from typing import Any, Mapping, Sequence


class QuorumDecisionRecoveryError(ValueError):
    pass


REQUIRED_BINDINGS = (
    "approval_id",
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
)


def validate_quorum_decision_recovery(
    quorum_results: Sequence[Mapping[str, Any]],
    approval: Mapping[str, Any],
    persisted: Mapping[str, Any],
    *,
    current_revoked_verifiers: frozenset[str] = frozenset(),
) -> None:
    if not quorum_results:
        raise QuorumDecisionRecoveryError("missing verifier quorum")

    for result in quorum_results:
        if result.get("result") != "pass":
            raise QuorumDecisionRecoveryError("quorum contains non-pass result")
        if result.get("human_approval") is True:
            raise QuorumDecisionRecoveryError("quorum cannot manufacture human approval")
        if result.get("runtime_authority") is True:
            raise QuorumDecisionRecoveryError("quorum cannot manufacture runtime authority")
        if result.get("verifier") in current_revoked_verifiers:
            raise QuorumDecisionRecoveryError("revoked verifier cannot authorize quorum")

    for field in REQUIRED_BINDINGS:
        if approval.get(field) in (None, "") or persisted.get(field) in (None, ""):
            raise QuorumDecisionRecoveryError(f"missing binding: {field}")
        if approval[field] != persisted[field]:
            raise QuorumDecisionRecoveryError(f"binding mismatch: {field}")

    if persisted.get("human_approval") is not True:
        raise QuorumDecisionRecoveryError("persisted state lacks independent human approval")
    if persisted.get("runtime_authority") is True:
        raise QuorumDecisionRecoveryError("persisted runtime authority is forbidden")

    # A quorum can support a human decision; it cannot create one.
    return
