from joumon_poc import run

def test_same_context_and_protocol_are_preserved():
    x = run()
    assert {r.context_id for r in x["results"]} == {"joumon-poc-context-001"}
    assert x["protocol"].input_context_id == "joumon-poc-context-001"

def test_each_evidence_record_preserves_runtime_provenance():
    x = run()
    assert {e.runtime_id for e in x["evidence"]} == {"mock-runtime-a", "mock-runtime-b"}
    assert all(e.context_id == x["context"].context_id for e in x["evidence"])

def test_evidence_is_non_authoritative():
    assert all(e.authority == "non-authoritative" for e in run()["evidence"])

def test_human_gate_remains_final_authority():
    gate = run()["human_gate"]
    assert gate.decision_authority == "human"
    assert gate.decision_status == "pending"

def test_runtime_can_be_replaced_without_changing_authority_boundary():
    x, y = run(("mock-runtime-a",)), run(("mock-runtime-b",))
    assert x["context"].final_decision_authority == y["context"].final_decision_authority == "human"
    assert x["human_gate"].decision_authority == y["human_gate"].decision_authority == "human"
