"""Regression tests for review archive integrity; never run A03 inference."""
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from scripts.validate_a03_preexecution_release import PACKAGE, verify_package

class ArchiveReviewTests(unittest.TestCase):
    """Verify both the valid frozen archive and intentional tampering failures."""

    def test_review_archive_passes_without_science_execution(self):
        """Check all manifests, historical evidence and closed activation flags."""
        report = verify_package()
        self.assertEqual(report["archive_integrity"], "PASS")
        self.assertFalse(report["experiment_executed"])
        self.assertFalse(report["activation_authorized"])

    def test_changed_verified_byte_fails_closed(self):
        """Reject tampering even in a non-operational historical report."""
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "release"
            shutil.copytree(PACKAGE, package)
            path = package / "requirements.txt"
            path.write_bytes(path.read_bytes() + b"\n# altered\n")
            with self.assertRaisesRegex(ValueError, "SHA-256 mismatch"):
                verify_package(package)

    def test_false_experiment_claim_fails_closed(self):
        """Reject a forged authorization flag before accepting a receipt."""
        with tempfile.TemporaryDirectory() as tmp:
            package = Path(tmp) / "release"
            shutil.copytree(PACKAGE, package)
            manifest = package / "SOURCE_MANIFEST.json"
            data = json.loads(manifest.read_text())
            data["science_boundaries"]["controlled_execution_authorized"] = True
            manifest.write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "scientific scope was promoted"):
                verify_package(package)

if __name__ == "__main__":
    unittest.main()
