import sys
from pathlib import Path

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from validate_project_handoff import validate


FIXTURE = Path(__file__).resolve().parents[1] / "handoff" / "project-to-project-validation-example.yaml"


def load_fixture():
    return yaml.safe_load(FIXTURE.read_text(encoding="utf-8"))


def test_project_handoff_preserves_semantic_boundary():
    result = validate(load_fixture())
    assert result == {
        "required_context_complete": True,
        "provenance_present": True,
        "authority_preserved": True,
        "human_gate_preserved": True,
        "unresolved_questions_preserved": True,
        "reconstruction_state": "verification_ready",
    }


def test_missing_context_is_rejected():
    document = load_fixture()
    document["project_handoff_validation"]["required_context"].remove("evidence")
    with pytest.raises(ValueError, match="missing required context"):
        validate(document)


def test_authority_cannot_cross_handoff_boundary():
    document = load_fixture()
    document["project_handoff_validation"]["authority"]["merge_authorized"] = True
    with pytest.raises(ValueError, match="authority boundary"):
        validate(document)


def test_unresolved_questions_must_survive():
    document = load_fixture()
    document["project_handoff_validation"]["unresolved_questions"]["preserved"] = False
    with pytest.raises(ValueError, match="unresolved questions"):
        validate(document)
