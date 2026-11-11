import pytest

from runtime.human_decision_replay import (
    HumanDecisionReplayError,
    validate_decision_sequence,
    validate_human_decision_event,
)


def decision(i="D1", approval="A1"):
    return {
        "decision_id": i,
        "actor_type": "human",
        "decision": "approve",
        "human_approval": True,
        "runtime_authority": False,
        "approval_id": approval,
        "context_version": "C1",
        "evidence_hash": "E1",
        "protocol_hash": "P1",
        "proposal_id": "PR1",
    }


def test_valid_decision():
    validate_human_decision_event(decision())


def test_duplicate_decision_id_is_replay():
    with pytest.raises(HumanDecisionReplayError):
        validate_decision_sequence([decision("D1"), decision("D1")])


def test_previously_seen_decision_is_rejected():
    with pytest.raises(HumanDecisionReplayError):
        validate_human_decision_event(
            decision("D1"), seen_decision_ids=frozenset({"D1"})
        )


def test_replayed_decision_with_different_approval_id_still_fails():
    with pytest.raises(HumanDecisionReplayError):
        validate_decision_sequence([decision("D1", "A1"), decision("D1", "A2")])


def test_runtime_cannot_replay_as_human():
    with pytest.raises(HumanDecisionReplayError):
        validate_human_decision_event({**decision(), "actor_type": "runtime"})


def test_missing_binding_fails_closed():
    with pytest.raises(HumanDecisionReplayError):
        validate_human_decision_event({**decision(), "evidence_hash": ""})


def test_runtime_authority_claim_fails():
    with pytest.raises(HumanDecisionReplayError):
        validate_human_decision_event({**decision(), "runtime_authority": True})
