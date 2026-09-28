"""Convert an observation into an explicitly reviewable evidence candidate.

An observation is not evidence merely because it came from AIwitness.
Validation is required before an EvidenceRecord / evidence_id can be created.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.aiwitness_observation_bridge import WitnessObservation


@dataclass(frozen=True)
class EvidenceCandidate:
    candidate_id: str
    observation_id: str
    witness_id: str
    trace_id: str
    approval_id: str
    protocol_id: str
    request_id: str
    source: str
    execution_status: str
    scope: Tuple[str, ...]
    validation_status: str = "pending"
    evidence_id: str | None = None
    decision_authority: bool = False


def build_evidence_candidate(
    *, candidate_id: str, observation: WitnessObservation
) -> EvidenceCandidate:
    return EvidenceCandidate(
        candidate_id=candidate_id,
        observation_id=observation.observation_id,
        witness_id=observation.witness_id,
        trace_id=observation.trace_id,
        approval_id=observation.approval_id,
        protocol_id=observation.protocol_id,
        request_id=observation.request_id,
        source=observation.source,
        execution_status=observation.execution_status,
        scope=observation.scope,
    )
