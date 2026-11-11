import pytest

from runtime.human_key_temporal import HumanKeyTemporalError, validate_key_at_decision_time


DECISION = {"key_id": "KEY1"}


def test_key_valid_at_decision_time():
    validate_key_at_decision_time(
        DECISION,
        decision_time="2026-10-07T10:00:00+00:00",
        trusted_from="2026-10-01T00:00:00+00:00",
        trusted_until="2026-11-01T00:00:00+00:00",
    )


def test_pre_activation_key_fails():
    with pytest.raises(HumanKeyTemporalError):
        validate_key_at_decision_time(
            DECISION,
            decision_time="2026-09-30T23:59:59+00:00",
            trusted_from="2026-10-01T00:00:00+00:00",
        )


def test_post_expiry_key_fails():
    with pytest.raises(HumanKeyTemporalError):
        validate_key_at_decision_time(
            DECISION,
            decision_time="2026-11-01T00:00:00+00:00",
            trusted_from="2026-10-01T00:00:00+00:00",
            trusted_until="2026-11-01T00:00:00+00:00",
        )


def test_post_revocation_key_fails():
    with pytest.raises(HumanKeyTemporalError):
        validate_key_at_decision_time(
            DECISION,
            decision_time="2026-10-20T00:00:00+00:00",
            trusted_from="2026-10-01T00:00:00+00:00",
            revoked_at="2026-10-15T00:00:00+00:00",
        )


def test_naive_timestamp_fails():
    with pytest.raises(HumanKeyTemporalError):
        validate_key_at_decision_time(
            DECISION,
            decision_time="2026-10-07T10:00:00",
            trusted_from="2026-10-01T00:00:00+00:00",
        )
