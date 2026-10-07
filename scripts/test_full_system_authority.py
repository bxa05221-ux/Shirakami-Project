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


def test_unrelated_historical_observation_can_coexist():
    competing = {
        "event_id": "obs-history",
        "event_type": "observation",
        "target_id": "T2",
        "occurred_at": "2026-10-07T09:00:00+00:00",
    }
    call(events=[*EVENTS, competing])


def test_unrelated_historical_evidence_can_coexist():
    competing = {
        "event_id": "evidence-history",
        "event_type": "evidence",
        "evidence_hash": "E-history",
        "context_version": "C0",
        "occurred_at": "2026-10-07T09:05:00+00:00",
        "parent_event_id": "obs-history",
    }
    observation = {
        "event_id": "obs-history",
        "event_type": "observation",
        "target_id": "T2",
        "occurred_at": "2026-10-07T09:00:00+00:00",
    }
    call(events=[*EVENTS, observation, competing])


def test_unrelated_historical_proposal_can_coexist():
    competing = {
        "event_id": "proposal-history",
        "event_type": "proposal",
        "proposal_id": "PR-history",
        "protocol_hash": "P-history",
        "context_version": "C0",
        "evidence_hash": "E-history",
        "occurred_at": "2026-10-07T09:10:00+00:00",
        "parent_event_id": "protocol-history",
    }
    protocol = {
        "event_id": "protocol-history",
        "event_type": "protocol",
        "protocol_hash": "P-history",
        "context_version": "C0",
        "evidence_hash": "E-history",
        "occurred_at": "2026-10-07T09:07:00+00:00",
        "parent_event_id": "evidence-history",
    }
    evidence = {
        "event_id": "evidence-history",
        "event_type": "evidence",
        "evidence_hash": "E-history",
        "context_version": "C0",
        "occurred_at": "2026-10-07T09:05:00+00:00",
        "parent_event_id": "obs-history",
    }
    observation = {
        "event_id": "obs-history",
        "event_type": "observation",
        "target_id": "T2",
        "occurred_at": "2026-10-07T09:00:00+00:00",
    }
    call(events=[*EVENTS, observation, evidence, protocol, competing])


