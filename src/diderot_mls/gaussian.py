"""Gaussian density, parameter estimation and reproducible figures."""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np


def gaussian_pdf(x: np.ndarray | float, mu: float, sigma: float) -> np.ndarray:
    """Return the univariate Gaussian probability density."""
    if sigma <= 0:
        raise ValueError("sigma must be strictly positive")
    values = np.asarray(x, dtype=float)
    coefficient = 1.0 / (np.sqrt(2.0 * np.pi) * sigma)
    return coefficient * np.exp(-0.5 * ((values - mu) / sigma) ** 2)


def estimate_parameters(samples: np.ndarray) -> tuple[float, float]:
    """Maximum-likelihood estimates (division by m) of mu and variance."""
    values = np.asarray(samples, dtype=float)
    if values.ndim != 1 or values.size == 0:
        raise ValueError("samples must be a non-empty one-dimensional array")
    mu = float(values.mean())
    variance = float(np.mean((values - mu) ** 2))
    return mu, variance


def anomaly_mask(samples: np.ndarray, mu: float, sigma: float, epsilon: float) -> np.ndarray:
    """Flag observations whose Gaussian density is below epsilon."""
    if epsilon < 0:
        raise ValueError("epsilon must be non-negative")
    return gaussian_pdf(samples, mu, sigma) < epsilon


def create_figure(output: str | Path) -> Path:
    """Create the four-comparison figure used by the book."""
    target = Path(output)
    target.parent.mkdir(parents=True, exist_ok=True)
    x = np.linspace(-6.0, 7.0, 1600)
    configurations = [
        (0.0, 1.0, r"$\mu=0,\ \sigma=1$"),
        (0.0, 0.5, r"$\mu=0,\ \sigma=0{,}5$"),
        (0.0, 2.0, r"$\mu=0,\ \sigma=2$"),
        (3.0, 0.5, r"$\mu=3,\ \sigma=0{,}5$"),
    ]
    fig, axes = plt.subplots(2, 2, figsize=(9.6, 6.2), sharex=True, sharey=True)
    for ax, (mu, sigma, title) in zip(axes.flat, configurations):
        density = gaussian_pdf(x, mu, sigma)
        ax.plot(x, density, color="#126E82", linewidth=2.4)
        ax.fill_between(x, density, color="#9ED9CC", alpha=0.45)
        ax.axvline(mu, color="#7A1F2B", linestyle="--", linewidth=1.3)
        ax.set_title(title)
        ax.set_xlim(-6, 7)
        ax.set_ylim(0, 0.85)
        ax.grid(alpha=0.18)
    fig.supxlabel("Valeur $x$")
    fig.supylabel("Densite $p(x)$")
    fig.tight_layout()
    fig.savefig(target, bbox_inches="tight")
    plt.close(fig)
    return target


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="book/figures/gaussian-comparison.pdf")
    args = parser.parse_args()
    create_figure(args.output)


if __name__ == "__main__":
    main()

