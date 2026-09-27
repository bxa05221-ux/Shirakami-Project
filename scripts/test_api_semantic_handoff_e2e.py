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
        "protocol_ids": ["PROTOCOL-HTTP-001"],
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
    assert body["protocol_ids"] == ["PROTOCOL-HTTP-001"]
    assert body["evidence_ids"] == [evidence["evidence_id"]]

    witness = build_witness({"evidence_record": evidence})["aiwitness"]
    assert witness["provenance"]["evidence_id"] in body["evidence_ids"]
    assert witness["provenance"]["trace_id"] == body["trace_id"]
    assert witness["provenance"]["execution_id"] == body["execution_id"]
    assert witness["provenance"]["protocol_ids"] == body["protocol_ids"]

    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True
    assert body["decision_authority"] is False

def test_provider_swap_preserves_evidence_and_aiwitness_lineage():
    runtime_results = [
        {
            "runtime_result": {
                "handoff_id": "SH-HO-SWAP-001",
                "trace_id": "TRACE-SWAP-001",
                "execution_id": "EXEC-SWAP-001",
                "provider": "provider-a",
                "output": {"provider": "a", "observed": True},
                "protocol_ids": ["PROTOCOL-SWAP-001"],
                "evidence_ids": ["EVIDENCE-INPUT-001"],
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            }
        },
        {
            "runtime_result": {
                "handoff_id": "SH-HO-SWAP-001",
                "trace_id": "TRACE-SWAP-001",
                "execution_id": "EXEC-SWAP-001",
                "provider": "provider-b",
                "output": {"provider": "b", "observed": True},
                "protocol_ids": ["PROTOCOL-SWAP-001"],
                "evidence_ids": ["EVIDENCE-INPUT-001"],
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            }
        },
    ]

    records = [build_evidence(result)["evidence_record"] for result in runtime_results]
    witnesses = [
        build_witness({"evidence_record": record})["aiwitness"]
        for record in records
    ]

    assert [record["source"]["provider"] for record in records] == ["provider-a", "provider-b"]
    assert [record["source"]["protocol_ids"] for record in records] == [
        ["PROTOCOL-SWAP-001"], ["PROTOCOL-SWAP-001"]
    ]
    assert [
        (record["source"]["handoff_id"], record["source"]["trace_id"],
         record["source"]["execution_id"], record["input_evidence_ids"])
        for record in records
    ] == [
        ("SH-HO-SWAP-001", "TRACE-SWAP-001", "EXEC-SWAP-001", ["EVIDENCE-INPUT-001"]),
        ("SH-HO-SWAP-001", "TRACE-SWAP-001", "EXEC-SWAP-001", ["EVIDENCE-INPUT-001"]),
    ]
    assert [
        (witness["provenance"]["handoff_id"], witness["provenance"]["trace_id"],
         witness["provenance"]["execution_id"], witness["provenance"]["provider"],
         witness["provenance"]["input_evidence_ids"])
        for witness in witnesses
    ] == [
        ("SH-HO-SWAP-001", "TRACE-SWAP-001", "EXEC-SWAP-001", "provider-a", ["EVIDENCE-INPUT-001"]),
        ("SH-HO-SWAP-001", "TRACE-SWAP-001", "EXEC-SWAP-001", "provider-b", ["EVIDENCE-INPUT-001"]),
    ]

    for record, witness in zip(records, witnesses):
        assert witness["provenance"]["evidence_id"] == record["evidence_id"]
        assert witness["provenance"]["protocol_ids"] == record["source"]["protocol_ids"]
        assert witness["authority"]["execution_authorized"] is False
        assert witness["authority"]["publish_authorized"] is False
        assert witness["authority"]["merge_authorized"] is False
        assert witness["authority"]["human_gate_required"] is True
