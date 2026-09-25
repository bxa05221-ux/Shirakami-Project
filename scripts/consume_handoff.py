#!/usr/bin/env python3
"""Convert a Shirakami Semantic Handoff into a deterministic Codex execution context."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import yaml


REQUIRED = (
    ("semantic_handoff", "id"),
    ("semantic_handoff", "status"),
    ("semantic_handoff", "project"),
    ("semantic_handoff", "objective"),
    ("semantic_handoff", "protocol"),
    ("semantic_handoff", "evidence"),
    ("semantic_handoff", "repository"),
    ("semantic_handoff", "change"),
    ("semantic_handoff", "verification"),
    ("semantic_handoff", "human_gate"),
)


def require(mapping, path):
    value = mapping
    for key in path:
        if not isinstance(value, dict) or key not in value:
            raise ValueError("missing required field: " + ".".join(path))
        value = value[key]
    return value


def consume(path: Path) -> dict:
    document = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(document, dict) or "semantic_handoff" not in document:
        raise ValueError("invalid Semantic Handoff root")

    handoff = document["semantic_handoff"]
    for root, key in REQUIRED:
        require(document, (root, key))

    status = handoff["status"]
    if status not in {"ready", "in_progress"}:
        raise ValueError(f"handoff status is not consumable: {status}")

    human_gate = handoff["human_gate"]
    if human_gate.get("required") is not True:
        raise ValueError("human_gate.required must remain true")

    result = {
        "source_handoff_id": handoff["id"],
        "project": handoff["project"],
        "objective": handoff["objective"].strip(),
        "protocols": handoff["protocol"].get("applicable", []),
        "evidence_ids": handoff["evidence"].get("evidence_ids", []),
        "provenance": handoff["evidence"].get("provenance", []),
        "repository": handoff["repository"],
        "requested_change": handoff["change"].get("requested", "").strip(),
        "constraints": handoff["change"].get("constraints", []),
        "out_of_scope": handoff["change"].get("out_of_scope", []),
        "verification": handoff["verification"],
        "unresolved_questions": handoff.get("unresolved_questions", []),
        "authority": {
            "execution_authorized": False,
            "publish_authorized": False,
            "merge_authorized": False,
            "human_gate_required": True,
            "human_gate_decision": human_gate.get("decision", "pending"),
        },
    }

    result["next_action"] = (
        "Inspect the local repository and identify the smallest implementation "
        "change within the requested scope; do not publish or merge."
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("handoff", type=Path)
    parser.add_argument("-o", "--output", type=Path)
    args = parser.parse_args()

    context = consume(args.handoff)
    payload = json.dumps(context, ensure_ascii=False, indent=2) + "\n"

    if args.output:
        args.output.write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
