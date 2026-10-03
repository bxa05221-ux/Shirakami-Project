from joumon_multi_hop import run_multi_hop
from joumon_evidence_verifier import verify
from joumon_human_gate import prepare_human_gate, record_human_decision


def test_multi_runtime_chain_reaches_human_gate():
    context, protocol, stages = run_multi_hop()
    evidence = tuple(stage[2].evidence[-1] for stage in stages)
    verification = tuple(verify(e, expected_context_id=context.context_id, expected_protocol_id=protocol.protocol_id) for e in evidence)
    assert all(v.verified for v in verification)
    gate = prepare_human_gate(
        gate_id="e2e-gate-001",
        context_id=context.context_id,
        protocol_id=protocol.protocol_id,
        evidence=evidence,
        verification_ids=tuple(v.evidence_id for v in verification),
    )
    record = record_human_decision(gate, decision="proceed to human-reviewed next step")
    assert record.authority == "human"
    assert len(record.evidence_ids) == 3


def test_runtime_does_not_become_decision_authority_at_end():
    context, protocol, stages = run_multi_hop()
    evidence = tuple(stage[2].evidence[-1] for stage in stages)
    gate = prepare_human_gate(
        gate_id="e2e-gate-002",
        context_id=context.context_id,
        protocol_id=protocol.protocol_id,
        evidence=evidence,
        verification_ids=tuple(e.evidence_id for e in evidence),
    )
    assert gate.decision_authority == "human"
