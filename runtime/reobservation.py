"""Re-observation queue boundary for unresolved Context meaning.

Unresolved items remain observable without being promoted to decisions.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ReObservationRequest:
    request_id: str
    source_observation_id: str
    unresolved_item: str
    context_id: str
    sequence: int
    status: str = "open"

    def __post_init__(self) -> None:
        for field in ("request_id", "source_observation_id", "unresolved_item", "context_id"):
            if not getattr(self, field):
                raise ValueError(f"{field} is required")
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")
        if self.status not in {"open", "observed"}:
            raise ValueError("status must be open or observed")


class ReObservationQueue:
    """Append-only queue carrying unresolved meaning into later observation."""

    def __init__(self) -> None:
        self._items: list[ReObservationRequest] = []
        self._ids: set[str] = set()

    def enqueue(
        self,
        *,
        request_id: str,
        source_observation_id: str,
        unresolved_items: Iterable[str],
        context_id: str,
        sequence: int,
    ) -> None:
        if request_id in self._ids:
            raise ValueError(f"duplicate request_id: {request_id}")
        values = tuple(str(item) for item in unresolved_items)
        if not values:
            raise ValueError("at least one unresolved item is required")
        for offset, item in enumerate(values):
            item_id = request_id if offset == 0 else f"{request_id}:{offset}"
            self._append(
                ReObservationRequest(
                    request_id=item_id,
                    source_observation_id=source_observation_id,
                    unresolved_item=item,
                    context_id=context_id,
                    sequence=sequence + offset,
                )
            )

    def _append(self, request: ReObservationRequest) -> None:
        if request.request_id in self._ids:
            raise ValueError(f"duplicate request_id: {request.request_id}")
        if self._items and request.sequence <= self._items[-1].sequence:
            raise ValueError("sequence must increase monotonically")
        self._items.append(request)
        self._ids.add(request.request_id)

    def pending(self) -> tuple[ReObservationRequest, ...]:
        return tuple(item for item in self._items if item.status == "open")

    def items(self) -> tuple[ReObservationRequest, ...]:
        return tuple(self._items)

    def mark_observed(self, request_id: str) -> ReObservationRequest:
        for index, item in enumerate(self._items):
            if item.request_id == request_id:
                if item.status == "observed":
                    return item
                updated = ReObservationRequest(
                    request_id=item.request_id,
                    source_observation_id=item.source_observation_id,
                    unresolved_item=item.unresolved_item,
                    context_id=item.context_id,
                    sequence=item.sequence,
                    status="observed",
                )
                self._items[index] = updated
                return updated
        raise KeyError(f"unknown request_id: {request_id}")

    @property
    def human_gate_required(self) -> bool:
        return True

    @property
    def decision_authority(self) -> bool:
        return False
