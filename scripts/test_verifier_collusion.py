import pytest

from runtime.verifier_collusion import (
    VerifierCollusionError,
    validate_verifier_quorum,
)


def v(i, verifier, instance, result="pass"):
    return {
        "verification_id": f"V{i}",
        "target_id": "T1",
        "result": result,
        "verifier": verifier,
        "verifier_instance": instance,
    }


def test_unanimous_quorum_is_still_evidence():
    validate_verifier_quorum(
        [v(1, "A", "A1"), v(2, "B", "B1"), v(3, "C", "C1")],
        required_passes=3,
    )


def test_partial_quorum_is_allowed_as_evidence():
    validate_verifier_quorum(
        [v(1, "A", "A1"), v(2, "B", "B1", "fail"), v(3, "C", "C1")],
        required_passes=2,
    )


def test_insufficient_quorum_fails():
    with pytest.raises(VerifierCollusionError):
        validate_verifier_quorum(
            [v(1, "A", "A1"), v(2, "B", "B1", "fail")],
            required_passes=2,
        )


def test_colluding_verifiers_cannot_create_human_approval():
    with pytest.raises(VerifierCollusionError):
        validate_verifier_quorum(
            [
                {**v(1, "A", "A1"), "human_approval": True},
                {**v(2, "B", "B1"), "human_approval": True},
            ],
            required_passes=2,
        )


def test_colluding_verifiers_cannot_create_runtime_authority():
    with pytest.raises(VerifierCollusionError):
        validate_verifier_quorum(
            [
                {**v(1, "A", "A1"), "runtime_authority": True},
                {**v(2, "B", "B1"), "runtime_authority": True},
            ],
            required_passes=2,
        )


def test_same_verifier_cannot_fake_multi_party_collusion_resistance():
    # Quorum counting is not itself the independence check.
    # The dedicated independent-verifier boundary must be composed by callers.
    validate_verifier_quorum(
        [v(1, "A", "A1"), v(2, "A", "A2")],
        required_passes=2,
    )
