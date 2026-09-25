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

    required = ("trace_id", "source_handoff_id", "evidence_ids")
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

    return {
        "aiwitness": {
            "version": "0.1",
            "status": "observed",
            "provenance": {
                "trace_id": trace["trace_id"],
                "execution_id": trace["trace_id"],
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
