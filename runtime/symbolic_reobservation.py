"""Bridge symbolic recursion to re-observation lineage without resolving meaning.
The symbolic trace and temporal lineage remain separate records; this bridge
only binds their provenance for later observation.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.reobservation_lineage import ReObservationLineage, ReObservationLink
from runtime.symbolic_recursion import SymbolicRecursion, SymbolicTrace


@dataclass(frozen=True)
class SymbolicReObservationRecord:
    link_id: str
    request_id: str
    source_observation_id: str
    result_observation_id: str
    symbol_id: str
    expression: str
    interpretations: Tuple[str, ...]
    context_refs: Tuple[str, ...]

    @property
    def human_gate_required(self) -> bool:
        return True

    @property
    def decision_authority(self) -> bool:
        return False


def record_symbolic_reobservation(
    *,
    symbolic: SymbolicRecursion,
    lineage: ReObservationLineage,
    symbol: SymbolicTrace,
    link: ReObservationLink,
) -> SymbolicReObservationRecord:
    symbolic.record(symbol)
    lineage.record(link)
    return SymbolicReObservationRecord(
        link_id=link.link_id,
        request_id=link.request_id,
        source_observation_id=link.source_observation_id,
        result_observation_id=link.result_observation_id,
        symbol_id=symbol.symbol_id,
        expression=symbol.expression,
        interpretations=tuple(symbol.interpretations),
        context_refs=tuple(symbol.context_refs),
    )
