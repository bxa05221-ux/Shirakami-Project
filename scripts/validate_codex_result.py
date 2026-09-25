"""Validate a Codex execution result without granting authority."""

from __future__ import annotations

import sys
import yaml


ALLOWED_STATUS = {"pending", "completed", "blocked", "failed"}
ALLOWED_VERIFICATION = {"pending", "passed", "failed", "not_run"}


def validate(payload: dict) -> list[str]:
    errors: list[str] = []
    root = payload.get("codex_result")
    if not isinstance(root, dict):
        return ["missing codex_result"]

    if not root.get("source_handoff_id"):
        errors.append("source_handoff_id is required")

    if root.get("status") not in ALLOWED_STATUS:
        errors.append("invalid result status")

    result = root.get("result")
    if not isinstance(result, dict):
        errors.append("result is required")
    else:
        for key in ("changed_paths", "observations", "deviations"):
            if not isinstance(result.get(key), list):
                errors.append(f"result.{key} must be a list")

    verification = root.get("verification")
    if not isinstance(verification, dict):
        errors.append("verification is required")
    else:
        if verification.get("status") not in ALLOWED_VERIFICATION:
            errors.append("invalid verification status")
        if not isinstance(verification.get("tests"), list):
            errors.append("verification.tests must be a list")

    authority = root.get("authority")
    if not isinstance(authority, dict):
        errors.append("authority is required")
    else:
        for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
            if authority.get(key) is not False:
                errors.append(f"authority.{key} must remain false")

    gate = root.get("human_gate")
    if not isinstance(gate, dict):
        errors.append("human_gate is required")
    else:
        if gate.get("required") is not True:
            errors.append("human_gate.required must remain true")
        if gate.get("decision") not in {"pending", "approved", "rejected"}:
            errors.append("invalid human_gate decision")

    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: validate_codex_result.py RESULT.yaml")
        return 2
    with open(sys.argv[1], encoding="utf-8") as handle:
        payload = yaml.safe_load(handle)
    errors = validate(payload or {})
    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1
    print("Codex result contract valid; authority remains with Human Gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
