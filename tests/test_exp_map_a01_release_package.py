"""Read-only package regression tests; no controlled experiment is invoked."""
import copy
import hashlib
import json
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import verify_exp_map_a01_release_package as package_verifier
from scripts.verify_exp_map_a01_release_package import (
    ROOT, PACKAGE, REVIEWED_APPROVAL, REVIEWED_APPROVAL_REVIEW_ID,
    REVIEWED_SHA256, EXPECTED_A03_EXPERIMENT_SHA256,
    check_a03_compatibility, registry, row_hash, verify,
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
        with self.assertRaisesRegex(ValueError, "A03 frozen experiment binding"):
            check_a03_compatibility(ds, modified, spec, meta["a03_original_dataset_sha256"])
        modified = dict(ds)
        modified["Notes"] += " invalid"
        with self.assertRaisesRegex(ValueError, "binding differs"):
            check_a03_compatibility(modified, a03, spec, meta["a03_original_dataset_sha256"])


    def make_root(self, path):
        """Copy the governed subset to a disposable integrity-mutation root."""
        root = Path(path)
        spec = json.loads((ROOT / "controlled_execution/specs/EXP-MAP-A01.json").read_text())
        paths = [
            PACKAGE + "/SOURCE_MANIFEST.json",
            "registry/experiment_registry_v0.2.csv",
            "registry/dataset_registry_v0.1.csv",
            "registry/data_provenance_registry_v0.1.csv",
            "registry/parameter_registry_v0.1.csv",
            "registry/null_registry_v0.1.csv",
            *REVIEWED_SHA256,
            *(item["path"] for group in ("config_files", "code_inputs")
              for item in spec[group]),
        ]
        for name in set(paths):
            dest = root / name
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, dest)
        return root

    def test_local_pass_does_not_claim_independently_checked_approval(self):
        """Separate hash-locked local checks from a live GitHub review lookup."""
        report = verify()
        self.assertTrue(report["approval_identity_pinned"])
        self.assertFalse(report["approval_verified_against_github"])
        self.assertIn("NOT_CHECKED", report["approval_evidence_level"])

    def test_reject_mutated_approval_identity_head_and_merge(self):
        """Refuse to certify approval details rewritten inside SOURCE_MANIFEST."""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            file = root / PACKAGE / "SOURCE_MANIFEST.json"
            original = json.loads(file.read_text())
            for field, value in (
                ("merge_sha", "0" * 40),
                ("final_head", "1" * 40),
                ("approved_by", "other-user"),
                ("approved_at_utc", "2026-10-10T01:05:41Z"),
            ):
                with self.subTest(field=field):
                    changed = copy.deepcopy(original)
                    changed["approval"][field] = value
                    file.write_text(json.dumps(changed))
                    with self.assertRaisesRegex(ValueError, "approval lineage"):
                        verify(root=root)
            file.write_text(json.dumps(original))

    def test_reject_modified_a03_experiment_assessment_with_flags_unchanged(self):
        """Reject A03 audit-assessment edits even when safety flags remain false."""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            path = root / "registry/experiment_registry_v0.2.csv"
            original = path.read_text()
            self.assertIn("EXP-MAP-A03", original)
            import csv
            with path.open(newline="", encoding="utf-8") as fh:
                rows = list(csv.DictReader(fh))
            changed = next(r for r in rows if r["Experiment_ID"] == "EXP-MAP-A03")
            changed["Current_Audit_Assessment"] += " unauthorized audit amendment"
            with path.open("w", newline="", encoding="utf-8") as fh:
                writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
                writer.writeheader()
                writer.writerows(rows)
            with self.assertRaisesRegex(ValueError, "A03 frozen experiment binding"):
                verify(root=root)

    def test_reject_modified_protocol_even_with_updated_spec_digest(self):
        """Reject a colluding spec/protocol hash update via independent anchors."""
        with tempfile.TemporaryDirectory() as temporary:
            root = self.make_root(temporary)
            proto = root / "preregistrations/EXP-MAP-A01/protocol.md"
            proto.write_text(proto.read_text() + "\nUnauthorised protocol edit\n")
            spec_path = root / "controlled_execution/specs/EXP-MAP-A01.json"
            spec = json.loads(spec_path.read_text())
            for item in spec["config_files"]:
                if item["path"] == "preregistrations/EXP-MAP-A01/protocol.md":
                    item["sha256"] = hashlib.sha256(proto.read_bytes()).hexdigest()
            spec_path.write_text(json.dumps(spec, indent=2) + "\n")
            with self.assertRaisesRegex(ValueError, "reviewed baseline SHA-256 mismatch"):
                verify(root=root)

    def test_independent_github_review_lookup_rejects_wrong_head(self):
        """Reject an online review from a different commit, even if APPROVED."""
        pr = {
            "merged": True, "merge_commit_sha": REVIEWED_APPROVAL["merge_sha"],
            "head": {"sha": REVIEWED_APPROVAL["final_head"]},
            "user": {"login": "LcosmosS"},
        }
        review = {
            "id": REVIEWED_APPROVAL_REVIEW_ID,
            "user": {"login": REVIEWED_APPROVAL["approved_by"]},
            "state": "APPROVED",
            "commit_id": "0" * 40,
            "submitted_at": REVIEWED_APPROVAL["approved_at_utc"],
        }
        with patch.object(package_verifier, "_github_json",
                          side_effect=[pr, [review]]):
            with self.assertRaisesRegex(ValueError, "reviewer identity"):
                package_verifier.verify_online_approval()

    def test_independent_github_review_lookup_accepts_exact_review(self):
        """Require the exact PR head, reviewer, timestamp, and compatibility PR."""
        pr = {
            "merged": True, "merge_commit_sha": REVIEWED_APPROVAL["merge_sha"],
            "head": {"sha": REVIEWED_APPROVAL["final_head"]},
            "user": {"login": "LcosmosS"},
        }
        review = {
            "id": REVIEWED_APPROVAL_REVIEW_ID,
            "user": {"login": REVIEWED_APPROVAL["approved_by"]},
            "state": "APPROVED",
            "commit_id": REVIEWED_APPROVAL["final_head"],
            "submitted_at": REVIEWED_APPROVAL["approved_at_utc"],
        }
        compat = {"merged": True,
                  "merge_commit_sha": package_verifier.REVIEWED_COMPAT_MERGE_SHA}
        with patch.object(package_verifier, "_github_json",
                          side_effect=[pr, [review], compat]):
            self.assertTrue(package_verifier.verify_online_approval())

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
