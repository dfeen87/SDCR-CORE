# core/dynamics.py
"""
SDCR-CORE: Open-system dynamics (Lindblad / GKSL)

This module provides a minimal, transparent Lindblad master-equation engine.

Design goals:
- Conservative: standard GKSL form, no speculative extensions
- Readable: explicit math, clear validation
- Reproducible: deterministic integration via SciPy solve_ivp

Density matrices are represented as (N, N) complex numpy arrays.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Sequence, Tuple, Union

import numpy as np
from numpy.typing import NDArray

from scipy.integrate import solve_ivp


ComplexArray = NDArray[np.complex128]
RealArray = NDArray[np.float64]


def dagger(a: ComplexArray) -> ComplexArray:
    """Hermitian conjugate."""
    return np.conjugate(a.T)


def commutator(a: ComplexArray, b: ComplexArray) -> ComplexArray:
    """[a, b] = ab - ba."""
    return a @ b - b @ a


def anticommutator(a: ComplexArray, b: ComplexArray) -> ComplexArray:
    """{a, b} = ab + ba."""
    return a @ b + b @ a


def is_square_matrix(a: ComplexArray) -> bool:
    return a.ndim == 2 and a.shape[0] == a.shape[1]


def _assert_square(name: str, a: ComplexArray) -> None:
    if not is_square_matrix(a):
        raise ValueError(f"{name} must be a square matrix; got shape {a.shape}.")


def _assert_same_dim(name_a: str, a: ComplexArray, name_b: str, b: ComplexArray) -> None:
    if a.shape != b.shape:
        raise ValueError(f"{name_a} and {name_b} must have same shape; got {a.shape} vs {b.shape}.")


def _trace(a: ComplexArray) -> complex:
    return np.trace(a)


def _hermitize(rho: ComplexArray) -> ComplexArray:
    """Project to the Hermitian part: (rho + rho†)/2."""
    return 0.5 * (rho + dagger(rho))


def lindblad_rhs(
    t: float,
    rho: ComplexArray,
    H: ComplexArray,
    L_ops: Sequence[ComplexArray],
    rates: Optional[Sequence[float]] = None,
) -> ComplexArray:
    r"""
    Lindblad (GKSL) master equation:

        dρ/dt = -i[H, ρ] + Σ_k γ_k ( L_k ρ L_k† - 1/2 {L_k† L_k, ρ} )

    Parameters
    ----------
    t : float
        Time (unused for time-independent H and L, but included for solver compatibility).
    rho : (N,N) complex array
        Density matrix at time t.
    H : (N,N) complex array
        System Hamiltonian (Hermitian recommended).
    L_ops : list of (N,N) complex arrays
        Lindblad operators.
    rates : list of floats, optional
        Nonnegative rates γ_k. If None, all rates default to 1.0.

    Returns
    -------
    drho_dt : (N,N) complex array
    """
    _assert_square("rho", rho)
    _assert_square("H", H)
    _assert_same_dim("rho", rho, "H", H)

    if rates is None:
        rates = [1.0] * len(L_ops)

    if len(rates) != len(L_ops):
        raise ValueError(f"rates length must match L_ops length; got {len(rates)} vs {len(L_ops)}.")

    # Unitary part
    drho = -1j * commutator(H, rho)

    # Dissipator
    for idx, (L, gamma) in enumerate(zip(L_ops, rates)):
        _assert_square(f"L_ops[{idx}]", L)
        _assert_same_dim("rho", rho, f"L_ops[{idx}]", L)
        if gamma < 0:
            raise ValueError(f"rates[{idx}] must be nonnegative; got {gamma}.")

        Ld = dagger(L)
        jump = L @ rho @ Ld
        damp = 0.5 * anticommutator(Ld @ L, rho)
        drho = drho + gamma * (jump - damp)

    return drho


def _vec(rho: ComplexArray) -> ComplexArray:
    """Column-stacking vectorization."""
    return rho.reshape(-1, order="F")


def _unvec(v: ComplexArray, dim: int) -> ComplexArray:
    """Inverse of column-stacking vectorization."""
    return v.reshape((dim, dim), order="F")


def solve_lindblad(
    rho0: ComplexArray,
    H: ComplexArray,
    L_ops: Sequence[ComplexArray],
    t_span: Tuple[float, float],
    t_eval: Optional[RealArray] = None,
    rates: Optional[Sequence[float]] = None,
    method: str = "RK45",
    rtol: float = 1e-8,
    atol: float = 1e-10,
    enforce_hermiticity: bool = True,
    renormalize_trace: bool = True,
) -> Tuple[RealArray, List[ComplexArray]]:
    """
    Integrate the Lindblad master equation using scipy.integrate.solve_ivp.

    Parameters
    ----------
    rho0 : (N,N)
        Initial density matrix.
    H : (N,N)
        Hamiltonian.
    L_ops : list of (N,N)
        Lindblad operators.
    t_span : (t0, tf)
        Integration interval.
    t_eval : array, optional
        Times at which to store the solution.
    rates : list of floats, optional
        Lindblad rates γ_k.
    method : str
        solve_ivp method (e.g. "RK45", "BDF").
    rtol, atol : float
        Solver tolerances.
    enforce_hermiticity : bool
        If True, project each output ρ to its Hermitian part.
    renormalize_trace : bool
        If True, normalize Tr(ρ)=1 at each stored time (defensive against numerical drift).

    Returns
    -------
    t : (M,) float array
        Evaluation times.
    rhos : list of (N,N) complex arrays
        Density matrices at each time.
    """
    _assert_square("rho0", rho0)
    _assert_square("H", H)
    _assert_same_dim("rho0", rho0, "H", H)

    dim = rho0.shape[0]
    y0 = _vec(rho0).astype(np.complex128)

    def rhs_vec(t: float, y: ComplexArray) -> ComplexArray:
        rho = _unvec(y, dim)
        drho = lindblad_rhs(t=t, rho=rho, H=H, L_ops=L_ops, rates=rates)
        return _vec(drho)

    sol = solve_ivp(
        fun=rhs_vec,
        t_span=t_span,
        y0=y0,
        t_eval=t_eval,
        method=method,
        rtol=rtol,
        atol=atol,
        vectorized=False,
    )

    if not sol.success:
        raise RuntimeError(f"Lindblad integration failed: {sol.message}")

    t_out = sol.t.astype(np.float64)
    rhos: List[ComplexArray] = []
    for k in range(sol.y.shape[1]):
        rho_k = _unvec(sol.y[:, k], dim)

        if enforce_hermiticity:
            rho_k = _hermitize(rho_k)

        if renormalize_trace:
            tr = _trace(rho_k)
            if tr == 0:
                raise RuntimeError("Trace became zero during integration; cannot renormalize.")
            rho_k = rho_k / tr

        rhos.append(rho_k)

    return t_out, rhos


def purity(rho: ComplexArray) -> float:
    """Purity Tr(ρ^2) as a simple coherence/mixedness diagnostic."""
    _assert_square("rho", rho)
    return float(np.real(np.trace(rho @ rho)))


def bloch_xy_coherence(rho: ComplexArray) -> float:
    """
    For 2-level systems only: return |ρ_01| as a simple coherence proxy.
    """
    _assert_square("rho", rho)
    if rho.shape != (2, 2):
        raise ValueError(f"bloch_xy_coherence expects a 2x2 density matrix; got {rho.shape}.")
    return float(np.abs(rho[0, 1]))


def phase_proxy(rho: ComplexArray) -> float:
    """
    Simple phase proxy for 2-level systems: arg(ρ_01).
    Use with caution; intended for demonstrations and null tests.
    """
    _assert_square("rho", rho)
    if rho.shape != (2, 2):
        raise ValueError(f"phase_proxy expects a 2x2 density matrix; got {rho.shape}.")
    return float(np.angle(rho[0, 1]))

