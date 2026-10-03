"""Minimal serialization bridge between JOUMON Semantic Handoff and Matome YAML."""
from dataclasses import asdict
from typing import Any
import json
from joumon_semantic_handoff import SemanticHandoff


def handoff_to_matome_yaml(handoff: SemanticHandoff) -> str:
    """Emit a dependency-free YAML-like interchange document.

    The v0.1 bridge intentionally emits JSON-compatible YAML so that the
    interchange remains dependency-free while preserving the Matome shape.
    """
    payload: dict[str, Any] = {
        "matome_version": "joumon-0.1",
        "handoff_id": handoff.handoff_id,
        "context_id": handoff.context_id,
        "protocol_id": handoff.protocol_id,
        "authority": {
            "handoff": handoff.authority,
            "final_decision": handoff.final_decision_authority,
        },
        "evidence": [asdict(e) for e in handoff.evidence],
        "lineage": [asdict(l) for l in handoff.lineage],
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def validate_matome_document(document: str) -> dict[str, Any]:
    payload = json.loads(document)
    required = {"matome_version", "handoff_id", "context_id", "protocol_id", "authority", "evidence", "lineage"}
    missing = required - payload.keys()
    if missing:
        raise ValueError(f"missing Matome fields: {sorted(missing)}")
    if payload["authority"].get("final_decision") != "human":
        raise ValueError("Matome handoff must preserve human final authority")
    return payload
