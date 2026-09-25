import sys
from pathlib import Path
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_protocol_runtime_request import build_protocol_runtime_request


def protocol():
    return {"protocol": {
        "protocol_id": "PROTOCOL-001", "protocol_state": "approved_for_runtime_review",
        "evidence_ids": ["EVIDENCE-001"], "proposal": {"change": "proposal"},
        "validation": {"status": "pass"},
        "approval": {"source": "human_gate", "approved": True},
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False, "human_gate_required": True},
    }}


def test_protocol_becomes_runtime_request_without_execution_authority():
    request = build_protocol_runtime_request(protocol(), "provider-neutral")["runtime_request"]
    assert request["request_id"] == "RUNTIME-FROM-PROTOCOL-001"
    assert request["protocol_ids"] == ["PROTOCOL-001"]
    assert request["evidence_ids"] == ["EVIDENCE-001"]
    assert request["runtime_target"] == "provider-neutral"
    assert request["authority"]["execution_authorized"] is False
    assert request["authority"]["human_gate_required"] is True


def test_unapproved_protocol_is_rejected():
    p = protocol()
    p["protocol"]["approval"]["approved"] = False
    with pytest.raises(ValueError, match="human approval"):
        build_protocol_runtime_request(p)


def test_protocol_cannot_smuggle_execution_authority():
    p = protocol()
    p["protocol"]["authority"]["execution_authorized"] = True
    with pytest.raises(ValueError, match="execution_authorized"):
        build_protocol_runtime_request(p)
