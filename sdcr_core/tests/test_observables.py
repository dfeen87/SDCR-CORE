# tests/test_observables.py
"""
SDCR-CORE: Observable sanity tests

These tests ensure that observable extraction utilities
behave consistently and return valid numerical values.
"""

import numpy as np

from sdcr_core.core.observables import (
    purity,
    coherence_01,
    phase_01,
    offdiagonal_norm,
)


def test_purity_bounds():
    """Purity must satisfy 0 < Tr(rho^2) <= 1."""
    rho_pure = np.array([[1, 0], [0, 0]], dtype=np.complex128)
    rho_mixed = 0.5 * np.eye(2, dtype=np.complex128)

    assert 0 < purity(rho_pure) <= 1.0
    assert 0 < purity(rho_mixed) <= 1.0


def test_coherence_and_phase_defined_for_two_level():
    """coherence_01 and phase_01 must return finite values."""
    rho = np.array(
        [[0.5, 0.25 + 0.1j],
         [0.25 - 0.1j, 0.5]],
        dtype=np.complex128,
    )

    coh = coherence_01(rho)
    ph = phase_01(rho)

    assert np.isfinite(coh)
    assert np.isfinite(ph)


def test_offdiagonal_norm_zero_for_diagonal_state():
    """Off-diagonal norm should vanish for diagonal density matrices."""
    rho = np.diag([0.7, 0.3]).astype(np.complex128)

    assert offdiagonal_norm(rho) == 0.0
