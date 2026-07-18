# tests/test_gksl_locked_qubit.py

import os
import shutil
import numpy as np
import scipy.linalg as la
import pytest

from sdcr_core.core.symmetry_selector import get_suppression_weights
from sdcr_core.core.gksl_locked_qubit import (
    SIGMA_X, SIGMA_Y, SIGMA_Z,
    vectorized_commutator, vectorized_dissipator,
    assemble_liouvillian, evolve_state, run_locked_qubit_benchmark
)
from sdcr_core.core.liouvillian_spectrum import (
    compute_liouvillian_eigenvalues, audit_liouvillian_spectra
)
from sdcr_core.core.validation import (
    compute_trace_errors, compute_hermiticity_errors,
    compute_minimum_eigenvalues, compute_coherence_auc,
    compute_all_validation_metrics
)
from sdcr_core.io.outputs import write_all_outputs


def test_pauli_matrices():
    # Pauli matrices must be Hermitian
    assert np.allclose(SIGMA_X, SIGMA_X.conj().T)
    assert np.allclose(SIGMA_Y, SIGMA_Y.conj().T)
    assert np.allclose(SIGMA_Z, SIGMA_Z.conj().T)

    # Pauli matrices must be involutory: S^2 = I
    I = np.eye(2, dtype=complex)
    assert np.allclose(SIGMA_X @ SIGMA_X, I)
    assert np.allclose(SIGMA_Y @ SIGMA_Y, I)
    assert np.allclose(SIGMA_Z @ SIGMA_Z, I)

    # Pauli matrices must be traceless
    assert np.trace(SIGMA_X) == 0
    assert np.trace(SIGMA_Y) == 0
    assert np.trace(SIGMA_Z) == 0


def test_symmetry_selector():
    # eta_sym = 0 -> weight = 1
    assert get_suppression_weights(0.0) == (1.0, 1.0)
    # eta_sym = 1 -> weight = 0
    assert get_suppression_weights(1.0) == (0.0, 0.0)
    # eta_sym = 0.3 -> weight = 0.7
    w_x, w_y = get_suppression_weights(0.3)
    assert np.isclose(w_x, 0.7)
    assert np.isclose(w_y, 0.7)


def test_vectorized_commutator_and_dissipator():
    # Generate random H and rho
    rng = np.random.default_rng(12345)
    # Random Hermitian H
    H = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    H = H + H.conj().T

    # Random rho
    rho = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    rho = rho @ rho.conj().T
    rho /= np.trace(rho)

    # Direct physical commutator: -i [H, rho]
    comm_direct = -1j * (H @ rho - rho @ H)

    # Vectorized commutator
    L_coh = vectorized_commutator(H)
    comm_vec = L_coh @ rho.flatten('C')

    assert np.allclose(comm_direct.flatten('C'), comm_vec)

    # Direct physical dissipator: D(L)(rho) = L rho L^dag - 0.5 {L^dag L, rho}
    L_op = SIGMA_X
    diss_direct = L_op @ rho @ L_op.conj().T - 0.5 * (L_op.conj().T @ L_op @ rho + rho @ L_op.conj().T @ L_op)

    # Vectorized dissipator
    D_vec_op = vectorized_dissipator(L_op)
    diss_vec = D_vec_op @ rho.flatten('C')

    assert np.allclose(diss_direct.flatten('C'), diss_vec)


def test_assemble_liouvillian_and_evolve():
    L = assemble_liouvillian(omega=1.0, eta_sym=1.0)
    assert L.shape == (4, 4)

    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    times = np.array([0.0, 1.0, 2.0])
    traj = evolve_state(rho0, L, times)

    assert traj.shape == (3, 2, 2)
    # Evolved states must be trace 1
    for r in traj:
        assert np.isclose(np.trace(r), 1.0)
        # and Hermitian
        assert np.allclose(r, r.conj().T)


def test_liouvillian_spectrum():
    L_protected = assemble_liouvillian(omega=1.0, eta_sym=1.0, gamma_z=0.1)
    evals = compute_liouvillian_eigenvalues(L_protected)

    # For eta=1.0, we have dephasing of rate gamma_z=0.1, omega=1.0
    # Expected eigenvalues: 0, 0, -0.2 + 1j, -0.2 - 1j
    expected = np.sort_complex(np.array([0.0, 0.0, -0.2 + 1j, -0.2 - 1j]))
    assert np.allclose(evals, expected, atol=1e-8)


def test_validation_metrics():
    # Construct a dummy trajectory
    times = np.array([0.0, 1.0])
    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex)
    rho1 = np.array([[0.5, 0.1j], [-0.1j, 0.5]], dtype=complex)
    traj = np.array([rho0, rho1])

    # Trace errors: rho0 trace = 1.0, rho1 trace = 1.0 -> error = 0.0
    assert np.isclose(compute_trace_errors(traj), 0.0)

    # Hermiticity errors: both are Hermitian -> error = 0.0
    assert np.isclose(compute_hermiticity_errors(traj), 0.0)

    # Minimum eigenvalues: rho0 -> 0, 1; rho1 -> 0.4, 0.6 -> min = 0.0
    assert np.isclose(compute_minimum_eigenvalues(traj), 0.0, atol=1e-7)

    # Coherence AUC: |rho_01(0)| = 0.0, |rho_01(1)| = 0.1. Area under curve of [0, 0.1] over [0, 1] is 0.05
    assert np.isclose(compute_coherence_auc(times, traj), 0.05)


def test_full_benchmark_and_io():
    result = run_locked_qubit_benchmark(eta_sym=1.0)
    assert "metrics" in result
    assert "spectra_df" in result

    # Test file output
    test_dir = "results_test_temp"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)

    try:
        write_all_outputs(result, output_dir=test_dir)

        # Verify files are written
        assert os.path.exists(os.path.join(test_dir, "summary_metrics.json"))
        assert os.path.exists(os.path.join(test_dir, "trajectories.csv"))
        assert os.path.exists(os.path.join(test_dir, "liouvillian_spectrum.csv"))
        assert os.path.exists(os.path.join(test_dir, "manifest.json"))

    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)
