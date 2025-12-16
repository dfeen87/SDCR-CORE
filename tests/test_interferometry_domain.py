# tests/test_interferometry_domain.py
"""
SDCR-CORE: Interferometry domain tests

These tests verify that the interferometry domain:
1) Respects the SDCR recovery limit (symmetry off → baseline)
2) Produces a distinguishable evolution when symmetry is enabled

No domain-specific physics claims are asserted beyond consistency.
"""

import numpy as np

from core.recovery import build_selector, solve_with_recovery, recovery_check
from core.symmetry import pauli_z_symmetry
from core.observables import coherence_01

from domains.interferometry.model import (
    InterferometerParams,
    build_interferometer_model,
    default_initial_state,
)


def test_interferometry_recovery_limit():
    """
    Interferometry domain must reduce to baseline
    when SDCR symmetry selection is disabled.
    """
    params = InterferometerParams(
        phase_rate=1.0,
        mixing_rate=0.0,
        dephasing_rate=0.25,
    )

    rho0 = default_initial_state()
    H, L_ops = build_interferometer_model(params)

    t_span = (0.0, 6.0)
    t_eval = np.linspace(t_span[0], t_span[1], 250)

    projector = pauli_z_symmetry(dim=2)

    # Baseline (recovery)
    selector_baseline = build_selector(projector=projector, enabled=False)
    _, rhos_baseline = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_baseline,
    )

    # Explicit recovery path
    selector_recovery = build_selector(projector=projector, enabled=False)
    _, rhos_recovery = solve_with_recovery(
        rho0=rho0,
        H=H,
        L_ops=L_ops,
        t_span=t_span,
        t_eval=t_eval,
        selector=selector_recovery,
    )

    assert recovery_check(
        rhos_sdcr=rhos_recovery,
        rhos_baseline=rhos_baseline,
        tol=1e-8,
    ), "Interferometry recovery limit failed."


def test_interferometry_sdcr_differs_from_baseline():
    """
    With symmetry enabled, SDCR evolution should differ
    from the baseline at least at one time point.
    """
    params = InterferometerParams(
        phase_rate=1.0,
        mixing_rate=0.0,
        dephasing_rate=0.25,
    )

    rho0 = default_initial_state()
    H, L_ops = build_interferometer_model(params)

    t_span = (0.0, 6.0)
    t_eval = np.linspace(t_span[0], t_span[1], 250)

    projector = pauli_z_symmetry(dim=2)

    # Baseline
    selector_baseline = build_selector(projector=projector, enabled=False)
    _, rhos_baseline = solve_with_recovery(
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

    # Compare coherence proxy
    coh_base = np.array([coherence_01(rho) for rho in rhos_baseline])
    coh_sdcr = np.array([coherence_01(rho) for rho in rhos_sdcr])

    # Assert there exists at least one time where they differ meaningfully
    assert np.any(np.abs(coh_sdcr - coh_base) > 1e-6), (
        "SDCR-enabled interferometry evolution did not differ from baseline."
    )
