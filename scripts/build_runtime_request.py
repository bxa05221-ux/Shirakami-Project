#!/usr/bin/env python3
"""Project provider-neutral API Context into a Runtime Adapter request.

The adapter request describes a runtime target and preserves provenance.
It never grants execution, publication, or merge authority.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import yaml

FALSE_AUTHORITY = (
    "execution_authorized",
    "publish_authorized",
    "merge_authorized",
)


def build_runtime_request(api_document: dict, runtime_target: str | None = None) -> dict:
    context = api_document.get("api_context")
    if not isinstance(context, dict):
        raise ValueError("missing api_context")

    required = (
        "handoff_id",
        "project",
        "objective",
        "protocol_ids",
        "evidence_ids",
        "verification_scope",
    )
    for key in required:
        if key not in context:
            raise ValueError(f"{key} is required")

    authority = context.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority is required")
    for key in FALSE_AUTHORITY:
        if authority.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    return {
        "runtime_request": {
            "version": "0.1",
            "handoff_id": context["handoff_id"],
            "trace_id": context.get("trace_id"),
            "execution_id": context.get("execution_id"),
            "project": context["project"],
            "objective": context["objective"],
            "protocol_ids": list(context["protocol_ids"]),
            "evidence_ids": list(context["evidence_ids"]),
            "verification_scope": context["verification_scope"],
            "verification": dict(context.get("verification", {})),
            "runtime_target": runtime_target,
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
    parser.add_argument("api_context", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--runtime-target")
    args = parser.parse_args()

    document = yaml.safe_load(args.api_context.read_text(encoding="utf-8"))
    result = build_runtime_request(document or {}, args.runtime_target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        yaml.safe_dump(result, allow_unicode=True, sort_keys=False),
        encoding="utf-8",
    )
    print(f"Created runtime adapter request: {args.output}")
    print("Runtime adapter request preserves provenance; authority remains with Human Gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
