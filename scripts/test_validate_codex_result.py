from validate_codex_result import validate


def test_completed_result_preserves_human_gate():
    payload = {
        "codex_result": {
            "version": "0.1",
            "source_handoff_id": "SH-HO-20260925-001",
            "status": "completed",
            "result": {
                "changed_paths": ["example.py"],
                "observations": ["implemented"],
                "deviations": [],
            },
            "verification": {"status": "passed", "tests": ["pytest"]},
            "commit": "abc123",
            "unresolved": [],
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }
    }
    assert validate(payload) == []


def test_authority_cannot_be_inferred_from_result():
    payload = {
        "codex_result": {
            "version": "0.1",
            "source_handoff_id": "SH-HO-20260925-001",
            "status": "completed",
            "result": {"changed_paths": [], "observations": [], "deviations": []},
            "verification": {"status": "passed", "tests": []},
            "commit": "abc123",
            "unresolved": [],
            "authority": {
                "execution_authorized": True,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }
    }
    assert "authority.execution_authorized must remain false" in validate(payload)
