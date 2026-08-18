import unittest

import numpy as np

from diderot_mls.waves_fdtd import (
    cfl_1d,
    cfl_2d,
    initial_previous_1d,
    initial_previous_2d,
    mode_shape_neumann_2d,
    step_1d,
    step_2d,
)


class WaveFDTDTests(unittest.TestCase):
    def test_cfl_1d_reports_stable_and_unstable_cases(self):
        self.assertTrue(cfl_1d(c=1.0, dt=0.5, dx=1.0).stable_by_condition)
        self.assertFalse(cfl_1d(c=1.0, dt=1.1, dx=1.0).stable_by_condition)

    def test_cfl_2d_square_grid_matches_one_over_sqrt_two_rule(self):
        h = 0.1
        stable = cfl_2d(c=1.0, dt=0.70 * h, dx=h, dy=h)
        unstable = cfl_2d(c=1.0, dt=0.72 * h, dx=h, dy=h)
        self.assertTrue(stable.stable_by_condition)
        self.assertFalse(unstable.stable_by_condition)

    def test_zero_1d_state_remains_zero_without_source(self):
        u_prev = np.zeros(11)
        u = np.zeros(11)
        u_next = step_1d(u_prev, u, c=1.0, dt=0.05, dx=0.1)
        np.testing.assert_allclose(u_next, 0.0)

    def test_zero_2d_state_remains_zero_without_source(self):
        u_prev = np.zeros((9, 9))
        u = np.zeros((9, 9))
        u_next = step_2d(u_prev, u, c=1.0, dt=0.05, dx=0.1, dy=0.1)
        np.testing.assert_allclose(u_next, 0.0)

    def test_constant_field_is_preserved_by_neumann_update_1d(self):
        u0 = np.full(21, 3.5)
        u_prev = initial_previous_1d(u0, c=1.0, dt=0.04, dx=0.1)
        u_next = step_1d(u_prev, u0, c=1.0, dt=0.04, dx=0.1)
        np.testing.assert_allclose(u_prev, u0)
        np.testing.assert_allclose(u_next, u0)

    def test_initial_previous_uses_initial_velocity(self):
        u0 = np.ones(15)
        v0 = np.full(15, 2.0)
        dt = 0.03
        u_prev = initial_previous_1d(
            u0, c=1.0, dt=dt, dx=0.1, velocity0=v0, boundary="neumann"
        )
        np.testing.assert_allclose(u_prev, u0 - dt * v0)

    def test_neumann_cosine_mode_is_preserved_as_a_shape_in_1d(self):
        n = 81
        x = np.linspace(0.0, 1.0, n)
        dx = x[1] - x[0]
        dt = 0.4 * dx
        u0 = np.cos(3.0 * np.pi * x)
        u_prev = initial_previous_1d(u0, c=1.0, dt=dt, dx=dx)
        u_next = step_1d(u_prev, u0, c=1.0, dt=dt, dx=dx)

        # With zero initial velocity, the exact centred first step is symmetric:
        # u(+dt) = u(-dt). More importantly, the cosine remains a single mode.
        np.testing.assert_allclose(u_next, u_prev, rtol=1e-12, atol=1e-12)
        scale = float(np.dot(u_next, u0) / np.dot(u0, u0))
        np.testing.assert_allclose(u_next, scale * u0, rtol=1e-12, atol=1e-12)

    def test_neumann_cosine_mode_is_preserved_as_a_shape_in_2d(self):
        x = np.linspace(0.0, 1.0, 51)
        y = np.linspace(0.0, 1.0, 41)
        dx = x[1] - x[0]
        dy = y[1] - y[0]
        dt = 0.45 / np.sqrt(1.0 / dx**2 + 1.0 / dy**2)
        u0 = mode_shape_neumann_2d(x, y, m=2, n=3, lx=1.0, ly=1.0)
        u_prev = initial_previous_2d(
            u0, c=1.0, dt=dt, dx=dx, dy=dy, boundary="neumann"
        )
        u_next = step_2d(
            u_prev, u0, c=1.0, dt=dt, dx=dx, dy=dy, boundary="neumann"
        )

        np.testing.assert_allclose(u_next, u_prev, rtol=1e-12, atol=1e-12)
        scale = float(np.vdot(u0, u_next) / np.vdot(u0, u0))
        np.testing.assert_allclose(u_next, scale * u0, rtol=1e-11, atol=1e-11)

    def test_dirichlet_boundaries_are_fixed_to_zero(self):
        u_prev = np.ones(9)
        u = np.ones(9)
        u_next = step_1d(
            u_prev, u, c=1.0, dt=0.02, dx=0.1, boundary="dirichlet"
        )
        self.assertEqual(u_next[0], 0.0)
        self.assertEqual(u_next[-1], 0.0)


if __name__ == "__main__":
    unittest.main()
