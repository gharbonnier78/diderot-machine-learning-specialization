import unittest

import numpy as np

from diderot_mls.wave_verification import (
    choose_dt_for_final_time,
    convergence_study_1d,
    neumann_mode_exact_1d,
    neumann_mode_wavelength,
    normalized_l2_error,
    observed_orders,
    physical_energy_diagnostic_1d,
    points_per_wavelength,
)


class WaveVerificationTests(unittest.TestCase):
    def test_exact_neumann_mode_has_zero_boundary_slope_analytically(self):
        length = 1.0
        m = 3
        k = m * np.pi / length
        # du/dx = -k sin(kx) cos(ckt), hence exactly zero at x=0,L.
        self.assertAlmostEqual(float(np.sin(k * 0.0)), 0.0, places=14)
        self.assertAlmostEqual(float(np.sin(k * length)), 0.0, places=14)

    def test_exact_solution_returns_initial_cosine(self):
        x = np.linspace(0.0, 1.0, 51)
        u = neumann_mode_exact_1d(x, 0.0, c=1.2, m=2, length=1.0)
        np.testing.assert_allclose(u, np.cos(2 * np.pi * x), atol=1e-14)

    def test_l2_error_is_zero_for_identical_arrays(self):
        x = np.linspace(0.0, 1.0, 21)
        u = np.cos(np.pi * x)
        self.assertAlmostEqual(normalized_l2_error(u, u.copy(), x[1] - x[0]), 0.0)

    def test_time_step_lands_exactly_on_final_time_and_respects_target_cfl(self):
        dt, steps, r = choose_dt_for_final_time(
            0.37, c=1.0, dx=0.02, target_courant=0.7
        )
        self.assertAlmostEqual(dt * steps, 0.37, places=14)
        self.assertLessEqual(r, 0.7 + 1e-14)

    def test_refinement_recovers_second_order_convergence(self):
        rows = convergence_study_1d(
            intervals=(40, 80, 160, 320),
            final_time=0.37,
            c=1.0,
            m=3,
            target_courant=0.7,
        )
        orders = observed_orders(rows)
        # Space and time are both second-order and dt scales with dx.
        # Allow room for pre-asymptotic effects while requiring the expected trend.
        self.assertTrue(all(p > 1.75 for p in orders[-2:]))
        self.assertLess(rows[-1].error_l2, rows[0].error_l2 / 20.0)

    def test_points_per_wavelength_doubles_when_dx_halves(self):
        wavelength = neumann_mode_wavelength(4, 1.0)
        self.assertAlmostEqual(points_per_wavelength(wavelength, 0.01), 50.0)
        self.assertAlmostEqual(points_per_wavelength(wavelength, 0.005), 100.0)

    def test_physical_energy_diagnostic_is_zero_for_zero_state(self):
        z = np.zeros(21)
        e = physical_energy_diagnostic_1d(
            z, z, z, c=1.0, dt=0.01, dx=0.05
        )
        self.assertEqual(e, 0.0)


if __name__ == "__main__":
    unittest.main()
