from pathlib import Path
import copy
import yaml
import pytest

from validate_aiwitness_boundary import validate

CONTRACT = Path(__file__).parents[1] / "aiwitness" / "AIWITNESS_BOUNDARY_CONTRACT.yaml"


def load_contract():
    with CONTRACT.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_aiwitness_boundary_contract_is_valid():
    validate(load_contract())


@pytest.mark.parametrize(
    "field",
    ["execution_authorized", "publish_authorized", "merge_authorized"],
)
def test_aiwitness_rejects_authority_propagation(field):
    data = load_contract()
    data["aiwitness"]["authority"][field] = True
    with pytest.raises(ValueError, match="must remain false"):
        validate(data)


def test_aiwitness_requires_human_gate():
    data = load_contract()
    data["aiwitness"]["authority"]["human_gate_required"] = False
    with pytest.raises(ValueError, match="human_gate_required"):
        validate(data)


def test_aiwitness_rejects_verification_as_authority():
    data = load_contract()
    data["aiwitness"]["integrity"]["forbidden"] = [
        rule
        for rule in data["aiwitness"]["integrity"]["forbidden"]
        if "theory proof" not in rule
    ]
    with pytest.raises(ValueError, match="integrity forbidden"):
        validate(data)


def test_aiwitness_preserves_required_input_identity():
    data = load_contract()
    required = set(data["aiwitness"]["input"]["required"])
    assert {"trace_id", "execution_id", "handoff_id", "evidence_ids"} <= required
