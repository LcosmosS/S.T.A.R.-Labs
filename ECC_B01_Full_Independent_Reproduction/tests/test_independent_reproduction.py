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
