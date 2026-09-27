from runtime.api import ShirakamiAPI


def test_api_get_semantic_handoff_and_http_shape():
    traces = {"TRACE-001": {"codex_traceability": {
        "trace_id": "TRACE-001",
        "execution_id": "EXEC-001",
        "source_handoff_id": "SH-HO-001",
        "evidence_ids": ["EVIDENCE-001"],
        "verification": {"status": "passed", "tests": []},
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
        },
        "human_gate": {"required": True, "decision": "pending"},
    }}}
    api = ShirakamiAPI(traces)
    status, body = api.get(
        "/v1/semantic-handoff/TRACE-001",
        project="Shirakami",
        objective="bridge",
        protocol_ids=["PROTOCOL-001"],
        verification_scope="boundary",
        activity_id="ACTIVITY-001",
    )
    assert status == 200
    assert body["handoff_id"] == "SH-HO-001"
    assert body["trace_id"] == "TRACE-001"
    assert body["execution_id"] == "EXEC-001"
    assert body["activity_id"] == "ACTIVITY-001"
    assert body["evidence_ids"] == ["EVIDENCE-001"]
    assert body["execution_authorized"] is False
    assert body["publish_authorized"] is False
    assert body["merge_authorized"] is False
    assert body["human_gate_required"] is True
    assert api.capabilities["semantic_handoff"] is True


def test_api_returns_404_for_unknown_trace():
    api = ShirakamiAPI({})
    status, body = api.get(
        "/v1/semantic-handoff/MISSING",
        project="p", objective="o", protocol_ids=[], verification_scope="v"
    )
    assert status == 404
    assert body["trace_id"] == "MISSING"
