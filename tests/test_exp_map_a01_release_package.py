"""Read-only package regression tests; no controlled experiment is invoked."""
import copy
import json
import tempfile
import unittest
from pathlib import Path

from scripts.verify_exp_map_a01_release_package import (
    ROOT, PACKAGE, check_a03_compatibility, registry, row_hash, verify,
)


class A01PackageTests(unittest.TestCase):
    """Check package bindings and expected fail-closed mutations."""

    def test_live_approved_activation_is_read_only(self):
        """Verify the release package without hydrating or running inference."""
        out = verify()
        self.assertEqual(out["status"], "PASS")
        self.assertFalse(out["a03_execution_eligible"])
        self.assertFalse(out["registered_experiment_executed_by_verifier"])

    def test_original_a03_dataset_sha(self):
        """Reconstruct the frozen inactive dataset binding after removing one bit."""
        meta = json.loads((ROOT / PACKAGE / "SOURCE_MANIFEST.json").read_text())
        row = copy.deepcopy(registry(ROOT, "dataset_registry_v0.1.csv", "Dataset_ID")["DATA-ARITHMETIC"])
        row["Controlled_Execution_Eligible"] = "false"
        self.assertEqual(row_hash(row), meta["a03_original_dataset_sha256"])

    def test_reject_a03_activation_and_dataset_mutation(self):
        """Reject other modifications to the shared dataset or A03 execution gate."""
        meta = json.loads((ROOT / PACKAGE / "SOURCE_MANIFEST.json").read_text())
        ds = registry(ROOT, "dataset_registry_v0.1.csv", "Dataset_ID")["DATA-ARITHMETIC"]
        a03 = registry(ROOT, "experiment_registry_v0.2.csv", "Experiment_ID")["EXP-MAP-A03"]
        spec = json.loads((ROOT / "controlled_execution/specs/EXP-MAP-A03.json").read_text())
        modified = dict(a03)
        modified["Controlled_Execution_Eligible"] = "true"
        with self.assertRaisesRegex(ValueError, "A03 experiment execution"):
            check_a03_compatibility(ds, modified, spec, meta["a03_original_dataset_sha256"])
        modified = dict(ds)
        modified["Notes"] += " invalid"
        with self.assertRaisesRegex(ValueError, "binding differs"):
            check_a03_compatibility(modified, a03, spec, meta["a03_original_dataset_sha256"])

    def test_duplicate_registry_ids_fail(self):
        """Reject duplicates instead of silently keeping the last row."""
        with tempfile.TemporaryDirectory() as path:
            p = Path(path) / "registry"
            p.mkdir()
            (p / "experiment_registry_v0.2.csv").write_text(
                "Experiment_ID,Mode\nEXP-MAP-A01,controlled\nEXP-MAP-A01,controlled\n")
            with self.assertRaisesRegex(ValueError, "duplicate registry IDs"):
                registry(Path(path), "experiment_registry_v0.2.csv", "Experiment_ID")


if __name__ == "__main__":
    unittest.main()
