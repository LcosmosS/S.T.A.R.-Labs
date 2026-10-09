"""Charter notice regression checks; no scientific status is advanced by these checks."""

from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
ERRATA = ROOT / "docs/registries/CHARTER_EPISTEMIC_CORRECTIONS_v0.1.md"
NEGATIVE = ROOT / "docs/registries/NEGATIVE_RESULTS_PUBLICATION_PROTOCOL_v0.1.md"
CHARTER = ROOT / "charter/STAR_Research_Charter_v0-2.pdf"
LEGACY = ("OVERVIEW.md", "2_STARMAP.md", "3_SMAT.md", "4_SFT.md")


class CharterIntegrityNoticeTests(unittest.TestCase):
    def test_governing_pdf_exists(self):
        self.assertTrue(CHARTER.is_file(), "The full PDF Charter is authoritative")

    def test_historical_docs_have_appended_status_notices(self):
        for path in LEGACY:
            with self.subTest(path=path):
                contents = (ROOT / path).read_text(encoding="utf-8")
                self.assertIn("Historical-source status notice (Charter v0.2", contents)
                self.assertIn("historical proposal", contents)
                self.assertIn("CHARTER_EPISTEMIC_CORRECTIONS_v0.1.md", contents)

    def test_readme_points_to_both_corrections_and_pdf(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for expected in (CHARTER.name, ERRATA.name, NEGATIVE.name):
            self.assertIn(expected, readme)

    def test_charter_category_codes_and_failure_separation(self):
        s = ERRATA.read_text(encoding="utf-8")
        for code in "DEMPHCTS":
            self.assertRegex(s, rf"\| {code} \|")
        self.assertIn("orthogonal", s)
        f = NEGATIVE.read_text(encoding="utf-8")
        for outcome in (
            "VALID_REJECT_NULL",
            "VALID_DO_NOT_REJECT_NULL",
            "VALID_OBSTRUCTION",
            "VALID_NEGATIVE_PREDICTION",
            "VALID_REPLICATION_FAILURE",
            "FRAME_EXHAUSTED_RETIRED",
            "INELIGIBLE_PROTOCOL_OR_DATA",
            "INCONCLUSIVE",
        ):
            self.assertIn(outcome, f)
        self.assertIn("not evidence that the null is true", f)
        self.assertIn("independent review", f)

    def test_all_local_markdown_links_resolve(self):
        for source in (ERRATA, NEGATIVE):
            contents = source.read_text(encoding="utf-8")
            links = re.findall(r"\]\(([^)\s]+)\)", contents)
            self.assertTrue(links, f"No links found in {source.name}")
            for link in links:
                if "://" in link or link.startswith("#"):
                    continue
                path = (source.parent / link.split("#", 1)[0]).resolve()
                with self.subTest(source=source.name, href=link):
                    self.assertTrue(path.is_file(), f"Broken local link: {source}: {link}")


if __name__ == "__main__":
    unittest.main()
