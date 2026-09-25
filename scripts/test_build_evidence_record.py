from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_evidence_record import build_evidence


def result():
    return {"runtime_result": {
        "handoff_id": "SH-001", "trace_id": "TR-001", "execution_id": "EX-001",
        "provider": "fake", "output": {"answer": "observed"}, "evidence_ids": ["E-001"],
        "execution_authorized": False, "publish_authorized": False,
        "merge_authorized": False, "human_gate_required": True,
    }}


def test_stable_evidence_id_and_provenance():
    record = build_evidence(result())["evidence_record"]
    assert record["evidence_id"].startswith("EVIDENCE-")
    assert record["source"]["trace_id"] == "TR-001"
    assert record["source"]["execution_id"] == "EX-001"
    assert record["input_evidence_ids"] == ["E-001"]


def test_result_cannot_grant_authority():
    payload = result()
    payload["runtime_result"]["merge_authorized"] = True
    with pytest.raises(ValueError, match="merge_authorized"):
        build_evidence(payload)


def test_human_gate_is_required():
    payload = result()
    payload["runtime_result"]["human_gate_required"] = False
    with pytest.raises(ValueError, match="human_gate_required"):
        build_evidence(payload)
