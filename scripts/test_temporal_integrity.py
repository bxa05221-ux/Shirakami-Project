import pytest

from runtime.temporal_integrity import TemporalIntegrityError, validate_event_graph


def _base():
    return [
        {
            "event_id": "obs-1",
            "event_type": "observation",
            "occurred_at": "2026-10-07T10:00:00+09:00",
        },
        {
            "event_id": "approval-1",
            "event_type": "human_approval",
            "approval_id": "A1",
            "context_version": 10,
            "occurred_at": "2026-10-07T10:05:00+09:00",
            "parent_event_id": "obs-1",
        },
        {
            "event_id": "exec-1",
            "event_type": "execution",
            "approval_id": "A1",
            "context_version": 10,
            "occurred_at": "2026-10-07T10:06:00+09:00",
            "parent_event_id": "approval-1",
        },
    ]


def test_valid_temporal_chain_passes():
    validate_event_graph(_base())


def test_stale_approval_is_rejected():
    events = _base()
    events[-1]["context_version"] = 11
    with pytest.raises(TemporalIntegrityError, match="stale approval"):
        validate_event_graph(events)


def test_future_evidence_is_rejected():
    events = [
        {
            "event_id": "decision-1",
            "event_type": "human_decision",
            "decision_id": "D1",
            "occurred_at": "2026-10-07T10:00:00+09:00",
            "evidence_occurred_at": "2026-10-07T10:01:00+09:00",
        }
    ]
    with pytest.raises(TemporalIntegrityError, match="future evidence"):
        validate_event_graph(events)


def test_replayed_decision_is_rejected():
    events = [
        {"event_id": "d1", "event_type": "human_decision", "decision_id": "D1",
         "occurred_at": "2026-10-07T10:00:00+09:00"},
        {"event_id": "d2", "event_type": "human_decision", "decision_id": "D1",
         "occurred_at": "2026-10-07T10:01:00+09:00"},
    ]
    with pytest.raises(TemporalIntegrityError, match="decision replay"):
        validate_event_graph(events)


def test_replayed_approval_is_rejected():
    events = _base()
    events.append({
        "event_id": "approval-2",
        "event_type": "human_approval",
        "approval_id": "A1",
        "context_version": 10,
        "occurred_at": "2026-10-07T10:07:00+09:00",
        "parent_event_id": "obs-1",
    })
    with pytest.raises(TemporalIntegrityError, match="approval replay"):
        validate_event_graph(events)


def test_execution_before_approval_is_rejected():
    events = _base()
    events[-1]["occurred_at"] = "2026-10-07T10:04:00+09:00"
    events[-1]["parent_event_id"] = None
    with pytest.raises(TemporalIntegrityError, match="execution precedes approval"):
        validate_event_graph(events)


def test_out_of_order_parent_is_rejected():
    events = _base()
    events[-1]["occurred_at"] = "2026-10-07T10:04:00+09:00"
    with pytest.raises(TemporalIntegrityError, match="precedes parent"):
        validate_event_graph(events)


def test_missing_parent_is_rejected():
    events = _base()
    events[1]["parent_event_id"] = "missing"
    with pytest.raises(TemporalIntegrityError, match="missing parent"):
        validate_event_graph(events)


def test_invalid_timestamp_fails_closed():
    events = _base()
    events[0]["occurred_at"] = "not-a-time"
    with pytest.raises(TemporalIntegrityError, match="invalid timestamp"):
        validate_event_graph(events)
