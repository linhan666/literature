"""Deterministic structural tests; not an LLM or scientific validation suite."""
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SPEC = importlib.util.spec_from_file_location("handoff", ROOT / "scripts/handoff.py")
assert SPEC and SPEC.loader
handoff = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(handoff)
SAMPLE = (ROOT / "assets/sample_provisional_handoff.md").read_text(encoding="utf-8")


class TestHandoff(unittest.TestCase):
    def test_example_is_valid_but_provisional(self):
        audit = handoff.validate(SAMPLE)
        self.assertTrue(audit["ok"], audit["errors"])
        self.assertEqual(audit["stage"], "provisional")
        self.assertEqual(audit["literature_status"], "not-searched")

    def test_reject_missing_heading(self):
        modified = SAMPLE.replace("## 11. Claim-verification backlog and search seeds", "## 11. Missing")
        audit = handoff.validate(modified)
        self.assertFalse(audit["ok"])
        self.assertTrue(any("Claim-verification backlog" in e for e in audit["errors"]))

    def test_reject_invalid_stage(self):
        modified = SAMPLE.replace("stage: provisional", "stage: all-verified", 1)
        audit = handoff.validate(modified)
        self.assertFalse(audit["ok"])
        self.assertTrue(any("Invalid stage" in e for e in audit["errors"]))

    def test_reject_leftover_template_markers(self):
        audit = handoff.validate(SAMPLE + "\n{{WORKING_TITLE}}\n")
        self.assertFalse(audit["ok"])
        self.assertTrue(any("placeholders" in e for e in audit["errors"]))

    def test_reject_missing_frontmatter(self):
        audit = handoff.validate(SAMPLE.split("---\n", 2)[-1])
        self.assertFalse(audit["ok"])
        self.assertTrue(any("frontmatter" in e.lower() for e in audit["errors"]))

    def test_init_does_not_overwrite_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            project = Path(td)
            result = handoff.init_project(project)
            self.assertEqual(len(result["created"]), 3)
            file = project / "input/topic.md"
            file.write_text("My original topic", encoding="utf-8")
            second = handoff.init_project(project)
            self.assertEqual(len(second["skipped_existing"]), 3)
            self.assertEqual(file.read_text(encoding="utf-8"), "My original topic")

    def test_provisional_export_is_blocked_by_default(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            handoff.init_project(p)
            draft = p / "drafts/discussion_summary.md"
            draft.write_text(SAMPLE, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "provisional"):
                handoff.export(p, None, False, False)
            self.assertFalse((p / "input/discussion_summary.md").exists())

    def test_export_provisional_with_explicit_permission(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            handoff.init_project(p)
            draft = p / "drafts/discussion_summary.md"
            draft.write_text(SAMPLE, encoding="utf-8")
            result = handoff.export(p, None, True, False)
            target = p / "input/discussion_summary.md"
            self.assertEqual(target.read_text(encoding="utf-8"), SAMPLE)
            self.assertEqual(result["stage"], "provisional")

    def test_no_silent_overwrite(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            handoff.init_project(p)
            (p / "drafts/discussion_summary.md").write_text(SAMPLE, encoding="utf-8")
            handoff.export(p, None, True, False)
            with self.assertRaisesRegex(ValueError, "already exists"):
                handoff.export(p, None, True, False)

    def test_complete_stage_requires_real_provenance_semantically(self):
        complete = SAMPLE.replace("stage: provisional", "stage: dialogue-complete", 1)
        # Even when structurally valid, the script cannot prove the source transcript
        # contained a real author confirmation. The skill instruction governs this.
        report = handoff.validate(complete)
        self.assertTrue(report["ok"])
        self.assertIn("Structural check only", report["note"])

    def test_cli_init_validate_exit_codes(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)
            self.assertEqual(handoff.main(["init", "--project", str(p)]), 0)
            draft = p / "drafts/discussion_summary.md"
            self.assertEqual(handoff.main(["validate", "--file", str(draft)]), 2)
            draft.write_text(SAMPLE, encoding="utf-8")
            self.assertEqual(handoff.main(["validate", "--file", str(draft)]), 0)


if __name__ == "__main__":
    unittest.main()
