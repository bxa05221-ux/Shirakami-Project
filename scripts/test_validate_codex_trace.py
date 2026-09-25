from validate_codex_trace import validate

def valid_payload():
    return {
        "codex_traceability": {
            "version": "0.1",
            "trace_id": "TRACE-001",
            "source_handoff_id": "SH-HO-20260925-001",
            "evidence_ids": ["AGENT-COORDINATION-001"],
            "result": {
                "status": "completed",
                "changed_paths": ["scripts/example.py"],
                "observations": ["observed"],
                "deviations": [],
            },
            "verification": {
                "status": "passed",
                "tests": ["pytest -q"],
            },
            "commit": "abc123",
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {
                "required": True,
                "decision": "pending",
            },
        }
    }

def test_valid_trace():
    assert validate(valid_payload()) == []

def test_trace_rejects_inferred_authority():
    payload = valid_payload()
    payload["codex_traceability"]["authority"]["merge_authorized"] = True
    assert "authority.merge_authorized must remain false" in validate(payload)
