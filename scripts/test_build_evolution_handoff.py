from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_evolution_handoff import build_handoff


def evidence():
    return {"evidence_record": {"evidence_id": "EVIDENCE-001"}}


def witness():
    return {"aiwitness": {
        "provenance": {"trace_id": "TR-001", "execution_id": "EX-001", "evidence_ids": ["EVIDENCE-001"]},
        "observation": {"verification_status": "pass"},
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False, "human_gate_required": True},
    }}


def test_evidence_returns_to_handoff():
    handoff = build_handoff(evidence(), witness(), "generate next candidate")["semantic_handoff"]
    assert handoff["handoff_id"] == "HANDOFF-FROM-EVIDENCE-001"
    assert handoff["source"]["trace_id"] == "TR-001"
    assert handoff["evidence_ids"] == ["EVIDENCE-001"]
    assert handoff["next_step"] == "candidate_generation"


def test_unrepresented_evidence_is_rejected():
    w = witness()
    w["aiwitness"]["provenance"]["evidence_ids"] = []
    with pytest.raises(ValueError, match="not represented"):
        build_handoff(evidence(), w, "next")


def test_handoff_cannot_gain_authority():
    w = witness()
    w["aiwitness"]["authority"]["merge_authorized"] = True
    with pytest.raises(ValueError, match="merge_authorized"):
        build_handoff(evidence(), w, "next")
