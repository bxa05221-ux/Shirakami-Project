from record_aiwitness import build_witness


def trace():
    return {
        "codex_traceability": {
            "version": "0.1",
            "trace_id": "TRACE-001",
            "execution_id": "EXEC-001",
            "source_handoff_id": "SH-HO-001",
            "evidence_ids": ["EVIDENCE-001"],
            "verification": {"status": "passed", "tests": ["pytest -q"]},
            "commit": "abc123",
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }
    }


def test_projection_preserves_identity_and_evidence():
    witness = build_witness(trace())["aiwitness"]
    assert witness["provenance"]["trace_id"] == "TRACE-001"
    assert witness["provenance"]["execution_id"] == "EXEC-001"
    assert witness["provenance"]["handoff_id"] == "SH-HO-001"
    assert witness["provenance"]["evidence_ids"] == ["EVIDENCE-001"]
    assert witness["observation"]["verification_status"] == "pass"


def test_projection_cannot_propagate_authority():
    payload = trace()
    payload["codex_traceability"]["authority"]["merge_authorized"] = True
    try:
        build_witness(payload)
    except ValueError as exc:
        assert "authority.merge_authorized" in str(exc)
    else:
        raise AssertionError("authority must not propagate")


def test_projection_requires_human_gate():
    payload = trace()
    payload["codex_traceability"]["human_gate"]["required"] = False
    try:
        build_witness(payload)
    except ValueError as exc:
        assert "human_gate.required" in str(exc)
    else:
        raise AssertionError("human gate must remain required")


def test_projection_preserves_milestones_and_branches():
    payload = trace()
    payload["milestone_map"] = {
        "current_milestone_id": "API_V1",
        "milestones": [
            {"id": "CORE", "status": "complete"},
            {"id": "API_V1", "status": "complete"},
            {"id": "EXTERNAL_HANDOFF", "status": "pending"},
        ],
        "decision_points": [
            {
                "id": "NEXT_01",
                "at_milestone": "API_V1",
                "options": [
                    {"id": "HANDOFF", "label": "external handoff"},
                    {"id": "RESEARCH", "label": "additional research"},
                ],
                "selected_option_id": None,
            }
        ],
    }
    witness = build_witness(payload)["aiwitness"]
    assert witness["milestone_map"]["current_milestone_id"] == "API_V1"
    assert len(witness["milestone_map"]["milestones"]) == 3
    assert witness["milestone_map"]["decision_points"][0]["options"][0]["id"] == "HANDOFF"
    assert witness["milestone_map"]["selection_authority"] == "human_gate"


def test_projection_rejects_unattributed_branch_selection():
    payload = trace()
    payload["milestone_map"] = {
        "current_milestone_id": "API_V1",
        "milestones": [],
        "decision_points": [
            {
                "id": "NEXT_01",
                "options": [{"id": "HANDOFF"}],
                "selected_option_id": "HANDOFF",
                "selection_authority": "aiwitness",
            }
        ],
    }
    try:
        build_witness(payload)
    except ValueError as exc:
        assert "human_gate" in str(exc)
    else:
        raise AssertionError("AIwitness must not claim branch selection")
