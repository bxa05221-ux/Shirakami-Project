#!/usr/bin/env python3
"""Validate the minimum semantic contract required for project-to-project handoff."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

REQUIRED_CONTEXT = {
    "objective",
    "protocol",
    "evidence",
    "repository",
    "change",
    "constraints",
    "unresolved_questions",
    "human_gate",
}


def validate(document: dict) -> dict:
    if not isinstance(document, dict):
        raise ValueError("document must be a mapping")

    package = document.get("project_handoff_validation")
    if not isinstance(package, dict):
        raise ValueError("project_handoff_validation is required")

    required_context = set(package.get("required_context", []))
    missing = sorted(REQUIRED_CONTEXT - required_context)
    if missing:
        raise ValueError(f"missing required context: {', '.join(missing)}")

    provenance = package.get("provenance")
    if not isinstance(provenance, dict):
        raise ValueError("provenance is required")
    if not provenance.get("source_handoff"):
        raise ValueError("source_handoff is required")
    if not provenance.get("evidence_ids"):
        raise ValueError("evidence_ids are required")

    authority = package.get("authority") or {}
    if any(authority.get(key) is not False for key in (
        "execution_authorized",
        "publish_authorized",
        "merge_authorized",
    )):
        raise ValueError("authority boundary must remain false")

    human_gate = package.get("human_gate") or {}
    if human_gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")

    unresolved = package.get("unresolved_questions") or {}
    if unresolved.get("preserved") is not True:
        raise ValueError("unresolved questions must be preserved")

    return {
        "required_context_complete": True,
        "provenance_present": True,
        "authority_preserved": True,
        "human_gate_preserved": True,
        "unresolved_questions_preserved": True,
        "reconstruction_state": "verification_ready",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("document", type=Path)
    args = parser.parse_args()
    document = yaml.safe_load(args.document.read_text(encoding="utf-8"))
    print(yaml.safe_dump(validate(document or {}), allow_unicode=True, sort_keys=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
