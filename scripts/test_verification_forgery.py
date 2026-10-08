import unittest

from runtime.verification_forgery import (
    VerificationForgeryError,
    validate_verification_integrity,
    verification_digest,
)


VALID = {
    "verification_id": "V1",
    "target_id": "EXEC-1",
    "result": "pass",
    "verifier": "verification-suite-v1",
    "verifier_instance": "verification-suite-v1-i1",
    "human_approval": False,
    "runtime_authority": False,
}


class VerificationForgeryTests(unittest.TestCase):
    def test_original_record_matches_digest(self):
        validate_verification_integrity(VALID, verification_digest(VALID))

    def test_result_mutation_is_detected(self):
        digest = verification_digest(VALID)
        mutated = {**VALID, "result": "fail"}
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)

    def test_target_mutation_is_detected(self):
        digest = verification_digest(VALID)
        mutated = {**VALID, "target_id": "EXEC-ATTACK"}
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)

    def test_verifier_mutation_is_detected(self):
        digest = verification_digest(VALID)
        mutated = {**VALID, "verifier": "forged-verifier"}
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)

    def test_missing_binding_is_detected(self):
        digest = verification_digest(VALID)
        mutated = dict(VALID)
        del mutated["verification_id"]
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)

    def test_authority_claim_is_detected(self):
        digest = verification_digest(VALID)
        mutated = {**VALID, "runtime_authority": True}
        # Authority is outside the digest on purpose: adding authority must
        # still be rejected even if the underlying verification is unchanged.
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)

    def test_human_approval_claim_is_detected(self):
        digest = verification_digest(VALID)
        mutated = {**VALID, "human_approval": True}
        with self.assertRaises(VerificationForgeryError):
            validate_verification_integrity(mutated, digest)


if __name__ == "__main__":
    unittest.main()
