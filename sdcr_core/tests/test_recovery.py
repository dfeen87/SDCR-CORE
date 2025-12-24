# tests/test_recovery.py
"""
SDCR-CORE: Recovery / null-limit tests

These tests verify the defining SDCR requirement:
when symmetry selection is disabled, the evolution reduces
to the baseline Lindblad dynamics within numerical tolerance.
"""

import numpy as np

from sdcr_core.core.dynamics import solve_lindblad
from sdcr_core.core.symmetry import pauli_z_symmetry
from sdcr_core.core.recovery import (
    build_selector,
    solve_with_recovery,
    recovery_check,
)


def test_recovery_limit_matches_baseline():
    """
    SDCR disabled must reproduce baseline evolution.
    """

    # ----------------------------
    # System definition (2-level)
    # ----------------------------

    sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

    omega = 1.0
    gamma = 0.3

    H = 0.5 * omega * sigma_x
    L_ops = [np.sqrt(gamma) * sigma_z]

    psi_plus = (1 / np.sqrt(2)) * np.array([1, 1], dtype=np.complex128)
    rho0 = np.outer(psi_plus, np.conjugate(psi_plus))

    t_span = (0.0, 5.0)
    t_eval = np.linspace(t_span[0], t_span[1], 200)

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
    # SDCR recovery evolution
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
    # Assert recovery
    # ----------------------------

    assert recovery_check(
        rhos_sdcr=rhos_recovery,
        rhos_baseline=rhos_baseline,
        tol=1e-8,
    ), "Recovery limit failed: SDCR-disabled evolution does not match baseline."
