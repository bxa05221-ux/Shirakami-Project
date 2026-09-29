import unittest

from src.github_japanese_context_bridge import build_pull_request_context, render_japanese_context


class JapaneseContextBridgeTest(unittest.TestCase):
    def test_unknown_ci_is_not_invented_as_success(self):
        context = build_pull_request_context(29, "open", True, 1, 279, 0, "afb67caf503b498beb7091235d07c1c030f2b475")
        self.assertIn("このコミットについて、CI/statusの結果は確認できていません。", context.unknowns)
        self.assertNotIn("成功", "\n".join(context.facts))
        self.assertTrue(context.human_gate)

    def test_render_keeps_fact_and_unknown_separate(self):
        context = build_pull_request_context(29, "open", True, 1, 279, 0, "afb67caf503b498beb7091235d07c1c030f2b475")
        rendered = render_japanese_context(context)
        self.assertIn("観測された事実", rendered)
        self.assertIn("未確認事項（UNKNOWN）", rendered)
        self.assertIn("Human Gate", rendered)


if __name__ == "__main__":
    unittest.main()
