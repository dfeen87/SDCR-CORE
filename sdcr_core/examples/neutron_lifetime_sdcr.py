"""
SDCR CORE — Neutron Lifetime Discrepancy Example
================================================

Implements Appendix D:
"HLV-SDCR as a Geometric Interpretation of the Neutron Lifetime Discrepancy"

This example demonstrates how symmetry-dependent reduced dynamics
can produce different *measured* neutron lifetimes in bottle and beam
experiments without modifying the intrinsic decay constant.

No new particles.
No exotic decay channels.
No beyond-Standard-Model forces.

This file serves as a first concrete, falsifiable SDCR exemplar.
"""

from dataclasses import dataclass
import numpy as np

from sdcr_core.examples.parameter_sweep import (
    SweepConfig,
    run_parameter_sweep,
    plot_sweep,
)

# ---------------------------------------------------------------------
# Parameter definition
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class NeutronLifetimeParameters:
    """
    Parameters governing the SDCR geometric bias model.
    """
    tau_intrinsic: float = 887.0        # seconds (SM-consistent baseline)
    epsilon: float = 1.0e-4             # SDCR geometric modulation strength
    alpha_bottle: float = 1.0           # symmetry weighting (quasi-rest frame)
    beta_beam: float = 0.9              # symmetry weighting (kinematic regime)


# ---------------------------------------------------------------------
# SDCR effective lifetime models
# ---------------------------------------------------------------------

def effective_lifetime_bottle(params: NeutronLifetimeParameters) -> float:
    """
    Effective neutron lifetime measured via the bottle method.

    In the quasi-rest frame, non-kinetic spiral-time components
    contribute more strongly to reduced dynamics, inducing a
    negative geometric bias.
    """
    return params.tau_intrinsic * (1.0 - params.alpha_bottle * params.epsilon)


def effective_lifetime_beam(params: NeutronLifetimeParameters) -> float:
    """
    Effective neutron lifetime measured via the beam method.

    In the kinematic regime, forward momentum suppresses geometric
    bias, yielding a longer apparent lifetime dominated by the
    standard beta-decay channel.
    """
    return params.tau_intrinsic * (1.0 + params.beta_beam * params.epsilon)


# ---------------------------------------------------------------------
# Single-point demonstration
# ---------------------------------------------------------------------

def run_single_point_demo(params: NeutronLifetimeParameters) -> None:
    """
    Demonstrate the neutron lifetime discrepancy at a single SDCR point.
    """
    tau_bottle = effective_lifetime_bottle(params)
    tau_beam = effective_lifetime_beam(params)
    delta_tau = tau_beam - tau_bottle

    print("\nSDCR Neutron Lifetime Demonstration")
    print("----------------------------------")
    print(f"Intrinsic lifetime τ₀        : {params.tau_intrinsic:.3f} s")
    print(f"SDCR modulation ε            : {params.epsilon:.2e}")
    print(f"Bottle lifetime τ_bottle     : {tau_bottle:.3f} s")
    print(f"Beam lifetime τ_beam         : {tau_beam:.3f} s")
    print(f"Δτ (beam − bottle)           : {delta_tau:.3f} s\n")


# ---------------------------------------------------------------------
# Parameter sweep using shared SDCR infrastructure
# ---------------------------------------------------------------------

def run_sdcr_parameter_sweep(params: NeutronLifetimeParameters) -> None:
    """
    Sweep the SDCR modulation parameter ε and visualize the induced
    neutron lifetime discrepancy using the shared parameter sweep utility.
    """

    def bottle_model(epsilon: float) -> float:
        p = NeutronLifetimeParameters(
            tau_intrinsic=params.tau_intrinsic,
            epsilon=epsilon,
            alpha_bottle=params.alpha_bottle,
            beta_beam=params.beta_beam,
        )
        return effective_lifetime_bottle(p)

    def beam_model(epsilon: float) -> float:
        p = NeutronLifetimeParameters(
            tau_intrinsic=params.tau_intrinsic,
            epsilon=epsilon,
            alpha_bottle=params.alpha_bottle,
            beta_beam=params.beta_beam,
        )
        return effective_lifetime_beam(p)

    config = SweepConfig(
        epsilon_range=(1e-5, 3e-4),
        num_points=120,
        ylabel="Effective neutron lifetime (s)",
        title="SDCR Geometric Bias in Neutron Lifetime Measurements"
    )

    eps_b, tau_bottle_vals = run_parameter_sweep(bottle_model, config)
    eps_m, tau_beam_vals = run_parameter_sweep(beam_model, config)

    plot_sweep(eps_b, tau_bottle_vals, config, label="Bottle lifetime")
    plot_sweep(eps_m, tau_beam_vals, config, label="Beam lifetime")


# ---------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------

if __name__ == "__main__":
    params = NeutronLifetimeParameters(
        tau_intrinsic=887.0,
        epsilon=1.0e-4,
        alpha_bottle=1.0,
        beta_beam=0.9,
    )

    run_single_point_demo(params)
    run_sdcr_parameter_sweep(params)
