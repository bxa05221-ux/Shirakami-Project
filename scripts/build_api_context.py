#!/usr/bin/env python3
"""Project a verified Semantic Handoff trace into provider-neutral API context."""
from __future__ import annotations
import argparse
from pathlib import Path
import yaml

def build_context(trace_document: dict, project: str, objective: str, protocol_ids: list[str], verification_scope: str) -> dict:
    trace = trace_document.get("codex_traceability")
    if not isinstance(trace, dict):
        raise ValueError("missing codex_traceability")
    for key in ("trace_id", "execution_id", "source_handoff_id", "evidence_ids"):
        if key not in trace:
            raise ValueError(f"{key} is required")
    authority = trace.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority is required")
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    gate = trace.get("human_gate")
    if not isinstance(gate, dict) or gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")
    return {"api_context": {
        "version": "0.1",
        "handoff_id": trace["source_handoff_id"],
        "trace_id": trace["trace_id"],
        "execution_id": trace["execution_id"],
        "project": project,
        "objective": objective,
        "protocol_ids": list(protocol_ids),
        "evidence_ids": list(trace["evidence_ids"]),
        "verification_scope": verification_scope,
        "verification": {
            "status": trace.get("verification", {}).get("status", "pending"),
            "tests": list(trace.get("verification", {}).get("tests", [])),
        },
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }}

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("trace", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--project", required=True)
    parser.add_argument("--objective", required=True)
    parser.add_argument("--protocol-id", action="append", default=[])
    parser.add_argument("--verification-scope", required=True)
    args = parser.parse_args()
    trace = yaml.safe_load(args.trace.read_text(encoding="utf-8"))
    context = build_context(trace or {}, args.project, args.objective, args.protocol_id, args.verification_scope)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(context, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created API context: {args.output}")
    print("API context preserves provenance; it grants no authority.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
