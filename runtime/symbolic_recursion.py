"""Symbolic recursion boundary for returning from symbol space to lived context.

Symbols are treated as context-bearing representations, not as authoritative
definitions. The boundary preserves ambiguity and supports re-observation
before returning to a human-facing context and Human Gate.
"""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SymbolicTrace:
    symbol_id: str
    expression: str
    interpretations: tuple[str, ...] = ()
    context_refs: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if not self.symbol_id:
            raise ValueError("symbol_id is required")
        if not self.expression:
            raise ValueError("expression is required")


class SymbolicRecursion:
    """Append-only symbolic interpretation and reality-return boundary.

    A symbol is not resolved into one universal meaning. Interpretations are
    retained as candidate context readings and can be re-observed later.
    """

    def __init__(self) -> None:
        self._traces: list[SymbolicTrace] = []
        self._ids: set[str] = set()

    def record(self, trace: SymbolicTrace) -> None:
        if trace.symbol_id in self._ids:
            raise ValueError(f"duplicate symbol_id: {trace.symbol_id}")
        self._traces.append(trace)
        self._ids.add(trace.symbol_id)

    def traces(self) -> tuple[SymbolicTrace, ...]:
        return tuple(self._traces)

    def interpretations(self, symbol_id: str) -> tuple[str, ...]:
        for trace in self._traces:
            if trace.symbol_id == symbol_id:
                return trace.interpretations
        raise KeyError(symbol_id)

    def context_refs(self, symbol_id: str) -> tuple[str, ...]:
        for trace in self._traces:
            if trace.symbol_id == symbol_id:
                return trace.context_refs
        raise KeyError(symbol_id)

    @property
    def returns_to_context(self) -> bool:
        return True

    @property
    def decision_authority(self) -> bool:
        return False

    @property
    def human_gate_required(self) -> bool:
        return True
