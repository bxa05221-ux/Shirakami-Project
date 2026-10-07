import pytest

from runtime.cross_layer_authority_chain import (
    CrossLayerAuthorityError,
    validate_cross_layer_authority_chain,
)
from runtime.verification_forgery import verification_digest

VERIFICATION = {
    "verification_id": "V1",
    "target_id": "T1",
    "result": "pass",
    "verifier": "v1",
    "verifier_instance": "v1-i1",
    "verification_time": "2026-10-07T10:04:00+09:00",
}

APPROVAL = {
    "approval_id": "A1",
    "context_version": 10,
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "verifier": "v1",
}

EXECUTION = {
    "approval_id": "A1",
    "context_version": 10,
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "runtime_authority": False,
}

PERSISTED = {
    **APPROVAL,
    "human_approval": True,
    "runtime_authority": False,
}

EVENTS = [
    {
        "event_id": "obs-1",
        "event_type": "observation",
        "occurred_at": "2026-10-07T10:00:00+09:00",
    },
    {
        "event_id": "approval-1",
        "event_type": "human_approval",
        "approval_id": "A1",
        "context_version": 10,
        "occurred_at": "2026-10-07T10:05:00+09:00",
        "parent_event_id": "obs-1",
    },
    {
        "event_id": "exec-1",
        "event_type": "execution",
        "approval_id": "A1",
        "context_version": 10,
        "occurred_at": "2026-10-07T10:06:00+09:00",
        "parent_event_id": "approval-1",
    },
]


def call(**overrides):
    verification = {**VERIFICATION, **overrides.pop("verification", {})}
    return validate_cross_layer_authority_chain(
        EVENTS,
        APPROVAL,
        EXECUTION,
        verification,
        verification_digest(verification),
        PERSISTED,
        trusted_at=frozenset({"v1"}),
        revoked_at=frozenset(),
        current_revoked_verifiers=overrides.pop("current_revoked_verifiers", set()),
        **overrides,
    )


def test_complete_cross_layer_chain_passes():
    call()


def test_revocation_blocks_resurrection():
    with pytest.raises(CrossLayerAuthorityError, match="revoked"):
        call(current_revoked_verifiers={"v1"})


def test_verification_mutation_blocks_chain():
    with pytest.raises(CrossLayerAuthorityError):
        call(verification={"result": "fail"})


def test_verifier_substitution_blocks_chain():
    with pytest.raises(CrossLayerAuthorityError):
        call(verification={"verifier": "v2"})


def test_approval_scope_mutation_blocks_chain():
    bad = dict(APPROVAL)
    bad["evidence_hash"] = "ATTACK"
    with pytest.raises(CrossLayerAuthorityError):
        validate_cross_layer_authority_chain(
            EVENTS, bad, EXECUTION, VERIFICATION,
            verification_digest(VERIFICATION), PERSISTED,
            trusted_at=frozenset({"v1"}), revoked_at=frozenset(),
            current_revoked_verifiers=set(),
        )


def test_persisted_missing_binding_blocks_chain():
    bad = dict(PERSISTED)
    bad.pop("protocol_hash")
    with pytest.raises(CrossLayerAuthorityError):
        validate_cross_layer_authority_chain(
            EVENTS, APPROVAL, EXECUTION, VERIFICATION,
            verification_digest(VERIFICATION), bad,
            trusted_at=frozenset({"v1"}), revoked_at=frozenset(),
            current_revoked_verifiers=set(),
        )


def test_runtime_authority_claim_blocks_chain():
    bad = {**EXECUTION, "runtime_authority": True}
    with pytest.raises(CrossLayerAuthorityError):
        validate_cross_layer_authority_chain(
            EVENTS, APPROVAL, bad, VERIFICATION,
            verification_digest(VERIFICATION), PERSISTED,
            trusted_at=frozenset({"v1"}), revoked_at=frozenset(),
            current_revoked_verifiers=set(),
        )
