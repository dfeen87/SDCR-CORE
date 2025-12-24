# tests/test_symmetry.py
"""
SDCR-CORE: Symmetry projector sanity tests

These tests verify that the symmetry-selection operator Π_sym
behaves as a true projector on operator space.
"""

import numpy as np

from sdcr_core.core.symmetry import (
    projector_from_basis,
    identity_projector,
    pauli_z_symmetry,
)


def test_identity_projector_is_identity():
    """Π_sym = I must return the operator unchanged."""
    A = np.array([[0, 1], [2, 3]], dtype=np.complex128)
    P = identity_projector
    assert np.allclose(P(A), A)


def test_projector_idempotent():
    """Π_sym(Π_sym(O)) = Π_sym(O)."""
    sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)

    P = projector_from_basis([identity, sigma_z])

    O = np.array([[1, 2], [3, 4]], dtype=np.complex128)
    once = P(O)
    twice = P(once)

    assert np.allclose(once, twice)


def test_projector_filters_off_diagonal_components():
    """
    σ_z symmetry should remove off-diagonal components
    in the computational basis.
    """
    P = pauli_z_symmetry(dim=2)

    O = np.array([[0, 1], [1, 0]], dtype=np.complex128)  # σ_x
    O_proj = P(O)

    assert np.allclose(O_proj, np.zeros_like(O))


def test_projector_preserves_diagonal_components():
    """σ_z symmetry should preserve diagonal operators."""
    P = pauli_z_symmetry(dim=2)

    O = np.array([[2.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
    O_proj = P(O)

    assert np.allclose(O_proj, O)
