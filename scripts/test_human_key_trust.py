import pytest

from runtime.human_key_trust import HumanKeyTrustError, validate_human_key_trust


DECISION = {
    "principal_id": "H1",
    "key_id": "KEY1",
    "actor_type": "human",
    "human_approval": True,
    "runtime_authority": False,
}


def test_trusted_key_passes():
    validate_human_key_trust(
        DECISION,
        trusted_principals=frozenset({"H1"}),
        trusted_keys=frozenset({"KEY1"}),
    )


def test_untrusted_principal_fails():
    with pytest.raises(HumanKeyTrustError):
        validate_human_key_trust(
            DECISION,
            trusted_principals=frozenset({"H2"}),
            trusted_keys=frozenset({"KEY1"}),
        )


def test_untrusted_key_fails():
    with pytest.raises(HumanKeyTrustError):
        validate_human_key_trust(
            DECISION,
            trusted_principals=frozenset({"H1"}),
            trusted_keys=frozenset({"KEY2"}),
        )


def test_revoked_key_fails():
    with pytest.raises(HumanKeyTrustError):
        validate_human_key_trust(
            DECISION,
            trusted_principals=frozenset({"H1"}),
            trusted_keys=frozenset({"KEY1"}),
            revoked_keys=frozenset({"KEY1"}),
        )


def test_key_substitution_requires_trust():
    with pytest.raises(HumanKeyTrustError):
        validate_human_key_trust(
            {**DECISION, "key_id": "KEY2"},
            trusted_principals=frozenset({"H1"}),
            trusted_keys=frozenset({"KEY1"}),
        )


def test_runtime_authority_claim_fails():
    with pytest.raises(HumanKeyTrustError):
        validate_human_key_trust(
            {**DECISION, "runtime_authority": True},
            trusted_principals=frozenset({"H1"}),
            trusted_keys=frozenset({"KEY1"}),
        )
