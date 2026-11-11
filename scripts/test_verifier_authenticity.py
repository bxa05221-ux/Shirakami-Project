import unittest

from runtime.verifier_authenticity import (
    VerifierAuthenticityError,
    sign_verification,
    validate_verifier_authenticity,
)


SECRET = b"shirakami-test-secret"
RECORD = {
    "verification_id": "V1",
    "target_id": "EXEC-1",
    "result": "pass",
    "verifier": "verification-suite-v1",
    "verifier_instance": "instance-001",
    "human_approval": False,
    "runtime_authority": False,
}


class VerifierAuthenticityTests(unittest.TestCase):
    def test_valid_signature_passes(self):
        signature = sign_verification(RECORD, SECRET)
        validate_verifier_authenticity(RECORD, signature, SECRET)

    def test_payload_mutation_fails(self):
        signature = sign_verification(RECORD, SECRET)
        mutated = {**RECORD, "result": "fail"}
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(mutated, signature, SECRET)

    def test_verifier_substitution_fails(self):
        signature = sign_verification(RECORD, SECRET)
        mutated = {**RECORD, "verifier": "forged-verifier"}
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(mutated, signature, SECRET)

    def test_instance_substitution_fails(self):
        signature = sign_verification(RECORD, SECRET)
        mutated = {**RECORD, "verifier_instance": "instance-999"}
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(mutated, signature, SECRET)

    def test_wrong_secret_fails(self):
        signature = sign_verification(RECORD, SECRET)
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(RECORD, signature, b"wrong-secret")

    def test_authenticated_verifier_cannot_create_human_approval(self):
        record = {**RECORD, "human_approval": True}
        signature = sign_verification(record, SECRET)
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(record, signature, SECRET)

    def test_authenticated_verifier_cannot_create_runtime_authority(self):
        record = {**RECORD, "runtime_authority": True}
        signature = sign_verification(record, SECRET)
        with self.assertRaises(VerifierAuthenticityError):
            validate_verifier_authenticity(record, signature, SECRET)


if __name__ == "__main__":
    unittest.main()
