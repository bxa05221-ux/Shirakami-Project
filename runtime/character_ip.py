"""Bounded character-IP observation runtime.

Character IPs observe Context and may propose interpretations.
They have no authority to mutate canonical Context.
"""
from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping


def observe(
    context: Mapping[str, Any],
    ip: Mapping[str, Any],
    *,
    question: str,
    observation: str,
    basis: list[str] | None = None,
    uncertainty: list[str] | None = None,
    proposal: str | None = None,
) -> dict[str, Any]:
    if not ip.get("id"):
        raise ValueError("ip.id is required")
    if ip.get("type") not in {"named_ip", "collective_ip", "anonymous_ip"}:
        raise ValueError("unsupported character IP type")

    return {
        "source_context": deepcopy(dict(context)),
        "ip": {
            "id": ip["id"],
            "type": ip["type"],
            "viewpoint": deepcopy(ip.get("viewpoint", [])),
        },
        "question": question,
        "observation": observation,
        "basis": list(basis or []),
        "uncertainty": list(uncertainty or []),
        "proposal": proposal,
        "provenance": {
            "source_context": "existing_context",
            "symbolic_layer": "character_ip",
            "generated_layer": "ai_interpretation",
        },
        "authority": {
            "character_ip": "none",
            "human_gate": "required",
        },
        "context_update": {
            "allowed": False,
        },
    }


def can_update_canonical_context(observation: Mapping[str, Any]) -> bool:
    """Always false: Character IP output cannot bypass Human Gate."""
    return observation.get("context_update", {}).get("allowed") is True