def test_competing_current_proposal_identity_blocks_authority():
    competing = {
        "event_id": "proposal-2",
        "event_type": "proposal",
        "proposal_id": "PR1",
        "protocol_hash": "P1",
        "context_version": "C1",
        "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:40+00:00",
        "parent_event_id": "protocol-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])


def test_competing_parent_with_same_semantic_identity_is_rejected():
    mutations = [
        (
            "evidence",
            "evidence-2",
            "obs-1",
            {"evidence_hash": EVENTS[1]["evidence_hash"], "context_version": "C1"},
        ),
        (
            "protocol",
            "protocol-2",
            "evidence-1",
            {
                "protocol_hash": EVENTS[2]["protocol_hash"],
                "context_version": "C1",
                "evidence_hash": "E1",
            },
        ),
        (
            "proposal",
            "proposal-2",
            "protocol-1",
            {
                "proposal_id": EVENTS[2]["proposal_id"],
                "protocol_hash": "P1",
                "context_version": "C1",
                "evidence_hash": "E1",
            },
        ),
        (
            "verification",
            "verification-2",
            "obs-1",
            {"verification_id": VERIFICATION["verification_id"], "target_id": "T1"},
        ),
        (
            "human_decision",
            "decision-2",
            "verification-1",
            {"decision_id": DECISION["decision_id"], "proposal_id": "PR1"},
        ),
        (
            "human_approval",
            "approval-2",
            "decision-1",
            {
                "approval_id": APPROVAL["approval_id"],
                "context_version": "C1",
                "evidence_hash": "E1",
                "protocol_hash": "P1",
                "proposal_id": "PR1",
            },
        ),
        (
            "execution",
            "execution-2",
            "approval-1",
            {
                "approval_id": EXECUTION["approval_id"],
                "context_version": "C1",
                "evidence_hash": "E1",
                "protocol_hash": "P1",
                "proposal_id": "PR1",
            },
        ),
    ]
    for event_type, event_id, parent_id, fields in mutations:
        competing = {
            "event_id": event_id,
            "event_type": event_type,
            "occurred_at": "2026-10-07T10:06:30+00:00",
            "parent_event_id": parent_id,
            **fields,
        }
        with pytest.raises(FullSystemAuthorityError):
            call(events=[*EVENTS, competing])


def test_competing_parent_cannot_be_smuggled_through_valid_timestamps():
    competing = {
        "event_id": "proposal-time-valid-substitute",
        "event_type": "proposal",
        "proposal_id": "PR1",
        "protocol_hash": "P1",
        "context_version": "C1",
        "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:40+00:00",
        "parent_event_id": "protocol-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])

def test_cross_layer_single_sided_mutation_matrix():
    cases = [
        ("verification", {"evidence_hash": "E-MUT"}),
        ("decision", {"proposal_id": "PR-MUT"}),
        ("approval", {"protocol_hash": "P-MUT"}),
        ("execution", {"approval_id": "A-MUT"}),
        ("identity", {"principal_id": "H-MUT"}),
        ("ui_event", {"decision_id": "D-MUT"}),
        ("persisted", {"context_version": "C-MUT"}),
    ]
    for artifact, changes in cases:
        kwargs = {}
        if artifact == "verification":
            value = dict(VERIFICATION); value.update(changes); kwargs["verification"] = value
        elif artifact == "decision":
            value = dict(DECISION); value.update(changes); kwargs["decision"] = value
        elif artifact == "approval":
            value = dict(APPROVAL); value.update(changes); kwargs["approval"] = value
        elif artifact == "execution":
            value = dict(EXECUTION); value.update(changes); kwargs["execution"] = value
        elif artifact == "identity":
            value = dict(IDENTITY); value.update(changes); kwargs["identity"] = value
        elif artifact == "ui_event":
            value = dict(UI); value.update(changes); kwargs["ui_event"] = value
        else:
            value = dict(PERSISTED); value.update(changes); kwargs["persisted"] = value
        with pytest.raises(FullSystemAuthorityError):
            call(**kwargs)


def test_cross_layer_dual_mutation_cannot_restore_authority():
    paired = [
        (dict(VERIFICATION, evidence_hash="E-MUT"), dict(DECISION, evidence_hash="E-MUT")),
        (dict(VERIFICATION, proposal_id="PR-MUT"), dict(APPROVAL, proposal_id="PR-MUT")),
        (dict(DECISION, context_version="C-MUT"), dict(EXECUTION, context_version="C-MUT")),
        (dict(APPROVAL, protocol_hash="P-MUT"), dict(EXECUTION, protocol_hash="P-MUT")),
    ]
    for verification, decision_or_approval in paired:
        kwargs = {"verification": verification}
        if decision_or_approval.get("decision_id"):
            kwargs["decision"] = decision_or_approval
        else:
            kwargs["approval"] = decision_or_approval
        with pytest.raises(FullSystemAuthorityError):
            call(**kwargs)


def test_cross_layer_mutation_cannot_be_hidden_by_unchanged_human_gate():
    verification = dict(VERIFICATION, context_version="C-MUT")
    decision = dict(DECISION)
    approval = dict(APPROVAL)
    execution = dict(EXECUTION)
    with pytest.raises(FullSystemAuthorityError):
        call(verification=verification, decision=decision, approval=approval, execution=execution)


def test_authority_chain_single_field_mutation_matrix():
    mutations = [
        ("verification_id", "V-MUT"),
        ("target_id", "T-MUT"),
        ("context_version", "C-MUT"),
        ("evidence_hash", "E-MUT"),
        ("protocol_hash", "P-MUT"),
        ("proposal_id", "PR-MUT"),
        ("verifier", "v-MUT"),
        ("verifier_instance", "v-i-MUT"),
    ]
    for field, value in mutations:
        verification = dict(VERIFICATION)
        verification[field] = value
        with pytest.raises(FullSystemAuthorityError):
            call(verification=verification)


def test_authority_chain_human_binding_single_field_mutation_matrix():
    mutations = [
        ("decision_id", "D-MUT"),
        ("approval_id", "A-MUT"),
        ("context_version", "C-MUT"),
        ("evidence_hash", "E-MUT"),
        ("protocol_hash", "P-MUT"),
        ("proposal_id", "PR-MUT"),
        ("principal_id", "H-MUT"),
        ("authentication_id", "AUTH-MUT"),
        ("key_id", "K-MUT"),
    ]
    for field, value in mutations:
        decision = dict(DECISION)
        decision[field] = value
        with pytest.raises(FullSystemAuthorityError):
            call(decision=decision)


def test_authority_chain_execution_binding_single_field_mutation_matrix():
    mutations = [
        ("approval_id", "A-MUT"),
        ("context_version", "C-MUT"),
        ("evidence_hash", "E-MUT"),
        ("protocol_hash", "P-MUT"),
        ("proposal_id", "PR-MUT"),
    ]
    for field, value in mutations:
        execution = dict(EXECUTION)
        execution[field] = value
        with pytest.raises(FullSystemAuthorityError):
            call(execution=execution)


def test_multiple_composite_attacks_fail_closed_regardless_of_injection_order():
    attacks = [
        {
            "event_id": "attack-evidence",
            "event_type": "evidence",
            "evidence_hash": "E1",
            "context_version": "C1",
            "occurred_at": "2026-10-07T10:02:30+00:00",
            "parent_event_id": "obs-1",
        },
        {
            "event_id": "attack-proposal",
            "event_type": "proposal",
            "proposal_id": "PR1",
            "protocol_hash": "P1",
            "context_version": "C1",
            "evidence_hash": "E1",
            "occurred_at": "2026-10-07T10:04:40+00:00",
            "parent_event_id": "protocol-1",
        },
        {
            "event_id": "attack-decision",
            "event_type": "human_decision",
            "decision_id": "D1",
            "proposal_id": "PR1",
            "occurred_at": "2026-10-07T10:05:10+00:00",
            "parent_event_id": "verification-1",
        },
        {
            "event_id": "attack-execution",
            "event_type": "execution",
            "approval_id": "A1",
            "context_version": "C1",
            "evidence_hash": "E1",
            "protocol_hash": "P1",
            "proposal_id": "PR1",
            "occurred_at": "2026-10-07T10:06:30+00:00",
            "parent_event_id": "approval-1",
        },
    ]
    orders = [
        attacks,
        list(reversed(attacks)),
        [attacks[1], attacks[3], attacks[0], attacks[2]],
    ]
    for injected in orders:
        with pytest.raises(FullSystemAuthorityError):
            call(events=[*EVENTS, *injected])


def test_invalid_history_cannot_turn_into_authority_by_being_appended_last():
    valid_history = {
        "event_id": "history-valid",
        "event_type": "observation",
        "target_id": "T2",
        "occurred_at": "2026-10-07T08:00:00+00:00",
    }
    attack = {
        "event_id": "late-attack",
        "event_type": "proposal",
        "proposal_id": "PR1",
        "protocol_hash": "P1",
        "context_version": "C1",
        "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:40+00:00",
        "parent_event_id": "protocol-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, valid_history, attack])



def test_same_semantic_identity_is_not_history_even_with_different_event_id():
    mutations = [
        ("evidence", "evidence_hash", EVENTS[1]["evidence_hash"]),
        ("protocol", "protocol_hash", EVENTS[2]["protocol_hash"]),
        ("proposal", "proposal_id", EVENTS[3].get("proposal_id", "PR1")),
        ("verification", "verification_id", VERIFICATION["verification_id"]),
        ("human_decision", "decision_id", DECISION["decision_id"]),
        ("human_approval", "approval_id", APPROVAL["approval_id"]),
        ("execution", "approval_id", EXECUTION["approval_id"]),
    ]
    for event_type, field, value in mutations:
        competing = {"event_id": f"duplicate-{event_type}", "event_type": event_type, field: value}
        with pytest.raises(FullSystemAuthorityError):
            call(events=[*EVENTS, competing])


def test_unrelated_history_does_not_change_selected_authority_identity():
    history = {
        "event_id": "obs-unrelated",
        "event_type": "observation",
        "target_id": "T99",
        "occurred_at": "2026-10-07T06:00:00+00:00",
    }
    result = call(events=[*EVENTS, history])
    assert result is None


def test_historical_candidates_can_coexist_with_selected_authority_chain():
    history = [
        {
            "event_id": "obs-history-2",
            "event_type": "observation",
            "target_id": "T2",
            "occurred_at": "2026-10-07T08:00:00+00:00",
        },
        {
            "event_id": "evidence-history-2",
            "event_type": "evidence",
            "evidence_hash": "E-history-2",
            "context_version": "C0",
            "occurred_at": "2026-10-07T08:01:00+00:00",
            "parent_event_id": "obs-history-2",
        },
        {
            "event_id": "protocol-history-2",
            "event_type": "protocol",
            "protocol_hash": "P-history-2",
            "context_version": "C0",
            "evidence_hash": "E-history-2",
            "occurred_at": "2026-10-07T08:02:00+00:00",
            "parent_event_id": "evidence-history-2",
        },
        {
            "event_id": "proposal-history-2",
            "event_type": "proposal",
            "proposal_id": "PR-history-2",
            "protocol_hash": "P-history-2",
            "context_version": "C0",
            "evidence_hash": "E-history-2",
            "occurred_at": "2026-10-07T08:03:00+00:00",
            "parent_event_id": "protocol-history-2",
        },
    ]
    call(events=[*EVENTS, *history])


def test_historical_observation_same_target_does_not_create_authority_ambiguity():
    history = {
        "event_id": "obs-history-3",
        "event_type": "observation",
        "target_id": EVENTS[0]["target_id"],
        "occurred_at": "2026-10-07T08:00:00+00:00",
    }
    call(events=[*EVENTS, history])


def test_historical_chain_with_different_semantic_ids_does_not_replace_selected_chain():
    history = [
        {
            "event_id": "obs-history-4",
            "event_type": "observation",
            "target_id": "T2",
            "occurred_at": "2026-10-07T07:00:00+00:00",
        },
        {
            "event_id": "evidence-history-4",
            "event_type": "evidence",
            "evidence_hash": "E4",
            "context_version": "C0",
            "occurred_at": "2026-10-07T07:01:00+00:00",
            "parent_event_id": "obs-history-4",
        },
        {
            "event_id": "protocol-history-4",
            "event_type": "protocol",
            "protocol_hash": "P4",
            "context_version": "C0",
            "evidence_hash": "E4",
            "occurred_at": "2026-10-07T07:02:00+00:00",
            "parent_event_id": "evidence-history-4",
        },
        {
            "event_id": "proposal-history-4",
            "event_type": "proposal",
            "proposal_id": "PR4",
            "protocol_hash": "P4",
            "context_version": "C0",
            "evidence_hash": "E4",
            "occurred_at": "2026-10-07T07:03:00+00:00",
            "parent_event_id": "protocol-history-4",
        },
        {
            "event_id": "verification-history-4",
            "event_type": "verification",
            "verification_id": "V4",
            "target_id": "T2",
            "occurred_at": "2026-10-07T07:04:00+00:00",
            "parent_event_id": "obs-history-4",
        },
    ]
    call(events=[*EVENTS, *history])


def test_competing_current_verification_identity_blocks_authority():
    competing = dict(VERIFICATION)
    competing["verification_id"] = VERIFICATION["verification_id"]
    competing["event_id"] = "verification-2"
    competing["parent_event_id"] = "obs-1"
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])


def test_competing_current_approval_identity_blocks_authority():
    competing = dict(APPROVAL)
    competing["approval_id"] = APPROVAL["approval_id"]
    competing["event_id"] = "approval-2"
    competing["parent_event_id"] = "decision-1"
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])


