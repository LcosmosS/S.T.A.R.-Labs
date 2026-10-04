     import unittest


     class TestEllipticCurveMapping(unittest.TestCase):
         def test_compute_discriminant(self):
             self.assertEqual(compute_discriminant(1, 1), -16 * (4 + 27))
