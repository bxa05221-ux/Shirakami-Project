import unittest

from runtime.verifier_provenance import (
    VerifierProvenanceError,
    validate_verifier_provenance,
)


VALID = {
    "verification_id": "V1",
    "target_id": "EXEC-1",
    "verifier": "verification-suite-v1",
    "verifier_instance": "instance-001",
    "verifier_authority": False,
    "human_approval": False,
    "runtime_authority": False,
}


class VerifierProvenanceTests(unittest.TestCase):
    def test_valid_provenance(self):
        validate_verifier_provenance(VALID)

    def test_missing_identity_fields_fail_closed(self):
        for field in ("verification_id", "target_id", "verifier", "verifier_instance"):
            with self.subTest(field=field):
                record = dict(VALID)
                del record[field]
                with self.assertRaises(VerifierProvenanceError):
                    validate_verifier_provenance(record)

    def test_verifier_cannot_claim_authority(self):
        record = {**VALID, "verifier_authority": True}
        with self.assertRaises(VerifierProvenanceError):
            validate_verifier_provenance(record)

    def test_verifier_cannot_create_human_approval(self):
        record = {**VALID, "human_approval": True}
        with self.assertRaises(VerifierProvenanceError):
            validate_verifier_provenance(record)

    def test_verifier_cannot_create_runtime_authority(self):
        record = {**VALID, "runtime_authority": True}
        with self.assertRaises(VerifierProvenanceError):
            validate_verifier_provenance(record)

    def test_same_verifier_different_instance_is_distinct_provenance(self):
        first = {**VALID, "verifier_instance": "instance-001"}
        second = {**VALID, "verifier_instance": "instance-002"}
        validate_verifier_provenance(first)
        validate_verifier_provenance(second)
        self.assertNotEqual(
            first["verifier_instance"], second["verifier_instance"]
        )


if __name__ == "__main__":
    unittest.main()
