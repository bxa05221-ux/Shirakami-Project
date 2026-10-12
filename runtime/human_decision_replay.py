"""Human decision authentication/replay boundary."""
from __future__ import annotations

from typing import Any, Mapping, Sequence


class HumanDecisionReplayError(ValueError):
    pass


def validate_human_decision_event(
    decision: Mapping[str, Any],
    *,
    seen_decision_ids: frozenset[str] = frozenset(),
) -> None:
    decision_id = decision.get("decision_id")
    if not decision_id:
        raise HumanDecisionReplayError("missing decision_id")
    if decision_id in seen_decision_ids:
        raise HumanDecisionReplayError("decision replay detected")

    if decision.get("actor_type") != "human":
        raise HumanDecisionReplayError("decision actor is not human")
    if decision.get("decision") not in {"approve", "reject", "revise"}:
        raise HumanDecisionReplayError("invalid human decision")

    if decision.get("runtime_authority") is True:
        raise HumanDecisionReplayError("runtime cannot hold human authority")

    for field in ("approval_id", "context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        if decision.get(field) in (None, ""):
            raise HumanDecisionReplayError(f"missing decision binding: {field}")

    if decision.get("human_approval") is not True:
        raise HumanDecisionReplayError("human approval must be explicit")

    return


def validate_decision_sequence(
    decisions: Sequence[Mapping[str, Any]],
) -> None:
    seen: set[str] = set()
    for decision in decisions:
        validate_human_decision_event(decision, seen_decision_ids=frozenset(seen))
        seen.add(decision["decision_id"])
