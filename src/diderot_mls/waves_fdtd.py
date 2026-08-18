"""Pedagogical finite-difference solvers for the scalar wave equation.

The goal is not high-performance CFD. The code is intentionally explicit so
that one can read the numerical scheme almost line by line from the mathematics.

1D model
--------
    u_tt = c**2 u_xx + S(x, t)

2D model
--------
    u_tt = c**2 (u_xx + u_yy) + S(x, y, t)

The centred finite-difference update is

    u_next = 2*u - u_prev + spatial_term + dt**2 * source

Because this is second order in time, two time levels are required. Helpers
``initial_previous_*`` construct the fictitious t=-dt state from displacement
u(x,0) and velocity u_t(x,0), using a Taylor expansion consistent with the
same PDE. This avoids the common pedagogical shortcut ``u_prev = u0``.

For homogeneous Neumann boundaries we use mirrored ghost points. In 1D, for
example, the left ghost value satisfies u[-1] = u[1]. Therefore the centred
normal derivative at the wall is zero and the second derivative at the wall
remains part of the PDE update. This is more faithful than simply copying the
first interior value onto the boundary after every step, and it preserves the
expected cosine cavity modes of the discrete operator.

Dirichlet boundaries are fixed at zero displacement.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import numpy as np

Boundary = Literal["neumann", "dirichlet"]


@dataclass(frozen=True)
class CFLReport:
    value: float
    limit: float
    stable_by_condition: bool


def cfl_1d(c: float, dt: float, dx: float) -> CFLReport:
    """Return the 1D Courant number c*dt/dx and its classical limit 1."""
    value = abs(c) * dt / dx
    return CFLReport(value=value, limit=1.0, stable_by_condition=value <= 1.0)


def cfl_2d(c: float, dt: float, dx: float, dy: float) -> CFLReport:
    """Return sqrt(c^2 dt^2(1/dx^2+1/dy^2)) and the limit 1.

    On a square grid dx=dy=h this is equivalent to c*dt/h <= 1/sqrt(2).
    """
    value = abs(c) * dt * np.sqrt(1.0 / dx**2 + 1.0 / dy**2)
    return CFLReport(value=float(value), limit=1.0, stable_by_condition=value <= 1.0)


def gaussian_pulse_1d(
    x: np.ndarray, center: float, sigma: float, amplitude: float = 1.0
) -> np.ndarray:
    """Smooth localized initial displacement."""
    return amplitude * np.exp(-0.5 * ((x - center) / sigma) ** 2)


def point_source_1d(n: int, index: int, amplitude: float) -> np.ndarray:
    """Return a localized per-cell forcing for a pedagogical 1D experiment.

    This is intentionally not normalized as a grid-independent Dirac delta.
    Its integrated strength therefore changes if the grid spacing changes.
    """
    s = np.zeros(n, dtype=float)
    s[index] = amplitude
    return s


def point_source_2d(
    shape: tuple[int, int], ij: tuple[int, int], amplitude: float
) -> np.ndarray:
    """Return a localized per-cell forcing for a pedagogical 2D experiment.

    This is intentionally not normalized as a grid-independent Dirac delta.
    """
    s = np.zeros(shape, dtype=float)
    s[ij] = amplitude
    return s


def _check_boundary(boundary: Boundary) -> None:
    if boundary not in ("neumann", "dirichlet"):
        raise ValueError(f"Unknown boundary: {boundary}")


def _second_difference_1d(u: np.ndarray, boundary: Boundary) -> np.ndarray:
    """Return the unscaled centred second difference in 1D.

    For Neumann boundaries, mirrored ghost points implement du/dn=0:
    the left ghost equals the first interior point and likewise on the right.
    For Dirichlet boundaries, only interior points are updated; wall values are
    constrained separately to zero.
    """
    _check_boundary(boundary)
    u = np.asarray(u, dtype=float)
    d2 = np.zeros_like(u, dtype=float)

    if boundary == "neumann":
        padded = np.pad(u, 1, mode="reflect")
        d2[:] = padded[2:] - 2.0 * padded[1:-1] + padded[:-2]
    else:
        d2[1:-1] = u[2:] - 2.0 * u[1:-1] + u[:-2]
    return d2


def _second_differences_2d(
    u: np.ndarray, boundary: Boundary
) -> tuple[np.ndarray, np.ndarray]:
    """Return unscaled centred second differences along x and y."""
    _check_boundary(boundary)
    u = np.asarray(u, dtype=float)
    dx2 = np.zeros_like(u, dtype=float)
    dy2 = np.zeros_like(u, dtype=float)

    if boundary == "neumann":
        padded = np.pad(u, ((1, 1), (1, 1)), mode="reflect")
        centre = padded[1:-1, 1:-1]
        dx2[:] = padded[2:, 1:-1] - 2.0 * centre + padded[:-2, 1:-1]
        dy2[:] = padded[1:-1, 2:] - 2.0 * centre + padded[1:-1, :-2]
    else:
        centre = u[1:-1, 1:-1]
        dx2[1:-1, 1:-1] = u[2:, 1:-1] - 2.0 * centre + u[:-2, 1:-1]
        dy2[1:-1, 1:-1] = u[1:-1, 2:] - 2.0 * centre + u[1:-1, :-2]
    return dx2, dy2


def _enforce_dirichlet_1d(u: np.ndarray, boundary: Boundary) -> None:
    if boundary == "dirichlet":
        u[0] = 0.0
        u[-1] = 0.0


def _enforce_dirichlet_2d(u: np.ndarray, boundary: Boundary) -> None:
    if boundary == "dirichlet":
        u[0, :] = 0.0
        u[-1, :] = 0.0
        u[:, 0] = 0.0
        u[:, -1] = 0.0


def initial_previous_1d(
    u0: np.ndarray,
    *,
    c: float,
    dt: float,
    dx: float,
    velocity0: np.ndarray | None = None,
    source0: np.ndarray | None = None,
    boundary: Boundary = "neumann",
) -> np.ndarray:
    """Construct u(t=-dt) from initial displacement and velocity.

    Taylor expansion:
        u(-dt) = u(0) - dt*u_t(0) + 0.5*dt^2*u_tt(0)

    and the PDE supplies u_tt(0) = c^2*u_xx(0) + S(0).
    """
    if u0.ndim != 1:
        raise ValueError("u0 must be a 1D array")
    _check_boundary(boundary)
    v0 = np.zeros_like(u0) if velocity0 is None else velocity0
    s0 = np.zeros_like(u0) if source0 is None else source0
    if v0.shape != u0.shape or s0.shape != u0.shape:
        raise ValueError("velocity0 and source0 must match u0")

    r2 = (c * dt / dx) ** 2
    d2 = _second_difference_1d(u0, boundary)
    u_prev = (
        u0.astype(float, copy=True)
        - dt * v0
        + 0.5 * r2 * d2
        + 0.5 * dt**2 * s0
    )
    _enforce_dirichlet_1d(u_prev, boundary)
    return u_prev


def initial_previous_2d(
    u0: np.ndarray,
    *,
    c: float,
    dt: float,
    dx: float,
    dy: float,
    velocity0: np.ndarray | None = None,
    source0: np.ndarray | None = None,
    boundary: Boundary = "neumann",
) -> np.ndarray:
    """Construct u(t=-dt) for the 2D second-order scheme."""
    if u0.ndim != 2:
        raise ValueError("u0 must be a 2D array")
    _check_boundary(boundary)
    v0 = np.zeros_like(u0) if velocity0 is None else velocity0
    s0 = np.zeros_like(u0) if source0 is None else source0
    if v0.shape != u0.shape or s0.shape != u0.shape:
        raise ValueError("velocity0 and source0 must match u0")

    rx2 = (c * dt / dx) ** 2
    ry2 = (c * dt / dy) ** 2
    d2x, d2y = _second_differences_2d(u0, boundary)
    u_prev = (
        u0.astype(float, copy=True)
        - dt * v0
        + 0.5 * rx2 * d2x
        + 0.5 * ry2 * d2y
        + 0.5 * dt**2 * s0
    )
    _enforce_dirichlet_2d(u_prev, boundary)
    return u_prev


def step_1d(
    u_prev: np.ndarray,
    u: np.ndarray,
    *,
    c: float,
    dt: float,
    dx: float,
    source: np.ndarray | None = None,
    boundary: Boundary = "neumann",
) -> np.ndarray:
    """Advance the 1D wave equation by one centred finite-difference step."""
    if u_prev.shape != u.shape or u.ndim != 1:
        raise ValueError("u_prev and u must be 1D arrays with identical shapes")
    _check_boundary(boundary)
    r2 = (c * dt / dx) ** 2
    d2 = _second_difference_1d(u, boundary)
    u_next = 2.0 * u - u_prev + r2 * d2

    if source is not None:
        if source.shape != u.shape:
            raise ValueError("source must have the same shape as u")
        u_next += dt**2 * source

    _enforce_dirichlet_1d(u_next, boundary)
    return u_next


def step_2d(
    u_prev: np.ndarray,
    u: np.ndarray,
    *,
    c: float,
    dt: float,
    dx: float,
    dy: float,
    source: np.ndarray | None = None,
    boundary: Boundary = "neumann",
) -> np.ndarray:
    """Advance the 2D wave equation by one centred finite-difference step."""
    if u_prev.shape != u.shape or u.ndim != 2:
        raise ValueError("u_prev and u must be 2D arrays with identical shapes")
    _check_boundary(boundary)

    rx2 = (c * dt / dx) ** 2
    ry2 = (c * dt / dy) ** 2
    d2x, d2y = _second_differences_2d(u, boundary)
    u_next = 2.0 * u - u_prev + rx2 * d2x + ry2 * d2y

    if source is not None:
        if source.shape != u.shape:
            raise ValueError("source must have the same shape as u")
        u_next += dt**2 * source

    _enforce_dirichlet_2d(u_next, boundary)
    return u_next


def mode_shape_neumann_2d(
    x: np.ndarray,
    y: np.ndarray,
    *,
    m: int,
    n: int,
    lx: float,
    ly: float,
) -> np.ndarray:
    """Rectangular-cavity cosine mode compatible with Neumann boundaries."""
    xx, yy = np.meshgrid(x, y, indexing="ij")
    return np.cos(m * np.pi * xx / lx) * np.cos(n * np.pi * yy / ly)


def mode_angular_frequency(
    c: float, *, m: int, n: int, lx: float, ly: float
) -> float:
    """Continuum angular frequency omega_mn for a rectangular cavity mode."""
    return c * np.pi * np.sqrt((m / lx) ** 2 + (n / ly) ** 2)
