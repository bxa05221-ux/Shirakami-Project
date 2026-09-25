#!/usr/bin/env python3
"""Convert a human-approved Candidate into a reviewable Protocol proposal."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def build_protocol(candidate_document: dict, approval: dict) -> dict:
    candidate = candidate_document.get("candidate")
    if not isinstance(candidate, dict):
        raise ValueError("missing candidate")
    if approval.get("source") != "human_gate" or approval.get("approved") is not True:
        raise ValueError("explicit human approval is required")
    if candidate.get("candidate_state") != "review_required":
        raise ValueError("candidate must be review_required")
    if not candidate.get("evidence_ids"):
        raise ValueError("evidence_ids are required")
    return {"protocol": {
        "version": "0.1",
        "protocol_id": f"PROTOCOL-FROM-{candidate['candidate_id']}",
        "source_candidate_id": candidate["candidate_id"],
        "evidence_ids": list(candidate["evidence_ids"]),
        "proposal": candidate.get("proposal", {}),
        "validation": candidate.get("validation", {}),
        "protocol_state": "approved_for_runtime_review",
        "approval": {"source": "human_gate", "approved": True},
        "authority": {"execution_authorized": False, "publish_authorized": False, "merge_authorized": False, "human_gate_required": True},
    }}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--approval", required=True)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    candidate = yaml.safe_load(args.candidate.read_text(encoding="utf-8"))
    approval = yaml.safe_load(args.approval)
    protocol = build_protocol(candidate or {}, approval or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(protocol, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created protocol proposal: {protocol['protocol']['protocol_id']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
