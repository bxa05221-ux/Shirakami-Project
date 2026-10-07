import pytest

from runtime.full_system_authority import (
    FullSystemAuthorityError,
    validate_full_system_authority,
)
from runtime.human_decision_signature import sign_human_decision
from runtime.verification_forgery import verification_digest

SECRET = b"system-secret"

DECISION = {
    "decision_id": "D1",
    "approval_id": "A1",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "key_id": "K1",
    "decision": "approve",
    "actor_type": "human",
    "human_approval": True,
    "runtime_authority": False,
}

IDENTITY = {
    "key_id": "K1",
    **{k: DECISION[k] for k in (
        "decision_id", "approval_id", "context_version",
        "evidence_hash", "protocol_hash", "proposal_id",
    )},
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "actor_type": "human",
    "authenticated": True,
    "authentication_method": "test",
}

APPROVAL = {
    **{k: DECISION[k] for k in (
        "approval_id", "context_version", "evidence_hash",
        "protocol_hash", "proposal_id",
    )},
    "verifier": "v1",
    "human_approval": True,
}

EXECUTION = {
    **{k: DECISION[k] for k in (
        "approval_id", "context_version", "evidence_hash",
        "protocol_hash", "proposal_id",
    )},
    "runtime_authority": False,
}

PERSISTED = {
    "decision_id": "D1",
    **APPROVAL,
    "principal_id": "H1",
    "authentication_id": "AUTH1",
    "key_id": "K1",
    "human_approval": True,
    "runtime_authority": False,
}

UI = {
    **{k: DECISION[k] for k in (
        "decision_id", "approval_id", "context_version",
        "evidence_hash", "protocol_hash", "proposal_id",
    )},
    "event_type": "human_interaction",
    "action": "approve",
    "synthetic": False,
    "runtime_generated": False,
    "actor_type": "human",
    "human_approval": True,
}

VERIFICATION = {
    "verification_id": "V1",
    "target_id": "T1",
    "result": "pass",
    "context_version": "C1",
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "verifier": "v1",
    "verifier_instance": "v1-i1",
    "verification_time": "2026-10-07T10:04:00+00:00",
}

EVENTS = [
    {"event_id": "obs-1", "event_type": "observation", "target_id": "T1",
     "occurred_at": "2026-10-07T10:00:00+00:00"},
    {"event_id": "evidence-1", "event_type": "evidence", "evidence_hash": "E1", "context_version": "C1", "occurred_at": "2026-10-07T10:02:00+00:00", "parent_event_id": "obs-1"},
    {"event_id": "proposal-1", "event_type": "proposal", "proposal_id": "PR1", "protocol_hash": "P1", "context_version": "C1", "evidence_hash": "E1", "occurred_at": "2026-10-07T10:04:30+00:00", "parent_event_id": "protocol-1"},
    {"event_id": "protocol-1", "event_type": "protocol", "protocol_hash": "P1", "context_version": "C1", "evidence_hash": "E1", "occurred_at": "2026-10-07T10:03:00+00:00", "parent_event_id": "evidence-1"},
    {"event_id": "verification-1", "event_type": "verification",
     "verification_id": "V1",
     "occurred_at": "2026-10-07T10:04:00+00:00",
     "parent_event_id": "obs-1"},
    {"event_id": "decision-1", "event_type": "human_decision",
     "decision_id": "D1", "proposal_id": "PR1",
     "occurred_at": "2026-10-07T10:05:00+00:00",
     "parent_event_id": "verification-1"},
    {"event_id": "approval-1", "event_type": "human_approval",
     "approval_id": "A1", "context_version": "C1",
     "evidence_hash": "E1", "protocol_hash": "P1", "proposal_id": "PR1",
     "occurred_at": "2026-10-07T10:05:00+00:00",
     "parent_event_id": "decision-1"},
    {"event_id": "exec-1", "event_type": "execution",
     "approval_id": "A1", "context_version": "C1",
     "evidence_hash": "E1", "protocol_hash": "P1", "proposal_id": "PR1",
     "occurred_at": "2026-10-07T10:06:00+00:00",
     "parent_event_id": "approval-1"},
]


