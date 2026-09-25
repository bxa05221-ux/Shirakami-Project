#!/usr/bin/env python3
"""Project an EvidenceRecord into AIwitness as an observed fact."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def build_witness(evidence_document: dict) -> dict:
    record = evidence_document.get("evidence_record")
    if not isinstance(record, dict):
        raise ValueError("missing evidence_record")
    for key in ("evidence_id", "source", "observed", "input_evidence_ids"):
        if key not in record:
            raise ValueError(f"{key} is required")
    source = record["source"]
    for key in ("handoff_id", "provider"):
        if not source.get(key):
            raise ValueError(f"source.{key} is required")
    authority = record.get("authority")
    if not isinstance(authority, dict):
        raise ValueError("authority is required")
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            raise ValueError(f"authority.{key} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    return {"aiwitness": {
        "version": "0.1",
        "status": "observed",
        "provenance": {
            "evidence_id": record["evidence_id"],
            "handoff_id": source["handoff_id"],
            "trace_id": source.get("trace_id"),
            "execution_id": source.get("execution_id"),
            "provider": source["provider"],
            "input_evidence_ids": list(record["input_evidence_ids"]),
        },
        "observation": {
            "kind": record.get("kind", "runtime_observation"),
            "output": record["observed"].get("output"),
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
    parser.add_argument("evidence", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    args = parser.parse_args()
    payload = yaml.safe_load(args.evidence.read_text(encoding="utf-8"))
    witness = build_witness(payload or {})
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(witness, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Projected EvidenceRecord into AIwitness: {witness['aiwitness']['provenance']['evidence_id']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
