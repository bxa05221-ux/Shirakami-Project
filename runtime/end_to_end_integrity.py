"""End-to-end authority preservation boundary for Shirakami.

Composes temporal, decision-binding, and persistence/recovery checks.
"""
from __future__ import annotations

from typing import Any, Mapping

from runtime.decision_binding import validate_decision_binding
from runtime.recovery_integrity import validate_recovery
from runtime.temporal_integrity import validate_event_graph


def validate_end_to_end(
    events: list[Mapping[str, Any]],
    approval: Mapping[str, Any],
    execution: Mapping[str, Any],
    persisted: Mapping[str, Any],
) -> None:
    """Validate one complete decision -> execution -> recovery chain."""
    validate_event_graph(events)
    validate_decision_binding(approval, execution)
    validate_recovery(approval, persisted)
