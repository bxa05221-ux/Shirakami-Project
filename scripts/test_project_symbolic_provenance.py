from project_symbolic_provenance import project_symbolic_provenance


def witness():
    return {"aiwitness": {"provenance": {"evidence_ids": ["EVIDENCE-001"]}, "observation": {"verification_observed": {}}}}


def symbolic():
    return {
        "link_id": "link-01",
        "request_id": "reobs-01",
        "source_observation_id": "obs-01",
        "result_observation_id": "obs-02",
        "symbol_id": "symbol-life",
        "expression": "生きろ",
        "interpretations": ["survival", "renewal", "continuation"],
        "context_refs": ["ctx-01"],
    }


def test_symbolic_provenance_preserves_evidence_identity():
    result = project_symbolic_provenance(witness(), symbolic())
    assert result["aiwitness"]["provenance"]["evidence_ids"] == ["EVIDENCE-001"]
    assert result["aiwitness"]["observation"]["verification_observed"]["symbolic_provenance"]["symbol_id"] == "symbol-life"


def test_symbolic_record_cannot_become_evidence():
    payload = symbolic()
    payload["evidence_id"] = "EVIDENCE-FAKE"
    try:
        project_symbolic_provenance(witness(), payload)
    except ValueError as exc:
        assert "evidence_id" in str(exc)
    else:
        raise AssertionError("symbolic interpretation must not become evidence")
