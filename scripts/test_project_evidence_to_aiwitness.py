from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from project_evidence_to_aiwitness import build_witness


def evidence():
    return {"evidence_record": {
        "version": "0.1", "evidence_id": "EVIDENCE-001", "kind": "runtime_observation",
        "source": {"handoff_id": "SH-001", "trace_id": "TR-001", "execution_id": "EX-001", "provider": "fake"},
        "observed": {"output": {"ok": True}}, "input_evidence_ids": ["E-000"],
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False, "human_gate_required": True},
    }}


def test_evidence_identity_reaches_aiwitness():
    witness = build_witness(evidence())["aiwitness"]
    assert witness["provenance"]["evidence_id"] == "EVIDENCE-001"
    assert witness["provenance"]["trace_id"] == "TR-001"
    assert witness["provenance"]["execution_id"] == "EX-001"
    assert witness["observation"]["output"] == {"ok": True}


def test_evidence_cannot_grant_authority():
    payload = evidence()
    payload["evidence_record"]["authority"]["publish_authorized"] = True
    with pytest.raises(ValueError, match="publish_authorized"):
        build_witness(payload)
