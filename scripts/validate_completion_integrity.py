#!/usr/bin/env python3
"""Validate evidence-backed completion state without accepting AI self-assessed percentages."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

FORBIDDEN = {"completion_percent", "overall_completion", "confidence_as_completion"}
ALLOWED_STATUS = {"verified", "unverified", "blocked", "not_applicable"}


def validate(document: dict) -> dict:
    if not isinstance(document, dict):
        raise ValueError("document must be a mapping")

    if FORBIDDEN.intersection(document):
        raise ValueError("AI self-assessed completion fields are forbidden")

    requirements = document.get("requirements")
    if not isinstance(requirements, list) or not requirements:
        raise ValueError("requirements must be a non-empty list")

    verified = 0
    counts = {status: 0 for status in ALLOWED_STATUS}

    for item in requirements:
        if not isinstance(item, dict):
            raise ValueError("each requirement must be a mapping")
        requirement_id = item.get("requirement_id")
        status = item.get("status")
        evidence_ids = item.get("evidence_ids", [])

        if not requirement_id:
            raise ValueError("requirement_id is required")
        if status not in ALLOWED_STATUS:
            raise ValueError(f"invalid status for {requirement_id}: {status}")
        if not isinstance(evidence_ids, list):
            raise ValueError(f"evidence_ids must be a list: {requirement_id}")

        if status == "verified":
            if not evidence_ids:
                raise ValueError(f"verified requirement requires evidence_ids: {requirement_id}")
            if not item.get("verification_source"):
                raise ValueError(f"verified requirement requires verification_source: {requirement_id}")
            verified += 1

        counts[status] += 1

    return {
        "requirements_total": len(requirements),
        "verified": verified,
        "unverified": counts["unverified"],
        "blocked": counts["blocked"],
        "not_applicable": counts["not_applicable"],
        "verification_state": "evidence_backed",
        "completion_percent": None,
        "human_gate_required": True,
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
        },
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
