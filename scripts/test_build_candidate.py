from pathlib import Path
import sys
import pytest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from build_candidate import build_candidate


def handoff():
    return {"semantic_handoff": {
        "handoff_id": "HANDOFF-001", "evidence_ids": ["EVIDENCE-001"],
        "observation": {"verification_status": "pass"}
    }}


def test_candidate_is_reviewable_not_authoritative():
    c = build_candidate(handoff(), "CANDIDATE-001", {"change": "proposal"}, {"status": "pass"})["candidate"]
    assert c["candidate_state"] == "review_required"
    assert c["source_handoff_id"] == "HANDOFF-001"
    assert c["evidence_ids"] == ["EVIDENCE-001"]
    assert c["authority"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
        "human_gate_required": True,
    }


def test_validation_status_is_explicit():
    with pytest.raises(ValueError, match="validation.status"):
        build_candidate(handoff(), "CANDIDATE-002", {}, {"status": "unknown"})


def test_evidence_is_required():
    h = handoff()
    h["semantic_handoff"]["evidence_ids"] = []
    with pytest.raises(ValueError, match="evidence_ids"):
        build_candidate(h, "CANDIDATE-003", {}, {"status": "pass"})
