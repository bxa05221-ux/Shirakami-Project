import unittest

from runtime.trust_root import TrustRootError, validate_trusted_verifier
from runtime.verifier_authenticity import sign_verification

SECRET = b"shirakami-test-secret"
RECORD = {
    "verification_id": "V1",
    "target_id": "EXEC-1",
    "result": "pass",
    "verifier": "trusted-verifier",
    "verifier_instance": "instance-001",
    "human_approval": False,
    "runtime_authority": False,
}


class TrustRootTests(unittest.TestCase):
    def test_trusted_authenticated_verifier_passes(self):
        signature = sign_verification(RECORD, SECRET)
        validate_trusted_verifier(
            RECORD, signature, SECRET, {"trusted-verifier"}
        )

    def test_authentic_but_untrusted_verifier_fails(self):
        record = {**RECORD, "verifier": "unknown-verifier"}
        signature = sign_verification(record, SECRET)
        with self.assertRaises(TrustRootError):
            validate_trusted_verifier(
                record, signature, SECRET, {"trusted-verifier"}
            )

    def test_signature_with_wrong_key_fails(self):
        signature = sign_verification(RECORD, SECRET)
        with self.assertRaises(TrustRootError):
            validate_trusted_verifier(
                RECORD, signature, b"wrong-secret", {"trusted-verifier"}
            )

    def test_trust_list_substitution_fails(self):
        signature = sign_verification(RECORD, SECRET)
        with self.assertRaises(TrustRootError):
            validate_trusted_verifier(
                RECORD, signature, SECRET, {"different-verifier"}
            )

    def test_trust_root_cannot_create_human_approval(self):
        record = {**RECORD, "human_approval": True}
        signature = sign_verification(record, SECRET)
        with self.assertRaises(TrustRootError):
            validate_trusted_verifier(
                record, signature, SECRET, {"trusted-verifier"}
            )

    def test_trust_root_cannot_create_runtime_authority(self):
        record = {**RECORD, "runtime_authority": True}
        signature = sign_verification(record, SECRET)
        with self.assertRaises(TrustRootError):
            validate_trusted_verifier(
                record, signature, SECRET, {"trusted-verifier"}
            )


if __name__ == "__main__":
    unittest.main()
