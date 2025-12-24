"""
SDCR CORE — Neutron Lifetime Null Test
=====================================

This example provides a falsification-oriented baseline for the
HLV-SDCR interpretation of the neutron lifetime discrepancy.

All SDCR geometric effects are explicitly disabled (ε = 0).

Expected outcome:
- Bottle and beam lifetimes are identical.
- No apparent discrepancy is observed.

This file exists to demonstrate that the neutron lifetime anomaly
does NOT arise from the framework itself, but only when SDCR symmetry
modulation is explicitly introduced.
"""

from dataclasses import dataclass

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
    Parameters for the neutron lifetime null test.
    """
    tau_intrinsic: float = 887.0   # seconds
    epsilon: float = 0.0           # SDCR DISABLED
    alpha_bottle: float = 1.0
    beta_beam: float = 1.0


# ---------------------------------------------------------------------
# Effective lifetime models (null case)
# ---------------------------------------------------------------------

def effective_lifetime_bottle(params: NeutronLifetimeParameters) -> float:
    """
    Bottle method lifetime with SDCR disabled.
    """
    return params.tau_intrinsic


def effective_lifetime_beam(params: NeutronLifetimeParameters) -> float:
    """
    Beam method lifetime with SDCR disabled.
    """
    return params.tau_intrinsic


# ---------------------------------------------------------------------
# Demonstration
# ---------------------------------------------------------------------

def run_null_test(params: NeutronLifetimeParameters) -> None:
    """
    Demonstrate absence of neutron lifetime discrepancy in the null case.
    """
    tau_bottle = effective_lifetime_bottle(params)
    tau_beam = effective_lifetime_beam(params)
    delta_tau = tau_beam - tau_bottle

    print("\nSDCR Neutron Lifetime Null Test")
    print("-------------------------------")
    print(f"Intrinsic lifetime τ₀        : {params.tau_intrinsic:.3f} s")
    print(f"SDCR modulation ε            : {params.epsilon:.1e} (disabled)")
    print(f"Bottle lifetime τ_bottle     : {tau_bottle:.3f} s")
    print(f"Beam lifetime τ_beam         : {tau_beam:.3f} s")
    print(f"Δτ (beam − bottle)           : {delta_tau:.3f} s\n")


# ---------------------------------------------------------------------
# Parameter sweep (should remain flat)
# ---------------------------------------------------------------------

def run_null_parameter_sweep(params: NeutronLifetimeParameters) -> None:
    """
    Sweep ε while forcing SDCR effects to zero to verify no induced bias.
    """

    def null_model(epsilon: float) -> float:
        # ε ignored by design
        return params.tau_intrinsic

    config = SweepConfig(
        epsilon_range=(1e-5, 3e-4),
        num_points=80,
        ylabel="Effective neutron lifetime (s)",
        title="Null Test: No SDCR-Induced Neutron Lifetime Bias"
    )

    eps, tau_vals = run_parameter_sweep(null_model, config)
    plot_sweep(eps, tau_vals, config, label="Null lifetime (bottle = beam)")


# ---------------------------------------------------------------------
# Main execution
# ---------------------------------------------------------------------

if __name__ == "__main__":
    params = NeutronLifetimeParameters()

    run_null_test(params)
    run_null_parameter_sweep(params)
