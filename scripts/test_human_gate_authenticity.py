import pytest

from runtime.human_gate_authenticity import (
    HumanGateAuthenticityError,
    validate_human_gate_authenticity,
)


BINDINGS = {
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
}

APPROVAL = {**BINDINGS, "human_approval": True}

DECISION = {
    **BINDINGS,
    "actor_type": "human",
    "decision": "approve",
    "human_approval": True,
    "runtime_authority": False,
}


def test_valid_human_decision_passes():
    validate_human_gate_authenticity(DECISION, APPROVAL)


def test_runtime_cannot_claim_human_actor():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            {**DECISION, "actor_type": "runtime"},
            APPROVAL,
        )


def test_missing_human_approval_fails_closed():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            {**DECISION, "human_approval": False},
            APPROVAL,
        )


def test_fake_approval_record_fails():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            DECISION,
            {**APPROVAL, "human_approval": False},
        )


def test_binding_mutation_fails():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            {**DECISION, "evidence_hash": "ATTACK"},
            APPROVAL,
        )


def test_runtime_authority_claim_fails():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            {**DECISION, "runtime_authority": True},
            APPROVAL,
        )


def test_invalid_decision_fails():
    with pytest.raises(HumanGateAuthenticityError):
        validate_human_gate_authenticity(
            {**DECISION, "decision": "execute"},
            APPROVAL,
        )
