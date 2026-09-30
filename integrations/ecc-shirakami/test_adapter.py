import unittest

from adapter import ECCShirakamiAdapter, HumanGate, ShirakamiContext


class AdapterBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.adapter = ECCShirakamiAdapter()
        self.context = ShirakamiContext(
            task="review a proposed change",
            context={"repo": "Shirakami-Project"},
            protocol="reviewer-protocol-v0.1",
            evidence_requirements=["execution_trace"],
        )

    def test_prepare_marks_runtime_as_non_authoritative(self):
        request = self.adapter.prepare(self.context)
        self.assertEqual(request.runtime, "ECC")
        self.assertEqual(request.authority, "none")
        self.assertTrue(request.request_id.startswith("SH-ECC-"))

    def test_runtime_result_stays_unverified_by_default(self):
        request = self.adapter.prepare(self.context)
        observation = self.adapter.observe(request, {"ok": True})
        self.assertEqual(observation.verification_status, "unverified")
        self.assertTrue(observation.uncertainties)

    def test_consequential_action_is_blocked_without_human_gate(self):
        request = self.adapter.prepare(self.context)
        observation = self.adapter.observe(request, {"ok": True})
        result = self.adapter.gate(observation, HumanGate())
        self.assertEqual(result["status"], "awaiting_human_gate")
        self.assertIsNone(result["decision"])

    def test_explicit_human_gate_is_recorded(self):
        request = self.adapter.prepare(self.context)
        observation = self.adapter.observe(request, {"ok": True}, verification_status="verified")
        gate = HumanGate(approved=True, decided_by="human", decision_note="approved for test")
        result = self.adapter.gate(observation, gate)
        self.assertEqual(result["status"], "human_approved")
        self.assertEqual(result["authority"], "human")
        self.assertEqual(result["decided_by"], "human")


if __name__ == "__main__":
    unittest.main()
