#!/usr/bin/env python3
"""Create a reviewable candidate from a Semantic Handoff without granting authority."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml

REQUIRED = ("candidate_id", "source_handoff_id", "evidence_ids", "proposal", "validation")


def build_candidate(handoff_document: dict, candidate_id: str, proposal: dict, validation: dict) -> dict:
    handoff = handoff_document.get("semantic_handoff")
    if not isinstance(handoff, dict):
        raise ValueError("missing semantic_handoff")
    if not handoff.get("handoff_id"):
        raise ValueError("handoff_id is required")
    evidence_ids = handoff.get("evidence_ids")
    if not evidence_ids:
        raise ValueError("evidence_ids are required")
    if validation.get("status") not in ("pass", "review_required"):
        raise ValueError("validation.status must be pass or review_required")

    candidate = {
        "candidate": {
            "candidate_id": candidate_id,
            "source_handoff_id": handoff["handoff_id"],
            "evidence_ids": list(evidence_ids),
            "proposal": proposal,
            "validation": validation,
            "candidate_state": "review_required",
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            },
        }
    }
    missing = [key for key in REQUIRED if key not in candidate["candidate"]]
    if missing:
        raise ValueError(f"missing candidate fields: {missing}")
    return candidate


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--proposal", required=True)
    parser.add_argument("--validation", required=True)
    args = parser.parse_args()
    handoff = yaml.safe_load(args.handoff.read_text(encoding="utf-8"))
    proposal = yaml.safe_load(args.proposal)
    validation = yaml.safe_load(args.validation)
    result = build_candidate(handoff or {}, args.candidate_id, proposal or {}, validation or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created review candidate: {args.candidate_id}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
