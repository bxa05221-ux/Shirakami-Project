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

def test_runtime_execution_closes_into_evidence_and_aiwitness():
    from build_evidence_record import build_evidence
    from project_evidence_to_aiwitness import build_witness

    runtime = execute(request(), {"answer": "observed"})["runtime_result"]
    evidence = build_evidence({"runtime_result": runtime})["evidence_record"]
    witness = build_witness({"evidence_record": evidence})["aiwitness"]

    assert evidence["source"]["handoff_id"] == runtime["handoff_id"]
    assert evidence["source"]["provider"] == runtime["provider"]
    assert witness["provenance"]["evidence_id"] == evidence["evidence_id"]
    assert witness["provenance"]["handoff_id"] == runtime["handoff_id"]
    assert witness["provenance"]["provider"] == runtime["provider"]
    assert witness["authority"]["execution_authorized"] is False
    assert witness["authority"]["publish_authorized"] is False
    assert witness["authority"]["merge_authorized"] is False
    assert witness["authority"]["human_gate_required"] is True
