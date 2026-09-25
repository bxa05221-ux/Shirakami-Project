from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_runtime_request import build_runtime_request


def sample_context():
    return {
        "api_context": {
            "version": "0.1",
            "handoff_id": "SH-001",
            "trace_id": "TR-001",
            "execution_id": "EX-001",
            "project": "demo",
            "objective": "verify adapter boundary",
            "protocol_ids": ["P-001"],
            "evidence_ids": ["E-001", "E-002"],
            "verification_scope": "unit",
            "verification": {"status": "passed", "tests": ["T-001"]},
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            },
        }
    }


def test_runtime_request_preserves_traceability():
    result = build_runtime_request(sample_context(), "local-llm")
    request = result["runtime_request"]
    assert request["handoff_id"] == "SH-001"
    assert request["trace_id"] == "TR-001"
    assert request["execution_id"] == "EX-001"
    assert request["protocol_ids"] == ["P-001"]
    assert request["evidence_ids"] == ["E-001", "E-002"]
    assert request["runtime_target"] == "local-llm"


@pytest.mark.parametrize(
    "field",
    ["execution_authorized", "publish_authorized", "merge_authorized"],
)
def test_runtime_target_cannot_grant_authority(field):
    document = sample_context()
    document["api_context"]["authority"][field] = True
    with pytest.raises(ValueError, match=field):
        build_runtime_request(document, "provider-x")


def test_human_gate_is_preserved():
    request = build_runtime_request(sample_context(), "provider-x")["runtime_request"]
    assert request["authority"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }


def test_runtime_target_is_descriptive_only():
    request = build_runtime_request(sample_context(), "openai")["runtime_request"]
    assert request["runtime_target"] == "openai"
    assert request["authority"]["execution_authorized"] is False
