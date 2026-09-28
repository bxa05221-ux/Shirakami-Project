"""Human Gate -> Protocol boundary.

A symbolic candidate can only become executable intent after an explicit human
acceptance. The resulting protocol remains distinct from the candidate and
carries the accepted scope into RuntimeRequest construction.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.symbolic_decision_boundary import SymbolicDecisionBoundary


@dataclass(frozen=True)
class HumanGateAcceptance:
    acceptance_id: str
    candidate_id: str
    actor_id: str
    accepted: bool
    scope: Tuple[str, ...]


@dataclass(frozen=True)
class HumanApprovedProtocol:
    protocol_id: str
    acceptance_id: str
    candidate_id: str
    actor_id: str
    scope: Tuple[str, ...]
    source_observation_ids: Tuple[str, ...]
    human_approved: bool = True
    decision_authority: bool = True


def accept_symbolic_candidate(
    *,
    boundary: SymbolicDecisionBoundary,
    acceptance_id: str,
    actor_id: str,
    scope: Tuple[str, ...],
) -> HumanGateAcceptance:
    if not actor_id:
        raise ValueError("Human Gate acceptance requires actor_id")
    if not scope:
        raise ValueError("Human Gate acceptance requires explicit scope")
    return HumanGateAcceptance(
        acceptance_id=acceptance_id,
        candidate_id=boundary.candidate.candidate_id,
        actor_id=actor_id,
        accepted=True,
        scope=tuple(scope),
    )


def build_human_approved_protocol(
    *,
    boundary: SymbolicDecisionBoundary,
    acceptance: HumanGateAcceptance,
    protocol_id: str,
) -> HumanApprovedProtocol:
    if not acceptance.accepted:
        raise ValueError("only accepted Human Gate decisions can create Protocol")
    if acceptance.candidate_id != boundary.candidate.candidate_id:
        raise ValueError("acceptance candidate does not match boundary candidate")
    return HumanApprovedProtocol(
        protocol_id=protocol_id,
        acceptance_id=acceptance.acceptance_id,
        candidate_id=acceptance.candidate_id,
        actor_id=acceptance.actor_id,
        scope=acceptance.scope,
        source_observation_ids=boundary.candidate.basis_observation_ids,
    )
