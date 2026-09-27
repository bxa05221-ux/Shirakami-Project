"""Lineage boundary connecting re-observation requests to later observations."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ReObservationLink:
    link_id: str
    request_id: str
    source_observation_id: str
    result_observation_id: str
    sequence: int

    def __post_init__(self) -> None:
        for field in (
            "link_id",
            "request_id",
            "source_observation_id",
            "result_observation_id",
        ):
            if not getattr(self, field):
                raise ValueError(f"{field} is required")
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")


class ReObservationLineage:
    """Append-only links from an unresolved request to its later observation."""

    def __init__(self) -> None:
        self._items: list[ReObservationLink] = []
        self._ids: set[str] = set()
        self._requests: set[str] = set()

    def record(self, link: ReObservationLink) -> None:
        if link.link_id in self._ids:
            raise ValueError(f"duplicate link_id: {link.link_id}")
        if link.request_id in self._requests:
            raise ValueError(f"request already linked: {link.request_id}")
        if self._items and link.sequence <= self._items[-1].sequence:
            raise ValueError("sequence must increase monotonically")
        self._items.append(link)
        self._ids.add(link.link_id)
        self._requests.add(link.request_id)

    def items(self) -> tuple[ReObservationLink, ...]:
        return tuple(self._items)

    def observations_for(self, request_id: str) -> tuple[str, ...]:
        return tuple(
            item.result_observation_id
            for item in self._items
            if item.request_id == request_id
        )

    @property
    def human_gate_required(self) -> bool:
        return True

    @property
    def decision_authority(self) -> bool:
        return False
