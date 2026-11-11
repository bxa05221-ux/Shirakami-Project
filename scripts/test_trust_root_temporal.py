import unittest

from runtime.trust_root_temporal import (
    TrustRootTemporalError,
    reject_revoked_replay,
    validate_trust_at_event_time,
)


class TrustRootTemporalTests(unittest.TestCase):
    def test_trusted_verifier_at_event_time_passes(self):
        validate_trust_at_event_time(
            verifier="v1",
            event_time="2026-10-07T06:00:00+00:00",
            trusted_at=frozenset({"v1"}),
            revoked_at=frozenset(),
        )

    def test_unknown_verifier_fails(self):
        with self.assertRaises(TrustRootTemporalError):
            validate_trust_at_event_time(
                verifier="unknown",
                event_time="2026-10-07T06:00:00+00:00",
                trusted_at=frozenset({"v1"}),
                revoked_at=frozenset(),
            )

    def test_revoked_verifier_fails(self):
        with self.assertRaises(TrustRootTemporalError):
            validate_trust_at_event_time(
                verifier="v1",
                event_time="2026-10-07T06:00:00+00:00",
                trusted_at=frozenset({"v1"}),
                revoked_at=frozenset({"v1"}),
            )

    def test_revoked_replay_is_rejected(self):
        with self.assertRaises(TrustRootTemporalError):
            reject_revoked_replay(
                verifier="v1",
                verification_time="2026-10-07T06:00:00+00:00",
                current_revoked=frozenset({"v1"}),
            )

    def test_invalid_timestamp_fails_closed(self):
        with self.assertRaises(TrustRootTemporalError):
            validate_trust_at_event_time(
                verifier="v1",
                event_time="not-a-time",
                trusted_at=frozenset({"v1"}),
                revoked_at=frozenset(),
            )


if __name__ == "__main__":
    unittest.main()
