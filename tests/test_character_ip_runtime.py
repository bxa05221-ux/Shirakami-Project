import unittest

from runtime.character_ip import can_update_canonical_context, observe


class CharacterIPRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.context = {
            "id": "brass-band-demo-001",
            "state": "45 members preparing for performance",
        }
        self.ip = {
            "id": "ichiro_kurotaki",
            "type": "named_ip",
            "viewpoint": ["実践", "全体観察", "合奏"],
        }

    def test_observation_preserves_provenance_and_has_no_authority(self):
        result = observe(
            self.context,
            self.ip,
            question="全員が参加できる方法はあるか？",
            observation="参加形態を複数用意すれば、全員参加の余地を残せる。",
            basis=["brass-band-demo-001"],
            uncertainty=["実際の運用負荷は未確認"],
            proposal="参加方法を一つに固定せず検討する。",
        )

        self.assertEqual(result["ip"]["id"], "ichiro_kurotaki")
        self.assertEqual(
            result["provenance"]["source_context"],
            "existing_context",
        )
        self.assertEqual(result["authority"]["character_ip"], "none")
        self.assertFalse(result["context_update"]["allowed"])
        self.assertFalse(can_update_canonical_context(result))

    def test_rejected_symbolic_output_cannot_update_context(self):
        result = observe(
            self.context,
            self.ip,
            question="test",
            observation="rejected proposal",
            proposal="do not commit",
        )

        self.assertFalse(can_update_canonical_context(result))
        self.assertEqual(
            result["source_context"],
            self.context,
        )


if __name__ == "__main__":
    unittest.main()
