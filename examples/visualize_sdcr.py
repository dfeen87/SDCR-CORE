"""
SDCR-CORE Visualization Script
==============================

Read-only visualization of SDCR behavior using existing domain models.

This script:
- Runs a fixed interferometry-domain configuration
- Validates all quantum states and operators before evolution
- Plots coherence (visibility proxy) and phase proxy vs time
- Compares baseline, SDCR-enabled, and recovery evolutions

No parameters are exposed for tuning.
This file is intended as a figure-style visualization companion,
not an exploratory dashboard.
"""

from __future__ import annotations

import sys
import os
from typing import Tuple, List

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


# =====================================================================
# VALIDATION LAYER
# =====================================================================

def validate_density_matrix(rho: np.ndarray, tol: float = 1e-10) -> None:
    """
    Validate that rho is a valid density matrix.
    
    Checks:
    - Square matrix
    - Hermitian
    - Trace = 1
    - Positive semidefinite
    
    Raises:
        ValueError: If any check fails
    """
    if rho.shape[0] != rho.shape[1]:
        raise ValueError("Density matrix must be square.")

    if not np.allclose(rho, rho.conj().T, atol=tol):
        raise ValueError("Density matrix must be Hermitian.")

    tr = np.trace(rho)
    if not np.isclose(tr, 1.0, atol=tol):
        raise ValueError(f"Density matrix trace must be 1 (got {tr}).")

    eigvals = np.linalg.eigvalsh(rho)
    if np.any(eigvals < -tol):
        raise ValueError("Density matrix must be positive semidefinite.")


def validate_hamiltonian(H: np.ndarray, tol: float = 1e-12) -> None:
    """
    Validate that H is a valid Hamiltonian.
    
    Checks:
    - Hermitian
    
    Raises:
        ValueError: If check fails
    """
    if not np.allclose(H, H.conj().T, atol=tol):
        raise ValueError("Hamiltonian must be Hermitian.")


def validate_lindblad_ops(L_ops: List[np.ndarray], dim: int) -> None:
    """
    Validate Lindblad operators.
    
    Checks:
    - Each operator matches system dimension
    
    Raises:
        ValueError: If any check fails
    """
    for i, L in enumerate(L_ops):
        if L.shape != (dim, dim):
            raise ValueError(
                f"Lindblad operator {i} has shape {L.shape}, "
                f"expected ({dim}, {dim})."
            )


def validate_time_grid(t_eval: np.ndarray) -> None:
    """
    Validate time evaluation grid.
    
    Checks:
    - Strictly increasing
    - Sufficient resolution for visualization
    
    Raises:
        ValueError: If any check fails
    """
    if np.any(np.diff(t_eval) <= 0):
        raise ValueError("Time grid must be strictly increasing.")

    if len(t_eval) < 10:
        raise ValueError("Time grid too coarse for visualization.")


def validate_observables(name: str, arr: np.ndarray) -> None:
    """
    Validate observable array before plotting.
    
    Checks:
    - No NaN or Inf values
    
    Raises:
        ValueError: If check fails
    """
    if not np.all(np.isfinite(arr)):
        raise ValueError(f"Observable '{name}' contains non-finite values.")


# =====================================================================
# MAIN VISUALIZATION LOGIC
# =====================================================================

def _run_interferometry() -> Tuple[np.ndarray, ...]:
    """Run baseline, SDCR, and recovery evolutions with full validation."""
    print("Running validation checks...")
    
    # Build model
    rho0 = default_initial_state()
    H, L_ops = build_interferometer_model(_PARAMS)

    # Validate initial state
    validate_density_matrix(rho0)
    print("✓ Initial density matrix is valid")
    
    # Validate Hamiltonian
    validate_hamiltonian(H)
    print("✓ Hamiltonian is valid")
    
    # Validate Lindblad operators
    dim = rho0.shape[0]
    validate_lindblad_ops(L_ops, dim)
    print(f"✓ All {len(L_ops)} Lindblad operator(s) are valid")

    # Build time grid
    t_span = (0.0, _T_FINAL)
    t_eval = np.linspace(t_span[0], t_span[1], _N_STEPS)
    
    # Validate time grid
    validate_time_grid(t_eval)
    print(f"✓ Time grid is valid ({len(t_eval)} points)")

    projector = pauli_z_symmetry(dim=2)

    print("\nRunning dynamics...")
    
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

    print("✓ Dynamics completed successfully")
    
    # Extract observables
    print("\nExtracting observables...")
    vis_base = 2.0 * time_series(rhos_base, coherence_01)
    vis_sdcr = 2.0 * time_series(rhos_sdcr, coherence_01)
    vis_rec = 2.0 * time_series(rhos_rec, coherence_01)

    ph_base = time_series(rhos_base, phase_01)
    ph_sdcr = time_series(rhos_sdcr, phase_01)
    ph_rec = time_series(rhos_rec, phase_01)

    # Validate observables before plotting
    validate_observables("visibility_baseline", vis_base)
    validate_observables("visibility_sdcr", vis_sdcr)
    validate_observables("visibility_recovery", vis_rec)
    print("✓ Visibility observables are valid")
    
    validate_observables("phase_baseline", ph_base)
    validate_observables("phase_sdcr", ph_sdcr)
    validate_observables("phase_recovery", ph_rec)
    print("✓ Phase observables are valid")

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
    print("=" * 60)
    print("SDCR Visualization (read-only with validation)")
    print("=" * 60)
    print("Domain       : Interferometry (two-path)")
    print(f"phase_rate   : {_PARAMS.phase_rate}")
    print(f"mixing_rate  : {_PARAMS.mixing_rate}")
    print(f"dephasing    : {_PARAMS.dephasing_rate}")
    print("")
    print("Note: Parameters are fixed by design.")
    print("This visualization is observational only.")
    print("=" * 60)
    print("")

    try:
        data = _run_interferometry()
        print("\n" + "=" * 60)
        print("All validation checks passed!")
        print("Generating plots...")
        print("=" * 60 + "\n")
        _plot(*data)
    except ValueError as e:
        print(f"\n❌ Validation failed: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
