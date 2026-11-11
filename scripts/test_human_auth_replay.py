import pytest

from runtime.human_auth_replay import HumanAuthReplayError, validate_human_auth_for_decision


IDENTITY = {
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "actor_type": "human",
    "authenticated": True,
    "authentication_method": "test-auth",
}

DECISION = {
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "human_approval": True,
    "runtime_authority": False,
}


def test_authenticated_session_passes():
    validate_human_auth_for_decision(IDENTITY, DECISION)


def test_authentication_replay_fails():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            IDENTITY, DECISION, seen_authentication_ids=frozenset({"AUTH1"})
        )


def test_revoked_authentication_fails():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            IDENTITY, DECISION, current_revoked_authentications=frozenset({"AUTH1"})
        )


def test_principal_substitution_fails():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            IDENTITY, {**DECISION, "principal_id": "H2"}
        )


def test_authentication_substitution_fails():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            IDENTITY, {**DECISION, "authentication_id": "AUTH2"}
        )


def test_runtime_cannot_use_human_auth():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            {**IDENTITY, "actor_type": "runtime"}, DECISION
        )


def test_runtime_authority_claim_fails():
    with pytest.raises(HumanAuthReplayError):
        validate_human_auth_for_decision(
            IDENTITY, {**DECISION, "runtime_authority": True}
        )
