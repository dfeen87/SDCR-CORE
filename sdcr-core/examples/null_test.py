# examples/null_test.py
"""
SDCR-CORE: Explicit null / recovery test

This script verifies the defining SDCR claim:
when symmetry selection is disabled, the dynamics
reduce exactly to the baseline evolution.

It is intended as a runnable falsifiability check,
not a unit test.
"""

import numpy as np

from core.dynamics import solve_lindblad
from core.symmetry import pauli_z_symmetry
from core.recovery import build_selector, solve_with_recovery, recovery_check


def run_null_test(verbose: bool = True) -> bool:
    # ----------------------------
    # System definition
    # ----------------------------

    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

    omega = 1.0
    gamma = 0.35

    H = 0.5 * omega * sigma_x
    L_ops = [np.sqrt(gamma) * sigma_z]

    psi_plus = (1 / np.sqrt(2)) * np.array([1, 1], dtype=np.complex128)
    rho0 = np.outer(psi_plus, np.conjugate(psi_plus))

    t_span = (0.0, 6.0)
    t_eval = np.linspace(t_span[0], t_span[1], 300)

    # ----------------------------
    # Baseline evolution
    # ----------------------------

    _, rhos_baseline = solve_lindblad(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
    )

    # ----------------------------
    # SDCR disabled (recovery)
    # ----------------------------

    projector = pauli_z_symmetry(dim=2)
    selector_recovery = build_selector(projector=projector, enabled=False)

    _, rhos_recovery = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_recovery,
    )

    # ----------------------------
    # Check recovery
    # ----------------------------

    passed = recovery_check(
        rhos_sdcr=rhos_recovery,
        rhos_baseline=rhos_baseline,
        tol=1e-8,
    )

    if verbose:
        print("SDCR Recovery / Null Test")
        print("-------------------------")
        print(f"Result: {'PASS' if passed else 'FAIL'}")

    return passed


if __name__ == "__main__":
    success = run_null_test(verbose=True)
    if not success:
        raise SystemExit(1)

