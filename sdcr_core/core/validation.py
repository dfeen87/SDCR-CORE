# sdcr_core/core/validation.py

"""
Validation Module for SDCR-CORE v0.2.
Computes deterministic validation metrics for standard density matrix trajectories.
"""

import numpy as np
import scipy.linalg as la
from typing import Any, Dict

def compute_trace_errors(trajectory: np.ndarray) -> float:
    """
    Computes max trace error across all times in a trajectory.
    |tr(rho(t)) - 1|
    """
    errors = [abs(np.trace(rho) - 1.0) for rho in trajectory]
    return float(np.max(errors))

def compute_hermiticity_errors(trajectory: np.ndarray) -> float:
    """
    Computes max Hermiticity error across all times in a trajectory.
    ||rho - rho^dag||_inf or np.max(np.abs(rho - rho.conj().T))
    """
    errors = [np.max(np.abs(rho - rho.conj().T)) for rho in trajectory]
    return float(np.max(errors))

def compute_minimum_eigenvalues(trajectory: np.ndarray) -> float:
    """
    Computes the minimum eigenvalue of rho(t) across all times to ensure positivity.
    """
    min_vals = []
    for rho in trajectory:
        # Since rho is Hermitian, we can use la.eigvalsh
        evals = la.eigvalsh(rho)
        min_vals.append(np.min(evals))
    return float(np.min(min_vals))

def compute_coherence_auc(times: np.ndarray, trajectory: np.ndarray) -> float:
    """
    Computes the Coherence AUC (Area Under Curve of |rho_01(t)|).
    """
    coherences = [abs(rho[0, 1]) for rho in trajectory]
    auc = np.trapezoid(coherences, times) if hasattr(np, 'trapezoid') else np.trapz(coherences, times)
    return float(auc)

def compute_all_validation_metrics(result: Dict[str, Any]) -> Dict[str, Any]:
    """
    Computes all validation metrics specified in v0.2.
    """
    times = result["times"]
    traj_protected = result["traj_protected"]
    traj_baseline = result["traj_baseline"]

    # 1. Trace and Hermiticity Errors
    max_trace_err = compute_trace_errors(traj_protected)
    max_herm_err = compute_hermiticity_errors(traj_protected)
    min_eig_val = compute_minimum_eigenvalues(traj_protected)

    # 2. Coherence AUCs
    auc_protected = compute_coherence_auc(times, traj_protected)
    auc_baseline = compute_coherence_auc(times, traj_baseline)

    # 3. eta=0 recovery error
    # Compute the trajectory with eta_sym=0 from the result, compare to traj_baseline
    recovery_error = float(np.max(np.abs(traj_protected - traj_baseline))) if result["eta_sym"] == 0.0 else 0.0
    # Note: the prompt says "eta=0 recovery error" is the error when eta=0.
    # To make it deterministic and general, we can run a separate check or return the exact discrepancy
    # if eta_sym is set to 0.0, or we can explicitly compute an eta_sym=0 trajectory and compare it to baseline.
    # Let's explicitly compare an evolved eta=0 trajectory against the baseline trajectory.
    # Since baseline IS eta=0, the difference between an eta=0 trajectory and baseline is analytically 0.
    # Let's compute a trajectory with eta_sym=0.0 and verify it perfectly matches the baseline trajectory.
    from sdcr_core.core.gksl_locked_qubit import assemble_liouvillian, evolve_state
    L_eta0 = assemble_liouvillian(
        omega=result["omega"],
        eta_sym=0.0,
        gamma_z=result["gamma_z"],
        gamma_x=result["gamma_x"],
        gamma_y=result["gamma_y"]
    )
    traj_eta0 = evolve_state(result["rho0"], L_eta0, times)
    eta0_recovery_error = float(np.max(np.abs(traj_eta0 - traj_baseline)))

    # 4. Null AUC distribution & target percentile
    # To construct a deterministic, reproducible null AUC distribution, we define a pseudo-random seed-based
    # generator or generate a deterministic set of random Hamiltonians/dissipators representing "disorder".
    # Let's construct a deterministic null distribution by varying Hamiltonian/Lindblad noise configurations
    # using a fixed random seed. Let's run N = 100 trials.
    # In each trial, we generate random weights for x and y channels (representing disordered symmetry breaking),
    # construct the resulting Liouvillian, compute the trajectory, and get its AUC.
    rng = np.random.default_rng(seed=42)
    null_aucs = []
    num_trials = 100

    for _ in range(num_trials):
        # random channel weights from [0, 1]
        w_x = rng.uniform(0.0, 1.0)
        w_y = rng.uniform(0.0, 1.0)

        # Assemble disordered Liouvillian
        from sdcr_core.core.gksl_locked_qubit import SIGMA_X, SIGMA_Y, SIGMA_Z, vectorized_commutator, vectorized_dissipator
        H = (result["omega"] / 2.0) * SIGMA_Z
        L_coh = vectorized_commutator(H)
        D_z = vectorized_dissipator(SIGMA_Z)
        D_x = vectorized_dissipator(SIGMA_X)
        D_y = vectorized_dissipator(SIGMA_Y)

        L_null = L_coh + result["gamma_z"] * D_z + w_x * result["gamma_x"] * D_x + w_y * result["gamma_y"] * D_y
        traj_null = evolve_state(result["rho0"], L_null, times)
        auc_null = compute_coherence_auc(times, traj_null)
        null_aucs.append(auc_null)

    null_aucs = np.array(null_aucs)

    # Compute target percentile
    # Where does the protected AUC fall within the null distribution?
    # Percentile = (fraction of null AUCs <= protected AUC) * 100
    target_percentile = float(np.sum(null_aucs <= auc_protected) / len(null_aucs) * 100.0)

    return {
        "max_trace_error": max_trace_err,
        "max_hermiticity_error": max_herm_err,
        "min_eigenvalue_rho": min_eig_val,
        "eta0_recovery_error": eta0_recovery_error,
        "coherence_auc_protected": auc_protected,
        "coherence_auc_baseline": auc_baseline,
        "null_auc_distribution": null_aucs.tolist(),
        "target_percentile": target_percentile
    }
