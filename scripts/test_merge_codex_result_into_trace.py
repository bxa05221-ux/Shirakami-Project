from merge_codex_result_into_trace import merge

def trace():
    return {"codex_traceability": {
        "version": "0.1", "trace_id": "TRACE-001",
        "source_handoff_id": "SH-HO-20260925-001",
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "result": {"status": "pending", "changed_paths": [], "observations": [], "deviations": []},
        "verification": {"status": "pending", "tests": []}, "commit": None,
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False},
        "human_gate": {"required": True, "decision": "pending"}}}

def result():
    return {"codex_result": {
        "version": "0.1", "source_handoff_id": "SH-HO-20260925-001",
        "status": "completed",
        "evidence_ids": ["AGENT-COORDINATION-001"],
        "result": {"changed_paths": ["scripts/x.py"], "observations": ["observed"], "deviations": []},
        "verification": {"status": "passed", "tests": ["pytest -q"]},
        "commit": "abc123",
        "human_gate": {"required": True, "decision": "pending"}}}

def test_merge_closes_result_and_verification():
    out = merge(trace(), result())["codex_traceability"]
    assert out["result"]["status"] == "completed"
    assert out["result"]["changed_paths"] == ["scripts/x.py"]
    assert out["verification"]["status"] == "passed"
    assert out["commit"] == "abc123"
    assert out["authority"]["merge_authorized"] is False
    assert out["human_gate"]["decision"] == "pending"

def test_merge_rejects_wrong_handoff():
    r = result()
    r["codex_result"]["source_handoff_id"] = "SH-WRONG"
    try:
        merge(trace(), r)
    except ValueError as exc:
        assert "source_handoff_id mismatch" in str(exc)
    else:
        raise AssertionError("mismatched handoff must be rejected")

def test_merge_rejects_evidence_drift():
    r = result()
    r["codex_result"]["evidence_ids"] = ["EVIDENCE-INVENTED"]
    try:
        merge(trace(), r)
    except ValueError as exc:
        assert "evidence_ids mismatch" in str(exc)
    else:
        raise AssertionError("evidence drift must be rejected")
