import unittest

from runtime.revocation_decision_recovery import (
    RevocationDecisionRecoveryError,
    validate_decision_recovery_after_revocation,
)

APPROVAL = {
    "approval_id": "A1",
    "context_version": 3,
    "evidence_hash": "E1",
    "protocol_hash": "P1",
    "proposal_id": "PR1",
    "verifier": "v1",
}

PERSISTED = {
    **APPROVAL,
    "human_approval": True,
    "runtime_authority": False,
}


class RevocationDecisionRecoveryTests(unittest.TestCase):
    def test_valid_recovery_passes(self):
        validate_decision_recovery_after_revocation(
            APPROVAL, PERSISTED, current_revoked_verifiers=set()
        )

    def test_revoked_verifier_cannot_resurrect_authority(self):
        with self.assertRaises(RevocationDecisionRecoveryError):
            validate_decision_recovery_after_revocation(
                APPROVAL, PERSISTED, current_revoked_verifiers={"v1"}
            )

    def test_approval_binding_missing_fails_closed(self):
        for field in (
            "approval_id",
            "context_version",
            "evidence_hash",
            "protocol_hash",
            "proposal_id",
        ):
            with self.subTest(field=field):
                approval = dict(APPROVAL)
                approval.pop(field)
                with self.assertRaises(RevocationDecisionRecoveryError):
                    validate_decision_recovery_after_revocation(
                        approval, PERSISTED, current_revoked_verifiers=set()
                    )

    def test_persisted_binding_missing_fails_closed(self):
        for field in (
            "approval_id",
            "context_version",
            "evidence_hash",
            "protocol_hash",
            "proposal_id",
        ):
            with self.subTest(field=field):
                persisted = dict(PERSISTED)
                persisted.pop(field)
                with self.assertRaises(RevocationDecisionRecoveryError):
                    validate_decision_recovery_after_revocation(
                        APPROVAL, persisted, current_revoked_verifiers=set()
                    )

    def test_binding_mutation_fails(self):
        persisted = {**PERSISTED, "evidence_hash": "ATTACK"}
        with self.assertRaises(RevocationDecisionRecoveryError):
            validate_decision_recovery_after_revocation(
                APPROVAL, persisted, current_revoked_verifiers=set()
            )

    def test_missing_human_approval_fails_closed(self):
        persisted = {**PERSISTED, "human_approval": False}
        with self.assertRaises(RevocationDecisionRecoveryError):
            validate_decision_recovery_after_revocation(
                APPROVAL, persisted, current_revoked_verifiers=set()
            )

    def test_runtime_authority_cannot_be_restored(self):
        persisted = {**PERSISTED, "runtime_authority": True}
        with self.assertRaises(RevocationDecisionRecoveryError):
            validate_decision_recovery_after_revocation(
                APPROVAL, persisted, current_revoked_verifiers=set()
            )


if __name__ == "__main__":
    unittest.main()
