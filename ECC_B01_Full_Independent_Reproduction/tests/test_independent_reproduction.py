"""Tests authored separately from the supplied Investigator-B starter implementation."""
import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
import reproduce as kit  # noqa: E402


class ExactMathematicsTests(unittest.TestCase):
    def test_symbolic_controls_all_pass(self):
        rec = kit.Recorder()
        kit.symbolic_controls(rec)
        self.assertGreaterEqual(len(rec.results), 20)
        failures = [r for r in rec.results if r["status"] != "PASS"]
        self.assertEqual([], failures)

    def test_independent_quadrature_controls_all_pass(self):
        rec = kit.Recorder()
        kit.quadrature_controls(rec)
        failures = [r for r in rec.results if r["status"] != "PASS"]
        self.assertEqual([], failures)


class DiscreteTorusTests(unittest.TestCase):
    def test_periods_and_closed_cochain_at_two_resolutions(self):
        for n in (5, 11):
            coords, faces = kit.structured_torus(n)
            rec = kit.Recorder()
            got = kit.add_cochain_checks(rec, n, coords, faces)
            self.assertAlmostEqual(got["phi_period"], 2*math.pi, delta=1e-9)
            self.assertAlmostEqual(got["psi_period"], 4*math.pi, delta=1e-9)
            self.assertLess(got["closure_residual"], 1e-9)
            self.assertTrue(all(r["status"] == "PASS" for r in rec.results))

    def test_candidate_c_face_integrals_and_nonzero_local_response(self):
        rms_errors = []
        for n in (4, 7, 13):
            coords, _ = kit.structured_torus(n)
            rec = kit.Recorder()
            got = kit.curvature_mesh_checks(rec, n, coords)
            self.assertAlmostEqual(got["exact_flux"], 4*math.pi**2, delta=2e-9)
            self.assertAlmostEqual(got["centroid_flux"], 4*math.pi**2, delta=2e-8)
            self.assertAlmostEqual(got["local_response_at_00"], -1.0, delta=1e-12)
            rms_errors.append(got["rms_local_face_quadrature_error"])
            self.assertTrue(all(r["status"] == "PASS" for r in rec.results))
        self.assertTrue(rms_errors[0] > rms_errors[1] > rms_errors[2], rms_errors)
        self.assertLess(rms_errors[-1], 0.002)


