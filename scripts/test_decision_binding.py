import pytest

from runtime.decision_binding import DecisionBindingError, validate_decision_binding


def _approval():
    return {
        "approval_id": "A1",
        "context_version": 10,
        "evidence_hash": "E10",
        "protocol_hash": "P10",
        "proposal_id": "PR10",
    }


def _execution():
    return {
        "approval_id": "A1",
        "context_version": 10,
        "evidence_hash": "E10",
        "protocol_hash": "P10",
        "proposal_id": "PR10",
        "runtime_authority": False,
    }


def test_exact_decision_binding_passes():
    validate_decision_binding(_approval(), _execution())


@pytest.mark.parametrize(
    "field,bad_value",
    [
        ("context_version", 11),
        ("evidence_hash", "E11"),
        ("protocol_hash", "P11"),
        ("proposal_id", "PR11"),
    ],
)
def test_scope_mismatch_is_rejected(field, bad_value):
    execution = _execution()
    execution[field] = bad_value
    with pytest.raises(DecisionBindingError, match="binding mismatch"):
        validate_decision_binding(_approval(), execution)


def test_missing_binding_is_rejected():
    execution = _execution()
    del execution["evidence_hash"]
    with pytest.raises(DecisionBindingError, match="missing binding"):
        validate_decision_binding(_approval(), execution)


def test_different_approval_is_rejected():
    execution = _execution()
    execution["approval_id"] = "A2"
    with pytest.raises(DecisionBindingError, match="different approval_id"):
        validate_decision_binding(_approval(), execution)


def test_runtime_authority_claim_is_rejected():
    execution = _execution()
    execution["runtime_authority"] = True
    with pytest.raises(DecisionBindingError, match="runtime authority"):
        validate_decision_binding(_approval(), execution)


def test_missing_approval_binding_fails_closed():
    approval = _approval()
    del approval["protocol_hash"]
    with pytest.raises(DecisionBindingError, match="approval missing binding"):
        validate_decision_binding(approval, _execution())
