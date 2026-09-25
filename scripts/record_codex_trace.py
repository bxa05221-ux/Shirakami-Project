#!/usr/bin/env python3
"""Create a pending trace artifact directly from a Semantic Handoff."""

from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def build_trace(document: dict, trace_id: str) -> dict:
    handoff = document.get("semantic_handoff")
    if not isinstance(handoff, dict):
        raise ValueError("invalid Semantic Handoff root")
    if handoff.get("status") not in {"ready", "in_progress"}:
        raise ValueError("handoff status is not consumable")
    gate = handoff.get("human_gate", {})
    if gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")

    return {
        "codex_traceability": {
            "version": "0.1",
            "trace_id": trace_id,
            "source_handoff_id": handoff["id"],
            "evidence_ids": list(handoff.get("evidence", {}).get("evidence_ids", [])),
            "result": {
                "status": "pending",
                "changed_paths": [],
                "observations": [],
                "deviations": [],
            },
            "verification": {"status": "pending", "tests": []},
            "commit": None,
            "authority": {
                "execution_authorized": False,
                "publish_authorized": False,
                "merge_authorized": False,
            },
            "human_gate": {"required": True, "decision": "pending"},
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--trace-id", required=True)
    args = parser.parse_args()

    document = yaml.safe_load(args.handoff.read_text(encoding="utf-8"))
    trace = build_trace(document or {}, args.trace_id)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(trace, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Created pending trace: {args.output}")
    print("Trace creation does not grant execution, publish, or merge authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
