import pytest

from runtime.human_decision_signature import (
    HumanDecisionSignatureError,
    sign_human_decision,
    validate_human_decision_signature,
)


SECRET = b"test-only-human-gate-secret"

DECISION = {
    "decision_id": "D1",
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "decision": "approve",
    "actor_type": "human",
    "human_approval": True,
    "runtime_authority": False,
}


def test_valid_signature_passes():
    signature = sign_human_decision(DECISION, SECRET)
    validate_human_decision_signature(DECISION, signature, SECRET)


@pytest.mark.parametrize("field", (
    "decision_id", "approval_id", "context_version", "evidence_hash",
    "protocol_hash", "proposal_id", "principal_id", "authentication_id",
    "decision",
))
def test_bound_field_mutation_fails(field):
    signature = sign_human_decision(DECISION, SECRET)
    mutated = {**DECISION, field: "ATTACK"}
    with pytest.raises(HumanDecisionSignatureError):
        validate_human_decision_signature(mutated, signature, SECRET)


def test_wrong_secret_fails():
    signature = sign_human_decision(DECISION, SECRET)
    with pytest.raises(HumanDecisionSignatureError):
        validate_human_decision_signature(DECISION, signature, b"wrong-secret")


def test_signature_substitution_fails():
    with pytest.raises(HumanDecisionSignatureError):
        validate_human_decision_signature(DECISION, "00" * 32, SECRET)


def test_runtime_authority_claim_fails_even_with_valid_signature():
    mutated = {**DECISION, "runtime_authority": True}
    signature = sign_human_decision(mutated, SECRET)
    with pytest.raises(HumanDecisionSignatureError):
        validate_human_decision_signature(mutated, signature, SECRET)
