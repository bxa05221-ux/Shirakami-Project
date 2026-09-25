from record_aiwitness import build_witness


def trace():
    return {
        "codex_traceability": {
            "version": "0.1",
            "trace_id": "TRACE-001",
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
