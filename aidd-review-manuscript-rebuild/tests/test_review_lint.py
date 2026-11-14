"""Tiny local tests for static checks, not an AIDD scientific benchmark."""
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from review_lint import extract_citekeys, hide_fenced_code, inspect, parse_bib


class StaticLintTests(unittest.TestCase):
    def test_bib_duplicate(self):
        keys, dupe = parse_bib("@article{one, title={A}}\n@book{one,title={B}}\n@article{two,title={C}}")
        self.assertEqual(keys, {"one", "two"})
        self.assertEqual(dupe, ["one"])

    def test_pandoc_and_latex_cites(self):
        value = "Evidence [@smith2024; @liu2025]. Later \\citet[see][p. 3]{smith2024,other}."
        self.assertEqual(extract_citekeys(value), ["smith2024", "other", "smith2024", "liu2025"])

    def test_skip_fenced_code(self):
        raw = "Before [@real].\n```md\nFake [@ignored].\n```\nAfter [@after].\n"
        self.assertEqual(extract_citekeys(hide_fenced_code(raw)), ["real", "after"])

    def test_missing_citation_figure_and_placeholder(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            md = root / "paper.md"
            bib = root / "references.bib"
            md.write_text("Text [@have; @missing].\n![Figure](figs/plot.svg)\nTODO\n", encoding="utf-8")
            bib.write_text("@article{have,title={Test}}\n", encoding="utf-8")
            out = inspect(md, bib)
            kinds = {v["type"] for v in out["issues"]}
            self.assertTrue({"MISSING_BIB_KEY", "MISSING_IMAGE", "PLACEHOLDER"} <= kinds)
            self.assertEqual(out["status"], "STATIC_ISSUES_FOUND")

    def test_clean_case_with_local_figure(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            md = root / "paper.md"
            bib = root / "ref.bib"
            fig = root / "figures" / "taxonomy.svg"
            fig.parent.mkdir()
            fig.write_text("<svg />", encoding="utf-8")
            md.write_text("Text [@a].\n![Taxonomy](figures/taxonomy.svg)\n", encoding="utf-8")
            bib.write_text("@article{a,title={T}}\n", encoding="utf-8")
            out = inspect(md, bib)
            self.assertEqual(out["status"], "NO_STATIC_ISSUES_DETECTED")
            self.assertEqual(out["issues"], [])


if __name__ == "__main__":
    unittest.main()
