import unittest

from runtime.decision_binding import DecisionBindingError
from runtime.end_to_end_integrity import validate_end_to_end
from runtime.recovery_integrity import RecoveryIntegrityError
from runtime.temporal_integrity import TemporalIntegrityError


APPROVAL = {
    "approval_id": "A1",
    "context_version": 10,
    "evidence_hash": "E10",
    "protocol_hash": "P10",
    "proposal_id": "PR10",
}

EXECUTION = {**APPROVAL, "runtime_authority": False}

EVENTS = [
    {"event_id": "obs-1", "event_type": "observation",
     "occurred_at": "2026-10-07T10:00:00+09:00"},
    {"event_id": "approval-1", "event_type": "human_approval",
     **APPROVAL, "occurred_at": "2026-10-07T10:05:00+09:00",
     "parent_event_id": "obs-1"},
    {"event_id": "exec-1", "event_type": "execution",
     **EXECUTION, "occurred_at": "2026-10-07T10:06:00+09:00",
     "parent_event_id": "approval-1"},
]


class EndToEndIntegrityTests(unittest.TestCase):
    def test_complete_chain_passes(self):
        validate_end_to_end(
            EVENTS, APPROVAL, EXECUTION, {**APPROVAL, "state": "committed"}
        )

    def test_temporal_failure_blocks_entire_chain(self):
        events = [dict(event) for event in EVENTS]
        events[-1]["occurred_at"] = "2026-10-07T10:04:00+09:00"
        events[-1]["parent_event_id"] = None
        with self.assertRaises(TemporalIntegrityError):
            validate_end_to_end(
                events, APPROVAL, EXECUTION, {**APPROVAL, "state": "committed"}
            )

    def test_decision_scope_mutation_blocks_entire_chain(self):
        execution = {**EXECUTION, "evidence_hash": "ATTACKED"}
        with self.assertRaises(DecisionBindingError):
            validate_end_to_end(
                EVENTS, APPROVAL, execution, {**APPROVAL, "state": "committed"}
            )

    def test_runtime_authority_mutation_blocks_entire_chain(self):
        execution = {**EXECUTION, "runtime_authority": True}
        with self.assertRaises(DecisionBindingError):
            validate_end_to_end(
                EVENTS, APPROVAL, execution, {**APPROVAL, "state": "committed"}
            )

    def test_recovery_crash_boundary_blocks_entire_chain(self):
        persisted = {**APPROVAL, "state": "execution_applied"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_end_to_end(EVENTS, APPROVAL, EXECUTION, persisted)

    def test_recovery_scope_mutation_blocks_entire_chain(self):
        persisted = {**APPROVAL, "state": "committed", "protocol_hash": "ATTACKED"}
        with self.assertRaises(RecoveryIntegrityError):
            validate_end_to_end(EVENTS, APPROVAL, EXECUTION, persisted)


if __name__ == "__main__":
    unittest.main()
