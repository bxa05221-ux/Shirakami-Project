"""Return execution witness facts to Observation without turning witness data into authority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.execution_aiwitness_bridge import AIwitnessExecutionProjection


@dataclass(frozen=True)
class WitnessObservation:
    observation_id: str
    witness_id: str
    trace_id: str
    approval_id: str
    protocol_id: str
    request_id: str
    candidate_id: str
    scope: Tuple[str, ...]
    execution_status: str
    source: str = "aiwitness"
    decision_authority: bool = False


def return_witness_to_observation(
    *, observation_id: str, witness: AIwitnessExecutionProjection
) -> WitnessObservation:
    return WitnessObservation(
        observation_id=observation_id,
        witness_id=witness.witness_id,
        trace_id=witness.trace_id,
        approval_id=witness.approval_id,
        protocol_id=witness.protocol_id,
        request_id=witness.request_id,
        candidate_id=witness.candidate_id,
        scope=witness.scope,
        execution_status=witness.execution_status,
    )