class ToolchainAndRunSafetyTests(unittest.TestCase):
    def _rows(self, gmsh=True, gudhi=True):
        mesh_source = "Gmsh linear simplex mesh" if gmsh else "fallback test mesh"
        homology = "GUDHI SimplexTree over GF(2)" if gudhi else "independent Python GF(2) boundary-rank fallback"
        shapes = {name: {"mesh_source": mesh_source, "homology_method": homology} for name in ("sphere", "torus", "ball")}
        return [{"target_h": 0.8, "shapes": shapes}]

    def test_fallback_backend_marks_gmsh_not_requested(self):
        got = kit.derive_mesh_gate_statuses("fallback", self._rows(gmsh=False, gudhi=False), [0.8], False, False)
        self.assertEqual(got["gmsh_gate_status"], "NOT_REQUESTED")
        self.assertEqual(got["gudhi_gate_status"], "BLOCKED_OPTIONAL_DEPENDENCY")
        self.assertEqual(got["full_requested_toolchain_gate_status"], "NOT_REQUESTED")

    def test_gmsh_pass_requires_every_shape(self):
        rows = self._rows(gmsh=True, gudhi=True)
        self.assertEqual(kit.derive_mesh_gate_statuses("gmsh", rows, [0.8], True, True)["gmsh_gate_status"], "PASS")
        rows[0]["shapes"]["ball"]["mesh_source"] = "fallback test mesh"
        self.assertEqual(kit.derive_mesh_gate_statuses("gmsh", rows, [0.8], True, True)["gmsh_gate_status"], "BLOCKED_RUNTIME_FAILURE")

    def test_gudhi_pass_requires_every_homology_record(self):
        rows = self._rows(gmsh=True, gudhi=True)
        self.assertEqual(kit.derive_mesh_gate_statuses("gmsh", rows, [0.8], True, True)["gudhi_gate_status"], "PASS")
        rows[0]["shapes"]["torus"]["homology_method"] = "independent Python GF(2) boundary-rank fallback"
        self.assertEqual(kit.derive_mesh_gate_statuses("gmsh", rows, [0.8], True, True)["gudhi_gate_status"], "BLOCKED_RUNTIME_FAILURE")

    def test_nonfinite_or_nonpositive_mesh_sizes_rejected(self):
        for value in (float("nan"), float("inf"), float("-inf"), 0.0, -0.1):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    kit.validate_mesh_resources([value])

    def test_mesh_resource_budget_rejects_extreme_resolution(self):
        with self.assertRaisesRegex(ValueError, "budget"):
            kit.validate_mesh_resources([0.01])

    def test_fallback_sphere_refinement_depends_on_h_not_input_order(self):
        self.assertIn("level 1", kit.fallback_mesh("sphere", 99, 0.8)[2])
        self.assertIn("level 4", kit.fallback_mesh("sphere", 0, 0.2)[2])

    def test_existing_output_directory_refused_and_untouched(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "existing"
            target.mkdir()
            sentinel = target / "prior-run.txt"
            sentinel.write_text("preserve", encoding="utf-8")
            with self.assertRaises(FileExistsError):
                kit.prepare_output_directory(str(target))
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")

    def test_explicit_gmsh_blocked_gate_returns_nonzero_and_receipt_hashes_match(self):
        import contextlib
        import io
        import json
        import tempfile
        from pathlib import Path
        from unittest.mock import patch
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "run-output"
            blocked = {"backend_requested": "gmsh", "backend_used": "fallback",
                       "gmsh_gate_status": "BLOCKED_OPTIONAL_DEPENDENCY",
                       "gudhi_gate_status": "BLOCKED_OPTIONAL_DEPENDENCY",
                       "full_requested_toolchain_gate_status": "BLOCKED_OPTIONAL_DEPENDENCY"}
            argv = ["reproduce.py", "--mesh", "--backend", "gmsh", "--h", "0.8", "--out-dir", str(target)]
            with patch.object(sys, "argv", argv), patch.object(kit, "run_mesh_suite", return_value=([], [], blocked)), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(kit.main(), 2)
            report = json.loads((target / "reproduction_results.json").read_text(encoding="utf-8"))
            receipt = json.loads((target / "run_receipt.json").read_text(encoding="utf-8"))
            self.assertEqual(report["mesh_manifest"]["full_requested_toolchain_gate_status"], "BLOCKED_OPTIONAL_DEPENDENCY")
            for artifact in receipt["artifacts"]:
                path = target / artifact["path"]
                self.assertEqual(path.stat().st_size, artifact["bytes"])
                import hashlib
                self.assertEqual(hashlib.sha256(path.read_bytes()).hexdigest(), artifact["sha256"])

    def test_manifest_writer_refuses_to_overwrite(self):
        import subprocess
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as temp:
            target = Path(temp) / "prior-manifest.json"
            target.write_text("preserve", encoding="utf-8")
            process = subprocess.run([sys.executable, str(kit.ROOT / "freeze_manifest.py"), "--out", str(target)], text=True, capture_output=True)
            self.assertNotEqual(process.returncode, 0)
            self.assertIn("refusing to overwrite existing manifest", process.stderr)
            self.assertEqual(target.read_text(encoding="utf-8"), "preserve")


class SimplicialTopologyTests(unittest.TestCase):
    def assert_chain_identities(self, top):
        report = kit.incidence_report(top)
        self.assertTrue(report["all_identities_pass"], report["coboundary_identity_checks"])

    def test_torus_homology_and_incidence(self):
        _, faces = kit.structured_torus(6)
        self.assertEqual(kit.gf2_betti(faces), [1, 2, 1])
        self.assert_chain_identities(faces)

    def test_sphere_homology_incidence_and_flux(self):
        points, faces = kit.refine_sphere(2)
        self.assertEqual(kit.gf2_betti(faces), [1, 0, 1])
        self.assert_chain_identities(faces)
        flux = kit.sphere_flux_methods(points, faces, charge=1.0)
        self.assertLess(flux["solid_angle_error"], 1e-10)
        self.assertLess(flux["planar_quadrature_error"], 0.02)

    def test_solid_ball_homology_and_incidence(self):
        _, tets = kit.cube_tetra_mesh(2)
        self.assertEqual(kit.gf2_betti(tets), [1, 0, 0, 0])
        self.assert_chain_identities(tets)

    def test_sphere_flat_facet_quadrature_converges(self):
        errors=[]
        for level in (1, 2, 3):
            points, faces = kit.refine_sphere(level)
            errors.append(kit.sphere_flux_methods(points, faces)["planar_quadrature_error"])
        self.assertTrue(errors[0] > errors[1] > errors[2], errors)


if __name__ == "__main__":
    unittest.main(verbosity=2)
