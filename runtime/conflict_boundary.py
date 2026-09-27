"""Conflict boundary for preserving competing impulses and future-path checks."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Direction = Literal["act", "stop", "wait", "alternative", "uncertainty", "provocation"]


@dataclass(frozen=True)
class ConflictSignal:
    signal_id: str
    direction: Direction
    observation: str
    weight: float = 1.0

    def __post_init__(self) -> None:
        if not self.signal_id:
            raise ValueError("signal_id is required")
        if not self.observation:
            raise ValueError("observation is required")
        if self.weight < 0:
            raise ValueError("weight must be non-negative")


@dataclass(frozen=True)
class FuturePath:
    path_id: str
    description: str
    kind: Literal["deadman", "life", "loss"]
    preserved: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.path_id:
            raise ValueError("path_id is required")
        if not self.description:
            raise ValueError("description is required")


class ConflictTrace:
    """Append-only observation of internal conflict and alternative futures.

    Deadman checks inspect consequences of a candidate path.
    Life checks search for ways to preserve a viable future without requiring
    that candidate. Loss paths record what can be surrendered while preserving
    specified values. None of these paths is a decision.
    """

    def __init__(self) -> None:
        self._signals: list[ConflictSignal] = []
        self._paths: list[FuturePath] = []
        self._ids: set[str] = set()

    def record_signal(self, signal: ConflictSignal) -> None:
        if signal.signal_id in self._ids:
            raise ValueError(f"duplicate signal_id: {signal.signal_id}")
        self._signals.append(signal)
        self._ids.add(signal.signal_id)

    def record_path(self, path: FuturePath) -> None:
        if path.path_id in self._ids:
            raise ValueError(f"duplicate path_id: {path.path_id}")
        self._paths.append(path)
        self._ids.add(path.path_id)

    def signals(self) -> tuple[ConflictSignal, ...]:
        return tuple(self._signals)

    def paths(self, kind: str | None = None) -> tuple[FuturePath, ...]:
        if kind is None:
            return tuple(self._paths)
        return tuple(path for path in self._paths if path.kind == kind)

    def direction_weight(self, direction: Direction) -> float:
        return sum(
            signal.weight for signal in self._signals if signal.direction == direction
        )

    @property
    def human_gate_required(self) -> bool:
        return True

    @property
    def decision_authority(self) -> bool:
        return False
