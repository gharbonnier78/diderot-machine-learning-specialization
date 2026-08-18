import unittest

import numpy as np

from diderot_mls.von_neumann import (
    amplification_roots_1d,
    phase_velocity_ratio_1d,
    second_difference_symbol,
    spectral_radius_1d,
    spectral_radius_2d,
    stable_for_all_modes_1d,
    stable_for_all_modes_2d,
)


class VonNeumannTests(unittest.TestCase):
    def test_second_difference_fourier_symbol(self):
        self.assertAlmostEqual(float(second_difference_symbol(0.0)), 0.0)
        self.assertAlmostEqual(float(second_difference_symbol(np.pi)), -4.0)

    def test_stable_1d_modes_have_unit_spectral_radius(self):
        theta = np.linspace(0.0, np.pi, 201)
        rho = spectral_radius_1d(0.8, theta)
        np.testing.assert_allclose(rho, 1.0, rtol=1e-12, atol=1e-12)
        self.assertTrue(stable_for_all_modes_1d(0.8))

    def test_high_frequency_mode_grows_when_1d_cfl_is_violated(self):
        rho = float(spectral_radius_1d(1.05, np.pi))
        self.assertGreater(rho, 1.0)
        self.assertFalse(stable_for_all_modes_1d(1.05))

    def test_amplification_roots_have_product_one(self):
        g1, g2 = amplification_roots_1d(0.65, 0.7 * np.pi)
        self.assertAlmostEqual(abs(g1 * g2 - 1.0), 0.0, places=12)

    def test_exact_cfl_nyquist_mode_has_repeated_minus_one_root(self):
        g1, g2 = amplification_roots_1d(1.0, np.pi)
        self.assertAlmostEqual(abs(g1 + 1.0), 0.0, places=12)
        self.assertAlmostEqual(abs(g2 + 1.0), 0.0, places=12)
        self.assertAlmostEqual(abs(g1 - g2), 0.0, places=12)

    def test_r_equal_one_is_dispersionless_for_1d_resolved_branch(self):
        theta = np.linspace(0.01, np.pi, 200)
        ratio = phase_velocity_ratio_1d(1.0, theta)
        np.testing.assert_allclose(ratio, 1.0, rtol=1e-12, atol=1e-12)

    def test_2d_cfl_condition(self):
        r = 1.0 / np.sqrt(2.0)
        self.assertTrue(stable_for_all_modes_2d(r, r))
        self.assertFalse(stable_for_all_modes_2d(0.72, 0.72))

    def test_2d_highest_frequency_mode_reveals_instability(self):
        stable_rho = float(spectral_radius_2d(0.70, 0.70, np.pi, np.pi))
        unstable_rho = float(spectral_radius_2d(0.72, 0.72, np.pi, np.pi))
        self.assertAlmostEqual(stable_rho, 1.0, places=12)
        self.assertGreater(unstable_rho, 1.0)


if __name__ == "__main__":
    unittest.main()
