import unittest

from runtime.verification_integrity import (
    VerificationIntegrityError,
    can_verification_authorize,
    validate_verification_result,
)


VALID = {
    "verification_id": "V1",
    "target_id": "EXEC-1",
    "result": "pass",
    "verifier": "verification-suite-v1",
    "human_approval": False,
    "runtime_authority": False,
}


class VerificationIntegrityTests(unittest.TestCase):
    def test_valid_pass_is_evidence_not_authority(self):
        validate_verification_result(VALID)
        self.assertFalse(can_verification_authorize(VALID))

    def test_missing_verification_identity_fails_closed(self):
        for field in ("verification_id", "target_id", "verifier"):
            value = dict(VALID)
            del value[field]
            with self.assertRaises(VerificationIntegrityError):
                validate_verification_result(value)

    def test_invalid_result_fails_closed(self):
        value = {**VALID, "result": "approved"}
        with self.assertRaises(VerificationIntegrityError):
            validate_verification_result(value)

    def test_verification_cannot_create_human_approval(self):
        value = {**VALID, "human_approval": True}
        with self.assertRaises(VerificationIntegrityError):
            validate_verification_result(value)

    def test_verification_cannot_claim_runtime_authority(self):
        value = {**VALID, "runtime_authority": True}
        with self.assertRaises(VerificationIntegrityError):
            validate_verification_result(value)

    def test_fail_is_still_not_authority(self):
        value = {**VALID, "result": "fail"}
        validate_verification_result(value)
        self.assertFalse(can_verification_authorize(value))


if __name__ == "__main__":
    unittest.main()
