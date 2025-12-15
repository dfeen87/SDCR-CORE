# core/symmetry.py
"""
SDCR-CORE: Symmetry selection operators (Π_sym)

This module implements explicit symmetry-selection mechanisms acting on
operators and reduced dynamics. It is intentionally conservative:
- No new dynamics
- No hidden parameters
- Explicit recovery (identity projector)

The symmetry selector Π_sym is implemented as a projector or filter acting
on operator content (e.g., Lindblad operators), not as a modification of
the underlying equations of motion.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Iterable, List, Optional, Sequence

import numpy as np
from numpy.typing import NDArray

from .dynamics import dagger, _assert_square, _assert_same_dim

ComplexArray = NDArray[np.complex128]


def identity_projector(op: ComplexArray) -> ComplexArray:
    """
    Identity projector: Π_sym = I (recovery limit).
    Returns the operator unchanged.
    """
    return op


def projector_from_basis(basis: Sequence[ComplexArray]) -> Callable[[ComplexArray], ComplexArray]:
    """
    Construct a symmetry projector Π_sym from a list of basis operators.

    The projection is defined as:
        Π_sym(O) = Σ_k Tr(B_k† O) B_k

    where {B_k} is an orthonormal operator basis (Hilbert-Schmidt inner product).

    Parameters
    ----------
    basis : list of (N,N) complex arrays
        Orthonormal operator basis defining the symmetry-aligned subspace.

    Returns
    -------
    projector : function
        A function Π_sym that maps operators to their symmetry-projected form.
    """
    if len(basis) == 0:
        raise ValueError("basis must contain at least one operator.")

    for idx, B in enumerate(basis):
        _assert_square(f"basis[{idx}]", B)

    # Precompute normalization (defensive)
    normed_basis: List[ComplexArray] = []
    for B in basis:
        norm = np.trace(dagger(B) @ B)
        if np.isclose(norm, 0):
            raise ValueError("Basis operator has zero norm.")
        normed_basis.append(B / np.sqrt(norm))

    def projector(op: ComplexArray) -> ComplexArray:
        _assert_square("op", op)
        _assert_same_dim("op", op, "basis[0]", normed_basis[0])

        out = np.zeros_like(op, dtype=np.complex128)
        for B in normed_basis:
            coeff = np.trace(dagger(B) @ op)
            out = out + coeff * B
        return out

    return projector


def apply_symmetry_to_operators(
    ops: Sequence[ComplexArray],
    projector: Optional[Callable[[ComplexArray], ComplexArray]] = None,
) -> List[ComplexArray]:
    """
    Apply a symmetry selector Π_sym to a list of operators.

    If projector is None, the identity projector is used (recovery limit).

    Parameters
    ----------
    ops : list of (N,N) complex arrays
        Operators to be symmetry-filtered (e.g., Lindblad operators).
    projector : callable or None
        Symmetry projector Π_sym. If None, Π_sym = I.

    Returns
    -------
    filtered_ops : list of (N,N) complex arrays
        Symmetry-aligned operators.
    """
    if projector is None:
        projector = identity_projector

    filtered: List[ComplexArray] = []
    for idx, op in enumerate(ops):
        _assert_square(f"ops[{idx}]", op)
        filtered.append(projector(op))
    return filtered


@dataclass(frozen=True)
class SymmetrySelector:
    """
    Container for symmetry selection configuration.

    Attributes
    ----------
    projector : callable
        Operator-level symmetry projector Π_sym.
    enabled : bool
        If False, symmetry selection is disabled (recovery limit).
    """

    projector: Callable[[ComplexArray], ComplexArray]
    enabled: bool = True

    def apply(self, ops: Sequence[ComplexArray]) -> List[ComplexArray]:
        """
        Apply Π_sym to a sequence of operators, or return them unchanged
        if symmetry selection is disabled.
        """
        if not self.enabled:
            return list(ops)
        return apply_symmetry_to_operators(ops, projector=self.projector)


def pauli_z_symmetry(dim: int = 2) -> Callable[[ComplexArray], ComplexArray]:
    """
    Convenience symmetry projector for a 2-level system aligned with σ_z.

    This keeps only operator components diagonal in the σ_z basis,
    suppressing off-diagonal decohering channels.

    Intended for demonstrations and MVP examples.
    """
    if dim != 2:
        raise ValueError("pauli_z_symmetry is defined only for dim=2.")

    sigma_z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)
    identity = np.eye(2, dtype=np.complex128)

    # Orthonormal operator basis: {I, σ_z}
    basis = [identity, sigma_z]
    return projector_from_basis(basis)

