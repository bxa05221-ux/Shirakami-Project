#!/usr/bin/env python3
"""Build the next Semantic Handoff from verified EvidenceRecord/AIwitness observations."""
from __future__ import annotations

import argparse
from pathlib import Path
import yaml


def build_handoff(evidence_document: dict, witness_document: dict, objective: str) -> dict:
    evidence = evidence_document.get("evidence_record")
    witness = witness_document.get("aiwitness")
    if not isinstance(evidence, dict):
        raise ValueError("missing evidence_record")
    if not isinstance(witness, dict):
        raise ValueError("missing aiwitness")

    evidence_id = evidence.get("evidence_id")
    if not evidence_id:
        raise ValueError("evidence_id is required")
    provenance = witness.get("provenance", {})
    if provenance.get("evidence_ids") is None:
        raise ValueError("AIwitness evidence_ids are required")
    if evidence_id not in provenance["evidence_ids"]:
        raise ValueError("EvidenceRecord is not represented by AIwitness")

    authority = witness.get("authority", {})
    for key in ("execution_authorized", "publish_authorized", "merge_authorized"):
        if authority.get(key) is not False:
            raise ValueError(f"authority.{key} must remain false")
    if authority.get("human_gate_required") is not True:
        raise ValueError("human_gate_required must remain true")

    return {"semantic_handoff": {
        "version": "0.1",
        "handoff_id": f"HANDOFF-FROM-{evidence_id}",
        "objective": objective,
        "source": {
            "evidence_id": evidence_id,
            "trace_id": provenance.get("trace_id"),
            "execution_id": provenance.get("execution_id"),
            "provider": provenance.get("provider"),
        },
        "evidence_ids": [evidence_id],
        "observation": witness.get("observation", {}),
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
        },
        "next_step": "candidate_generation",
    }}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("evidence", type=Path)
    parser.add_argument("witness", type=Path)
    parser.add_argument("-o", "--output", type=Path, required=True)
    parser.add_argument("--objective", required=True)
    args = parser.parse_args()
    evidence = yaml.safe_load(args.evidence.read_text(encoding="utf-8"))
    witness = yaml.safe_load(args.witness.read_text(encoding="utf-8"))
    handoff = build_handoff(evidence or {}, witness or {}, args.objective)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(yaml.safe_dump(handoff, allow_unicode=True, sort_keys=False), encoding="utf-8")
    print(f"Created next Semantic Handoff: {handoff['semantic_handoff']['handoff_id']}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
