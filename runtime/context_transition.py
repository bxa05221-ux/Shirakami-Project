"""Context transition history boundary.

A transition records how an Observation relates two Context states.
It preserves unresolved meaning and provenance without turning a transition
into a decision or an authority grant.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ContextTransition:
    transition_id: str
    sequence: int
    observation_id: str
    from_context_id: str
    to_context_id: str
    unresolved_items: tuple[str, ...] = ()
    transition_kind: str = "observed"
    provenance: Mapping[str, Any] | None = None
    human_gate_required: bool = True
    decision_authority: bool = False

    def __post_init__(self) -> None:
        for field in (
            "transition_id",
            "observation_id",
            "from_context_id",
            "to_context_id",
        ):
            if not getattr(self, field):
                raise ValueError(f"{field} is required")
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")
        if self.transition_kind not in {"observed", "candidate"}:
            raise ValueError("transition_kind must be observed or candidate")
        if self.human_gate_required is not True:
            raise ValueError("human_gate_required must remain true")
        if self.decision_authority is not False:
            raise ValueError("decision_authority must remain false")

    @classmethod
    def from_observation(
        cls,
        observation: Mapping[str, Any],
        *,
        transition_id: str,
        sequence: int,
        from_context_id: str,
        to_context_id: str,
        transition_kind: str = "observed",
        provenance: Mapping[str, Any] | None = None,
    ) -> "ContextTransition":
        observation_id = observation.get("observation_id")
        if not observation_id:
            raise ValueError("observation_id is required")
        unresolved = observation.get("unresolved_items", ())
        if unresolved is None:
            unresolved = ()
        if isinstance(unresolved, str) or not isinstance(unresolved, Iterable):
            raise ValueError("unresolved_items must be iterable")
        return cls(
            transition_id=transition_id,
            sequence=sequence,
            observation_id=str(observation_id),
            from_context_id=from_context_id,
            to_context_id=to_context_id,
            unresolved_items=tuple(str(item) for item in unresolved),
            transition_kind=transition_kind,
            provenance=provenance,
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["unresolved_items"] = list(self.unresolved_items)
        if self.provenance is None:
            data["provenance"] = {}
        return data


class ContextTransitionHistory:
    """Append-only history for Observation-to-Context transitions."""

    def __init__(self) -> None:
        self._items: list[ContextTransition] = []
        self._ids: set[str] = set()

    def append(self, transition: ContextTransition) -> None:
        if transition.transition_id in self._ids:
            raise ValueError(f"duplicate transition_id: {transition.transition_id}")
        if self._items and transition.sequence <= self._items[-1].sequence:
            raise ValueError("sequence must increase monotonically")
        self._items.append(transition)
        self._ids.add(transition.transition_id)

    def items(self) -> tuple[ContextTransition, ...]:
        return tuple(self._items)

    def unresolved_items(self) -> tuple[str, ...]:
        values: list[str] = []
        for item in self._items:
            for unresolved in item.unresolved_items:
                if unresolved not in values:
                    values.append(unresolved)
        return tuple(values)