def replace_event(events, event_type, **changes):
    result = [dict(event) for event in events]
    for index, event in enumerate(result):
        if event.get("event_type") == event_type:
            result[index] = {**event, **changes}
            return result
    raise AssertionError(f"event type not found: {event_type}")


def call(**overrides):
    data = {
        "events": EVENTS,
        "approval": APPROVAL,
        "execution": EXECUTION,
        "verification": VERIFICATION,
        "verification_digest": verification_digest(VERIFICATION),
        "persisted": PERSISTED,
        "ui_event": UI,
        "identity": IDENTITY,
        "decision": DECISION,
        "signature": sign_human_decision(DECISION, SECRET),
        "secret": SECRET,
        "decision_time": "2026-10-07T10:05:00+00:00",
        "trusted_principals": frozenset({"H1"}),
        "trusted_verifiers": frozenset({"v1"}),
        "trusted_keys": frozenset({"K1"}),
        "trusted_from": "2026-10-01T00:00:00+00:00",
        "verifier_revoked_at": frozenset(),
    }
    data.update(overrides)
    return validate_full_system_authority(**data)


def test_complete_system_chain_passes():
    call()


@pytest.mark.parametrize("field", [
    "context_version", "evidence_hash", "protocol_hash", "proposal_id",
])
def test_cross_layer_substitution_blocks(field):
    bad = {**APPROVAL, field: "OTHER"}
    with pytest.raises(FullSystemAuthorityError):
        call(approval=bad)


def test_verification_mutation_with_original_digest_blocks():
    bad = {**VERIFICATION, "result": "fail"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_verifier_substitution_blocks():
    bad = {**VERIFICATION, "verifier": "v2"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_human_decision_from_other_context_blocks():
    bad = {**DECISION, "context_version": "C2"}
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad)


def test_fixed_human_signature_rejects_decision_mutation():
    bad = {**DECISION, "proposal_id": "OTHER"}
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad, signature=sign_human_decision(DECISION, SECRET))


def test_persisted_recovery_substitution_blocks():
    bad = {**PERSISTED, "proposal_id": "OTHER"}
    with pytest.raises(FullSystemAuthorityError):
        call(persisted=bad)


def test_runtime_authority_cannot_cross_complete_chain():
    bad = {**EXECUTION, "runtime_authority": True}
    with pytest.raises(FullSystemAuthorityError):
        call(execution=bad)


def test_revoked_verifier_cannot_restore_authority():
    with pytest.raises(FullSystemAuthorityError):
        call(verifier_revoked_at=frozenset({"v1"}))


def test_future_verification_relative_to_decision_blocks():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "verification", occurred_at="2026-10-07T10:06:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_execution_before_approval_blocks_full_system():
    bad = [dict(e) for e in EVENTS]
    bad[-1] = {**bad[-1], "occurred_at": "2026-10-07T10:04:30+00:00"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_decision_from_wrong_temporal_position_blocks():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "human_decision", occurred_at="2026-10-07T10:03:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_missing_verification_event_blocks():
    bad = [e for e in EVENTS if e["event_type"] != "verification"]
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_approval_event_context_substitution_blocks():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "human_approval", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_execution_event_approval_substitution_blocks():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "execution", approval_id="OTHER")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_execution_event_evidence_substitution_blocks():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "execution", evidence_hash="OTHER")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

@pytest.mark.parametrize("field", [
    "context_version", "evidence_hash", "protocol_hash", "proposal_id",
])
def test_verification_semantic_substitution_blocks(field):
    bad = {**VERIFICATION, field: "OTHER"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_verification_missing_semantic_binding_blocks():
    bad = {k: v for k, v in VERIFICATION.items() if k != "evidence_hash"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)

def test_valid_verification_cannot_be_rebound_to_other_decision():
    bad = {**DECISION, "decision_id": "D2", "approval_id": "A2"}
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad)


