from pathlib import Path
import sys

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.semantic_integrity import ProtocolRegistry, verify_protocol_reference


def protocol(**overrides):
    value = {
        "protocol_id": "PROTOCOL-001",
        "version": "0.1",
        "source_candidate_id": "CANDIDATE-001",
        "evidence_ids": ["EVIDENCE-001"],
        "approval": {"source": "human_gate", "approved": True},
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }
    value.update(overrides)
    return value


def test_valid_reference_resolves_without_authority():
    result = verify_protocol_reference(
        ProtocolRegistry({"PROTOCOL-001": protocol()}),
        protocol_id="PROTOCOL-001",
        handoff_protocol_id="PROTOCOL-001",
    )
    assert result.status == "resolved"
    assert result.resolved_version == "0.1"
    assert result.execution_authorized is False
    assert result.publish_authorized is False
    assert result.merge_authorized is False
    assert result.human_gate_required is True


@pytest.mark.parametrize(
    ("registry", "protocol_id", "handoff_protocol_id", "status"),
    [
        ({}, "PROTOCOL-404", "PROTOCOL-404", "unresolved"),
        (
            {"PROTOCOL-001": [protocol(), protocol(version="0.2")]},
            "PROTOCOL-001",
            "PROTOCOL-001",
            "ambiguous",
        ),
        ({"PROTOCOL-001": protocol()}, "PROTOCOL-001", "PROTOCOL-002", "mismatch"),
    ],
)
def test_reference_failures_do_not_infer_or_substitute(
    registry, protocol_id, handoff_protocol_id, status
):
    result = verify_protocol_reference(
        ProtocolRegistry(registry),
        protocol_id=protocol_id,
        handoff_protocol_id=handoff_protocol_id,
    )
    assert result.status == status
    assert result.execution_authorized is False
    assert result.publish_authorized is False
    assert result.merge_authorized is False
    assert result.human_gate_required is True


def test_missing_lineage_is_incomplete():
    value = protocol(evidence_ids=[])
    result = verify_protocol_reference(
        ProtocolRegistry({"PROTOCOL-001": value}),
        protocol_id="PROTOCOL-001",
        handoff_protocol_id="PROTOCOL-001",
    )
    assert result.status == "incomplete"


def test_missing_human_gate_provenance_is_unverified():
    value = protocol(approval=None)
    result = verify_protocol_reference(
        ProtocolRegistry({"PROTOCOL-001": value}),
        protocol_id="PROTOCOL-001",
        handoff_protocol_id="PROTOCOL-001",
    )
    assert result.status == "unverified"


def test_authority_cannot_be_smuggled_through_protocol():
    value = protocol(
        authority={
            "execution_authorized": True,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        }
    )
    result = verify_protocol_reference(
        ProtocolRegistry({"PROTOCOL-001": value}),
        protocol_id="PROTOCOL-001",
        handoff_protocol_id="PROTOCOL-001",
    )
    assert result.status == "unverified"
    assert result.execution_authorized is False
    assert result.publish_authorized is False
    assert result.merge_authorized is False
    assert result.human_gate_required is True
