# sdcr_core/io/outputs.py

"""
Output Writer Module for SDCR-CORE v0.2.
Handles saving simulation results, spectra, and validation metrics to CSV and JSON formats.
"""

import os
import json
import numpy as np
import pandas as pd
from typing import Any, Dict

def write_all_outputs(result: Dict[str, Any], output_dir: str = "results") -> None:
    """
    Writes all simulation outputs to the designated output directory:
    - results/summary_metrics.json
    - results/trajectories.csv
    - results/liouvillian_spectrum.csv
    """
    os.makedirs(output_dir, exist_ok=True)

    # 1. Save summary_metrics.json
    metrics = result["metrics"]
    # Convert any lists/numpy arrays in metrics to JSON-serializable types
    serializable_metrics = {}
    for k, v in metrics.items():
        if isinstance(v, np.ndarray):
            serializable_metrics[k] = v.tolist()
        elif isinstance(v, (np.float32, np.float64)):
            serializable_metrics[k] = float(v)
        elif isinstance(v, (np.int32, np.int64)):
            serializable_metrics[k] = int(v)
        else:
            serializable_metrics[k] = v

    metrics_path = os.path.join(output_dir, "summary_metrics.json")
    with open(metrics_path, "w") as f:
        json.dump(serializable_metrics, f, indent=4)

    # 2. Save trajectories.csv
    times = result["times"]
    traj_protected = result["traj_protected"]
    traj_baseline = result["traj_baseline"]

    records = []
    for i, t in enumerate(times):
        rho_p = traj_protected[i]
        rho_b = traj_baseline[i]

        records.append({
            "time": float(t),
            "protected_rho00_real": float(rho_p[0, 0].real),
            "protected_rho00_imag": float(rho_p[0, 0].imag),
            "protected_rho01_real": float(rho_p[0, 1].real),
            "protected_rho01_imag": float(rho_p[0, 1].imag),
            "protected_rho10_real": float(rho_p[1, 0].real),
            "protected_rho10_imag": float(rho_p[1, 0].imag),
            "protected_rho11_real": float(rho_p[1, 1].real),
            "protected_rho11_imag": float(rho_p[1, 1].imag),
            "baseline_rho00_real": float(rho_b[0, 0].real),
            "baseline_rho00_imag": float(rho_b[0, 0].imag),
            "baseline_rho01_real": float(rho_b[0, 1].real),
            "baseline_rho01_imag": float(rho_b[0, 1].imag),
            "baseline_rho10_real": float(rho_b[1, 0].real),
            "baseline_rho10_imag": float(rho_b[1, 0].imag),
            "baseline_rho11_real": float(rho_b[1, 1].real),
            "baseline_rho11_imag": float(rho_b[1, 1].imag),
        })

    traj_df = pd.DataFrame(records)
    traj_path = os.path.join(output_dir, "trajectories.csv")
    traj_df.to_csv(traj_path, index=False)

    # 3. Save liouvillian_spectrum.csv
    spectra_df = result["spectra_df"]
    spectrum_path = os.path.join(output_dir, "liouvillian_spectrum.csv")
    spectra_df.to_csv(spectrum_path, index=False)

    # 4. Generate manifest.json if needed
    from sdcr_core.io.manifest import generate_manifest
    generate_manifest(output_dir)
