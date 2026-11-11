import pytest

from runtime.quorum_decision_recovery import (
    QuorumDecisionRecoveryError,
    validate_quorum_decision_recovery,
)


def v(i, verifier):
    return {
        "verification_id": f"V{i}",
        "target_id": "T1",
        "result": "pass",
        "verifier": verifier,
        "verifier_instance": f"{verifier}-1",
    }


APPROVAL = {
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
}

PERSISTED = {
    **APPROVAL,
    "human_approval": True,
    "runtime_authority": False,
}


def test_quorum_can_support_existing_human_approval():
    validate_quorum_decision_recovery(
        [v(1, "A"), v(2, "B")], APPROVAL, PERSISTED
    )


def test_quorum_cannot_create_human_approval():
    with pytest.raises(QuorumDecisionRecoveryError):
        validate_quorum_decision_recovery(
            [{**v(1, "A"), "human_approval": True}, v(2, "B")],
            APPROVAL,
            {**PERSISTED, "human_approval": False},
        )


def test_quorum_cannot_create_runtime_authority():
    with pytest.raises(QuorumDecisionRecoveryError):
        validate_quorum_decision_recovery(
            [{**v(1, "A"), "runtime_authority": True}, v(2, "B")],
            APPROVAL,
            PERSISTED,
        )


def test_binding_mutation_blocks_recovery():
    with pytest.raises(QuorumDecisionRecoveryError):
        validate_quorum_decision_recovery(
            [v(1, "A"), v(2, "B")],
            APPROVAL,
            {**PERSISTED, "evidence_hash": "ATTACK"},
        )


def test_missing_human_approval_blocks_recovery():
    with pytest.raises(QuorumDecisionRecoveryError):
        validate_quorum_decision_recovery(
            [v(1, "A"), v(2, "B")],
            APPROVAL,
            {**PERSISTED, "human_approval": False},
        )


def test_revoked_verifier_blocks_quorum_recovery():
    with pytest.raises(QuorumDecisionRecoveryError):
        validate_quorum_decision_recovery(
            [v(1, "A"), v(2, "B")],
            APPROVAL,
            PERSISTED,
            current_revoked_verifiers=frozenset({"B"}),
        )


def test_quorum_does_not_replace_decision_binding():
    # This layer only verifies the boundary; exact decision binding remains
    # the responsibility of the existing decision-binding validator.
    validate_quorum_decision_recovery(
        [v(1, "A"), v(2, "B")], APPROVAL, PERSISTED
    )
