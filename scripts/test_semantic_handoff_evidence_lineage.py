from build_evidence_record import build_evidence
from project_evidence_to_aiwitness import build_witness
from runtime.semantic_handoff import SemanticHandoff


def test_real_evidence_id_reaches_handoff_and_aiwitness():
    runtime_result = {"runtime_result": {
        "handoff_id": "SH-HO-001",
        "trace_id": "TRACE-001",
        "execution_id": "EXEC-001",
        "provider": "test-provider",
        "output": {"observed": True},
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }}
    evidence = build_evidence(runtime_result)["evidence_record"]
    trace = {"codex_traceability": {
        "trace_id": "TRACE-001",
        "execution_id": "EXEC-001",
        "activity_id": "ACTIVITY-001",
        "source_handoff_id": "SH-HO-001",
        "evidence_ids": [evidence["evidence_id"]],
        "verification": {"status": "passed", "tests": ["evidence-lineage"]},
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
        },
        "human_gate": {"required": True, "decision": "pending"},
    }}
    handoff = SemanticHandoff.from_trace(
        trace,
        project="Shirakami",
        objective="evidence lineage",
        protocol_ids=["PROTOCOL-001"],
        verification_scope="lineage",
    )
    witness = build_witness({"evidence_record": evidence})["aiwitness"]
    assert evidence["evidence_id"] in handoff.evidence_ids
    assert witness["provenance"]["evidence_id"] == evidence["evidence_id"]
    assert witness["provenance"]["evidence_id"] in handoff.evidence_ids
    assert witness["provenance"]["trace_id"] == handoff.trace_id
    assert witness["provenance"]["execution_id"] == handoff.execution_id
    assert handoff.execution_authorized is False
    assert witness["authority"]["merge_authorized"] is False
