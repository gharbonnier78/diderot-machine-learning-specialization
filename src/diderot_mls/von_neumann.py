"""Small, explicit helpers for Von Neumann analysis of the centred wave scheme.

The module supports the pedagogical path used in Diderot ML:

    finite-difference stencil
        -> Fourier mode
        -> discrete eigenvalue / symbol
        -> amplification factor G
        -> spectral radius |G|
        -> CFL stability condition
        -> numerical dispersion

We analyse the standard centred explicit scheme for

    u_tt = c^2 u_xx

and its 2D extension.  The code is intentionally transparent rather than
optimised.
"""

from __future__ import annotations

import numpy as np


def second_difference_symbol(theta):
    """Fourier symbol of u[j+1] - 2u[j] + u[j-1].

    For the Fourier mode exp(i*j*theta), the centred second-difference operator
    multiplies the mode by

        exp(i theta) - 2 + exp(-i theta)
        = -4 sin(theta/2)^2.
    """
    theta = np.asarray(theta, dtype=float)
    return -4.0 * np.sin(theta / 2.0) ** 2


def amplification_a_1d(r, theta):
    """Return a in G + 1/G = 2a for the 1D wave scheme.

    r = c*dt/dx is the Courant number.
    """
    r = np.asarray(r, dtype=float)
    theta = np.asarray(theta, dtype=float)
    return 1.0 - 2.0 * r**2 * np.sin(theta / 2.0) ** 2


def amplification_roots_1d(r, theta):
    """Return the two amplification roots G for a 1D Fourier mode.

    Substitution of u_j^n = G^n exp(i*j*theta) gives

        G^2 - 2 a G + 1 = 0,

    where a = 1 - 2 r^2 sin(theta/2)^2.
    """
    a = amplification_a_1d(r, theta)
    root = np.lib.scimath.sqrt(a**2 - 1.0)
    return a + root, a - root


def spectral_radius_1d(r, theta):
    """Maximum modulus of the two amplification roots."""
    g1, g2 = amplification_roots_1d(r, theta)
    return np.maximum(np.abs(g1), np.abs(g2))


def stable_for_all_modes_1d(r, atol=1e-12):
    """Classical Von Neumann result for the centred 1D wave scheme: |r| <= 1."""
    return bool(abs(float(r)) <= 1.0 + atol)


def amplification_a_2d(rx, ry, theta_x, theta_y):
    """Return a in G + 1/G = 2a for the 2D centred wave scheme.

    rx = c*dt/dx and ry = c*dt/dy.
    """
    rx = np.asarray(rx, dtype=float)
    ry = np.asarray(ry, dtype=float)
    theta_x = np.asarray(theta_x, dtype=float)
    theta_y = np.asarray(theta_y, dtype=float)
    return (
        1.0
        - 2.0 * rx**2 * np.sin(theta_x / 2.0) ** 2
        - 2.0 * ry**2 * np.sin(theta_y / 2.0) ** 2
    )


def amplification_roots_2d(rx, ry, theta_x, theta_y):
    """Return the two amplification roots G for a 2D Fourier mode."""
    a = amplification_a_2d(rx, ry, theta_x, theta_y)
    root = np.lib.scimath.sqrt(a**2 - 1.0)
    return a + root, a - root


def spectral_radius_2d(rx, ry, theta_x, theta_y):
    """Maximum modulus of the two 2D amplification roots."""
    g1, g2 = amplification_roots_2d(rx, ry, theta_x, theta_y)
    return np.maximum(np.abs(g1), np.abs(g2))


def stable_for_all_modes_2d(rx, ry, atol=1e-12):
    """Classical 2D condition rx^2 + ry^2 <= 1."""
    return bool(float(rx) ** 2 + float(ry) ** 2 <= 1.0 + atol)


def omega_dt_1d(r, theta):
    """Dimensionless numerical angular frequency omega_num*dt.

    In the stable regime the amplification roots can be written

        G = exp(+- i omega_num dt)

    and the dispersion relation is

        sin(omega_num dt / 2) = r sin(theta / 2),

    with theta = k*dx. Values outside the stable real branch are returned as
    NaN because no real oscillation frequency exists there.
    """
    r = np.asarray(r, dtype=float)
    theta = np.asarray(theta, dtype=float)
    argument = r * np.sin(theta / 2.0)
    valid = np.abs(argument) <= 1.0
    out = np.full(np.broadcast(r, theta).shape, np.nan, dtype=float)
    arg_b = np.broadcast_to(argument, out.shape)
    valid_b = np.broadcast_to(valid, out.shape)
    out[valid_b] = 2.0 * np.arcsin(arg_b[valid_b])
    return out


def phase_velocity_ratio_1d(r, theta):
    """Return numerical phase velocity divided by physical speed c.

    theta = k*dx and r = c*dt/dx, hence

        v_phase,num / c = (omega_num*dt) / (r*theta).

    The theta=0 limit is 1.
    """
    r = float(r)
    theta = np.asarray(theta, dtype=float)
    omega_dt = omega_dt_1d(r, theta)
    ratio = np.empty_like(theta, dtype=float)
    small = np.isclose(theta, 0.0)
    ratio[small] = 1.0
    ratio[~small] = omega_dt[~small] / (r * theta[~small])
    return ratio
