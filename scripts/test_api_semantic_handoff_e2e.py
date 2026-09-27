from build_evidence_record import build_evidence
from project_evidence_to_aiwitness import build_witness
from runtime.api import ShirakamiAPI


def test_http_boundary_preserves_lineage_and_authority():
    runtime_result = {"runtime_result": {
        "handoff_id": "SH-HO-HTTP-001",
        "trace_id": "TRACE-HTTP-001",
        "execution_id": "EXEC-HTTP-001",
        "provider": "test-provider",
        "output": {"observed": True},
        "evidence_ids": ["AGENT-COORDINATION-HTTP-001"],
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }}
    evidence = build_evidence(runtime_result)["evidence_record"]

    traces = {"TRACE-HTTP-001": {"codex_traceability": {
        "trace_id": "TRACE-HTTP-001",
        "execution_id": "EXEC-HTTP-001",
        "activity_id": "ACTIVITY-HTTP-001",
        "source_handoff_id": "SH-HO-HTTP-001",
        "evidence_ids": [evidence["evidence_id"]],
        "verification": {"status": "passed", "tests": ["http-lineage"]},
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
        },
        "human_gate": {"required": True, "decision": "pending"},
    }}}
    api = ShirakamiAPI(traces)

    status, body = api.get(
        "/v1/semantic-handoff/TRACE-HTTP-001",
        project="Shirakami",
        objective="HTTP lineage boundary",
        protocol_ids=["PROTOCOL-HTTP-001"],
        verification_scope="http",
    )

    assert status == 200
    assert body["handoff_id"] == "SH-HO-HTTP-001"
    assert body["trace_id"] == "TRACE-HTTP-001"
    assert body["execution_id"] == "EXEC-HTTP-001"
    assert body["activity_id"] == "ACTIVITY-HTTP-001"
    assert body["evidence_ids"] == [evidence["evidence_id"]]

    witness = build_witness({"evidence_record": evidence})["aiwitness"]
    assert witness["provenance"]["evidence_id"] in body["evidence_ids"]
    assert witness["provenance"]["trace_id"] == body["trace_id"]
    assert witness["provenance"]["execution_id"] == body["execution_id"]

    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True
    assert body["decision_authority"] is False
