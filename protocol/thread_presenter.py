"""Thread Presenter boundary.

Renders observer outputs as a contextual discussion without collapsing
perspectives into a decision. Presentation is deliberately separate from
judgment and authority.
"""

from typing import Any


def present_observation_set(observation_set: dict[str, Any]) -> dict[str, Any]:
    observations = observation_set.get("observations", [])
    return {
        "type": "thread_presentation",
        "entries": [
            {
                "observer_id": item.get("observer_id"),
                "perspective": item.get("perspective"),
                "observation": item.get("observation"),
                "unresolved": item.get("unresolved", []),
            }
            for item in observations
        ],
        "agreement": observation_set.get("agreement", []),
        "differences": observation_set.get("differences", []),
        "decision_authority": False,
        "human_gate_required": True,
    }
