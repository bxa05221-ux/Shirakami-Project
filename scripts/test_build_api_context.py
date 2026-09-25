from build_api_context import build_context

def trace():
    return {"codex_traceability": {
        "trace_id": "TRACE-001", "execution_id": "EXEC-001",
        "source_handoff_id": "SH-HO-001", "evidence_ids": ["EVIDENCE-001"],
        "verification": {"status": "passed", "tests": ["pytest -q"]},
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False},
        "human_gate": {"required": True, "decision": "pending"},
    }}

def test_api_context_preserves_identity():
    context = build_context(trace(), "Shirakami", "bridge", ["PROTOCOL-001"], "boundary")["api_context"]
    assert context["handoff_id"] == "SH-HO-001"
    assert context["trace_id"] == "TRACE-001"
    assert context["execution_id"] == "EXEC-001"
    assert context["evidence_ids"] == ["EVIDENCE-001"]
    assert context["protocol_ids"] == ["PROTOCOL-001"]

def test_api_context_cannot_gain_authority():
    payload = trace()
    payload["codex_traceability"]["authority"]["execution_authorized"] = True
    try:
        build_context(payload, "p", "o", [], "v")
    except ValueError as exc:
        assert "execution_authorized" in str(exc)
    else:
        raise AssertionError("authority must not propagate")

def test_api_context_requires_human_gate():
    payload = trace()
    payload["codex_traceability"]["human_gate"]["required"] = False
    try:
        build_context(payload, "p", "o", [], "v")
    except ValueError as exc:
        assert "human_gate.required" in str(exc)
    else:
        raise AssertionError("human gate must remain required")
