# sdcr_core/core/liouvillian_spectrum.py

"""
Liouvillian Spectrum Module for SDCR-CORE v0.2.
Computes eigenvalues of the Liouvillian and performs audits for CSV exporting.
"""

import numpy as np
import scipy.linalg as la
import pandas as pd
from typing import Any, Dict

def compute_liouvillian_eigenvalues(L: np.ndarray) -> np.ndarray:
    """
    Computes eigenvalues of the 4x4 Liouvillian matrix.
    Returns them sorted complex-wise (by real part first, then imaginary part, or using np.sort_complex)
    to ensure full determinism.
    """
    evals = la.eigvals(L)
    # To be perfectly deterministic, sort them. Let's use np.sort_complex.
    return np.sort_complex(evals)

def audit_liouvillian_spectra(result: Dict[str, Any]) -> pd.DataFrame:
    """
    Computes and audits the eigenvalues of the baseline and protected Liouvillians.
    Returns a pandas DataFrame with fields:
    case, eta, mode, Re(lambda), Im(lambda)
    """
    records = []

    # 1. Protected Case
    L_protected = result["L_protected"]
    eta_protected = result["eta_sym"]
    evals_protected = compute_liouvillian_eigenvalues(L_protected)

    for mode_idx, val in enumerate(evals_protected):
        records.append({
            "case": "protected",
            "eta": float(eta_protected),
            "mode": int(mode_idx),
            "Re(lambda)": float(val.real),
            "Im(lambda)": float(val.imag)
        })

    # 2. Baseline Case
    L_baseline = result["L_baseline"]
    evals_baseline = compute_liouvillian_eigenvalues(L_baseline)

    for mode_idx, val in enumerate(evals_baseline):
        records.append({
            "case": "baseline",
            "eta": 0.0,
            "mode": int(mode_idx),
            "Re(lambda)": float(val.real),
            "Im(lambda)": float(val.imag)
        })

    df = pd.DataFrame(records)
    return df
