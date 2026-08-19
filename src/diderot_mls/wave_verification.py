"""Verification helpers for the pedagogical wave-equation laboratories.

This module separates three questions that are often mixed together:

1. **Stability**: does the numerical scheme remain bounded?
2. **Verification / convergence**: does the discrete solution approach the
   solution of the stated PDE as the mesh is refined?
3. **Validation**: is the PDE itself an adequate model of the physical system?

The functions below intentionally use a Neumann standing-wave mode because it
has a closed-form exact solution and is compatible with the finite-difference
solver used in the previous Diderot labs.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from .waves_fdtd import initial_previous_1d, step_1d


@dataclass(frozen=True)
class ConvergenceRow:
    intervals: int
    dx: float
    dt: float
    courant: float
    steps: int
    error_l2: float
    points_per_wavelength: float


def neumann_mode_wavenumber(m: int, length: float = 1.0) -> float:
    """Return k=m*pi/L for a 1D cosine mode with Neumann walls."""
    if m < 0:
        raise ValueError("m must be non-negative")
    if length <= 0:
        raise ValueError("length must be positive")
    return m * np.pi / length


def neumann_mode_wavelength(m: int, length: float = 1.0) -> float:
    """Return the physical wavelength 2L/m for m>0."""
    if m <= 0:
        raise ValueError("m must be positive to define a finite wavelength")
    return 2.0 * length / m


def neumann_mode_exact_1d(
    x: np.ndarray,
    t: float,
    *,
    c: float = 1.0,
    m: int = 2,
    length: float = 1.0,
    amplitude: float = 1.0,
) -> np.ndarray:
    """Exact standing-wave solution cos(kx) cos(ckt).

    It solves u_tt = c^2 u_xx with homogeneous Neumann boundaries and
    initial data u(x,0)=A cos(kx), u_t(x,0)=0.
    """
    k = neumann_mode_wavenumber(m, length)
    return amplitude * np.cos(k * x) * np.cos(c * k * t)


def normalized_l2_error(numerical: np.ndarray, exact: np.ndarray, dx: float) -> float:
    """Approximate ||num-exact||_L2 / sqrt(L) using trapezoidal weights."""
    if numerical.shape != exact.shape or numerical.ndim != 1:
        raise ValueError("numerical and exact must be 1D arrays with same shape")
    if dx <= 0:
        raise ValueError("dx must be positive")
    diff2 = (numerical - exact) ** 2
    weights = np.ones_like(diff2)
    if len(weights) > 1:
        weights[0] = 0.5
        weights[-1] = 0.5
    length = dx * max(len(diff2) - 1, 1)
    integral = dx * float(np.sum(weights * diff2))
    return float(np.sqrt(integral / length))


def choose_dt_for_final_time(
    final_time: float,
    *,
    c: float,
    dx: float,
    target_courant: float = 0.7,
) -> tuple[float, int, float]:
    """Choose an integer number of steps that lands exactly on final_time.

    The returned Courant number is <= target_courant (up to roundoff).
    """
    if final_time <= 0 or dx <= 0 or c == 0:
        raise ValueError("final_time and dx must be positive and c non-zero")
    if not (0 < target_courant < 1):
        raise ValueError("target_courant must lie strictly between 0 and 1")
    dt_max = target_courant * dx / abs(c)
    nsteps = int(math.ceil(final_time / dt_max))
    dt = final_time / nsteps
    r = abs(c) * dt / dx
    return dt, nsteps, r


def solve_neumann_mode_1d(
    intervals: int,
    *,
    final_time: float,
    c: float = 1.0,
    m: int = 2,
    length: float = 1.0,
    target_courant: float = 0.7,
) -> tuple[np.ndarray, np.ndarray, float, float, int]:
    """Numerically evolve one exact Neumann mode to final_time."""
    if intervals < 4:
        raise ValueError("intervals must be at least 4")
    x = np.linspace(0.0, length, intervals + 1)
    dx = length / intervals
    dt, nsteps, r = choose_dt_for_final_time(
        final_time, c=c, dx=dx, target_courant=target_courant
    )
    u0 = neumann_mode_exact_1d(x, 0.0, c=c, m=m, length=length)
    u_prev = initial_previous_1d(
        u0, c=c, dt=dt, dx=dx, velocity0=np.zeros_like(u0), boundary="neumann"
    )
    u = u0.copy()
    for _ in range(nsteps):
        u_next = step_1d(
            u_prev, u, c=c, dt=dt, dx=dx, boundary="neumann"
        )
        u_prev, u = u, u_next
    return x, u, dt, r, nsteps


def convergence_study_1d(
    intervals=(40, 80, 160, 320),
    *,
    final_time: float = 0.37,
    c: float = 1.0,
    m: int = 3,
    length: float = 1.0,
    target_courant: float = 0.7,
) -> list[ConvergenceRow]:
    """Run a grid-refinement study against the known exact solution."""
    rows: list[ConvergenceRow] = []
    wavelength = neumann_mode_wavelength(m, length)
    for n in intervals:
        x, u, dt, r, nsteps = solve_neumann_mode_1d(
            int(n),
            final_time=final_time,
            c=c,
            m=m,
            length=length,
            target_courant=target_courant,
        )
        dx = length / int(n)
        exact = neumann_mode_exact_1d(
            x, final_time, c=c, m=m, length=length
        )
        rows.append(
            ConvergenceRow(
                intervals=int(n),
                dx=dx,
                dt=dt,
                courant=r,
                steps=nsteps,
                error_l2=normalized_l2_error(u, exact, dx),
                points_per_wavelength=wavelength / dx,
            )
        )
    return rows


def observed_orders(rows: list[ConvergenceRow]) -> list[float]:
    """Estimate p from E ~ C h^p between consecutive refinement levels."""
    if len(rows) < 2:
        return []
    orders: list[float] = []
    for coarse, fine in zip(rows[:-1], rows[1:]):
        if coarse.error_l2 <= 0 or fine.error_l2 <= 0:
            orders.append(float("nan"))
            continue
        p = np.log(coarse.error_l2 / fine.error_l2) / np.log(coarse.dx / fine.dx)
        orders.append(float(p))
    return orders


def points_per_wavelength(wavelength: float, dx: float) -> float:
    """Return lambda/dx, a simple spatial-resolution diagnostic."""
    if wavelength <= 0 or dx <= 0:
        raise ValueError("wavelength and dx must be positive")
    return float(wavelength / dx)


def physical_energy_diagnostic_1d(
    u_prev: np.ndarray,
    u: np.ndarray,
    u_next: np.ndarray,
    *,
    c: float,
    dt: float,
    dx: float,
) -> float:
    """Approximate the continuum wave energy at the current time level.

    This is a *diagnostic*, not the exact discrete invariant of leapfrog.
    Velocity uses a centered time difference; strain uses edge differences.
    """
    if not (u_prev.shape == u.shape == u_next.shape) or u.ndim != 1:
        raise ValueError("all states must be 1D arrays with identical shape")
    velocity = (u_next - u_prev) / (2.0 * dt)
    grad = np.diff(u) / dx

    kinetic_weights = np.ones_like(velocity)
    if len(kinetic_weights) > 1:
        kinetic_weights[0] = kinetic_weights[-1] = 0.5
    kinetic = 0.5 * dx * float(np.sum(kinetic_weights * velocity**2))
    potential = 0.5 * c**2 * dx * float(np.sum(grad**2))
    return kinetic + potential
