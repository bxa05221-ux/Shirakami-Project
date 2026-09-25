"""Validate the provider-neutral API boundary contract.

The contract is descriptive and traceable. It must never create execution,
publication, or merge authority.
"""

from pathlib import Path
import yaml


FALSE_AUTHORITY = (
    "execution_authorized",
    "publish_authorized",
    "merge_authorized",
)


def validate(contract: dict) -> dict:
    root = contract.get("api_boundary")
    if not isinstance(root, dict):
        raise ValueError("missing api_boundary")

    if root.get("version") != "0.1":
        raise ValueError("unsupported contract version")

    required = root.get("input", {}).get("required", [])
    expected_required = {
        "handoff_id",
        "project",
        "objective",
        "protocol_ids",
        "evidence_ids",
        "verification_scope",
    }
    if set(required) != expected_required:
        raise ValueError("required input fields do not match contract")

    authority = root.get("authority", {})
    for field in FALSE_AUTHORITY:
        if authority.get(field) is not False:
            raise ValueError(f"{field} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must be true")

    output = root.get("output", {})
    if set(output.get("must_preserve", [])) != {
        "handoff_id",
        "trace_id",
        "evidence_ids",
    }:
        raise ValueError("traceability preservation contract changed")

    forbidden = set(output.get("must_not_infer", []))
    if forbidden != set(FALSE_AUTHORITY):
        raise ValueError("authority inference boundary changed")

    if root.get("verification", {}).get("rule") != "一変更一検証":
        raise ValueError("verification rule changed")

    return {
        "valid": True,
        "authority": {field: False for field in FALSE_AUTHORITY},
        "human_gate_required": True,
    }


def main() -> None:
    path = Path(__file__).resolve().parents[1] / "api" / "API_BOUNDARY_CONTRACT.yaml"
    with path.open(encoding="utf-8") as handle:
        contract = yaml.safe_load(handle)
    print(validate(contract))


if __name__ == "__main__":
    main()
