import pytest

from runtime.human_identity_auth import HumanIdentityAuthError, validate_authenticated_human_decision


BINDINGS = {
    "decision_id": "D1",
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
}

IDENTITY = {
    **BINDINGS,
    "principal_id": "HUMAN-001",
    "authentication_id": "AUTH-001",
    "actor_type": "human",
    "authenticated": True,
    "authentication_method": "test-auth",
}

DECISION = {
    **BINDINGS,
    "principal_id": "HUMAN-001",
    "authentication_id": "AUTH-001",
    "actor_type": "human",
    "human_approval": True,
    "runtime_authority": False,
}


def test_authenticated_human_decision_passes():
    validate_authenticated_human_decision(IDENTITY, DECISION)


@pytest.mark.parametrize("field", BINDINGS)
def test_identity_binding_mutation_fails(field):
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            {**IDENTITY, field: "ATTACK"}, DECISION
        )


def test_unauthenticated_human_fails():
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            {**IDENTITY, "authenticated": False}, DECISION
        )


def test_runtime_cannot_claim_human_identity():
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            {**IDENTITY, "actor_type": "runtime"}, DECISION
        )


def test_principal_substitution_fails():
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            IDENTITY, {**DECISION, "principal_id": "HUMAN-ATTACK"}
        )


def test_authentication_substitution_fails():
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            IDENTITY, {**DECISION, "authentication_id": "AUTH-ATTACK"}
        )


def test_runtime_authority_claim_fails():
    with pytest.raises(HumanIdentityAuthError):
        validate_authenticated_human_decision(
            IDENTITY, {**DECISION, "runtime_authority": True}
        )
