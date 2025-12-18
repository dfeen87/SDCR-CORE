"""
SDCR-CORE Visualization Script
==============================

Read-only visualization of SDCR behavior using existing domain models.

This script:
- Runs a fixed interferometry-domain configuration
- Plots coherence (visibility proxy) and phase proxy vs time
- Compares baseline, SDCR-enabled, and recovery evolutions

No parameters are exposed for tuning.
This file is intended as a figure-style visualization companion,
not an exploratory dashboard.
"""

from __future__ import annotations

import sys
import os
from typing import Tuple

import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Path safety: allow direct execution from repo root
# ---------------------------------------------------------------------
if __name__ == "__main__" and "core" not in sys.modules:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

# ---------------------------------------------------------------------
# Imports from SDCR-CORE
# ---------------------------------------------------------------------
from core.recovery import build_selector, solve_with_recovery
from core.symmetry import pauli_z_symmetry
from core.observables import coherence_01, phase_01, time_series

from domains.interferometry.model import (
    InterferometerParams,
    build_interferometer_model,
    default_initial_state,
)

# ---------------------------------------------------------------------
# Fixed visualization configuration (intentional)
# ---------------------------------------------------------------------
_PARAMS = InterferometerParams(
    phase_rate=1.0,
    mixing_rate=0.0,
    dephasing_rate=0.3,
)

_T_FINAL = 10.0
_N_STEPS = 400


def _run_interferometry() -> Tuple[np.ndarray, ...]:
    """Run baseline, SDCR, and recovery evolutions."""
    rho0 = default_initial_state()
    H, L_ops = build_interferometer_model(_PARAMS)

    t_span = (0.0, _T_FINAL)
    t_eval = np.linspace(t_span[0], t_span[1], _N_STEPS)

    projector = pauli_z_symmetry(dim=2)

    # Baseline (symmetry disabled)
    selector_baseline = build_selector(projector=projector, enabled=False)
    t, rhos_base = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_baseline,
    )

    # SDCR enabled
    selector_sdcr = build_selector(projector=projector, enabled=True)
    _, rhos_sdcr = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_sdcr,
    )

    # Explicit recovery (same as baseline, shown for clarity)
    selector_recovery = build_selector(projector=projector, enabled=False)
    _, rhos_rec = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_recovery,
    )

    # Observables
    vis_base = 2.0 * time_series(rhos_base, coherence_01)
    vis_sdcr = 2.0 * time_series(rhos_sdcr, coherence_01)
    vis_rec = 2.0 * time_series(rhos_rec, coherence_01)

    ph_base = time_series(rhos_base, phase_01)
    ph_sdcr = time_series(rhos_sdcr, phase_01)
    ph_rec = time_series(rhos_rec, phase_01)

    return t, vis_base, vis_sdcr, vis_rec, ph_base, ph_sdcr, ph_rec


def _plot(
    t: np.ndarray,
    vis_base: np.ndarray,
    vis_sdcr: np.ndarray,
    vis_rec: np.ndarray,
    ph_base: np.ndarray,
    ph_sdcr: np.ndarray,
    ph_rec: np.ndarray,
) -> None:
    """Generate figure-style plots."""
    plt.rcParams.update(
        {
            "figure.figsize": (9, 4),
            "axes.grid": True,
            "grid.alpha": 0.3,
            "lines.linewidth": 2.0,
        }
    )

    # -----------------------------------------------------------------
    # Visibility / coherence proxy
    # -----------------------------------------------------------------
    plt.figure()
    plt.plot(t, vis_base, label="Baseline")
    plt.plot(t, vis_sdcr, label="SDCR (symmetry on)")
    plt.plot(t, vis_rec, "--", label="Recovery")
    plt.xlabel("Time")
    plt.ylabel("Visibility proxy  2|ρ₀₁|")
    plt.title("SDCR Interferometry — Coherence / Visibility")
    plt.legend()
    plt.tight_layout()

    # -----------------------------------------------------------------
    # Phase proxy
    # -----------------------------------------------------------------
    plt.figure()
    plt.plot(t, ph_base, label="Baseline")
    plt.plot(t, ph_sdcr, label="SDCR (symmetry on)")
    plt.plot(t, ph_rec, "--", label="Recovery")
    plt.xlabel("Time")
    plt.ylabel("Phase proxy  arg(ρ₀₁)")
    plt.title("SDCR Interferometry — Phase")
    plt.legend()
    plt.tight_layout()

    plt.show()


def main() -> None:
    print("SDCR Visualization (read-only)")
    print("--------------------------------")
    print("Domain       : Interferometry (two-path)")
    print(f"phase_rate   : {_PARAMS.phase_rate}")
    print(f"mixing_rate  : {_PARAMS.mixing_rate}")
    print(f"dephasing    : {_PARAMS.dephasing_rate}")
    print("")
    print("Note: Parameters are fixed by design.")
    print("This visualization is observational only.\n")

    data = _run_interferometry()
    _plot(*data)


if __name__ == "__main__":
    main()