def test_competing_current_execution_identity_blocks_authority():
    competing = dict(EXECUTION)
    competing["approval_id"] = EXECUTION["approval_id"]
    competing["event_id"] = "execution-2"
    competing["parent_event_id"] = "approval-1"
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])


def test_competing_current_decision_identity_blocks_authority():
    competing = {
        "event_id": "decision-2",
        "event_type": "human_decision",
        "decision_id": "D1",
        "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:05:10+00:00",
        "parent_event_id": "verification-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing])


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
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:05:30+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_proposal_predating_verification_blocks():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:03:00+00:00")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_verification_before_proposal_is_required():
    bad = replace_event(EVENTS, "proposal", occurred_at="2026-10-07T10:03:30+00:00")
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


@pytest.mark.parametrize(("event_type", "occurred_at"), [
    ("observation", "2026-10-07T10:07:00+00:00"),
    ("evidence", "2026-10-07T10:07:00+00:00"),
    ("verification", "2026-10-07T10:07:00+00:00"),
    ("proposal", "2026-10-07T10:02:00+00:00"),
    ("human_decision", "2026-10-07T10:01:30+00:00"),
    ("human_approval", "2026-10-07T10:01:45+00:00"),
    ("execution", "2026-10-07T10:01:50+00:00"),
])
def test_temporal_permutation_blocks(event_type, occurred_at):
    bad = replace_event(EVENTS, event_type, occurred_at=occurred_at)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


@pytest.mark.parametrize(("event_type", "parent_event_id", "replacement"), [
    ("evidence", "protocol-1",
     {"event_id": "obs-2", "event_type": "observation", "target_id": "T1",
      "occurred_at": "2026-10-07T10:01:00+00:00"}),
    ("protocol", "proposal-1",
     {"event_id": "evidence-2", "event_type": "evidence", "evidence_hash": "E1",
      "context_version": "C1", "occurred_at": "2026-10-07T10:02:30+00:00",
      "parent_event_id": "obs-1"}),
    ("proposal", "evidence-1",
     {"event_id": "protocol-2", "event_type": "protocol", "protocol_hash": "P1",
      "context_version": "C1", "evidence_hash": "E1",
      "occurred_at": "2026-10-07T10:03:30+00:00", "parent_event_id": "evidence-1"}),
    ("verification", "protocol-1",
     {"event_id": "obs-2", "event_type": "observation", "target_id": "T1",
      "occurred_at": "2026-10-07T10:01:00+00:00"}),
    ("human_decision", "proposal-1",
     {"event_id": "verification-2", "event_type": "verification",
      "verification_id": "V2", "occurred_at": "2026-10-07T10:04:15+00:00",
      "parent_event_id": "obs-1"}),
    ("human_approval", "verification-1",
     {"event_id": "decision-2", "event_type": "human_decision",
      "decision_id": "D2", "proposal_id": "PR1",
      "occurred_at": "2026-10-07T10:05:30+00:00",
      "parent_event_id": "verification-1"}),
    ("execution", "decision-1",
     {"event_id": "approval-2", "event_type": "human_approval",
      "approval_id": "A2", "context_version": "C1", "evidence_hash": "E1",
      "protocol_hash": "P1", "proposal_id": "PR1",
      "occurred_at": "2026-10-07T10:05:30+00:00",
      "parent_event_id": "decision-1"}),
])
def test_authority_edge_cannot_follow_competing_parent(event_type, parent_event_id, replacement):
    bad = [dict(e) for e in EVENTS] + [dict(replacement)]
    bad = replace_event(bad, event_type, parent_event_id=parent_event_id)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_semantic_parent_rebinding_blocks(event_type, parent_event_id):
    bad = replace_event(EVENTS, event_type, parent_event_id=parent_event_id)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


@pytest.mark.parametrize(("event_type", "field", "value"), [
    ("protocol", "context_version", "C2"),
    ("protocol", "evidence_hash", "E2"),
    ("proposal", "protocol_hash", "P2"),
    ("proposal", "evidence_hash", "E2"),
    ("execution", "context_version", "C2"),
])
def test_parent_content_rebinding_blocks(event_type, field, value):
    bad = replace_event(EVENTS, event_type, **{field: value})
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


@pytest.mark.parametrize(("event_type", "parent_event_id", "occurred_at"), [
    ("evidence", "obs-1", "2026-10-07T09:59:00+00:00"),
    ("protocol", "evidence-1", "2026-10-07T10:01:00+00:00"),
    ("proposal", "protocol-1", "2026-10-07T10:02:00+00:00"),
    ("human_decision", "verification-1", "2026-10-07T10:03:00+00:00"),
    ("human_approval", "decision-1", "2026-10-07T10:04:00+00:00"),
    ("execution", "approval-1", "2026-10-07T10:04:30+00:00"),
])
def test_parent_future_timestamp_blocks(event_type, parent_event_id, occurred_at):
    bad = replace_event(EVENTS, event_type, parent_event_id=parent_event_id, occurred_at=occurred_at)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


@pytest.mark.parametrize(("event_type", "parent_event_id"), [
    ("observation", "obs-1"),
    ("evidence", "evidence-1"),
    ("protocol", "proposal-1"),
    ("human_decision", "decision-1"),
    ("human_approval", "approval-1"),
    ("execution", "exec-1"),
])
def test_event_graph_cycle_blocks(event_type, parent_event_id):
    bad = replace_event(EVENTS, event_type, parent_event_id=parent_event_id)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_duplicate_event_id_blocks():
    bad = list(EVENTS) + [dict(EVENTS[0])]
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_missing_event_id_blocks():
    bad = replace_event(EVENTS, "evidence", event_id=None)
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_semantic_duplicate_evidence_blocks():
    duplicate = dict(EVENTS[1])
    duplicate["event_id"] = "evidence-2"
    bad = list(EVENTS) + [duplicate]
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_duplicate_observation_target_is_allowed():
    duplicate = dict(EVENTS[0])
    duplicate["event_id"] = "obs-2"
    duplicate["occurred_at"] = "2026-10-07T10:01:00+00:00"
    call(events=list(EVENTS) + [duplicate])


def test_cross_chain_evidence_fork_cannot_enter_verified_chain():
    bad = list(EVENTS)
    bad.extend([
        {"event_id": "obs-2", "event_type": "observation", "target_id": "T2",
         "occurred_at": "2026-10-07T10:01:00+00:00"},
        {"event_id": "evidence-2", "event_type": "evidence",
         "evidence_hash": "E2", "context_version": "C2",
         "occurred_at": "2026-10-07T10:02:30+00:00",
         "parent_event_id": "obs-2"},
    ])
    bad = replace_event(bad, "protocol", evidence_hash="E2", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_disconnected_protocol_cannot_supply_verified_proposal():
    bad = list(EVENTS)
    bad.extend([
        {"event_id": "protocol-2", "event_type": "protocol",
         "protocol_hash": "P2", "context_version": "C2",
         "evidence_hash": "E2", "occurred_at": "2026-10-07T10:03:30+00:00",
         "parent_event_id": "evidence-2"},
        {"event_id": "evidence-2", "event_type": "evidence",
         "evidence_hash": "E2", "context_version": "C2",
         "occurred_at": "2026-10-07T10:02:30+00:00",
         "parent_event_id": "obs-2"},
        {"event_id": "obs-2", "event_type": "observation", "target_id": "T2",
         "occurred_at": "2026-10-07T10:01:00+00:00"},
    ])
    bad = replace_event(bad, "proposal", protocol_hash="P2",
                        evidence_hash="E2", context_version="C2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_forked_proposal_cannot_be_rebound_to_verified_proposal():
    bad = list(EVENTS)
    bad.append({
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:15+00:00",
        "parent_event_id": "protocol-1",
    })
    bad = replace_event(bad, "human_decision", proposal_id="PR2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_legitimate_proposal_fork_is_allowed_when_not_selected():
    fork = {
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:15+00:00",
        "parent_event_id": "protocol-1",
    }
    call(events=list(EVENTS) + [fork])


def test_unselected_proposal_cannot_inherit_selected_human_approval():
    fork = {
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:15+00:00",
        "parent_event_id": "protocol-1",
    }
    bad = list(EVENTS) + [fork]
    bad = replace_event(bad, "execution", proposal_id="PR2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)





def test_duplicate_selected_evidence_identity_is_rejected():
    duplicate = dict(EVENTS[1])
    duplicate["event_id"] = "evidence-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_selected_protocol_identity_is_rejected():
    duplicate = dict(EVENTS[2])
    duplicate["event_id"] = "protocol-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_selected_proposal_identity_is_rejected():
    duplicate = dict(EVENTS[3])
    duplicate["event_id"] = "proposal-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_decision_identity_is_rejected():
    duplicate = dict(EVENTS[5])
    duplicate["event_id"] = "decision-attack"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_selected_decision_identity_is_rejected():
    duplicate = dict(EVENTS[5])
    duplicate["event_id"] = "decision-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_human_decision_cannot_be_rebound_to_other_verification():
    bad = dict(EVENTS[5])
    bad["parent_event_id"] = "verification-2"
    competing = {
        "event_id": "verification-2",
        "event_type": "verification",
        "verification_id": "V2",
        "target_id": "T1",
        "result": "pass",
        "context_version": "C1",
        "evidence_hash": "E1",
        "protocol_hash": "P1",
        "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:04:30+00:00",
        "parent_event_id": "obs-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS[:-3], bad, competing, *EVENTS[-3:]], decision=bad)


def test_execution_cannot_be_rebound_to_approval_with_different_identity():
    bad = dict(EVENTS[7])
    bad["parent_event_id"] = "approval-2"
    competing = {
        "event_id": "approval-2",
        "event_type": "human_approval",
        "approval_id": "A2",
        "context_version": "C1",
        "evidence_hash": "E1",
        "protocol_hash": "P1",
        "proposal_id": "PR1",
        "verifier": "v1",
        "human_approval": True,
        "occurred_at": "2026-10-07T10:05:30+00:00",
        "parent_event_id": "decision-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS[:-1], bad, competing], execution=bad)


def test_execution_cannot_be_rebound_to_other_approval():
    bad = dict(EVENTS[7])
    bad["parent_event_id"] = "approval-2"
    competing = {
        "event_id": "approval-2",
        "event_type": "human_approval",
        "approval_id": "A2",
        "context_version": "C1",
        "evidence_hash": "E1",
        "protocol_hash": "P1",
        "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:05:30+00:00",
        "parent_event_id": "decision-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS[:-1], bad, competing], execution=bad)


def test_approval_cannot_be_rebound_to_different_decision_with_same_proposal():
    bad = dict(EVENTS[6])
    bad["parent_event_id"] = "decision-2"
    competing = {
        "event_id": "decision-2",
        "event_type": "human_decision",
        "decision_id": "D2",
        "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:05:30+00:00",
        "parent_event_id": "verification-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS[:-2], bad, competing, EVENTS[-1]], approval=bad)


def test_approval_cannot_be_rebound_to_other_decision():
    bad = dict(EVENTS[6])
    bad["parent_event_id"] = "decision-2"
    competing = {
        "event_id": "decision-2",
        "event_type": "human_decision",
        "decision_id": "D2",
        "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:05:30+00:00",
        "parent_event_id": "verification-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=[*EVENTS, competing], approval=bad)


def test_duplicate_selected_approval_identity_is_rejected():
    duplicate = dict(EVENTS[6])
    duplicate["event_id"] = "approval-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_selected_execution_identity_is_rejected():
    duplicate = dict(EVENTS[7])
    duplicate["event_id"] = "execution-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_selected_verification_identity_is_rejected():
    duplicate = dict(EVENTS[5])
    duplicate["event_id"] = "verification-duplicate"
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_verification_identity_with_mutated_parent_is_rejected():
    duplicate = {**EVENTS[5], "event_id": "verification-attack", "parent_event_id": "obs-2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_evidence_identity_with_mutated_parent_is_rejected():
    duplicate = {**EVENTS[1], "event_id": "evidence-attack", "parent_event_id": "obs-2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_protocol_identity_with_mutated_binding_is_rejected():
    duplicate = {**EVENTS[2], "event_id": "protocol-attack", "evidence_hash": "E2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_duplicate_proposal_identity_with_mutated_binding_is_rejected():
    duplicate = {**EVENTS[3], "event_id": "proposal-attack", "protocol_hash": "P2"}
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [duplicate])


def test_selected_verification_event_parent_cannot_be_rebound():
    bad = replace_event(list(EVENTS), "verification", parent_event_id="obs-2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_selected_evidence_event_parent_cannot_be_rebound():
    bad = replace_event(list(EVENTS), "evidence", parent_event_id="obs-2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_selected_protocol_event_cannot_be_rebound_to_other_evidence():
    bad = replace_event(list(EVENTS), "protocol", evidence_hash="E2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)


def test_selected_proposal_event_cannot_be_rebound_to_other_protocol():
    bad = replace_event(list(EVENTS), "proposal", protocol_hash="P2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_unselected_earlier_observation_does_not_replace_selected_lineage():
    competing = {
        "event_id": "obs-2", "event_type": "observation",
        "target_id": "T2",
        "occurred_at": "2026-10-07T10:00:30+00:00",
    }
    call(events=[competing] + list(EVENTS))

def test_unselected_earlier_evidence_does_not_replace_selected_evidence():
    competing = {
        "event_id": "evidence-2", "event_type": "evidence",
        "evidence_hash": "E2", "context_version": "C2",
        "occurred_at": "2026-10-07T10:01:30+00:00",
        "parent_event_id": "obs-1",
    }
    call(events=[competing] + list(EVENTS))


def test_unselected_earlier_proposal_does_not_replace_selected_proposal():
    competing = {
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:03:30+00:00",
        "parent_event_id": "protocol-1",
    }
    call(events=[competing] + list(EVENTS))

def test_unselected_earlier_human_decision_does_not_replace_selected_chain():
    earlier = {
        "event_id": "decision-0", "event_type": "human_decision",
        "decision_id": "D0", "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:04:30+00:00",
        "parent_event_id": "verification-1",
    }
    call(events=[earlier] + list(EVENTS))


def test_reordered_competing_human_decision_does_not_replace_selected_decision():
    second = {
        "event_id": "decision-2", "event_type": "human_decision",
        "decision_id": "D2", "proposal_id": "PR2",
        "occurred_at": "2026-10-07T10:05:10+00:00",
        "parent_event_id": "verification-1",
    }
    fork = {
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:15+00:00",
        "parent_event_id": "protocol-1",
    }
    call(events=[second, fork] + list(EVENTS))


def test_selected_decision_id_cannot_be_rebound_to_competing_proposal():
    bad_decision = dict(DECISION, proposal_id="PR2")
    fork = {
        "event_id": "proposal-2", "event_type": "proposal",
        "proposal_id": "PR2", "protocol_hash": "P1",
        "context_version": "C1", "evidence_hash": "E1",
        "occurred_at": "2026-10-07T10:04:15+00:00",
        "parent_event_id": "protocol-1",
    }
    with pytest.raises(FullSystemAuthorityError):
        call(events=list(EVENTS) + [fork],
             decision=bad_decision,
             signature=sign_human_decision(bad_decision, SECRET))



def test_competing_approval_cannot_authorize_mismatched_execution():
    second = {
        "event_id": "approval-2", "event_type": "human_approval",
        "approval_id": "A2", "context_version": "C1",
        "evidence_hash": "E1", "protocol_hash": "P1",
        "proposal_id": "PR2", "occurred_at": "2026-10-07T10:05:10+00:00",
        "parent_event_id": "decision-1",
    }
    bad = [second] + list(EVENTS)
    bad = replace_event(bad, "execution", approval_id="A2", proposal_id="PR2")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad)

def test_unselected_verification_disagreement_is_evidence_not_authority():
    competing = {
        "event_id": "verification-2", "event_type": "verification",
        "verification_id": "V2", "target_id": "T1", "result": "fail",
        "context_version": "C1", "evidence_hash": "E1",
        "protocol_hash": "P1", "proposal_id": "PR1",
        "verifier": "v2", "verifier_instance": "v2-i1",
        "verification_time": "2026-10-07T10:04:10+00:00",
        "occurred_at": "2026-10-07T10:04:10+00:00",
        "parent_event_id": "obs-1",
    }
    call(events=list(EVENTS) + [competing])


def test_approval_cannot_select_competing_verifier():
    competing = dict(APPROVAL, verifier="v2")
    with pytest.raises(FullSystemAuthorityError):
        call(approval=competing)


def test_competing_verification_cannot_replace_selected_verification():
    competing = {
        "event_id": "verification-2", "event_type": "verification",
        "verification_id": "V2", "target_id": "T2", "result": "pass",
        "context_version": "C2", "evidence_hash": "E2",
        "protocol_hash": "P2", "proposal_id": "PR2",
        "verifier": "v2", "verifier_instance": "v2-i1",
        "verification_time": "2026-10-07T10:04:10+00:00",
        "occurred_at": "2026-10-07T10:04:10+00:00",
        "parent_event_id": "obs-1",
    }
    bad = [competing] + list(EVENTS)
    call(events=bad)


def test_later_reject_is_recorded_without_mutating_existing_approval():
    later_reject = {
        "event_id": "decision-2", "event_type": "human_decision",
        "decision_id": "D2", "proposal_id": "PR1",
        "occurred_at": "2026-10-07T10:07:00+00:00",
        "parent_event_id": "verification-1",
    }
    # A later decision event must not silently mutate the already-bound
    # approval/execution chain. It may exist as a separate candidate/event.
    bad = list(EVENTS) + [later_reject]
    call(events=bad)


def test_later_approve_cannot_override_prior_reject_without_new_binding():
    reject = dict(DECISION, decision="reject", human_approval=False, approval_id="A2")
    with pytest.raises(FullSystemAuthorityError):
        call(decision=reject, signature=sign_human_decision(reject, SECRET))




def test_decision_artifact_cannot_swap_approval_binding():
    bad_decision = dict(DECISION, approval_id="A2")
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad_decision,
             signature=sign_human_decision(bad_decision, SECRET))


def test_approval_requires_exact_approve_decision():
    revise = dict(DECISION, decision="revise", human_approval=False)
    approval = dict(APPROVAL)
    with pytest.raises(FullSystemAuthorityError):
        call(decision=revise, approval=approval,
             signature=sign_human_decision(revise, SECRET))


def test_reject_decision_cannot_authorize_execution():
    bad_decision = dict(DECISION, decision="reject", human_approval=False)
    bad_identity = dict(IDENTITY)
    bad = replace_event(list(EVENTS), "human_decision", proposal_id="PR1")
    with pytest.raises(FullSystemAuthorityError):
        call(events=bad, decision=bad_decision, identity=bad_identity,
             signature=sign_human_decision(bad_decision, SECRET))


def test_revise_decision_cannot_authorize_execution():
    bad_decision = dict(DECISION, decision="revise", human_approval=False)
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad_decision,
             signature=sign_human_decision(bad_decision, SECRET))


def test_reject_decision_cannot_be_reinterpreted_as_approval():
    bad_decision = dict(DECISION, decision="reject", human_approval=True)
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad_decision,
             signature=sign_human_decision(bad_decision, SECRET))


def test_revise_decision_cannot_be_reinterpreted_as_approval():
    bad_decision = dict(DECISION, decision="revise", human_approval=True)
    with pytest.raises(FullSystemAuthorityError):
        call(decision=bad_decision,
             signature=sign_human_decision(bad_decision, SECRET))


