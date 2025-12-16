"""
SDCR CORE — Neutrinos Models
===========================

Conservative neutrino oscillation models with optional SDCR-induced
geometric phase bias.

We model *measurement-accessible oscillation phase* in standard
two-flavor vacuum oscillations, and optionally apply a small
symmetry-weighted geometric phase offset (SDCR).

No new particles. No exotic interactions. No modification to intrinsic
neutrino parameters is assumed.
"""

from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class NeutrinoOscillationParameters:
    """
    Two-flavor vacuum oscillation parameters with optional SDCR bias.

    Units / Conventions:
    - L_km: baseline in km
    - E_GeV: neutrino energy in GeV
    - delta_m2_eV2: mass-squared splitting in eV^2
    - theta_rad: mixing angle in radians

    SDCR:
    - epsilon: small modulation strength (dimensionless)
    - symmetry_weight: symmetry selector factor (dimensionless)
    """
    L_km: float = 295.0
    E_GeV: float = 0.6
    delta_m2_eV2: float = 2.45e-3
    theta_rad: float = np.deg2rad(45.0)

    epsilon: float = 0.0
    symmetry_weight: float = 1.0


def standard_oscillation_phase(params: NeutrinoOscillationParameters) -> float:
    """
    Standard two-flavor vacuum oscillation phase.

    Uses the common phenomenology factor:
        phi = 1.267 * Δm^2(eV^2) * L(km) / E(GeV)
    """
    if params.E_GeV <= 0.0:
        raise ValueError("E_GeV must be > 0")
    if params.L_km < 0.0:
        raise ValueError("L_km must be >= 0")

    return 1.267 * params.delta_m2_eV2 * params.L_km / params.E_GeV


def sdcr_geometric_phase_bias(params: NeutrinoOscillationParameters) -> float:
    """
    SDCR geometric phase bias applied to the measured oscillation phase.

    This is modeled as a small symmetry-weighted fraction of the
    standard oscillation phase (measurement-accessible bias).
    """
    phi0 = standard_oscillation_phase(params)
    return params.symmetry_weight * params.epsilon * phi0


def effective_phase(params: NeutrinoOscillationParameters) -> float:
    """
    Effective measured phase including SDCR bias.
    """
    return standard_oscillation_phase(params) + sdcr_geometric_phase_bias(params)


def survival_probability(params: NeutrinoOscillationParameters) -> float:
    """
    Two-flavor survival probability:
        P(ν -> ν) = 1 - sin^2(2θ) * sin^2(phi)
    """
    phi = effective_phase(params)
    amp = np.sin(2.0 * params.theta_rad) ** 2
    return float(1.0 - amp * (np.sin(phi) ** 2))


def appearance_probability(params: NeutrinoOscillationParameters) -> float:
    """
    Two-flavor appearance probability:
        P(ν_a -> ν_b) = sin^2(2θ) * sin^2(phi)
    """
    phi = effective_phase(params)
    amp = np.sin(2.0 * params.theta_rad) ** 2
    return float(amp * (np.sin(phi) ** 2))

