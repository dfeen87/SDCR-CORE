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
    Computes all validation metrics specified in v0.2, including the null battery.
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

    # 4. Run Null Battery to get null distribution and baseline selectors
    from sdcr_core.core.null_battery import run_null_battery
    # Run full 100 trials
    null_battery_df, null_battery_raw = run_null_battery(result, num_random_axis_trials=100)

    # Store in result dictionary so it's accessible for saving/plotting later
    result["null_battery_df"] = null_battery_df
    result["null_battery_raw"] = null_battery_raw

    # Extract null distribution AUCs (from the random-axis trials)
    random_axis_aucs = null_battery_raw["random_axis"]["aucs"]

    # Other null selector AUCs
    auc_norm_matched = null_battery_raw["norm_matched"]["auc"]
    auc_permutation = null_battery_raw["channel_permutation"]["auc"]
    auc_eta0_baseline = null_battery_raw["eta0_baseline"]["auc"]

    # Compute target percentile
    # Percentile fraction: p = #{null AUC < target AUC} / N
    N = len(random_axis_aucs)
    less_than_target_count = sum(1 for auc in random_axis_aucs if auc < auc_protected)
    percentile_fraction = float(less_than_target_count / N)
    target_percentile_pct = percentile_fraction * 100.0

    return {
        "max_trace_error": max_trace_err,
        "max_hermiticity_error": max_herm_err,
        "min_eigenvalue_rho": min_eig_val,
        "eta0_recovery_error": eta0_recovery_error,
        "coherence_auc_protected": auc_protected,
        "coherence_auc_baseline": auc_baseline,
        "coherence_auc_norm_matched": auc_norm_matched,
        "coherence_auc_channel_permutation": auc_permutation,
        "coherence_auc_eta0_baseline": auc_eta0_baseline,
        "null_auc_distribution": [float(a) for a in random_axis_aucs],
        "percentile_fraction": percentile_fraction,
        "target_percentile": target_percentile_pct
    }
