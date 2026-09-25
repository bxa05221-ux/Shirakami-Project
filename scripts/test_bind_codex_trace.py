from bind_codex_trace import bind

def base():
    return {"codex_traceability": {
        "version": "0.1",
        "trace_id": "TRACE-001",
        "source_handoff_id": "SH-HO-20260925-001",
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "result": {"status": "pending", "changed_paths": [], "observations": [], "deviations": []},
        "verification": {"status": "pending", "tests": []},
        "commit": None,
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False},
        "human_gate": {"required": True, "decision": "pending"},
    }}

def test_bind_commit_and_paths():
    out = bind(base(), "abc123", ["scripts/foo.py"])
    root = out["codex_traceability"]
    assert root["commit"] == "abc123"
    assert root["result"]["changed_paths"] == ["scripts/foo.py"]
    assert root["authority"]["merge_authorized"] is False
    assert root["human_gate"]["required"] is True

def test_bind_requires_commit():
    try:
        bind(base(), "", [])
    except ValueError as exc:
        assert "commit is required" in str(exc)
    else:
        raise AssertionError("empty commit must be rejected")
