import unittest

from runtime.trust_root_governance import (
    TrustRootGovernanceError,
    validate_trust_root_transition,
    verifier_is_trusted,
)


class TrustRootGovernanceTests(unittest.TestCase):
    def test_authorized_transition_passes(self):
        result = validate_trust_root_transition(
            frozenset({"v1"}),
            frozenset({"v1", "v2"}),
            change_authorized=True,
        )
        self.assertEqual(result, frozenset({"v1", "v2"}))

    def test_unauthorized_transition_fails_closed(self):
        with self.assertRaises(TrustRootGovernanceError):
            validate_trust_root_transition(
                frozenset({"v1"}),
                frozenset({"v1", "attacker"}),
                change_authorized=False,
            )

    def test_revoked_verifier_cannot_be_added(self):
        with self.assertRaises(TrustRootGovernanceError):
            validate_trust_root_transition(
                frozenset({"v1"}),
                frozenset({"v1", "v2"}),
                change_authorized=True,
                revoked=frozenset({"v2"}),
            )

    def test_revocation_overrides_trust(self):
        self.assertFalse(
            verifier_is_trusted(
                "v1",
                frozenset({"v1"}),
                frozenset({"v1"}),
            )
        )

    def test_unknown_verifier_is_untrusted(self):
        self.assertFalse(
            verifier_is_trusted("unknown", frozenset({"v1"}))
        )

    def test_invalid_identity_fails_closed(self):
        with self.assertRaises(TrustRootGovernanceError):
            validate_trust_root_transition(
                frozenset({"v1"}),
                frozenset({"v1", ""}),
                change_authorized=True,
            )


if __name__ == "__main__":
    unittest.main()
