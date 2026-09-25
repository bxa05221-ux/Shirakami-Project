from pathlib import Path
import sys

import pytest
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from validate_api_boundary import validate


def load_contract():
    path = Path(__file__).resolve().parents[1] / "api" / "API_BOUNDARY_CONTRACT.yaml"
    with path.open(encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_api_boundary_contract_is_valid():
    result = validate(load_contract())
    assert result["valid"] is True
    assert result["authority"] == {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
    }
    assert result["human_gate_required"] is True


@pytest.mark.parametrize(
    "field",
    ["execution_authorized", "publish_authorized", "merge_authorized"],
)
def test_authority_cannot_be_enabled_by_contract(field):
    contract = load_contract()
    contract["api_boundary"]["authority"][field] = True
    with pytest.raises(ValueError, match=field):
        validate(contract)


def test_traceability_fields_are_preserved():
    contract = load_contract()
    assert set(contract["api_boundary"]["output"]["must_preserve"]) == {
        "handoff_id",
        "trace_id",
        "evidence_ids",
    }


def test_authority_inference_fields_are_forbidden():
    contract = load_contract()
    assert set(contract["api_boundary"]["output"]["must_not_infer"]) == {
        "execution_authorized",
        "publish_authorized",
        "merge_authorized",
    }
