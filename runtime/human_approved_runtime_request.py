"""Convert an explicitly human-approved Protocol into a bounded RuntimeRequest."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class HumanApprovedProtocol:
    approval_id: str
    protocol_id: str
    approver_id: str
    scope: Tuple[str, ...]
    candidate_id: str
    approved_at: str

    def __post_init__(self) -> None:
        if not self.scope:
            raise ValueError("human approval requires a non-empty scope")


@dataclass(frozen=True)
class RuntimeRequest:
    request_id: str
    protocol_id: str
    approval_id: str
    scope: Tuple[str, ...]
    candidate_id: str
    human_approved: bool = True
    decision_authority: bool = False


def build_runtime_request(*, request_id: str, approved: HumanApprovedProtocol) -> RuntimeRequest:
    """Create execution intent only from an already approved protocol."""
    return RuntimeRequest(
        request_id=request_id,
        protocol_id=approved.protocol_id,
        approval_id=approved.approval_id,
        scope=approved.scope,
        candidate_id=approved.candidate_id,
    )
