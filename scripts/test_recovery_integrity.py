import unittest

from runtime.recovery_integrity import (
    RecoveryIntegrityError,
    recovery_action,
    validate_recovery,
)


APPROVAL = {
    "approval_id": "A1",
    "context_version": 10,
    "evidence_hash": "E10",
    "protocol_hash": "P10",
    "proposal_id": "PR10",
}


class RecoveryIntegrityTests(unittest.TestCase):
    def test_durable_approved_state_can_recover(self):
        persisted = {**APPROVAL, "state": "approved"}
        validate_recovery(APPROVAL, persisted)
        self.assertEqual(recovery_action(persisted), "resume_after_integrity_check")

    def test_candidate_recovery_does_not_execute(self):
        persisted = {**APPROVAL, "state": "candidate_created"}
        validate_recovery(APPROVAL, persisted)
        self.assertEqual(recovery_action(persisted), "reconcile_candidate")

    def test_verified_recovery_requires_reconciliation(self):
        persisted = {**APPROVAL, "state": "verified"}
        validate_recovery(APPROVAL, persisted)
        self.assertEqual(recovery_action(persisted), "reconcile_verified")

    def test_committed_recovery_never_resumes_execution(self):
        persisted = {**APPROVAL, "state": "committed"}
        validate_recovery(APPROVAL, persisted)
        self.assertEqual(recovery_action(persisted), "reconcile_committed")

    def test_crash_after_apply_start_is_quarantined(self):
        for state in ("apply_started", "execution_applied", "crashed", "incomplete"):
            persisted = {**APPROVAL, "state": state}
            self.assertEqual(recovery_action(persisted), "quarantine_and_reverify")
            with self.assertRaises(RecoveryIntegrityError):
                validate_recovery(APPROVAL, persisted)

    def test_unknown_state_is_fail_closed(self):
        persisted = {**APPROVAL, "state": "mystery"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)

    def test_approval_cannot_be_replayed_into_other_context(self):
        persisted = {**APPROVAL, "state": "approved", "context_version": 11}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)

    def test_evidence_cannot_be_swapped_after_restart(self):
        persisted = {**APPROVAL, "state": "verified", "evidence_hash": "E11"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)

    def test_protocol_cannot_be_swapped_after_restart(self):
        persisted = {**APPROVAL, "state": "candidate_created", "protocol_hash": "P11"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)

    def test_proposal_cannot_be_swapped_after_restart(self):
        persisted = {**APPROVAL, "state": "committed", "proposal_id": "PR11"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)

    def test_runtime_cannot_gain_authority_during_recovery(self):
        persisted = {**APPROVAL, "state": "approved", "runtime_authority": True}
        with self.assertRaises(RecoveryIntegrityError):
            validate_recovery(APPROVAL, persisted)


if __name__ == "__main__":
    unittest.main()
