# sdcr_core/core/null_battery.py

"""
Null Battery Module for SDCR-CORE v0.2.
Implements the fair comparison null selectors to remove symmetry-selector specificity
while maintaining equivalent dissipative strength.
"""

import numpy as np
import scipy.linalg as la
import pandas as pd
from typing import Dict, Any, List, Tuple

from sdcr_core.core.gksl_locked_qubit import (
    SIGMA_X, SIGMA_Y, SIGMA_Z,
    vectorized_commutator, vectorized_dissipator,
    evolve_state, assemble_liouvillian
)
from sdcr_core.core.validation import compute_coherence_auc


def get_random_unitary(seed: int) -> np.ndarray:
    """
    Generates a deterministic 2x2 unitary matrix using QR decomposition
    from a pseudo-random seed.
    """
    rng = np.random.default_rng(seed)
    # Generate a random complex 2x2 matrix
    X = rng.normal(size=(2, 2)) + 1j * rng.normal(size=(2, 2))
    # QR decomposition
    Q, R = la.qr(X)
    # Make Q unique by scaling columns by the phase of the diagonal of R
    d = np.diagonal(R)
    ph = d / np.abs(d)
    Q = Q @ np.diag(ph)
    return Q


def get_norm_matched_null_liouvillian(
    omega: float,
    eta_sym: float,
    gamma_z: float,
    gamma_x: float,
    gamma_y: float
) -> np.ndarray:
    """
    Computes the norm-matched null Liouvillian.
    The dissipator part has the exact same Frobenius norm as SDCR,
    but we scale the baseline dissipator to match it, removing symmetry structure.
    """
    H = (omega / 2.0) * SIGMA_Z
    L_coh = vectorized_commutator(H)
    D_z = vectorized_dissipator(SIGMA_Z)
    D_x = vectorized_dissipator(SIGMA_X)
    D_y = vectorized_dissipator(SIGMA_Y)

    # SDCR dissipator
    D_sdcr = gamma_z * D_z + (1.0 - eta_sym) * gamma_x * D_x + (1.0 - eta_sym) * gamma_y * D_y
    # Baseline dissipator
    D_baseline = gamma_z * D_z + gamma_x * D_x + gamma_y * D_y

    norm_sdcr = la.norm(D_sdcr, 'fro')
    norm_baseline = la.norm(D_baseline, 'fro')

    scale = norm_sdcr / norm_baseline if norm_baseline > 0 else 1.0
    D_null = scale * D_baseline

    return L_coh + D_null


def get_random_axis_liouvillian(
    omega: float,
    eta_sym: float,
    gamma_z: float,
    gamma_x: float,
    gamma_y: float,
    seed: int
) -> np.ndarray:
    """
    Computes a random-axis null Liouvillian.
    Applies a random Pauli-axis rotation to the system's dissipators,
    breaking the alignment between the Hamiltonian axis and the symmetry axis.
    """
    U = get_random_unitary(seed)

    # Rotate the Pauli matrices
    s_z_rot = U @ SIGMA_Z @ U.conj().T
    s_x_rot = U @ SIGMA_X @ U.conj().T
    s_y_rot = U @ SIGMA_Y @ U.conj().T

    # Fixed Hamiltonian (alignment is broken because the operators are rotated)
    H = (omega / 2.0) * SIGMA_Z
    L_coh = vectorized_commutator(H)

    D_z_rot = vectorized_dissipator(s_z_rot)
    D_x_rot = vectorized_dissipator(s_x_rot)
    D_y_rot = vectorized_dissipator(s_y_rot)

    # Use the same suppression rates as SDCR
    L = L_coh + gamma_z * D_z_rot + (1.0 - eta_sym) * gamma_x * D_x_rot + (1.0 - eta_sym) * gamma_y * D_y_rot
    return L


