"""Deterministic regression tests for logged dialogue states (no LLM tests)."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("dialogue_tracker", ROOT / "scripts/dialogue_tracker.py")
assert SPEC and SPEC.loader
tracker = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(tracker)


class TestDialogueTracker(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.p = Path(self.temp.name)
        tracker.initialize(self.p)

    def tearDown(self):
        self.temp.cleanup()

    def test_defaults_and_no_overwrite(self):
        state = tracker.load(self.p)
        self.assertEqual(state["budget"]["target_min"], 10)
        self.assertEqual(state["budget"]["target_max"], 12)
        tracker.record_round(self.p, "P1-positioning", "substantial", "User title", "Critique and question")
        self.assertFalse(tracker.initialize(self.p)["created"])
        self.assertEqual(len(tracker.load(self.p)["rounds"]), 1)

    def test_phase_gates_require_examined_not_proposed(self):
        for dim in tracker.PHASES["P1-positioning"]:
            tracker.set_coverage(self.p, dim, "proposed", "assistant provided candidate")
        self.assertFalse(tracker.assess(tracker.load(self.p))["phase_gates"]["P1-positioning"]["ready_for_researcher_review"])
        for dim in tracker.PHASES["P1-positioning"]:
            tracker.set_coverage(self.p, dim, "examined", "user and assistant examined tradeoffs")
        self.assertTrue(tracker.assess(tracker.load(self.p))["phase_gates"]["P1-positioning"]["ready_for_researcher_review"])

    def test_three_non_novel_rounds_trigger_heuristic(self):
        for i in range(3):
            tracker.record_round(self.p, "P2-frameworks", "none", f"User {i}", f"Analysis {i}")
        report = tracker.assess(tracker.load(self.p))
        self.assertTrue(report["saturation_heuristic_triggered"])
        self.assertFalse(report["eligible_to_offer_final_review"])
        self.assertIn("do not mistake repetition", report["suggested_action"])

    def test_no_false_saturation_from_incremental_round(self):
        for novelty in ("none", "incremental", "none"):
            tracker.record_round(self.p, "P3-critique", novelty, "User", "Analysis")
        self.assertFalse(tracker.assess(tracker.load(self.p))["saturation_heuristic_triggered"])

    def test_critical_issue_blocks_offer_even_with_full_coverage(self):
        for dim in tracker.COVERAGE:
            tracker.set_coverage(self.p, dim, "examined", "examined in transcript")
        self.assertTrue(tracker.assess(tracker.load(self.p))["eligible_to_offer_final_review"])
        issue = tracker.raise_issue(self.p, "critical", "Taxonomy core category disputed")
        self.assertFalse(tracker.assess(tracker.load(self.p))["eligible_to_offer_final_review"])
        tracker.resolve_issue(self.p, issue["id"], "Deferred to source verification with alternatives preserved")
        self.assertTrue(tracker.assess(tracker.load(self.p))["eligible_to_offer_final_review"])

    def test_extension_requires_reason_and_logs(self):
        with self.assertRaisesRegex(ValueError, "reason"):
            tracker.extend(self.p, " ")
        result = tracker.extend(self.p, "New unresolved benchmark leakage confound", 3)
        self.assertEqual(result["target_max"], 15)
        self.assertEqual(tracker.load(self.p)["budget"]["extensions"][0]["at_round"], 0)

    def test_invalid_record_and_coverage_rejected(self):
        with self.assertRaises(ValueError):
            tracker.record_round(self.p, "P1-positioning", "none", "", "analysis")
        with self.assertRaises(ValueError):
            tracker.set_coverage(self.p, "scope", "examined", "")
        with self.assertRaises(ValueError):
            tracker.set_coverage(self.p, "invented", "examined", "something")
        self.assertEqual(len(tracker.load(self.p)["rounds"]), 0)

    def test_no_silent_overwrite_state(self):
        tracker.raise_issue(self.p, "high", "One open issue")
        with self.assertRaises(ValueError):
            tracker.resolve_issue(self.p, "ISS-999", "Resolution")
        self.assertEqual(len(tracker.load(self.p)["issues"]), 1)

    def test_cli_status_and_extension(self):
        self.assertEqual(tracker.main(["status", "--project", str(self.p)]), 0)
        self.assertEqual(tracker.main(["extend", "--project", str(self.p), "--reason", "pending dispute"]), 0)
        self.assertEqual(tracker.load(self.p)["budget"]["target_max"], 15)


if __name__ == "__main__":
    unittest.main()
