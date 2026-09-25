import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from execute_runtime_request import execute


def request():
    return {"runtime_request": {
        "request_id": "RUNTIME-001", "protocol_ids": ["PROTOCOL-001"],
        "evidence_ids": ["EVIDENCE-001"], "proposal": {"change": "proposal"},
        "runtime_target": "fixture"
    }}


def test_runtime_request_produces_traceable_non_authoritative_result():
    result = execute(request(), {"answer": "ok"})["runtime_result"]
    assert result["handoff_id"] == "RUNTIME-001"
    assert result["provider"] == "fixture"
    assert result["evidence_ids"] == ["EVIDENCE-001"]
    assert result["output"] == {"answer": "ok"}
    assert result["authority"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }


def test_runtime_request_requires_evidence():
    r = request()
    r["runtime_request"]["evidence_ids"] = []
    with pytest.raises(ValueError, match="evidence_ids"):
        execute(r)
