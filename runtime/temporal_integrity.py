"""Temporal integrity boundary for Shirakami decisions.

This module validates causal/time bindings without treating timestamps as
authoritative evidence by themselves.
"""
from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping


class TemporalIntegrityError(ValueError):
    """Raised when an event graph violates a temporal authority invariant."""


def _time(value: str) -> datetime:
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise TemporalIntegrityError(f"invalid timestamp: {value}") from exc


def validate_event_graph(events: list[Mapping[str, Any]]) -> None:
    """Fail closed on replay, stale approval, future evidence, and bad causality."""
    by_id: dict[str, Mapping[str, Any]] = {}
    for event in events:
        event_id = event.get("event_id")
        if not event_id:
            raise TemporalIntegrityError("event_id is required")
        event_id = str(event_id)
        if event_id in by_id:
            raise TemporalIntegrityError(f"duplicate event_id: {event_id}")
        by_id[event_id] = event

    for event in events:
        event_id = str(event["event_id"])
        current_time = _time(str(event["occurred_at"]))
        parent_id = event.get("parent_event_id")
        if parent_id:
            parent = by_id.get(str(parent_id))
            if parent is None:
                raise TemporalIntegrityError(f"missing parent_event_id: {parent_id}")
            if current_time < _time(str(parent["occurred_at"])):
                raise TemporalIntegrityError(f"event precedes parent: {event_id}")

        if event.get("event_type") == "human_decision":
            evidence_time = event.get("evidence_occurred_at")
            if evidence_time is not None and current_time < _time(str(evidence_time)):
                raise TemporalIntegrityError(
                    f"decision uses future evidence: {event_id}"
                )

    decisions: set[str] = set()
    approvals: dict[str, Mapping[str, Any]] = {}
    for event in events:
        if event.get("event_type") == "human_decision":
            decision_id = event.get("decision_id")
            if not decision_id:
                raise TemporalIntegrityError("decision_id is required")
            decision_id = str(decision_id)
            if decision_id in decisions:
                raise TemporalIntegrityError(f"decision replay: {decision_id}")
            decisions.add(decision_id)

        if event.get("event_type") == "human_approval":
            approval_id = event.get("approval_id")
            if not approval_id:
                raise TemporalIntegrityError("approval_id is required")
            approval_id = str(approval_id)
            if approval_id in approvals:
                raise TemporalIntegrityError(f"approval replay: {approval_id}")
            approvals[approval_id] = event

    for event in events:
        if event.get("event_type") != "execution":
            continue
        approval_id = event.get("approval_id")
        if not approval_id:
            raise TemporalIntegrityError("execution requires approval_id")
        approval = approvals.get(str(approval_id))
        if approval is None:
            raise TemporalIntegrityError(f"approval not found: {approval_id}")
        if event.get("context_version") != approval.get("context_version"):
            raise TemporalIntegrityError(
                f"stale approval/context mismatch: {approval_id}"
            )
        if _time(str(event["occurred_at"])) < _time(str(approval["occurred_at"])):
            raise TemporalIntegrityError(
                f"execution precedes approval: {event['event_id']}"
            )
