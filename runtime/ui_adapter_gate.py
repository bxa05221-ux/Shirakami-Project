"""UI/Adapter boundary: presentation cannot mint Human Gate authority."""
from __future__ import annotations

from typing import Any, Mapping


class UIAdapterGateError(ValueError):
    pass


IMMUTABLE_FIELDS = (
    "decision_id",
    "approval_id",
    "context_version",
    "evidence_hash",
    "protocol_hash",
    "proposal_id",
)


def validate_ui_adapter_decision(
    ui_event: Mapping[str, Any],
    decision: Mapping[str, Any],
) -> None:
    if ui_event.get("event_type") != "human_interaction":
        raise UIAdapterGateError("missing explicit human interaction event")

    if ui_event.get("synthetic") is True:
        raise UIAdapterGateError("synthetic UI event cannot authorize")

    if ui_event.get("runtime_generated") is True:
        raise UIAdapterGateError("runtime-generated UI event cannot authorize")

    if ui_event.get("action") not in {"approve", "reject", "revise"}:
        raise UIAdapterGateError("invalid UI decision action")

    if ui_event.get("human_approval") is True and ui_event.get("actor_type") != "human":
        raise UIAdapterGateError("non-human UI actor cannot claim approval")

    if decision.get("actor_type") != "human":
        raise UIAdapterGateError("decision is not attributed to human")

    if decision.get("decision") != ui_event.get("action"):
        raise UIAdapterGateError("UI action/decision mismatch")

    if decision.get("human_approval") is not True:
        raise UIAdapterGateError("decision lacks explicit human approval")

    for field in IMMUTABLE_FIELDS:
        if ui_event.get(field) != decision.get(field):
            raise UIAdapterGateError(f"UI/decision binding mismatch: {field}")

    if decision.get("runtime_authority") is True:
        raise UIAdapterGateError("runtime authority cannot cross UI boundary")

    return
