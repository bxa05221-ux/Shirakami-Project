"""Protocol-level anonymous observer instance.

The observer is intentionally ephemeral and non-authoritative. It consumes a
validated semantic handoff and emits observations/candidates without creating
or persisting a personality.
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AnonymousObserver:
    perspective: str
    observer_id: str

    def observe(self, handoff: dict[str, Any]) -> dict[str, Any]:
        return {
            "observer_id": self.observer_id,
            "perspective": self.perspective,
            "observation": handoff.get("context", {}),
            "candidate": None,
            "unresolved": handoff.get("unresolved", []),
            "human_gate_required": True,
            "decision_authority": False,
            "persistent_personality": False,
        }
