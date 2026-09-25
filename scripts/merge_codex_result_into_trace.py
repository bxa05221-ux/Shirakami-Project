#!/usr/bin/env python3
"""Merge an observed Codex Result into its originating Trace."""

from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def merge(trace: dict, result: dict) -> dict:
    t = trace.get("codex_traceability")
    r = result.get("codex_result")
    if not isinstance(t, dict) or not isinstance(r, dict):
        raise ValueError("invalid trace or result root")

    if t.get("source_handoff_id") != r.get("source_handoff_id"):
        raise ValueError("source_handoff_id mismatch")

    trace_evidence = list(t.get("evidence_ids", []))
    result_evidence = list(r.get("evidence_ids", trace_evidence))
    if result_evidence != trace_evidence:
        raise ValueError("evidence_ids mismatch")

    t["result"] = {
        "status": r["status"],
        "changed_paths": list(r["result"]["changed_paths"]),
        "observations": list(r["result"]["observations"]),
        "deviations": list(r["result"]["deviations"]),
    }
    t["verification"] = {
        "status": r["verification"]["status"],
        "tests": list(r["verification"]["tests"]),
    }
    t["commit"] = r.get("commit")

    # Result data can never elevate authority.
    t["authority"] = {
        "execution_authorized": False,
        "publish_authorized": False,
        "merge_authorized": False,
    }
    t["human_gate"] = {
        "required": True,
        "decision": r.get("human_gate", {}).get("decision", "pending"),
    }
    return trace


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("result", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()

    trace = yaml.safe_load(args.trace.read_text(encoding="utf-8"))
    result = yaml.safe_load(args.result.read_text(encoding="utf-8"))
    merged = merge(trace or {}, result or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(merged, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Merged Codex Result into trace: {args.output}")
    print("Result merge does not grant execution, publish, or merge authority.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
