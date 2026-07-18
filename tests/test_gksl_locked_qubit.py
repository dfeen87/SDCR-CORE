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
        assert os.path.exists(os.path.join(test_dir, "SHA256_MANIFEST.json"))

    finally:
        if os.path.exists(test_dir):
            shutil.rmtree(test_dir)


def test_null_battery():
    from sdcr_core.core.null_battery import run_null_battery

    # Run a baseline benchmark
    result = run_locked_qubit_benchmark(eta_sym=1.0)

    # Run the null battery with fewer trials for fast unit testing
    df, raw = run_null_battery(result, num_random_axis_trials=10)

    # Verify selectors exist in df
    unique_selectors = df["selector_type"].unique()
    assert "norm_matched" in unique_selectors
    assert "channel_permutation" in unique_selectors
    assert "eta0_baseline" in unique_selectors
    assert "random_axis_trial_0" in unique_selectors
    assert "random_axis_trial_9" in unique_selectors

    # Check shape
    # 3 selectors + 10 random trials = 13 selectors * 101 times = 1313 rows
    assert df.shape[0] == 1313
    assert "coherence" in df.columns
    assert "auc" in df.columns

    # Verify that norm_matched has the same norm of the dissipator
    # D_sdcr norm vs D_norm_matched norm
    from sdcr_core.core.gksl_locked_qubit import vectorized_dissipator
    D_z = vectorized_dissipator(SIGMA_Z)
    D_x = vectorized_dissipator(SIGMA_X)
    D_y = vectorized_dissipator(SIGMA_Y)

    eta_sym = result["eta_sym"]
    gamma_z = result["gamma_z"]
    gamma_x = result["gamma_x"]
    gamma_y = result["gamma_y"]

    D_sdcr = gamma_z * D_z + (1.0 - eta_sym) * gamma_x * D_x + (1.0 - eta_sym) * gamma_y * D_y
    norm_sdcr = la.norm(D_sdcr, 'fro')

    # Extract the norm-matched Liouvillian from raw
    L_nm = raw["norm_matched"]["L"]
    # Subtract L_coh from L_nm to get the dissipator part
    H = (result["omega"] / 2.0) * SIGMA_Z
    from sdcr_core.core.gksl_locked_qubit import vectorized_commutator
    L_coh = vectorized_commutator(H)
    D_nm = L_nm - L_coh

    norm_nm = la.norm(D_nm, 'fro')
    assert np.isclose(norm_sdcr, norm_nm)


def test_percentile_and_validation():
    # Run benchmark
    result = run_locked_qubit_benchmark(eta_sym=1.0)

    # Check that all required metrics are in results["metrics"]
    metrics = result["metrics"]
    assert "percentile_fraction" in metrics
    assert "target_percentile" in metrics
    assert "coherence_auc_norm_matched" in metrics
    assert "coherence_auc_channel_permutation" in metrics
    assert "coherence_auc_eta0_baseline" in metrics
    assert "null_auc_distribution" in metrics

    # Verify values are sensible
    assert 0.0 <= metrics["percentile_fraction"] <= 1.0
    assert 0.0 <= metrics["target_percentile"] <= 100.0
    assert len(metrics["null_auc_distribution"]) == 100
