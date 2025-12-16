# domains/interferometry/plots.py
"""
Plotting helpers for the interferometry domain.

Kept separate so the core remains plotting-agnostic.
"""

from __future__ import annotations

from typing import Optional

import numpy as np
import matplotlib.pyplot as plt
from numpy.typing import NDArray

RealArray = NDArray[np.float64]


def plot_visibility(
    t: RealArray,
    vis_baseline: RealArray,
    vis_sdcr: RealArray,
    vis_recovery: RealArray,
    title: str = "Interferometry Visibility",
) -> None:
    plt.figure(figsize=(9, 4))
    plt.plot(t, vis_baseline, label="Baseline", linewidth=2)
    plt.plot(t, vis_sdcr, label="SDCR (symmetry on)", linewidth=2)
    plt.plot(t, vis_recovery, "--", label="Recovery (symmetry off)", linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Visibility (proxy)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()


def plot_phase(
    t: RealArray,
    phase_baseline: RealArray,
    phase_sdcr: RealArray,
    phase_recovery: RealArray,
    title: str = "Interferometry Phase Proxy",
) -> None:
    plt.figure(figsize=(9, 4))
    plt.plot(t, phase_baseline, label="Baseline", linewidth=2)
    plt.plot(t, phase_sdcr, label="SDCR (symmetry on)", linewidth=2)
    plt.plot(t, phase_recovery, "--", label="Recovery (symmetry off)", linewidth=2)
    plt.xlabel("Time")
    plt.ylabel("Phase proxy arg(ρ₀₁)")
    plt.title(title)
    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.show()
