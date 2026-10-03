from joumon_adapter_poc import run

def test_same_context_and_protocol_cross_adapter_boundary():
    context, protocol, results, _, _ = run()
    assert {r.context_id for r in results} == {context.context_id}
    assert protocol.input_context_id == context.context_id

def test_runtime_identity_survives_adapter_boundary():
    _, _, _, evidence, _ = run()
    assert {e.runtime_id for e in evidence} == {"runtime-a", "runtime-b"}

def test_evidence_remains_non_authoritative():
    _, _, _, evidence, _ = run()
    assert all(e.authority == "non-authoritative" for e in evidence)

def test_human_gate_remains_authority():
    context, _, _, _, gate = run()
    assert context.final_decision_authority == "human"
    assert gate.decision_authority == "human"
    assert gate.decision_status == "pending"

def test_runtime_implementation_can_change_behavior_without_authority_change():
    context, _, results, _, gate = run()
    assert results[0].output != results[1].output
    assert context.final_decision_authority == gate.decision_authority == "human"
