from runtime.human_gate_protocol import (
    accept_symbolic_candidate,
    build_human_approved_protocol,
)
from runtime.symbolic_decision_boundary import build_symbolic_decision_boundary


def test_human_gate_acceptance_creates_explicit_protocol_boundary():
    boundary = build_symbolic_decision_boundary(
        candidate_id="candidate-01",
        symbol_id="symbol-life",
        expression="生きろ",
        interpretations=("survival", "renewal"),
        basis_observation_ids=("obs-10",),
    )
    acceptance = accept_symbolic_candidate(
        boundary=boundary,
        acceptance_id="accept-01",
        actor_id="human-01",
        scope=("create_restart_plan",),
    )
    protocol = build_human_approved_protocol(
        boundary=boundary,
        acceptance=acceptance,
        protocol_id="protocol-01",
    )

    assert protocol.human_approved is True
    assert protocol.decision_authority is True
    assert protocol.source_observation_ids == ("obs-10",)
    assert protocol.scope == ("create_restart_plan",)


def test_human_gate_cannot_approve_without_explicit_scope():
    boundary = build_symbolic_decision_boundary(
        candidate_id="candidate-02",
        symbol_id="symbol-stop",
        expression="止まれ",
        interpretations=("danger",),
        basis_observation_ids=("obs-11",),
    )

    try:
        accept_symbolic_candidate(
            boundary=boundary,
            acceptance_id="accept-02",
            actor_id="human-01",
            scope=(),
        )
    except ValueError as exc:
        assert "scope" in str(exc)
    else:
        raise AssertionError("empty scope must not create Human Gate acceptance")
