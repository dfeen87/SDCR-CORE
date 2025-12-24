# domains/interferometry/model.py
"""
Interferometry domain model (minimal, conservative).

We represent a two-path interferometer as a 2-level system:
- |0> and |1> correspond to the two arms/paths.
- Relative phase accumulation between arms is modeled by a σ_z term.
- A beam-splitter / recombination action is modeled by a σ_x term (mixing).

Decoherence is modeled with standard Lindblad operators (e.g., dephasing).

This module contains no SDCR-specific logic; it only provides a domain mapping
to core dynamics + symmetry selection.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import numpy as np
from numpy.typing import NDArray

ComplexArray = NDArray[np.complex128]


def pauli_x() -> ComplexArray:
    return np.array([[0.0, 1.0], [1.0, 0.0]], dtype=np.complex128)


def pauli_z() -> ComplexArray:
    return np.array([[1.0, 0.0], [0.0, -1.0]], dtype=np.complex128)


def ket_plus() -> ComplexArray:
    """|+> = (|0> + |1>)/sqrt(2)"""
    return (1.0 / np.sqrt(2.0)) * np.array([1.0, 1.0], dtype=np.complex128)


def density_from_state(psi: ComplexArray) -> ComplexArray:
    return np.outer(psi, np.conjugate(psi))


@dataclass(frozen=True)
class InterferometerParams:
    """
    Minimal interferometer parameters.

    phase_rate:
        Relative phase accumulation rate between arms (rad / unit time).
        Appears as (phase_rate/2)*σ_z in the Hamiltonian.

    mixing_rate:
        Beam-splitter / recombination mixing strength.
        Appears as (mixing_rate/2)*σ_x in the Hamiltonian.

    dephasing_rate:
        Standard dephasing rate in the path basis (σ_z Lindblad operator).

    mixing_dephasing_rate:
        Optional dephasing rate that acts in the σ_x basis to introduce
        off-diagonal noise channels.
    """

    phase_rate: float = 1.0
    mixing_rate: float = 0.0
    dephasing_rate: float = 0.3
    mixing_dephasing_rate: float = 0.0


def build_interferometer_model(params: InterferometerParams) -> Tuple[ComplexArray, List[ComplexArray]]:
    """
    Build (H, L_ops) for the interferometer-as-qubit model.

    Returns
    -------
    H : (2,2) complex array
        Hamiltonian with σ_z (phase) and σ_x (mixing) terms.
    L_ops : list of (2,2) complex arrays
        Lindblad operators (currently dephasing in the path basis).
    """
    sx = pauli_x()
    sz = pauli_z()

    H = 0.5 * params.phase_rate * sz + 0.5 * params.mixing_rate * sx

    # Dephasing in the path basis
    # L = sqrt(gamma) * σ_z  (standard dephasing channel)
    if params.dephasing_rate < 0:
        raise ValueError("dephasing_rate must be nonnegative.")
    if params.mixing_dephasing_rate < 0:
        raise ValueError("mixing_dephasing_rate must be nonnegative.")

    L_ops: List[ComplexArray] = []
    if params.dephasing_rate > 0:
        L_ops.append(np.sqrt(params.dephasing_rate) * sz)
    if params.mixing_dephasing_rate > 0:
        L_ops.append(np.sqrt(params.mixing_dephasing_rate) * sx)

    return H, L_ops


def default_initial_state() -> ComplexArray:
    """
    Default initial state for an interferometry-style demo:
    |+><+| corresponds to equal superposition of paths.
    """
    return density_from_state(ket_plus())
