"""Observation Set: preserve agreement and disagreement across observers.

The set is a reporting structure, not a decision engine. Observer outputs remain
separate so disagreement is retained as context rather than collapsed by vote.
"""

from typing import Any


def build_observation_set(observations: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "observations": observations,
        "agreement": _shared_values(observations, "observation"),
        "differences": [
            {
                "observer_id": item.get("observer_id"),
                "perspective": item.get("perspective"),
                "observation": item.get("observation"),
            }
            for item in observations
        ],
        "decision_authority": False,
        "human_gate_required": True,
    }


def _shared_values(items: list[dict[str, Any]], key: str) -> list[Any]:
    if not items:
        return []
    values = [item.get(key) for item in items]
    first = values[0]
    return [first] if all(value == first for value in values) else []
