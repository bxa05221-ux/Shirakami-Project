#!/usr/bin/env python3
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from runtime.human_gate_profile import get_profile, review_requirements, validate_profile


class HumanGateProfileTests(unittest.TestCase):
    def test_strategic_profile_preserves_human_authority(self):
        profile = get_profile()
        validate_profile(profile)
        self.assertEqual(profile["invariants"]["selection_authority"], "human_gate")
        self.assertFalse(profile["authority"]["ai"]["may_select_strategy"])
        self.assertFalse(profile["authority"]["ai"]["may_commit_decision"])
        self.assertTrue(profile["authority"]["human_gate"]["may_select_strategy"])

    def test_strategic_profile_exposes_setting_and_asymmetry_checks(self):
        requirements = review_requirements()
        for name in ("setting", "positioning", "asymmetry", "assumptions",
                     "evidence", "alternatives", "reset"):
            self.assertIn(name, requirements)

    def test_profile_rejects_ai_strategy_selection(self):
        profile = get_profile()
        profile["authority"]["ai"]["may_select_strategy"] = True
        with self.assertRaises(ValueError):
            validate_profile(profile)

    def test_profile_rejects_authority_transfer(self):
        profile = get_profile()
        profile["invariants"]["execution_authorized"] = True
        with self.assertRaises(ValueError):
            validate_profile(profile)


if __name__ == "__main__":
    unittest.main()
