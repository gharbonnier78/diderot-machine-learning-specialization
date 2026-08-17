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

Boundaries can be Neumann (reflecting, zero normal derivative) or Dirichlet
(fixed, zero displacement).
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
    """Discrete approximation of a localized 1D source."""
    s = np.zeros(n, dtype=float)
    s[index] = amplitude
    return s


def point_source_2d(
    shape: tuple[int, int], ij: tuple[int, int], amplitude: float
) -> np.ndarray:
    """Discrete approximation of a localized 2D source."""
    s = np.zeros(shape, dtype=float)
    s[ij] = amplitude
    return s


def _apply_boundary_1d(u: np.ndarray, boundary: Boundary) -> None:
    if boundary == "neumann":
        # du/dn = 0: copy the adjacent interior value.
        u[0] = u[1]
        u[-1] = u[-2]
    elif boundary == "dirichlet":
        u[0] = 0.0
        u[-1] = 0.0
    else:
        raise ValueError(f"Unknown boundary: {boundary}")


def _apply_boundary_2d(u: np.ndarray, boundary: Boundary) -> None:
    if boundary == "neumann":
        u[0, :] = u[1, :]
        u[-1, :] = u[-2, :]
        u[:, 0] = u[:, 1]
        u[:, -1] = u[:, -2]
    elif boundary == "dirichlet":
        u[0, :] = 0.0
        u[-1, :] = 0.0
        u[:, 0] = 0.0
        u[:, -1] = 0.0
    else:
        raise ValueError(f"Unknown boundary: {boundary}")


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
    v0 = np.zeros_like(u0) if velocity0 is None else velocity0
    s0 = np.zeros_like(u0) if source0 is None else source0
    if v0.shape != u0.shape or s0.shape != u0.shape:
        raise ValueError("velocity0 and source0 must match u0")

    r2 = (c * dt / dx) ** 2
    u_prev = u0.astype(float, copy=True)
    lap = u0[2:] - 2.0 * u0[1:-1] + u0[:-2]
    u_prev[1:-1] = (
        u0[1:-1]
        - dt * v0[1:-1]
        + 0.5 * r2 * lap
        + 0.5 * dt**2 * s0[1:-1]
    )
    _apply_boundary_1d(u_prev, boundary)
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
    v0 = np.zeros_like(u0) if velocity0 is None else velocity0
    s0 = np.zeros_like(u0) if source0 is None else source0
    if v0.shape != u0.shape or s0.shape != u0.shape:
        raise ValueError("velocity0 and source0 must match u0")

    rx2 = (c * dt / dx) ** 2
    ry2 = (c * dt / dy) ** 2
    centre = u0[1:-1, 1:-1]
    lap_x = u0[2:, 1:-1] - 2.0 * centre + u0[:-2, 1:-1]
    lap_y = u0[1:-1, 2:] - 2.0 * centre + u0[1:-1, :-2]

    u_prev = u0.astype(float, copy=True)
    u_prev[1:-1, 1:-1] = (
        centre
        - dt * v0[1:-1, 1:-1]
        + 0.5 * rx2 * lap_x
        + 0.5 * ry2 * lap_y
        + 0.5 * dt**2 * s0[1:-1, 1:-1]
    )
    _apply_boundary_2d(u_prev, boundary)
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
    if u_prev.shape != u.shape:
        raise ValueError("u_prev and u must have the same shape")
    r2 = (c * dt / dx) ** 2
    u_next = np.empty_like(u, dtype=float)
    u_next[1:-1] = (
        2.0 * u[1:-1]
        - u_prev[1:-1]
        + r2 * (u[2:] - 2.0 * u[1:-1] + u[:-2])
    )
    if source is not None:
        if source.shape != u.shape:
            raise ValueError("source must have the same shape as u")
        u_next[1:-1] += dt**2 * source[1:-1]
    _apply_boundary_1d(u_next, boundary)
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

    rx2 = (c * dt / dx) ** 2
    ry2 = (c * dt / dy) ** 2
    u_next = np.empty_like(u, dtype=float)

    centre = u[1:-1, 1:-1]
    lap_x = u[2:, 1:-1] - 2.0 * centre + u[:-2, 1:-1]
    lap_y = u[1:-1, 2:] - 2.0 * centre + u[1:-1, :-2]
    u_next[1:-1, 1:-1] = (
        2.0 * centre
        - u_prev[1:-1, 1:-1]
        + rx2 * lap_x
        + ry2 * lap_y
    )

    if source is not None:
        if source.shape != u.shape:
            raise ValueError("source must have the same shape as u")
        u_next[1:-1, 1:-1] += dt**2 * source[1:-1, 1:-1]

    _apply_boundary_2d(u_next, boundary)
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
    """Rectangular-cavity eigenmode compatible with Neumann boundaries."""
    xx, yy = np.meshgrid(x, y, indexing="ij")
    return np.cos(m * np.pi * xx / lx) * np.cos(n * np.pi * yy / ly)


def mode_angular_frequency(
    c: float, *, m: int, n: int, lx: float, ly: float
) -> float:
    """Angular frequency omega_mn for a rectangular scalar-wave cavity."""
    return c * np.pi * np.sqrt((m / lx) ** 2 + (n / ly) ** 2)
