"""Full-system authority chain composing temporal, verification, trust, and human gate boundaries."""
from __future__ import annotations
from typing import Any, Mapping

from runtime.cross_layer_authority_chain import validate_cross_layer_authority_chain
from runtime.full_human_gate import validate_full_human_gate

class FullSystemAuthorityError(ValueError):
    pass


def _event_time(event: Mapping[str, Any]):
    from datetime import datetime
    value = str(event.get("occurred_at", ""))
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError as exc:
        raise FullSystemAuthorityError(f"invalid system event timestamp: {value}") from exc


def _validate_system_temporal_binding(events, verification, decision, approval, execution) -> None:
    verification_id = verification.get("verification_id")
    decision_id = decision.get("decision_id")
    approval_id = approval.get("approval_id")
    if not verification_id or not decision_id or not approval_id:
        raise FullSystemAuthorityError("system temporal binding identifiers are required")
    verification_events = [e for e in events if e.get("event_type") == "verification" and e.get("verification_id") == verification_id]
    decision_events = [e for e in events if e.get("event_type") == "human_decision" and e.get("decision_id") == decision_id]
    approval_events = [e for e in events if e.get("event_type") == "human_approval" and e.get("approval_id") == approval_id]
    execution_events = [e for e in events if e.get("event_type") == "execution" and e.get("approval_id") == approval_id]
    if not all((verification_events, decision_events, approval_events, execution_events)):
        raise FullSystemAuthorityError("system temporal artifacts are incomplete")
    verification_event = verification_events[0]
    decision_event = decision_events[0]
    approval_event = approval_events[0]
    execution_event = execution_events[0]
    if verification_event.get("verification_id") != verification_id:
        raise FullSystemAuthorityError("verification event binding mismatch")
    if decision_event.get("decision_id") != decision_id:
        raise FullSystemAuthorityError("decision event binding mismatch")
    for field in ("approval_id", "context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        if approval_event.get(field) != approval.get(field):
            raise FullSystemAuthorityError(f"approval event {field} mismatch")
    for field in ("approval_id", "context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        if execution_event.get(field) != execution.get(field):
            raise FullSystemAuthorityError(f"execution event {field} mismatch")
    vt, dt, at, xt = map(_event_time, (verification_event, decision_event, approval_event, execution_event))
    if not (vt <= dt <= at <= xt):
        raise FullSystemAuthorityError("system temporal order violation")


def _validate_semantic_event_uniqueness(events) -> None:
    # Only uniquely identified semantic artifacts are subject to duplicate
    # rejection. Multiple observations may legitimately share a target.
    semantic_keys = (
        ("evidence", "evidence_hash"),
        ("protocol", "protocol_hash"),
        ("proposal", "proposal_id"),
        ("verification", "verification_id"),
        ("human_decision", "decision_id"),
        ("human_approval", "approval_id"),
        ("execution", "approval_id"),
    )
    seen = set()
    for event_type, identity_field in semantic_keys:
        for event in events:
            if event.get("event_type") != event_type:
                continue
            identity = event.get(identity_field)
            if identity is None:
                continue
            key = (event_type, identity)
            if key in seen:
                raise FullSystemAuthorityError("ambiguous duplicate semantic event")
            seen.add(key)


def _validate_unique_event_ids(events) -> None:
    seen = set()
    for event in events:
        event_id = event.get("event_id")
        if not event_id:
            raise FullSystemAuthorityError("event id missing")
        if event_id in seen:
            raise FullSystemAuthorityError("duplicate event id")
        seen.add(event_id)


def _validate_event_graph_acyclic(events) -> None:
    by_id = {event.get("event_id"): event for event in events if event.get("event_id")}
    for start_id in by_id:
        seen = set()
        current_id = start_id
        while current_id:
            if current_id in seen:
                raise FullSystemAuthorityError("event graph cycle detected")
            seen.add(current_id)
            parent_id = by_id[current_id].get("parent_event_id")
            if not parent_id:
                break
            if parent_id not in by_id:
                raise FullSystemAuthorityError("event graph parent missing")
            current_id = parent_id


def _validate_parent_time_constraints(events) -> None:
    by_id = {event.get("event_id"): event for event in events if event.get("event_id")}
    for event in events:
        parent_id = event.get("parent_event_id")
        if not parent_id or parent_id not in by_id:
            continue
        parent = by_id[parent_id]
        child_time = _event_time(event)
        parent_time = _event_time(parent)
        if parent_time > child_time:
            raise FullSystemAuthorityError("parent event occurs after child event")


def _validate_parent_binding_content(events) -> None:
    by_id = {event.get("event_id"): event for event in events if event.get("event_id")}
    required_bindings = {
        ("protocol", "evidence"): ("context_version", "evidence_hash"),
        ("proposal", "protocol"): ("context_version", "evidence_hash", "protocol_hash"),
        ("human_decision", "verification"): ("context_version", "evidence_hash", "protocol_hash"),
        ("execution", "human_approval"): ("context_version", "evidence_hash", "protocol_hash", "proposal_id", "approval_id"),
    }
    for event in events:
        event_type = event.get("event_type")
        parent_id = event.get("parent_event_id")
        if not parent_id or parent_id not in by_id:
            continue
        parent = by_id[parent_id]
        fields = required_bindings.get((event_type, parent.get("event_type")), ())
        for field in fields:
            if event.get(field) != parent.get(field):
                raise FullSystemAuthorityError(f"{event_type} parent binding mismatch: {field}")


def _validate_semantic_parent_chain(events) -> None:
    expected = {
        "evidence": ("observation",),
        "protocol": ("evidence",),
        "proposal": ("protocol",),
        "verification": ("observation",),
        "human_decision": ("verification",),
        "human_approval": ("human_decision",),
        "execution": ("human_approval",),
    }
    by_id = {event.get("event_id"): event for event in events if event.get("event_id")}
    for event in events:
        event_type = event.get("event_type")
        if event_type not in expected:
            continue
        parent_id = event.get("parent_event_id")
        if not parent_id or parent_id not in by_id:
            raise FullSystemAuthorityError(f"{event_type} parent event missing")
        parent_type = by_id[parent_id].get("event_type")
        if parent_type not in expected[event_type]:
            raise FullSystemAuthorityError(f"{event_type} parent event type mismatch")


def _validate_temporal_permutation(events, verification, decision, approval, execution) -> None:
    # Authority-bearing artifacts must be selected by identity, not list position.
    selected_ids = {
        "verification": verification.get("verification_id"),
        "human_decision": decision.get("decision_id"),
        "human_approval": approval.get("approval_id"),
        "execution": execution.get("approval_id"),
    }
    selected_fields = {
        "evidence": ("evidence_hash", verification.get("evidence_hash")),
        "protocol": ("protocol_hash", verification.get("protocol_hash")),
        "proposal": ("proposal_id", verification.get("proposal_id")),
        "verification": ("verification_id", selected_ids["verification"]),
        "human_decision": ("decision_id", selected_ids["human_decision"]),
        "human_approval": ("approval_id", selected_ids["human_approval"]),
        "execution": ("approval_id", selected_ids["execution"]),
    }
    selected_evidence = next((event for event in events if event.get("event_type") == "evidence" and event.get("evidence_hash") == verification.get("evidence_hash")), None)
    selected_observation_id = selected_evidence.get("parent_event_id") if selected_evidence else None
    selected_fields["observation"] = ("event_id", selected_observation_id)
    positions = []
    for event_type in ("observation", "evidence", "verification", "proposal", "human_decision", "human_approval", "execution"):
        if event_type in selected_fields:
            field, value = selected_fields[event_type]
            matches = [
                event for event in events
                if event.get("event_type") == event_type
                and event.get(field) == value
            ]
        else:
            matches = [event for event in events if event.get("event_type") == event_type]
        if not matches:
            raise FullSystemAuthorityError("temporal permutation artifacts missing")
        positions.append((event_type, matches[0]))
    from datetime import datetime
    parsed = []
    for event_type, event in positions:
        value = str(event.get("occurred_at", ""))
        try:
            parsed.append((event_type, datetime.fromisoformat(value.replace("Z", "+00:00"))))
        except ValueError as exc:
            raise FullSystemAuthorityError("invalid temporal permutation timestamp") from exc
    if not all(parsed[i][1] <= parsed[i + 1][1] for i in range(len(parsed) - 1)):
        raise FullSystemAuthorityError("temporal permutation detected")


def _validate_observation_evidence_temporal_binding(events, verification) -> None:
    evidence_hash = verification.get("evidence_hash")
    evidence_events = [
        event for event in events
        if event.get("event_type") == "evidence"
        and event.get("evidence_hash") == evidence_hash
    ]
    if not evidence_events:
        raise FullSystemAuthorityError("observation evidence temporal artifacts missing")
    evidence_event = evidence_events[0]
    parent_id = evidence_event.get("parent_event_id")
    observation_events = [
        event for event in events
        if event.get("event_type") == "observation"
        and event.get("event_id") == parent_id
    ]
    if not observation_events:
        raise FullSystemAuthorityError("evidence parent observation missing")
    from datetime import datetime
    def parse(event):
        value = str(event.get("occurred_at", ""))
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise FullSystemAuthorityError("invalid observation evidence timestamp") from exc
    observation_time = parse(observation_events[0])
    evidence_time = parse(evidence_event)
    if observation_time > evidence_time:
        raise FullSystemAuthorityError("evidence occurs before observation")


def _validate_evidence_verification_temporal_binding(events, verification) -> None:
    verification_id = verification.get("verification_id")
    evidence_hash = verification.get("evidence_hash")
    verification_events = [
        event for event in events
        if event.get("event_type") == "verification"
        and event.get("verification_id") == verification_id
    ]
    evidence_events = [
        event for event in events
        if event.get("event_type") == "evidence"
        and event.get("evidence_hash") == evidence_hash
    ]
    if not verification_events or not evidence_events:
        raise FullSystemAuthorityError("evidence verification temporal artifacts missing")
    from datetime import datetime
    def parse(event):
        value = str(event.get("occurred_at", ""))
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise FullSystemAuthorityError("invalid evidence verification timestamp") from exc
    evidence_time = parse(evidence_events[0])
    verification_time = parse(verification_events[0])
    if evidence_time > verification_time:
        raise FullSystemAuthorityError("evidence occurs after verification")


def _validate_verification_proposal_temporal_binding(events, verification) -> None:
    verification_id = verification.get("verification_id")
    proposal_id = verification.get("proposal_id")
    verification_events = [
        event for event in events
        if event.get("event_type") == "verification"
        and event.get("verification_id") == verification_id
    ]
    proposal_events = [
        event for event in events
        if event.get("event_type") == "proposal"
        and event.get("proposal_id") == proposal_id
    ]
    if not verification_events or not proposal_events:
        raise FullSystemAuthorityError("verification proposal temporal artifacts missing")
    from datetime import datetime
    def parse(event):
        value = str(event.get("occurred_at", ""))
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise FullSystemAuthorityError("invalid verification proposal timestamp") from exc
    verification_time = parse(verification_events[0])
    proposal_time = parse(proposal_events[0])
    if proposal_time < verification_time:
        raise FullSystemAuthorityError("proposal predates its verification")


def _validate_proposal_temporal_binding(events, verification, decision, approval, execution) -> None:
    proposal_id = verification.get("proposal_id")
    proposal_events = [
        event for event in events
        if event.get("event_type") == "proposal"
        and event.get("proposal_id") == proposal_id
    ]
    decision_id = decision.get("decision_id")
    decision_events = [
        event for event in events
        if event.get("event_type") == "human_decision"
        and event.get("decision_id") == decision_id
    ]
    if not proposal_events or not decision_events:
        raise FullSystemAuthorityError("proposal decision temporal artifacts missing")
    from datetime import datetime
    def parse(event):
        value = str(event.get("occurred_at", ""))
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as exc:
            raise FullSystemAuthorityError("invalid proposal decision timestamp") from exc
    proposal_time = parse(proposal_events[0])
    decision_time = parse(decision_events[0])
    if proposal_time > decision_time:
        raise FullSystemAuthorityError("proposal occurs after human decision")


def _validate_proposal_decision_binding(
    events, verification, decision, approval, execution
) -> None:
    proposal_id = verification.get("proposal_id")
    for artifact_name, artifact in (
        ("decision", decision),
        ("approval", approval),
        ("execution", execution),
    ):
        if artifact.get("proposal_id") != proposal_id:
            raise FullSystemAuthorityError(
                f"{artifact_name} is bound to a different proposal"
            )
    proposal_events = [
        event for event in events
        if event.get("event_type") == "proposal"
        and event.get("proposal_id") == proposal_id
    ]
    decision_id = decision.get("decision_id")
    decision_events = [
        event for event in events
        if event.get("event_type") == "human_decision"
        and event.get("decision_id") == decision_id
    ]
    if not decision_events:
        raise FullSystemAuthorityError("human decision provenance event missing")
    if decision_events[0].get("proposal_id") != proposal_id:
        raise FullSystemAuthorityError(
            "human decision is not bound to the verified proposal"
        )
    if not proposal_events:
        raise FullSystemAuthorityError("proposal provenance event missing")


def _validate_proposal_binding(events, verification) -> None:
    proposal_id = verification.get("proposal_id")
    protocol_hash = verification.get("protocol_hash")
    context_version = verification.get("context_version")
    evidence_hash = verification.get("evidence_hash")
    if not proposal_id:
        raise FullSystemAuthorityError("verification proposal_id is required")
    proposal_events = [
        event for event in events
        if event.get("event_type") == "proposal"
        and event.get("proposal_id") == proposal_id
    ]
    if not proposal_events:
        raise FullSystemAuthorityError("proposal provenance event missing")
    if not any(
        event.get("protocol_hash") == protocol_hash
        and event.get("context_version") == context_version
        and event.get("evidence_hash") == evidence_hash
        for event in proposal_events
    ):
        raise FullSystemAuthorityError("proposal is not bound to protocol, evidence and context")


def _validate_protocol_binding(events, verification) -> None:
    protocol_hash = verification.get("protocol_hash")
    if not protocol_hash:
        raise FullSystemAuthorityError("verification protocol_hash is required")
    evidence_hash = verification.get("evidence_hash")
    context_version = verification.get("context_version")
    protocol_events = [
        event for event in events
        if event.get("event_type") == "protocol"
        and event.get("protocol_hash") == protocol_hash
    ]
    if not protocol_events:
        raise FullSystemAuthorityError("protocol provenance event missing")
    if not any(
        event.get("context_version") == context_version
        and event.get("evidence_hash") == evidence_hash
        for event in protocol_events
    ):
        raise FullSystemAuthorityError("protocol is not bound to evidence and context")


def _validate_evidence_context_binding(events, verification) -> None:
    evidence_hash = verification.get("evidence_hash")
    context_version = verification.get("context_version")
    if not evidence_hash or not context_version:
        raise FullSystemAuthorityError("evidence context binding fields are required")
    evidence_events = [
        event for event in events
        if event.get("event_type") == "evidence"
        and event.get("evidence_hash") == evidence_hash
    ]
    if not evidence_events:
        raise FullSystemAuthorityError("evidence context event missing")
    if not any(event.get("context_version") == context_version for event in evidence_events):
        raise FullSystemAuthorityError("evidence context mismatch")


def _validate_evidence_provenance(events, verification) -> None:
    evidence_hash = verification.get("evidence_hash")
    if not evidence_hash:
        raise FullSystemAuthorityError("verification evidence_hash is required")
    observation_ids = {
        event.get("parent_event_id")
        for event in events
        if event.get("event_type") == "verification"
        and event.get("verification_id") == verification.get("verification_id")
        and event.get("parent_event_id")
    }
    evidence_events = [
        event for event in events
        if event.get("event_type") == "evidence"
        and event.get("evidence_hash") == evidence_hash
    ]
    if not evidence_events:
        raise FullSystemAuthorityError("evidence provenance event missing")
    if len(evidence_events) != 1:
        raise FullSystemAuthorityError("selected evidence identity is ambiguous")
    if not any(event.get("parent_event_id") in observation_ids for event in evidence_events):
        raise FullSystemAuthorityError("evidence is not derived from verification observation")


def _validate_verification_target_binding(events, verification) -> None:
    target_id = verification.get("target_id")
    if not target_id:
        raise FullSystemAuthorityError("verification target_id is required")
    verification_events = [
        event for event in events
        if event.get("event_type") == "verification"
        and event.get("verification_id") == verification.get("verification_id")
    ]
    if not verification_events:
        raise FullSystemAuthorityError("verification event missing")
    if len(verification_events) != 1:
        raise FullSystemAuthorityError("selected verification identity is ambiguous")
    observation_ids = {
        event.get("parent_event_id")
        for event in verification_events
        if event.get("parent_event_id")
    }
    observations = {
        event.get("event_id"): event
        for event in events
        if event.get("event_type") == "observation"
    }
    if not observation_ids:
        raise FullSystemAuthorityError("verification observation binding missing")
    if not any(observations.get(oid, {}).get("target_id") == target_id for oid in observation_ids):
        raise FullSystemAuthorityError("verification target does not match observation")


def _validate_verification_semantic_binding(verification, decision, approval, execution) -> None:
    for field in ("context_version", "evidence_hash", "protocol_hash", "proposal_id"):
        value = verification.get(field)
        if not value:
            raise FullSystemAuthorityError(f"verification binding missing: {field}")
        if value != decision.get(field):
            raise FullSystemAuthorityError(f"verification decision {field} mismatch")
        if value != approval.get(field):
            raise FullSystemAuthorityError(f"verification approval {field} mismatch")
        if value != execution.get(field):
            raise FullSystemAuthorityError(f"verification execution {field} mismatch")


def validate_full_system_authority(
    *,
    events,
    approval: Mapping[str, Any],
    execution: Mapping[str, Any],
    verification: Mapping[str, Any],
    verification_digest: str,
    persisted: Mapping[str, Any],
    ui_event: Mapping[str, Any],
    identity: Mapping[str, Any],
    decision: Mapping[str, Any],
    signature: str,
    secret: bytes,
    decision_time: str,
    trusted_principals: frozenset[str],
    trusted_verifiers: frozenset[str],
    trusted_keys: frozenset[str],
    trusted_from: str,
    trusted_until: str | None = None,
    revoked_at: str | None = None,
    verifier_revoked_at: frozenset[str] = frozenset(),
    current_revoked_authentications: frozenset[str] = frozenset(),
    seen_authentication_ids: frozenset[str] = frozenset(),
    current_revoked_keys: frozenset[str] = frozenset(),
    seen_decision_ids: frozenset[str] = frozenset(),
) -> None:
    try:
        validate_cross_layer_authority_chain(
            events, approval, execution, verification, verification_digest,
            persisted, trusted_at=trusted_verifiers, revoked_at=verifier_revoked_at,
            current_revoked_verifiers=verifier_revoked_at,
        )
        _validate_system_temporal_binding(events, verification, decision, approval, execution)
        _validate_verification_target_binding(events, verification)
        _validate_evidence_provenance(events, verification)
        _validate_evidence_context_binding(events, verification)
        _validate_protocol_binding(events, verification)
        _validate_proposal_binding(events, verification)
        _validate_proposal_decision_binding(events, verification, decision, approval, execution)
        _validate_semantic_parent_chain(events)
        _validate_parent_binding_content(events)
        _validate_parent_time_constraints(events)
        _validate_unique_event_ids(events)
        _validate_event_graph_acyclic(events)
        _validate_semantic_event_uniqueness(events)
        _validate_temporal_permutation(events, verification, decision, approval, execution)
        _validate_observation_evidence_temporal_binding(events, verification)
        _validate_evidence_verification_temporal_binding(events, verification)
        _validate_verification_proposal_temporal_binding(events, verification)
        _validate_proposal_temporal_binding(events, verification, decision, approval, execution)
        _validate_verification_semantic_binding(verification, decision, approval, execution)
        validate_full_human_gate(
            ui_event=ui_event, identity=identity, decision=decision,
            approval=approval, execution=execution, signature=signature,
            secret=secret, persisted=persisted, decision_time=decision_time,
            trusted_principals=trusted_principals, trusted_keys=trusted_keys,
            trusted_from=trusted_from, trusted_until=trusted_until,
            revoked_at=revoked_at,
            current_revoked_authentications=current_revoked_authentications,
            seen_authentication_ids=seen_authentication_ids,
            current_revoked_keys=current_revoked_keys,
            seen_decision_ids=seen_decision_ids,
        )
        if decision.get("approval_id") != approval.get("approval_id"):
            raise FullSystemAuthorityError("human decision approval mismatch")
        if decision.get("context_version") != approval.get("context_version"):
            raise FullSystemAuthorityError("human decision context mismatch")
        if decision.get("evidence_hash") != approval.get("evidence_hash"):
            raise FullSystemAuthorityError("human decision evidence mismatch")
        if decision.get("protocol_hash") != approval.get("protocol_hash"):
            raise FullSystemAuthorityError("human decision protocol mismatch")
        if decision.get("proposal_id") != approval.get("proposal_id"):
            raise FullSystemAuthorityError("human decision proposal mismatch")
    except Exception as exc:
        if isinstance(exc, FullSystemAuthorityError):
            raise
        raise FullSystemAuthorityError(str(exc)) from exc
