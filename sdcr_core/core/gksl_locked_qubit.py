# sdcr_core/core/gksl_locked_qubit.py

"""
GKSL Locked Qubit Module for SDCR-CORE v0.2.
Implements the core open-system dynamics of a qubit under symmetry protection.
"""

import numpy as np
import scipy.linalg as la
from typing import Any, Dict, Optional

from sdcr_core.core.symmetry_selector import get_suppression_weights

# Standard Pauli matrices
SIGMA_X = np.array([[0.0, 1.0], [1.0, 0.0]], dtype=complex)
SIGMA_Y = np.array([[0.0, -1j], [1j, 0.0]], dtype=complex)
SIGMA_Z = np.array([[1.0, 0.0], [0.0, -1.0]], dtype=complex)

def vectorized_commutator(H: np.ndarray) -> np.ndarray:
    r"""
    Computes the 4x4 row-major vectorized commutator term -i [H, rho].
    -i [H, rho] = -i * (H @ rho - rho @ H)
    Row-major vectorized:
    -1j * (H \otimes I - I \otimes H^T)
    """
    I = np.eye(2, dtype=complex)
    return -1j * (np.kron(H, I) - np.kron(I, H.T))

def vectorized_dissipator(L: np.ndarray) -> np.ndarray:
    r"""
    Computes the 4x4 row-major vectorized Lindblad superoperator D(L) for a 2x2 operator L.
    D(rho) = L @ rho @ L^dag - 0.5 * {L^dag @ L, rho}
    Row-major vectorized:
    L \otimes L^* - 0.5 * ( (L^dag @ L) \otimes I + I \otimes (L^dag @ L)^T )
    """
    I = np.eye(2, dtype=complex)
    L_dag = L.conj().T
    term1 = np.kron(L, L.conj())
    term2 = -0.5 * (np.kron(L_dag @ L, I) + np.kron(I, (L_dag @ L).T))
    return term1 + term2

def assemble_liouvillian(
    omega: float,
    eta_sym: float,
    gamma_z: float = 0.1,
    gamma_x: float = 0.1,
    gamma_y: float = 0.1
) -> np.ndarray:
    r"""
    Assembles the 4x4 Liouvillian matrix.
    L = -i(H \otimes I - I \otimes H^T) + gamma_z * D_z + (1-eta_sym)*gamma_x*D_x + (1-eta_sym)*gamma_y*D_y
    """
    H = (omega / 2.0) * SIGMA_Z
    L_coh = vectorized_commutator(H)
    D_z = vectorized_dissipator(SIGMA_Z)
    D_x = vectorized_dissipator(SIGMA_X)
    D_y = vectorized_dissipator(SIGMA_Y)

    # Get weights from symmetry selector
    w_x, w_y = get_suppression_weights(eta_sym)

    L = L_coh + gamma_z * D_z + w_x * gamma_x * D_x + w_y * gamma_y * D_y
    return L

def evolve_state(rho0: np.ndarray, L: np.ndarray, times: np.ndarray) -> np.ndarray:
    """
    Evolves the initial density matrix rho0 under the Liouvillian L for given times.
    rho(t) = vec^-1( exp(L * t) * vec(rho0) )
    Returns a trajectory array of shape (len(times), 2, 2).
    """
    v0 = rho0.flatten('C')
    trajectory = []
    for t in times:
        vt = la.expm(L * t) @ v0
        rhot = vt.reshape((2, 2), order='C')
        trajectory.append(rhot)
    return np.array(trajectory)

def run_locked_qubit_benchmark(
    eta_sym: float = 1.0,
    times: Optional[np.ndarray] = None,
    omega: float = 1.0,
    gamma_z: float = 0.1,
    gamma_x: float = 0.1,
    gamma_y: float = 0.1
) -> Dict[str, Any]:
    """
    Runs the locked qubit benchmark and returns the complete set of simulation results,
    including protected and baseline trajectories, spectra, and validation metrics.
    """
    if times is None:
        times = np.linspace(0.0, 10.0, 101)

    rho0 = np.array([[1.0, 0.0], [0.0, 0.0]], dtype=complex) # |0><0|

    # Assemble Liouvillians
    L_protected = assemble_liouvillian(omega, eta_sym, gamma_z, gamma_x, gamma_y)
    L_baseline = assemble_liouvillian(omega, 0.0, gamma_z, gamma_x, gamma_y)

    # Evolve trajectories
    traj_protected = evolve_state(rho0, L_protected, times)
    traj_baseline = evolve_state(rho0, L_baseline, times)

    # Build results structure
    result = {
        "eta_sym": eta_sym,
        "times": times,
        "omega": omega,
        "gamma_z": gamma_z,
        "gamma_x": gamma_x,
        "gamma_y": gamma_y,
        "rho0": rho0,
        "L_protected": L_protected,
        "L_baseline": L_baseline,
        "traj_protected": traj_protected,
        "traj_baseline": traj_baseline,
    }

    # Import validation and spectra dynamically or execute them here to fill results.
    # We will invoke the audit and validation modules and populate the result dict before returning.
    from sdcr_core.core.liouvillian_spectrum import audit_liouvillian_spectra
    from sdcr_core.core.validation import compute_all_validation_metrics

    spectra_df = audit_liouvillian_spectra(result)
    result["spectra_df"] = spectra_df

    metrics = compute_all_validation_metrics(result)
    result["metrics"] = metrics

    return result
