"""Bridge symbolic interpretation into Context Transition provenance.

The bridge does not resolve a symbol. It records which symbolic observation
was used to revisit context, so later evidence can distinguish interpretation
from lived context.
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.context_transition import ContextTransition
from runtime.symbolic_recursion import SymbolicRecursion, SymbolicTrace


def build_symbolic_context_transition(
    *,
    symbolic: SymbolicRecursion,
    symbol: SymbolicTrace,
    observation: Mapping[str, Any],
    transition_id: str,
    sequence: int,
    from_context_id: str,
    to_context_id: str,
) -> ContextTransition:
    symbolic.record(symbol)
    provenance = dict(observation.get("provenance") or {})
    provenance["symbolic_recursion"] = {
        "symbol_id": symbol.symbol_id,
        "expression": symbol.expression,
        "interpretations": list(symbol.interpretations),
        "context_refs": list(symbol.context_refs),
    }
    return ContextTransition.from_observation(
        observation,
        transition_id=transition_id,
        sequence=sequence,
        from_context_id=from_context_id,
        to_context_id=to_context_id,
        provenance=provenance,
    )
