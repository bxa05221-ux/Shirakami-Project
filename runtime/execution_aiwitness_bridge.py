"""Project bounded execution facts into an AIwitness trace without granting authority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.runtime_execution_trace import ExecutionTrace


@dataclass(frozen=True)
class AIwitnessExecutionProjection:
    witness_id: str
    trace_id: str
    approval_id: str
    protocol_id: str
    request_id: str
    candidate_id: str
    scope: Tuple[str, ...]
    execution_status: str
    decision_authority: bool = False


def project_execution_to_aiwitness(
    *, witness_id: str, trace: ExecutionTrace
) -> AIwitnessExecutionProjection:
    return AIwitnessExecutionProjection(
        witness_id=witness_id,
        trace_id=trace.trace_id,
        approval_id=trace.approval_id,
        protocol_id=trace.protocol_id,
        request_id=trace.request_id,
        candidate_id=trace.candidate_id,
        scope=trace.scope,
        execution_status=trace.status,
    )
