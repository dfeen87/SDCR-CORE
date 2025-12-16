"""
SDCR CORE — Interferometry Models
================================

Conservative interferometric models for exploring SDCR-induced
geometric phase effects.

This module models *measurement-accessible phase shifts* rather than
microscopic dynamics. No modification of fundamental constants or
interactions is assumed.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class InterferometerParameters:
    """
    Parameters for an interferometric SDCR model.
    """
    wavelength: float = 633e-9        # meters (HeNe default)
    arm_length: float = 1.0           # meters
    epsilon: float = 0.0              # SDCR modulation strength
    symmetry_weight: float = 1.0      # symmetry selector factor


def geometric_phase_shift(params: InterferometerParameters) -> float:
    """
    Compute an SDCR-induced geometric phase shift.

    This represents a small symmetry-dependent correction to the
    measured phase, not a change in propagation speed.
    """
    base_phase = 2.0 * np.pi * params.arm_length / params.wavelength
    sdcr_phase = params.symmetry_weight * params.epsilon * base_phase
    return sdcr_phase


def total_phase(params: InterferometerParameters) -> float:
    """
    Total effective phase measured by the interferometer.
    """
    base_phase = 2.0 * np.pi * params.arm_length / params.wavelength
    return base_phase + geometric_phase_shift(params)


def fringe_intensity(phase: float) -> float:
    """
    Normalized interferometric fringe intensity.
    """
    return 0.5 * (1.0 + np.cos(phase))

