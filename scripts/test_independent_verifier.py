import pytest

from runtime.independent_verifier import (
    IndependentVerifierError,
    validate_independent_verifiers,
)

BASE = {
    "target_id": "T1",
    "result": "pass",
}

def v(vid, verifier, instance):
    return {
        **BASE,
        "verification_id": vid,
        "verifier": verifier,
        "verifier_instance": instance,
    }


def test_two_independent_passes_are_evidence():
    validate_independent_verifiers(
        [v("V1", "A", "A1"), v("V2", "B", "B1")]
    )


def test_single_verifier_cannot_satisfy_independence():
    with pytest.raises(IndependentVerifierError):
        validate_independent_verifiers([v("V1", "A", "A1")])


def test_duplicate_verifier_instance_fails():
    with pytest.raises(IndependentVerifierError):
        validate_independent_verifiers(
            [v("V1", "A", "A1"), v("V2", "A", "A1")]
        )


def test_different_instances_of_same_verifier_are_not_independent():
    with pytest.raises(IndependentVerifierError):
        validate_independent_verifiers(
            [v("V1", "A", "A1"), v("V2", "A", "A2")]
        )


def test_disagreement_is_not_authority():
    validate_independent_verifiers(
        [v("V1", "A", "A1"), {**v("V2", "B", "B1"), "result": "fail"}]
    )


def test_consensus_cannot_create_human_approval():
    bad = {**v("V1", "A", "A1"), "human_approval": True}
    with pytest.raises(IndependentVerifierError):
        validate_independent_verifiers([bad, v("V2", "B", "B1")])


def test_consensus_cannot_create_runtime_authority():
    bad = {**v("V1", "A", "A1"), "runtime_authority": True}
    with pytest.raises(IndependentVerifierError):
        validate_independent_verifiers([bad, v("V2", "B", "B1")])
