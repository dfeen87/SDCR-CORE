# core/observables.py
"""
SDCR-CORE: Observable extraction utilities

This module provides small, explicit functions for extracting
observable quantities from density matrices produced by open-system
dynamics.

Design principles:
- Minimal and transparent
- No hidden normalization or filtering
- Suitable for falsifiability and null tests
"""

from __future__ import annotations

from typing import Iterable, List, Sequence

import numpy as np
from numpy.typing import NDArray

from .dynamics import _assert_square

ComplexArray = NDArray[np.complex128]
RealArray = NDArray[np.float64]


def trace(rho: ComplexArray) -> complex:
    """Return Tr(ρ)."""
    _assert_square("rho", rho)
    return np.trace(rho)


def purity(rho: ComplexArray) -> float:
    """
    Purity Tr(ρ²).

    Useful as a global coherence / mixedness diagnostic.
    """
    _assert_square("rho", rho)
    return float(np.real(np.trace(rho @ rho)))


def offdiagonal_norm(rho: ComplexArray) -> float:
    """
    Frobenius norm of off-diagonal elements.

    A basis-dependent but simple measure of coherence.
    """
    _assert_square("rho", rho)
    diag = np.diag(np.diag(rho))
    off = rho - diag
    return float(np.linalg.norm(off))


def coherence_01(rho: ComplexArray) -> float:
    """
    |ρ_01| coherence for a 2-level system.

    Intended for MVP demonstrations only.
    """
    _assert_square("rho", rho)
    if rho.shape != (2, 2):
        raise ValueError(f"coherence_01 expects a 2x2 density matrix; got {rho.shape}.")
    return float(np.abs(rho[0, 1]))


def phase_01(rho: ComplexArray) -> float:
    """
    arg(ρ_01) phase proxy for a 2-level system.

    Intended for demonstration and null tests.
    """
    _assert_square("rho", rho)
    if rho.shape != (2, 2):
        raise ValueError(f"phase_01 expects a 2x2 density matrix; got {rho.shape}.")
    return float(np.angle(rho[0, 1]))


def time_series(
    rhos: Sequence[ComplexArray],
    observable: callable,
) -> RealArray:
    """
    Apply an observable function to a time-ordered list of density matrices.

    Parameters
    ----------
    rhos : list of density matrices
    observable : callable
        Function mapping rho -> scalar

    Returns
    -------
    values : array
        Observable values over time
    """
    return np.array([observable(rho) for rho in rhos], dtype=np.float64)


def compare_series(
    series_a: RealArray,
    series_b: RealArray,
) -> RealArray:
    """
    Compute pointwise difference between two observable time series.

    Useful for SDCR vs baseline residuals.
    """
    if series_a.shape != series_b.shape:
        raise ValueError(
            f"Series must have same shape; got {series_a.shape} vs {series_b.shape}."
        )
    return series_a - series_b