def get_channel_permutation_liouvillian(
    omega: float,
    eta_sym: float,
    gamma_z: float,
    gamma_x: float,
    gamma_y: float
) -> np.ndarray:
    """
    Computes a channel-permutation null Liouvillian.
    Swaps the roles of channels so that the symmetry-aligned channel is suppressed
    and an incompatible channel is protected.
    """
    H = (omega / 2.0) * SIGMA_Z
    L_coh = vectorized_commutator(H)
    D_z = vectorized_dissipator(SIGMA_Z)
    D_x = vectorized_dissipator(SIGMA_X)
    D_y = vectorized_dissipator(SIGMA_Y)

    # Permute weights: suppress z (aligned channel) and protect x (incompatible channel)
    w_z = 1.0 - eta_sym
    w_x = 1.0
    w_y = 1.0 - eta_sym

    return L_coh + w_z * gamma_z * D_z + w_x * gamma_x * D_x + w_y * gamma_y * D_y


def get_eta0_baseline_liouvillian(
    omega: float,
    gamma_z: float,
    gamma_x: float,
    gamma_y: float
) -> np.ndarray:
    """
    Computes the eta=0 recovery baseline Liouvillian (standard GKSL with no suppression).
    """
    return assemble_liouvillian(omega, 0.0, gamma_z, gamma_x, gamma_y)


def run_null_battery(
    result: Dict[str, Any],
    num_random_axis_trials: int = 100
) -> Tuple[pd.DataFrame, Dict[str, Any]]:
    """
    Executes the full null battery simulation.
    Each null selector produces: Liouvillian, trajectory, coherence curve, and AUC.
    Returns:
        - A pandas DataFrame containing the detailed coherence curves and AUCs.
        - A dictionary of raw simulation outputs for each selector (useful for plotting).
    """
    omega = result["omega"]
    eta_sym = result["eta_sym"]
    gamma_z = result["gamma_z"]
    gamma_x = result["gamma_x"]
    gamma_y = result["gamma_y"]
    times = result["times"]
    rho0 = result["rho0"]

    records = []
    raw_outputs = {}

    # Define the core null configurations
    null_configs = {
        "norm_matched": get_norm_matched_null_liouvillian(omega, eta_sym, gamma_z, gamma_x, gamma_y),
        "channel_permutation": get_channel_permutation_liouvillian(omega, eta_sym, gamma_z, gamma_x, gamma_y),
        "eta0_baseline": get_eta0_baseline_liouvillian(omega, gamma_z, gamma_x, gamma_y)
    }

    # Compute for the fixed configurations
    for name, L in null_configs.items():
        traj = evolve_state(rho0, L, times)
        coherences = [float(abs(rho[0, 1])) for rho in traj]
        auc = compute_coherence_auc(times, traj)

        raw_outputs[name] = {
            "L": L,
            "trajectory": traj,
            "coherence": coherences,
            "auc": auc
        }

        for idx, t in enumerate(times):
            records.append({
                "selector_type": name,
                "time": float(t),
                "coherence": coherences[idx],
                "auc": auc
            })

    # Run random-axis trials
    random_axis_aucs = []
    random_axis_trajs = []
    random_axis_coherences_list = []

    for trial_idx in range(num_random_axis_trials):
        L_rand = get_random_axis_liouvillian(omega, eta_sym, gamma_z, gamma_x, gamma_y, seed=trial_idx)
        traj_rand = evolve_state(rho0, L_rand, times)
        coherences_rand = [float(abs(rho[0, 1])) for rho in traj_rand]
        auc_rand = compute_coherence_auc(times, traj_rand)

        random_axis_aucs.append(auc_rand)
        random_axis_trajs.append(traj_rand)
        random_axis_coherences_list.append(coherences_rand)

        selector_name = f"random_axis_trial_{trial_idx}"
        for idx, t in enumerate(times):
            records.append({
                "selector_type": selector_name,
                "time": float(t),
                "coherence": coherences_rand[idx],
                "auc": auc_rand
            })

    raw_outputs["random_axis"] = {
        "aucs": random_axis_aucs,
        "trajectories": random_axis_trajs,
        "coherences_list": random_axis_coherences_list
    }

    df = pd.DataFrame(records)
    return df, raw_outputs
