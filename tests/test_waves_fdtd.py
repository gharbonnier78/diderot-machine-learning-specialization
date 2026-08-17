import numpy as np

from diderot_mls.waves_fdtd import cfl_1d, cfl_2d, step_1d, step_2d


def test_cfl_1d_reports_stable_and_unstable_cases():
    assert cfl_1d(c=1.0, dt=0.5, dx=1.0).stable_by_condition
    assert not cfl_1d(c=1.0, dt=1.1, dx=1.0).stable_by_condition


def test_cfl_2d_square_grid_matches_one_over_sqrt_two_rule():
    h = 0.1
    stable = cfl_2d(c=1.0, dt=0.70 * h, dx=h, dy=h)
    unstable = cfl_2d(c=1.0, dt=0.72 * h, dx=h, dy=h)
    assert stable.stable_by_condition
    assert not unstable.stable_by_condition


def test_zero_1d_state_remains_zero_without_source():
    u_prev = np.zeros(11)
    u = np.zeros(11)
    u_next = step_1d(u_prev, u, c=1.0, dt=0.05, dx=0.1)
    np.testing.assert_allclose(u_next, 0.0)


def test_zero_2d_state_remains_zero_without_source():
    u_prev = np.zeros((9, 9))
    u = np.zeros((9, 9))
    u_next = step_2d(u_prev, u, c=1.0, dt=0.05, dx=0.1, dy=0.1)
    np.testing.assert_allclose(u_next, 0.0)


def test_neumann_boundaries_copy_adjacent_values_1d():
    u_prev = np.zeros(7)
    u = np.array([0.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0])
    u_next = step_1d(u_prev, u, c=1.0, dt=0.02, dx=0.1, boundary="neumann")
    assert u_next[0] == u_next[1]
    assert u_next[-1] == u_next[-2]
