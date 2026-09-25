from record_codex_trace import build_trace


def test_trace_is_generated_from_handoff():
    handoff = {
        "semantic_handoff": {
            "id": "SH-HO-20260925-001",
            "status": "ready",
            "evidence": {"evidence_ids": ["AGENT-COORDINATION-001"]},
            "human_gate": {"required": True, "decision": "pending"},
        }
    }
    trace = build_trace(handoff, "TRACE-001", "EXEC-001")["codex_traceability"]
    assert trace["trace_id"] == "TRACE-001"
    assert trace["execution_id"] == "EXEC-001"
    assert trace["source_handoff_id"] == "SH-HO-20260925-001"
    assert trace["evidence_ids"] == ["AGENT-COORDINATION-001"]
    assert trace["result"]["status"] == "pending"
    assert trace["commit"] is None
    assert trace["authority"]["execution_authorized"] is False
    assert trace["human_gate"]["required"] is True


def test_trace_generation_rejects_non_consumable_handoff():
    handoff = {
        "semantic_handoff": {
            "id": "SH-001",
            "status": "draft",
            "evidence": {"evidence_ids": []},
            "human_gate": {"required": True},
        }
    }
    try:
        build_trace(handoff, "TRACE-002", "EXEC-002")
    except ValueError as exc:
        assert "not consumable" in str(exc)
    else:
        raise AssertionError("draft handoff must be rejected")


def test_trace_generation_requires_execution_identity():
    handoff = {
        "semantic_handoff": {
            "id": "SH-001",
            "status": "ready",
            "evidence": {"evidence_ids": []},
            "human_gate": {"required": True},
        }
    }
    try:
        build_trace(handoff, "TRACE-003", "")
    except ValueError as exc:
        assert "execution_id" in str(exc)
    else:
        raise AssertionError("execution identity must be explicit")
