#!/usr/bin/env python3
"""Project a human-approved Protocol into a provider-neutral RuntimeRequest."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def build_protocol_runtime_request(protocol_document: dict, runtime_target: str | None = None) -> dict:
    protocol = protocol_document.get("protocol")
    if not isinstance(protocol, dict):
        raise ValueError("missing protocol")
    if protocol.get("protocol_state") != "approved_for_runtime_review":
        raise ValueError("protocol is not approved for runtime review")
    approval = protocol.get("approval")
    if not isinstance(approval, dict) or approval.get("source") != "human_gate" or approval.get("approved") is not True:
        raise ValueError("explicit human approval is required")
    if not protocol.get("evidence_ids"):
        raise ValueError("evidence_ids are required")
    authority = protocol.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority is required")
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    return {"runtime_request": {
        "version": "0.1",
        "request_id": f"RUNTIME-FROM-{protocol['protocol_id']}",
        "protocol_ids": [protocol["protocol_id"]],
        "evidence_ids": list(protocol["evidence_ids"]),
        "proposal": protocol.get("proposal", {}),
        "validation": protocol.get("validation", {}),
        "runtime_target": runtime_target,
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("protocol", type=Path)
    parser.add_argument("--runtime-target")
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    document = yaml.safe_load(args.protocol.read_text(encoding="utf-8"))
    result = build_protocol_runtime_request(document or {}, args.runtime_target)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(result, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created runtime request: {result['runtime_request']['request_id']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
