# domains/interferometry/runs.py
"""
Runnable interferometry domain demo.

This script:
- builds an interferometer-as-qubit model
- runs baseline vs SDCR vs recovery evolutions
- extracts visibility and phase proxies
- (optionally) plots results

Usage (from repo root):
  python -m domains.interferometry.run --plot

or:
  python domains/interferometry/run.py --plot
"""

from __future__ import annotations

import argparse
import sys
from typing import Tuple

import numpy as np

# Allow running as a script from repo root without installation
# (keeps it friendly for scientists cloning the repo)
if __name__ == "__main__" and "core" not in sys.modules:
    # Ensure repo root is on sys.path when running directly
    # Example: python domains/interferometry/run.py
    import os

    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    if repo_root not in sys.path:
        sys.path.insert(0, repo_root)

from sdcr_core.core.observables import coherence_01, phase_01, time_series
from sdcr_core.core.recovery import build_selector, solve_with_recovery
from sdcr_core.core.symmetry import pauli_z_symmetry

from .models import InterferometerParams, build_interferometer_model, default_initial_state

try:
    from .plots import plot_phase, plot_visibility
except Exception:  # pragma: no cover
    plot_phase = None
    plot_visibility = None


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="SDCR interferometry domain demo (conservative).")
    p.add_argument("--phase-rate", type=float, default=1.0, help="Relative phase accumulation rate (rad/unit time).")
    p.add_argument("--mixing-rate", type=float, default=0.0, help="Mixing (beam-splitter/recombination) rate.")
    p.add_argument("--dephasing-rate", type=float, default=0.3, help="Dephasing rate in path basis.")
    p.add_argument("--t-final", type=float, default=10.0, help="Final simulation time.")
    p.add_argument("--n-steps", type=int, default=400, help="Number of evaluation steps.")
    p.add_argument("--plot", action="store_true", help="Plot visibility and phase.")
    return p.parse_args()


def run_demo(
    params: InterferometerParams,
    t_final: float,
    n_steps: int,
) -> Tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """
    Returns
    -------
    t, vis_base, vis_sdcr, vis_rec, ph_base, ph_sdcr, ph_rec
    """
    rho0 = default_initial_state()
    H, L_ops = build_interferometer_model(params)

    t_span = (0.0, float(t_final))
    t_eval = np.linspace(t_span[0], t_span[1], int(n_steps))

    # Baseline: SDCR disabled (recovery limit)
    projector = pauli_z_symmetry(dim=2)

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

    # Recovery explicitly (same as baseline, but kept for clarity)
    selector_recovery = build_selector(projector=projector, enabled=False)
    _, rhos_rec = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_recovery,
    )

    # Visibility proxy: 2|ρ01| (bounded in [0,1] for pure equal-superposition initial state)
    vis_base = 2.0 * time_series(rhos_base, coherence_01)
    vis_sdcr = 2.0 * time_series(rhos_sdcr, coherence_01)
    vis_rec = 2.0 * time_series(rhos_rec, coherence_01)

    # Phase proxy
    ph_base = time_series(rhos_base, phase_01)
    ph_sdcr = time_series(rhos_sdcr, phase_01)
    ph_rec = time_series(rhos_rec, phase_01)

    return t, vis_base, vis_sdcr, vis_rec, ph_base, ph_sdcr, ph_rec


def main() -> None:
    args = parse_args()

    params = InterferometerParams(
        phase_rate=float(args.phase_rate),
        mixing_rate=float(args.mixing_rate),
        dephasing_rate=float(args.dephasing_rate),
    )

    t, vis_base, vis_sdcr, vis_rec, ph_base, ph_sdcr, ph_rec = run_demo(
        params=params,
        t_final=float(args.t_final),
        n_steps=int(args.n_steps),
    )

    # Console summary (calm, falsifiability-oriented)
    print("SDCR Interferometry Demo")
    print("------------------------")
    print(f"phase_rate     = {params.phase_rate}")
    print(f"mixing_rate    = {params.mixing_rate}")
    print(f"dephasing_rate = {params.dephasing_rate}")
    print("")
    print("Final values:")
    print(f"Visibility  baseline : {vis_base[-1]:.6f}")
    print(f"Visibility  SDCR     : {vis_sdcr[-1]:.6f}")
    print(f"Visibility  recovery : {vis_rec[-1]:.6f}")
    print(f"Phase proxy  baseline: {ph_base[-1]:.6f}")
    print(f"Phase proxy  SDCR    : {ph_sdcr[-1]:.6f}")
    print(f"Phase proxy  recovery: {ph_rec[-1]:.6f}")

    if args.plot:
        if plot_visibility is None or plot_phase is None:
            raise RuntimeError("Plotting helpers unavailable. Ensure matplotlib is installed.")
        plot_visibility(t, vis_base, vis_sdcr, vis_rec)
        plot_phase(t, ph_base, ph_sdcr, ph_rec)


if __name__ == "__main__":
    main()
