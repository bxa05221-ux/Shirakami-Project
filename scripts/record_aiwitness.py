#!/usr/bin/env python3
"""Project a completed execution trace into the provider-neutral AIwitness layer.

The projection preserves provenance and verification facts. It never grants
execution, publish, or merge authority.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import yaml


ALLOWED_TRACE_VERIFICATION = {"pending", "passed", "failed", "not_run"}


def build_witness(trace_document: dict) -> dict:
    trace = trace_document.get("codex_traceability")
    if not isinstance(trace, dict):
        raise ValueError("missing codex_traceability")

    required = ("trace_id", "execution_id", "source_handoff_id", "evidence_ids")
    for key in required:
        if not trace.get(key):
            raise ValueError(f"{key} is required")

    verification = trace.get("verification")
    if not isinstance(verification, dict):
        raise ValueError("verification is required")

    status = verification.get("status")
    if status not in ALLOWED_TRACE_VERIFICATION:
        raise ValueError("invalid trace verification status")

    authority = trace.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority is required")

    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            raise ValueError(f"authority.{key} must remain false")

    gate = trace.get("human_gate")
    if not isinstance(gate, dict) or gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")

    milestone_map = trace_document.get("milestone_map")
    if milestone_map is not None:
        if not isinstance(milestone_map, dict):
            raise ValueError("milestone_map must be a mapping")
        current = milestone_map.get("current_milestone_id")
        milestones = milestone_map.get("milestones", [])
        decision_points = milestone_map.get("decision_points", [])
        if current is not None and not isinstance(current, str):
            raise ValueError("milestone_map.current_milestone_id must be a string or null")
        if not isinstance(milestones, list) or not isinstance(decision_points, list):
            raise ValueError("milestone_map lists are required")
        for point in decision_points:
            if not isinstance(point, dict):
                raise ValueError("decision_points must contain mappings")
            if "options" not in point or not isinstance(point["options"], list):
                raise ValueError("decision point options are required")
            if point.get("selected_option_id") is not None and point.get("selection_authority") != "human_gate":
                raise ValueError("branch selection must be attributed to human_gate")
        milestone_projection = {
            "current_milestone_id": current,
            "milestones": milestones,
            "decision_points": decision_points,
            "selection_authority": "human_gate",
        }
    else:
        milestone_projection = None

    return {
        "aiwitness": {
            "version": "0.1",
            "status": "observed",
            "provenance": {
                "trace_id": trace["trace_id"],
                "execution_id": trace["execution_id"],
                "handoff_id": trace["source_handoff_id"],
                "evidence_ids": list(trace["evidence_ids"]),
                "commit": trace.get("commit"),
            },
            "observation": {
                "verification_status": (
                    "pending" if status == "pending"
                    else "pass" if status == "passed"
                    else "fail" if status == "failed"
                    else "pending"
                ),
                "verification_uncertainty": None,
                "verification_observed": {
                    "status": status,
                    "tests": list(verification.get("tests", [])),
                },
            },
            "milestone_map": milestone_projection,
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
                "human_gate_required": True,
            },
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    trace = yaml.safe_load(args.trace.read_text(encoding="utf-8"))
    witness = build_witness(trace or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(witness, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Created AIwitness observation: {args.output}")
    print("AIwitness projection preserves provenance; authority remains with Human Gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
