import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_protocol import build_protocol


def candidate():
    return {"candidate": {"candidate_id": "CANDIDATE-001", "candidate_state": "review_required", "evidence_ids": ["EVIDENCE-001"], "proposal": {"change": "proposal"}, "validation": {"status": "pass"}}}


def test_human_approval_creates_protocol_without_authority():
    p = build_protocol(candidate(), {"source": "human_gate", "approved": True})["protocol"]
    assert p["protocol_id"] == "PROTOCOL-FROM-CANDIDATE-001"
    assert p["protocol_state"] == "approved_for_runtime_review"
    assert p["authority"]["execution_authorized"] is False
    assert p["authority"]["publish_authorized"] is False
    assert p["authority"]["merge_authorized"] is False
    assert p["authority"]["human_gate_required"] is True


def test_non_human_approval_is_rejected():
    with pytest.raises(ValueError, match="human approval"):
        build_protocol(candidate(), {"source": "aiwitness", "approved": True})


def test_missing_approval_is_rejected():
    with pytest.raises(ValueError, match="human approval"):
        build_protocol(candidate(), {"source": "human_gate", "approved": False})
