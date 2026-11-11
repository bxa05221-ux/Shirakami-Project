import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_completion_integrity import validate


def base():
    return {"requirements": [
        {
            "requirement_id": "R-001",
            "status": "verified",
            "evidence_ids": ["E-001"],
            "verification_source": "ci:test",
        },
        {
            "requirement_id": "R-002",
            "status": "unverified",
            "evidence_ids": [],
        },
    ]}


def test_completion_is_evidence_backed_not_a_percentage():
    result = validate(base())
    assert result["requirements_total"] == 2
    assert result["verified"] == 1
    assert result["unverified"] == 1
    assert result["completion_percent"] is None
    assert result["human_gate_required"] is True
    assert result["authority"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
    }


def test_ai_self_assessed_completion_is_rejected():
    document = base()
    document["completion_percent"] = 80
    with pytest.raises(ValueError, match="self-assessed"):
        validate(document)


def test_verified_requires_evidence():
    document = base()
    document["requirements"][0]["evidence_ids"] = []
    with pytest.raises(ValueError, match="evidence_ids"):
        validate(document)


def test_verified_requires_verification_source():
    document = base()
    document["requirements"][0].pop("verification_source")
    with pytest.raises(ValueError, match="verification_source"):
        validate(document)
