#!/usr/bin/env python3
"""Convert a validated RuntimeResult into an auditable EvidenceRecord."""
from __future__ import annotations

import argparse
from pathlib import Path
import hashlib
import yaml


def build_evidence(runtime_result: dict) -> dict:
    result = runtime_result.get("runtime_result")
    if not isinstance(result, dict):
        raise ValueError("missing runtime_result")
    for key in ("handoff_id", "provider", "output", "evidence_ids"):
        if key not in result:
            raise ValueError(f"{key} is required")
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if result.get(key) is not False:
            raise ValueError(f"{key} must remain false")
    if result.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    canonical = yaml.safe_dump(result, allow_unicode=True, sort_keys=True)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    evidence_id = f"EVIDENCE-{digest[:16]}"

    return {"evidence_record": {
        "version": "0.1",
        "evidence_id": evidence_id,
        "kind": "runtime_observation",
        "source": {
            "handoff_id": result["handoff_id"],
            "trace_id": result.get("trace_id"),
            "execution_id": result.get("execution_id"),
            "provider": result["provider"],
        },
        "observed": {"output": result["output"]},
        "input_evidence_ids": list(result["evidence_ids"]),
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
    }}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("runtime_result", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    payload = yaml.safe_load(args.runtime_result.read_text(encoding="utf-8"))
    record = build_evidence(payload or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(record, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created EvidenceRecord: {record['evidence_record']['evidence_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
