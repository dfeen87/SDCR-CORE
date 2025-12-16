"""
SDCR CORE — Neutrinos Runs
=========================

Executable demonstrations for neutrino oscillations with optional SDCR bias.

Run:
    python -m sdcr_core.domains.neutrinos.runs
"""

import numpy as np

from .models import (
    NeutrinoOscillationParameters,
    survival_probability,
    appearance_probability,
)

from .plots import (
    plot_probability_vs_energy,
    plot_probability_vs_baseline,
    plot_delta_probability,
)


def run_energy_scan_survival(eps: float = 0.0):
    """
    Scan survival probability vs energy for a fixed baseline.
    """
    energies = np.linspace(0.1, 5.0, 400)
    probs = []

    base = NeutrinoOscillationParameters(epsilon=eps)

    for E in energies:
        p = NeutrinoOscillationParameters(
            L_km=base.L_km,
            E_GeV=float(E),
            delta_m2_eV2=base.delta_m2_eV2,
            theta_rad=base.theta_rad,
            epsilon=base.epsilon,
            symmetry_weight=base.symmetry_weight,
        )
        probs.append(survival_probability(p))

    title = "Neutrino Survival Probability vs Energy"
    if eps != 0.0:
        title += f" (SDCR ε={eps:.1e})"
    plot_probability_vs_energy(energies, probs, title, ylabel="P(ν → ν)")


def run_baseline_scan_appearance(eps: float = 0.0):
    """
    Scan appearance probability vs baseline for a fixed energy.
    """
    baselines = np.linspace(1.0, 1300.0, 500)
    probs = []

    base = NeutrinoOscillationParameters(epsilon=eps)

    for L in baselines:
        p = NeutrinoOscillationParameters(
            L_km=float(L),
            E_GeV=base.E_GeV,
            delta_m2_eV2=base.delta_m2_eV2,
            theta_rad=base.theta_rad,
            epsilon=base.epsilon,
            symmetry_weight=base.symmetry_weight,
        )
        probs.append(appearance_probability(p))

    title = "Neutrino Appearance Probability vs Baseline"
    if eps != 0.0:
        title += f" (SDCR ε={eps:.1e})"
    plot_probability_vs_baseline(baselines, probs, title, ylabel="P(νₐ → νᵦ)")


def run_sdcr_delta_energy_scan(eps: float = 1e-4):
    """
    Show ΔP induced by SDCR (SDCR − baseline) across an energy scan.
    """
    energies = np.linspace(0.1, 5.0, 400)
    deltas = []

    base0 = NeutrinoOscillationParameters(epsilon=0.0)
    base1 = NeutrinoOscillationParameters(epsilon=eps)

    for E in energies:
        p0 = NeutrinoOscillationParameters(
            L_km=base0.L_km,
            E_GeV=float(E),
            delta_m2_eV2=base0.delta_m2_eV2,
            theta_rad=base0.theta_rad,
            epsilon=0.0,
            symmetry_weight=base0.symmetry_weight,
        )
        p1 = NeutrinoOscillationParameters(
            L_km=base1.L_km,
            E_GeV=float(E),
            delta_m2_eV2=base1.delta_m2_eV2,
            theta_rad=base1.theta_rad,
            epsilon=eps,
            symmetry_weight=base1.symmetry_weight,
        )

        deltas.append(survival_probability(p1) - survival_probability(p0))

    plot_delta_probability(
        energies,
        deltas,
        xlabel="Neutrino Energy E (GeV)",
        title=f"SDCR-Induced Deviation in Survival Probability (ε={eps:.1e})",
    )


if __name__ == "__main__":
    # Baselines
    run_energy_scan_survival(eps=0.0)
    run_baseline_scan_appearance(eps=0.0)

    # SDCR-on demonstrations
    run_energy_scan_survival(eps=1e-4)
    run_baseline_scan_appearance(eps=1e-4)

    # Delta plot (SDCR − baseline)
    run_sdcr_delta_energy_scan(eps=1e-4)

