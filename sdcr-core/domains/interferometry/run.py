"""
SDCR CORE — Interferometry Runs
==============================

Executable interferometry experiments demonstrating SDCR effects.
"""

import numpy as np

from .models import (
    InterferometerParameters,
    geometric_phase_shift,
    total_phase,
    fringe_intensity,
)

from .plots import (
    plot_phase_vs_epsilon,
    plot_fringe_pattern,
)


def run_phase_sweep():
    """
    Sweep SDCR modulation ε and visualize the induced phase shift.
    """
    eps_values = np.linspace(0.0, 3e-4, 120)
    phase_shifts = []

    for eps in eps_values:
        params = InterferometerParameters(epsilon=eps)
        phase_shifts.append(geometric_phase_shift(params))

    plot_phase_vs_epsilon(eps_values, phase_shifts)


def run_fringe_demo():
    """
    Demonstrate fringe pattern distortion under SDCR phase bias.
    """
    phases = np.linspace(0.0, 2.0 * np.pi, 500)
    intensities = [fringe_intensity(p) for p in phases]

    plot_fringe_pattern(phases, intensities)


if __name__ == "__main__":
    run_phase_sweep()
    run_fringe_demo()

