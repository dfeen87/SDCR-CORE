# core/recovery.py
"""
SDCR-CORE: Recovery and null-limit enforcement

This module guarantees the SDCR recovery principle:
when symmetry selection is disabled, the dynamics reduce
exactly to the baseline (non-SDCR) evolution.

There is no physics here—only explicit control logic.
"""

from __future__ import annotations

from typing import Callable, Optional, Sequence, Tuple, List

import numpy as np
from numpy.typing import NDArray

from .symmetry import SymmetrySelector, identity_projector
from .dynamics import solve_lindblad

ComplexArray = NDArray[np.complex128]
RealArray = NDArray[np.float64]


def build_selector(
    projector: Optional[Callable[[ComplexArray], ComplexArray]] = None,
    enabled: bool = True,
) -> SymmetrySelector:
    """
    Construct a SymmetrySelector with explicit recovery control.

    Parameters
    ----------
    projector : callable or None
        Symmetry projector Π_sym. If None, identity projector is used.
    enabled : bool
        If False, symmetry selection is disabled (recovery limit).

    Returns
    -------
    selector : SymmetrySelector
    """
    if projector is None:
        projector = identity_projector
    return SymmetrySelector(projector=projector, enabled=enabled)


def solve_with_recovery(
    rho0: ComplexArray,
    H: ComplexArray,
    L_ops: Sequence[ComplexArray],
    t_span: Tuple[float, float],
    t_eval: Optional[RealArray] = None,
    rates: Optional[Sequence[float]] = None,
    selector: Optional[SymmetrySelector] = None,
    **solver_kwargs,
) -> Tuple[RealArray, List[ComplexArray]]:
    """
    Solve Lindblad dynamics with explicit SDCR recovery handling.

    If selector is None or selector.enabled is False, the baseline
    Lindblad evolution is returned.

    Parameters
    ----------
    rho0, H, L_ops, t_span, t_eval, rates
        Passed directly to solve_lindblad.
    selector : SymmetrySelector or None
        Symmetry selection configuration.
    solver_kwargs
        Additional keyword arguments forwarded to solve_lindblad.

    Returns
    -------
    t : array
        Time points.
    rhos : list of density matrices
        Evolution result.
    """
    if selector is None or not selector.enabled:
        # Recovery limit: baseline evolution
        return solve_lindblad(
            rho0=rho0,
            H=H,
            L_ops=L_ops,
            t_span=t_span,
            t_eval=t_eval,
            rates=rates,
            **solver_kwargs,
        )

    # Apply symmetry selection to Lindblad operators only
    filtered_L_ops = selector.apply(L_ops)

    return solve_lindblad(
        rho0=rho0,
        H=H,
        L_ops=filtered_L_ops,
        t_span=t_span,
        t_eval=t_eval,
        rates=rates,
        **solver_kwargs,
    )


def recovery_check(
    rhos_sdcr: Sequence[ComplexArray],
    rhos_baseline: Sequence[ComplexArray],
    tol: float = 1e-8,
) -> bool:
    """
    Check that SDCR evolution reduces to baseline evolution
    in the recovery limit (within numerical tolerance).

    Parameters
    ----------
    rhos_sdcr : list of density matrices
        Evolution with SDCR disabled.
    rhos_baseline : list of density matrices
        Baseline evolution.
    tol : float
        Numerical tolerance.

    Returns
    -------
    bool
        True if recovery holds at all times.
    """
    if len(rhos_sdcr) != len(rhos_baseline):
        return False

    for rho_s, rho_b in zip(rhos_sdcr, rhos_baseline):
        if not np.allclose(rho_s, rho_b, atol=tol, rtol=0):
            return False

    return True

