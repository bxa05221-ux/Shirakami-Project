from bidirectional_handoff import (
    receive_from_project_a,
    respond_from_project_b,
    validate_returned_to_project_a,
)


def test_project_a_to_b_to_a_preserves_context_lineage_and_human_gate():
    source = {
        "context": {"project": "A", "topic": "handoff"},
        "evidence": ["E-001"],
        "provenance": [{"source": "Project A", "evidence_id": "E-001"}],
        "unresolved": ["Who may decide?"],
        "human_gate": {"required": True, "decision": "pending"},
        "authority_transfer": False,
    }

    received = receive_from_project_a(source)
    returned = respond_from_project_b(received, {"project_b_observation": "received"})
    validate_returned_to_project_a(returned)

    assert returned["context"] == {
        "project": "A",
        "topic": "handoff",
        "project_b_observation": "received",
    }
    assert returned["evidence"] == ["E-001"]
    assert returned["provenance"] == source["provenance"]
    assert returned["unresolved"] == ["Who may decide?"]
    assert returned["human_gate"] == {"required": True, "decision": "pending"}
    assert returned["authority_transfer"] is False
    assert returned["authority_transferred"] is False


def test_roundtrip_rejects_authority_transfer():
    source = {
        "context": {},
        "evidence": [],
        "provenance": [],
        "unresolved": [],
        "human_gate": {"required": True},
        "authority_transfer": True,
    }

    try:
        receive_from_project_a(source)
    except ValueError as exc:
        assert "authority_transfer" in str(exc)
    else:
        raise AssertionError("authority transfer must be rejected")
