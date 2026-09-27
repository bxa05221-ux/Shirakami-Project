"""Provider-neutral Semantic Handoff boundary.

This module projects an existing ExecutionTrace into a stable lineage envelope.
Identifiers preserve provenance only; they never grant authority.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any, Mapping


FALSE_AUTHORITY = (
    "execution_authorized",
    "publish_authorized",
    "merge_authorized",
)


@dataclass(frozen=True)
class SemanticHandoff:
    handoff_id: str
    trace_id: str
    execution_id: str
    activity_id: str | None
    evidence_ids: tuple[str, ...]
    project: str
    objective: str
    protocol_ids: tuple[str, ...]
    verification_scope: str
    verification_status: str
    execution_authorized: bool = False
    publish_authorized: bool = False
    merge_authorized: bool = False
    human_gate_required: bool = True
    decision_authority: bool = False

    def __post_init__(self) -> None:
        for key in FALSE_AUTHORITY:
            if getattr(self, key) is not False:
                raise ValueError(f"{key} must remain false")
        if self.human_gate_required is not True:
            raise ValueError("human_gate_required must remain true")
        if self.decision_authority is not False:
            raise ValueError("decision_authority must remain false")
        for key in ("handoff_id", "trace_id", "execution_id", "project", "objective", "verification_scope"):
            if not getattr(self, key):
                raise ValueError(f"{key} is required")

    @classmethod
    def from_trace(
        cls,
        trace_document: Mapping[str, Any],
        *,
        project: str,
        objective: str,
        protocol_ids: list[str] | tuple[str, ...],
        verification_scope: str,
        activity_id: str | None = None,
    ) -> "SemanticHandoff":
        trace = trace_document.get("codex_traceability")
        if not isinstance(trace, Mapping):
            raise ValueError("missing codex_traceability")
        for key in ("trace_id", "execution_id", "source_handoff_id", "evidence_ids"):
            if key not in trace:
                raise ValueError(f"{key} is required")
        authority = trace.get("authority")
        if not isinstance(authority, Mapping):
            raise ValueError("authority is required")
        for key in FALSE_AUTHORITY:
            if authority.get(key) is not False:
                raise ValueError(f"{key} must remain false")
        gate = trace.get("human_gate")
        if not isinstance(gate, Mapping) or gate.get("required") is not True:
            raise ValueError("human_gate.required must remain true")
        verification = trace.get("verification")
        if not isinstance(verification, Mapping):
            raise ValueError("verification is required")

        return cls(
            handoff_id=str(trace["source_handoff_id"]),
            trace_id=str(trace["trace_id"]),
            execution_id=str(trace["execution_id"]),
            activity_id=activity_id if activity_id is not None else trace.get("activity_id"),
            evidence_ids=tuple(trace["evidence_ids"]),
            project=project,
            objective=objective,
            protocol_ids=tuple(protocol_ids),
            verification_scope=verification_scope,
            verification_status=str(verification.get("status", "pending")),
        )

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["evidence_ids"] = list(self.evidence_ids)
        data["protocol_ids"] = list(self.protocol_ids)
        return data


class SemanticHandoffStore:
    """Read-only trace projection store used by the API boundary."""

    def __init__(self, traces: Mapping[str, Mapping[str, Any]]):
        self._traces = traces

    def get(
        self,
        trace_id: str,
        *,
        project: str,
        objective: str,
        protocol_ids: list[str] | tuple[str, ...],
        verification_scope: str,
        activity_id: str | None = None,
    ) -> SemanticHandoff:
        trace = self._traces.get(trace_id)
        if trace is None:
            raise KeyError(trace_id)
        return SemanticHandoff.from_trace(
            trace,
            project=project,
            objective=objective,
            protocol_ids=protocol_ids,
            verification_scope=verification_scope,
            activity_id=activity_id,
        )
