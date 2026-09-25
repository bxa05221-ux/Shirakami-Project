"""Provider-neutral Runtime Adapter interface.

Concrete providers implement this contract without receiving authority.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class RuntimeRequest:
    handoff_id: str
    trace_id: str | None
    execution_id: str | None
    project: str
    objective: str
    protocol_ids: tuple[str, ...]
    evidence_ids: tuple[str, ...]
    verification_scope: str
    input_data: Any
    runtime_target: str | None = None


@dataclass(frozen=True)
class RuntimeResult:
    handoff_id: str
    trace_id: str | None
    execution_id: str | None
    provider: str
    output: Any
    evidence_ids: tuple[str, ...]
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True


class ProviderAdapter(ABC):
    """Replaceable provider boundary; never an authority boundary."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def execute(self, request: RuntimeRequest) -> RuntimeResult:
        """Execute provider work while returning traceable, non-authoritative output."""
        raise NotImplementedError

    def validate_result(self, result: RuntimeResult) -> None:
        if result.execution_authorized:
            raise ValueError("provider result cannot grant execution authority")
        if result.publish_authorized:
            raise ValueError("provider result cannot grant publication authority")
        if result.merge_authorized:
            raise ValueError("provider result cannot grant merge authority")
        if not result.human_gate_required:
            raise ValueError("human_gate_required must remain true")
        if not result.handoff_id:
            raise ValueError("handoff identity is required")
        if not result.provider:
            raise ValueError("provider identity is required")
