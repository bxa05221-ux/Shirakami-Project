import pytest

from runtime.ui_adapter_gate import UIAdapterGateError, validate_ui_adapter_decision


BINDINGS = {
    "decision_id": "D1",
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
}

DECISION = {
    **BINDINGS,
    "actor_type": "human",
    "decision": "approve",
    "human_approval": True,
    "runtime_authority": False,
}

UI = {
    **BINDINGS,
    "event_type": "human_interaction",
    "actor_type": "human",
    "action": "approve",
    "synthetic": False,
    "runtime_generated": False,
    "human_approval": True,
}


def test_real_human_ui_event_passes():
    validate_ui_adapter_decision(UI, DECISION)


@pytest.mark.parametrize("field", BINDINGS)
def test_ui_binding_mutation_fails(field):
    mutated = {**UI, field: "ATTACK"}
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision(mutated, DECISION)


def test_synthetic_ui_event_cannot_authorize():
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision({**UI, "synthetic": True}, DECISION)


def test_runtime_generated_ui_event_cannot_authorize():
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision({**UI, "runtime_generated": True}, DECISION)


def test_non_human_actor_cannot_claim_ui_approval():
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision({**UI, "actor_type": "runtime"}, DECISION)


def test_ui_action_must_match_decision():
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision({**UI, "action": "reject"}, DECISION)


def test_runtime_authority_cannot_cross_ui_boundary():
    with pytest.raises(UIAdapterGateError):
        validate_ui_adapter_decision(UI, {**DECISION, "runtime_authority": True})
