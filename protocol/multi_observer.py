"""Minimal multi-perspective observer composition.

Observers remain ephemeral, non-authoritative and perspective-scoped.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class ObserverPerspective:
    observer_id: str
    perspective: str


def observe_from_perspectives(
    handoff: dict[str, Any], perspectives: list[ObserverPerspective]
) -> list[dict[str, Any]]:
    """Produce independent observations without merging authority or personality."""
    return [
        {
            "observer_id": item.observer_id,
            "perspective": item.perspective,
            "observation": handoff.get("context", {}),
            "unresolved": handoff.get("unresolved", []),
            "decision_authority": False,
            "persistent_personality": False,
            "human_gate_required": True,
        }
        for item in perspectives
    ]
