"""
SDCR CORE — Parameter Sweep Utility
==================================

Generic parameter sweep helper for SDCR-based models.

This example demonstrates how small symmetry-driven geometric
modulations (ε-scale) propagate into observable quantities.

Designed to be reused by:
- neutron_lifetime_sdcr.py
- future SDCR exemplars (spectroscopy, interferometry, clocks)

No domain-specific assumptions are made here.
"""

from dataclasses import dataclass
from typing import Callable, Tuple
import numpy as np
import matplotlib.pyplot as plt


# ---------------------------------------------------------------------
# Generic sweep configuration
# ---------------------------------------------------------------------

@dataclass(frozen=True)
class SweepConfig:
    """
    Configuration for a one-dimensional SDCR parameter sweep.
    """
    epsilon_range: Tuple[float, float] = (1e-5, 3e-4)
    num_points: int = 100
    xlabel: str = "SDCR modulation parameter ε"
    ylabel: str = "Observable value"
    title: str = "SDCR Parameter Sweep"


# ---------------------------------------------------------------------
# Core sweep engine
# ---------------------------------------------------------------------

def run_parameter_sweep(
    model_fn: Callable[[float], float],
    config: SweepConfig,
    label: str = "Observable"
):
    """
    Run a parameter sweep over ε and return sampled values.

    Parameters
    ----------
    model_fn : callable
        Function of the form f(epsilon) -> observable
    config : SweepConfig
        Sweep configuration
    label : str
        Label for plotting

    Returns
    -------
    eps_values : np.ndarray
    obs_values : np.ndarray
    """
    eps_values = np.linspace(
        config.epsilon_range[0],
        config.epsilon_range[1],
        config.num_points
    )

    obs_values = np.array([model_fn(eps) for eps in eps_values])

    return eps_values, obs_values


# ---------------------------------------------------------------------
# Plotting helper
# ---------------------------------------------------------------------

def plot_sweep(
    eps_values: np.ndarray,
    obs_values: np.ndarray,
    config: SweepConfig,
    label: str = "Observable"
):
    """
    Plot sweep results with consistent SDCR styling.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(eps_values, obs_values, label=label)
    plt.xlabel(config.xlabel)
    plt.ylabel(config.ylabel)
    plt.title(config.title)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# ---------------------------------------------------------------------
# Demonstration (standalone usage)
# ---------------------------------------------------------------------

if __name__ == "__main__":
    # Example: linear SDCR geometric response
    tau_0 = 887.0  # baseline observable (e.g., intrinsic lifetime)

    def example_model(epsilon: float) -> float:
        """
        Simple illustrative SDCR response model.
        """
        return tau_0 * (1.0 + epsilon)

    config = SweepConfig(
        epsilon_range=(1e-5, 3e-4),
        num_points=120,
        ylabel="Effective observable",
        title="Example SDCR Linear Response"
    )

    eps, vals = run_parameter_sweep(example_model, config)
    plot_sweep(eps, vals, config, label="SDCR response")

