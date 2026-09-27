from runtime.semantic_handoff import SemanticHandoff


def trace(authority=None, activity_id=None):
    return {"codex_traceability": {
        "trace_id": "TRACE-001",
        "execution_id": "EXEC-001",
        "source_handoff_id": "SH-HO-001",
        "evidence_ids": ["EVIDENCE-001", "EVIDENCE-002"],
        "verification": {"status": "passed", "tests": ["pytest -q"]},
        "authority": authority or {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
        },
        "human_gate": {"required": True, "decision": "pending"},
    }}


def test_semantic_handoff_preserves_lineage():
    handoff = SemanticHandoff.from_trace(
        trace(),
        project="Shirakami",
        objective="lineage",
        protocol_ids=["PROTOCOL-001"],
        verification_scope="boundary",
        activity_id="ACTIVITY-001",
    )
    assert handoff.handoff_id == "SH-HO-001"
    assert handoff.trace_id == "TRACE-001"
    assert handoff.execution_id == "EXEC-001"
    assert handoff.activity_id == "ACTIVITY-001"
    assert handoff.evidence_ids == ("EVIDENCE-001", "EVIDENCE-002")
    assert handoff.protocol_ids == ("PROTOCOL-001",)


def test_semantic_handoff_has_no_authority():
    handoff = SemanticHandoff.from_trace(
        trace(), project="p", objective="o", protocol_ids=[], verification_scope="v"
    )
    assert handoff.execution_authorized is False
    assert handoff.publish_authorized is False
    assert handoff.merge_authorized is False
    assert handoff.human_gate_required is True
    assert handoff.decision_authority is False


def test_semantic_handoff_rejects_authority_in_trace():
    payload = trace()
    payload["codex_traceability"]["authority"]["publish_authorized"] = True
    try:
        SemanticHandoff.from_trace(
            payload, project="p", objective="o", protocol_ids=[], verification_scope="v"
        )
    except ValueError as exc:
        assert "publish_authorized" in str(exc)
    else:
        raise AssertionError("authority must not cross the boundary")


def test_semantic_handoff_requires_human_gate():
    payload = trace()
    payload["codex_traceability"]["human_gate"]["required"] = False
    try:
        SemanticHandoff.from_trace(
            payload, project="p", objective="o", protocol_ids=[], verification_scope="v"
        )
    except ValueError as exc:
        assert "human_gate.required" in str(exc)
    else:
        raise AssertionError("human gate must remain required")
