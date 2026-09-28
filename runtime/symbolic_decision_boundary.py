"""Decision boundary for symbolic interpretation.

Symbolic interpretation may generate questions or candidates, but it cannot
become an instruction, approval, or decision without the Human Gate.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class SymbolicCandidate:
    candidate_id: str
    symbol_id: str
    expression: str
    interpretations: Tuple[str, ...]
    basis_observation_ids: Tuple[str, ...]


@dataclass(frozen=True)
class SymbolicDecisionBoundary:
    candidate: SymbolicCandidate
    human_gate_required: bool = True
    decision_authority: bool = False

    def as_human_gate_request(self) -> dict:
        return {
            "candidate_id": self.candidate.candidate_id,
            "symbol_id": self.candidate.symbol_id,
            "expression": self.candidate.expression,
            "interpretations": list(self.candidate.interpretations),
            "basis_observation_ids": list(self.candidate.basis_observation_ids),
            "human_gate_required": self.human_gate_required,
            "decision_authority": self.decision_authority,
        }


def build_symbolic_decision_boundary(
    *,
    candidate_id: str,
    symbol_id: str,
    expression: str,
    interpretations: Tuple[str, ...],
    basis_observation_ids: Tuple[str, ...],
) -> SymbolicDecisionBoundary:
    if not interpretations:
        raise ValueError("symbolic candidate requires at least one interpretation")
    if not basis_observation_ids:
        raise ValueError("symbolic candidate requires observation provenance")
    return SymbolicDecisionBoundary(
        candidate=SymbolicCandidate(
            candidate_id=candidate_id,
            symbol_id=symbol_id,
            expression=expression,
            interpretations=tuple(interpretations),
            basis_observation_ids=tuple(basis_observation_ids),
        )
    )