def test_valid_verification_cannot_be_rebound_to_other_context():
    bad = {**DECISION, "context_version": "C2"}
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad)


def test_verification_event_cannot_be_rebound_to_other_verification():
    bad = [dict(e) for e in EVENTS]
    bad = replace_event(bad, "verification", verification_id="V2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_verification_target_substitution_blocks():
    bad = {**VERIFICATION, "target_id": "T2"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_observation_target_substitution_blocks():
    bad = [dict(e) for e in EVENTS]
    bad[0] = {**bad[0], "target_id": "T2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_evidence_provenance_substitution_blocks():
    bad = [dict(e) for e in EVENTS]
    for index, event in enumerate(bad):
        if event.get("event_type") == "evidence":
            bad[index] = {**event, "evidence_hash": "E2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_evidence_from_other_observation_blocks():
    bad = [dict(e) for e in EVENTS]
    bad.append({
        "event_id": "obs-2", "event_type": "observation",
        "target_id": "T2", "occurred_at": "2026-10-07T10:01:00+00:00",
    })
    for index, event in enumerate(bad):
        if event.get("event_type") == "evidence":
            bad[index] = {**event, "parent_event_id": "obs-2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_evidence_context_substitution_blocks():
    bad = replace_event(EVENTS, "evidence", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_evidence_hash_cannot_be_rebound_to_other_context():
    bad = {**VERIFICATION, "context_version": "C2"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_protocol_context_substitution_blocks():
    bad = replace_event(EVENTS, "protocol", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_protocol_evidence_substitution_blocks():
    bad = replace_event(EVENTS, "protocol", evidence_hash="E2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_protocol_hash_substitution_blocks():
    bad = {**VERIFICATION, "protocol_hash": "P2"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)

def test_proposal_protocol_substitution_blocks():
    bad = replace_event(EVENTS, "proposal", protocol_hash="P2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_context_substitution_blocks():
    bad = replace_event(EVENTS, "proposal", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_evidence_substitution_blocks():
    bad = replace_event(EVENTS, "proposal", evidence_hash="E2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_id_cannot_be_rebound():
    bad = {**VERIFICATION, "proposal_id": "PR2"}
    with pytest.raises(FullSystemAuthorityError):
        call(verification=bad)


def test_human_decision_cannot_switch_verified_proposal():
    bad = replace_event(EVENTS, "human_decision", proposal_id="PR2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_decision_proposal_binding_mutation_blocks():
    bad = {**DECISION, "proposal_id": "PR2"}
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad)


def test_approval_proposal_binding_mutation_blocks():
    bad = {**APPROVAL, "proposal_id": "PR2"}
    with pytest.raises(FullSystemAuthorityError):
        call(approval=bad)


def test_execution_proposal_binding_mutation_blocks():
    bad = {**EXECUTION, "proposal_id": "PR2"}
    with pytest.raises(FullSystemAuthorityError):
        call(execution=bad)


def test_proposal_after_human_decision_blocks():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:06:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_before_human_decision_is_required():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:04:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_predating_verification_blocks():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:03:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_verification_before_proposal_is_required():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:04:30+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_evidence_after_verification_blocks():
    bad = replace_event(EVENTS, "evidence", occurred_at="2026-10-07T10:05:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_evidence_before_verification_is_required():
    bad = replace_event(EVENTS, "evidence", occurred_at="2026-10-07T10:03:30+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_evidence_before_observation_blocks():
    bad = replace_event(EVENTS, "evidence", occurred_at="2026-10-07T09:59:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_observation_before_evidence_is_required():
    bad = replace_event(EVENTS, "observation", occurred_at="2026-10-07T10:02:30+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)
