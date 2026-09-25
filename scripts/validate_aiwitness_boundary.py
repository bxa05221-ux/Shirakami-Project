#!/usr/bin/env python3
"""Validate the Shirakami AIwitness boundary contract."""

from pathlib import Path
import yaml

CONTRACT = Path("aiwitness/AIWITNESS_BOUNDARY_CONTRACT.yaml")

REQUIRED_INPUT = {
    "trace_id",
    "execution_id",
    "handoff_id",
    "evidence_ids",
    "verification_status",
}
ALLOWED_STATUS = {"pending", "pass", "fail"}


def validate(data: dict) -> None:
    root = data.get("aiwitness")
    if not isinstance(root, dict):
        raise ValueError("missing aiwitness root")

    if root.get("version") != "0.1":
        raise ValueError("unsupported aiwitness version")

    if root.get("status") != "design_boundary":
        raise ValueError("unexpected aiwitness status")

    inputs = root.get("input")
    if not isinstance(inputs, dict):
        raise ValueError("missing input section")
    required = set(inputs.get("required", []))
    if required != REQUIRED_INPUT:
        raise ValueError("input required fields do not match boundary")

    observation = root.get("observation")
    if not isinstance(observation, dict):
        raise ValueError("missing observation section")
    if set(str(observation.get("verification_status", "")).split(" | ")) != ALLOWED_STATUS:
        raise ValueError("verification status vocabulary must be pending | pass | fail")

    authority = root.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("missing authority section")
    for field in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(field) is not False:
            raise ValueError(f"{field} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    integrity = root.get("integrity")
    if not isinstance(integrity, dict):
        raise ValueError("missing integrity section")
    forbidden = set(integrity.get("forbidden", []))
    expected_forbidden = {
        "AIwitness may not modify the source execution trace.",
        "AIwitness may not grant authority.",
        "AIwitness may not silently replace Evidence with inference.",
        "AIwitness may not convert a passing test into theory proof.",
    }
    if forbidden != expected_forbidden:
        raise ValueError("integrity forbidden rules changed")

    verification = root.get("verification")
    if not isinstance(verification, dict) or verification.get("rule") != "一変更一検証":
        raise ValueError("verification rule must be 一変更一検証")


def main() -> None:
    with CONTRACT.open(encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    validate(data)
    print(f"AIwitness boundary contract valid: {CONTRACT}")


if __name__ == "__main__":
    main()
