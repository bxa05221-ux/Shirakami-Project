"""Bind a bounded RuntimeRequest to an execution trace without granting authority."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple

from runtime.human_approved_runtime_request import RuntimeRequest


@dataclass(frozen=True)
class ExecutionTrace:
    trace_id: str
    request_id: str
    approval_id: str
    protocol_id: str
    candidate_id: str
    scope: Tuple[str, ...]
    status: str
    decision_authority: bool = False


def record_execution(*, trace_id: str, request: RuntimeRequest, status: str) -> ExecutionTrace:
    if not request.human_approved:
        raise ValueError("execution requires an explicitly human-approved RuntimeRequest")
    if not request.scope:
        raise ValueError("execution requires a bounded scope")
    return ExecutionTrace(
        trace_id=trace_id,
        request_id=request.request_id,
        approval_id=request.approval_id,
        protocol_id=request.protocol_id,
        candidate_id=request.candidate_id,
        scope=request.scope,
        status=status,
    )
