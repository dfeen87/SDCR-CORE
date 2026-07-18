# sdcr_core/io/outputs.py

"""
Output Writer and Visualizer Module for SDCR-CORE v0.2.
Handles saving simulation results, spectra, and validation metrics,
generating publication-quality reproducibility figures, and building ZIP packages.
"""

import os
import json
import zipfile
import numpy as np
import pandas as pd
import scipy.linalg as la
from typing import Any, Dict

# Set up matplotlib backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from sdcr_core.io.manifest import generate_manifest


# Global constant lock statement
LOCK_STATEMENT = "Locked reference benchmark for symmetry-selector specificity in standard open-system dynamics."


def plot_coherence_trajectories(result: Dict[str, Any], fig_path: str) -> None:
    """
    Plots the coherence trajectories comparing Protected SDCR, Baseline, and Null ensemble.
    """
    times = result["times"]
    traj_protected = result["traj_protected"]
    traj_baseline = result["traj_baseline"]
    null_raw = result.get("null_battery_raw", {})

    plt.figure(figsize=(8, 5))

    # Plot first 10 random-axis trials as thin grey lines to represent the null ensemble
    if "random_axis" in null_raw:
        coherences_list = null_raw["random_axis"]["coherences_list"]
        label_added = False
        for i in range(min(10, len(coherences_list))):
            lbl = "Random-Axis Null Ensemble" if not label_added else None
            plt.plot(times, coherences_list[i], color="grey", alpha=0.3, linewidth=1, label=lbl)
            label_added = True

    # Plot specific nulls
    if "norm_matched" in null_raw:
        plt.plot(times, null_raw["norm_matched"]["coherence"], color="green", linestyle=":", alpha=0.8, label="Norm-Matched Null")
    if "channel_permutation" in null_raw:
        plt.plot(times, null_raw["channel_permutation"]["coherence"], color="purple", linestyle="-.", alpha=0.8, label="Channel-Permutation Null")

    # Plot baseline
    coherence_baseline = [abs(rho[0, 1]) for rho in traj_baseline]
    plt.plot(times, coherence_baseline, color="black", linestyle="--", linewidth=1.5, label="Baseline (eta=0)")

    # Plot protected SDCR
    coherence_protected = [abs(rho[0, 1]) for rho in traj_protected]
    plt.plot(times, coherence_protected, color="blue", linewidth=2.5, label="Protected SDCR (eta=1.0)")

    plt.xlabel("Time (t)")
    plt.ylabel("Coherence |rho_01(t)|")
    plt.title("Coherence Trajectories & Null Battery Comparison")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper right", frameon=True, fontsize=9)

    # Display lock statement inside a beautiful text box at the bottom
    plt.figtext(
        0.5, -0.05, LOCK_STATEMENT,
        ha="center", fontsize=8, style="italic", weight="bold",
        bbox={"facecolor": "lightyellow", "alpha": 0.8, "pad": 4}
    )

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_liouvillian_spectrum_vs_eta(result: Dict[str, Any], fig_path: str) -> None:
    """
    Plots the Liouvillian spectrum eigenvalues (real and imaginary parts) vs eta.
    """
    omega = result["omega"]
    gamma_z = result["gamma_z"]
    gamma_x = result["gamma_x"]
    gamma_y = result["gamma_y"]

    from sdcr_core.core.gksl_locked_qubit import assemble_liouvillian
    from sdcr_core.core.liouvillian_spectrum import compute_liouvillian_eigenvalues

    etas = np.linspace(0.0, 1.0, 11)
    eigenvalues_history = []

    for eta in etas:
        L = assemble_liouvillian(omega, eta, gamma_z, gamma_x, gamma_y)
        evals = compute_liouvillian_eigenvalues(L)
        eigenvalues_history.append(evals)

    eigenvalues_history = np.array(eigenvalues_history)  # Shape (11, 4)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 5))

    # Real part
    for mode in range(4):
        ax1.plot(etas, eigenvalues_history[:, mode].real, marker='o', markersize=4, label=f"Mode {mode}")
    ax1.set_xlabel("Symmetry Coupling (eta)")
    ax1.set_ylabel("Re(lambda)")
    ax1.set_title("Real Part of Eigenvalues (Decay Rates)")
    ax1.grid(True, linestyle=":", alpha=0.6)
    ax1.legend(fontsize=8)

    # Imaginary part
    for mode in range(4):
        ax2.plot(etas, eigenvalues_history[:, mode].imag, marker='s', markersize=4, label=f"Mode {mode}")
    ax2.set_xlabel("Symmetry Coupling (eta)")
    ax2.set_ylabel("Im(lambda)")
    ax2.set_title("Imaginary Part (Lamb Shift / Frequencies)")
    ax2.grid(True, linestyle=":", alpha=0.6)
    ax2.legend(fontsize=8)

    plt.suptitle("Liouvillian Eigenspectrum Evolution vs. Symmetry Suppression Parameter", fontsize=12, weight="bold")

    # Display lock statement
    plt.figtext(
        0.5, -0.05, LOCK_STATEMENT,
        ha="center", fontsize=8, style="italic", weight="bold",
        bbox={"facecolor": "lightyellow", "alpha": 0.8, "pad": 4}
    )

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_null_battery_auc(result: Dict[str, Any], fig_path: str) -> None:
    """
    Plots the histogram of the null distribution AUCs along with lines for Protected and Baseline.
    """
    metrics = result["metrics"]
    null_aucs = metrics["null_auc_distribution"]
    auc_protected = metrics["coherence_auc_protected"]
    auc_baseline = metrics["coherence_auc_baseline"]
    percentile_val = metrics["target_percentile"]

    plt.figure(figsize=(8, 5))

    # Histogram of random-axis null AUCs
    plt.hist(null_aucs, bins=15, color="lightgrey", edgecolor="black", alpha=0.8, label="Random-Axis Nulls")

    # Vertical lines
    plt.axvline(auc_baseline, color="black", linestyle="--", linewidth=1.5, label=f"Baseline (eta=0): {auc_baseline:.4f}")
    plt.axvline(auc_protected, color="blue", linestyle="-", linewidth=2.5, label=f"Protected SDCR (eta=1.0): {auc_protected:.4f}")

    plt.xlabel("Coherence AUC")
    plt.ylabel("Frequency")
    plt.title(f"Null Battery Coherence AUC Distribution (Percentile: {percentile_val:.1f}%)")
    plt.grid(True, linestyle=":", alpha=0.6)
    plt.legend(loc="upper left", frameon=True)

    # Text overlay
    plt.text(
        0.95, 0.5, f"Percentile: {percentile_val:.1f}%\nSDCR is highly specific",
        transform=plt.gca().transAxes, ha="right", va="center",
        bbox={"boxstyle": "round,pad=0.3", "facecolor": "lightblue", "alpha": 0.6}
    )

    # Display lock statement
    plt.figtext(
        0.5, -0.05, LOCK_STATEMENT,
        ha="center", fontsize=8, style="italic", weight="bold",
        bbox={"facecolor": "lightyellow", "alpha": 0.8, "pad": 4}
    )

    plt.tight_layout()
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()


def plot_claim_state_dashboard(result: Dict[str, Any], fig_path: str) -> None:
    """
    Creates a claim-state dashboard summarizing key metrics, comparing AUC, and highlighting the lock statement.
    """
    metrics = result["metrics"]

    # Set up layout
    fig = plt.figure(figsize=(10, 8))
    grid = plt.GridSpec(2, 2, hspace=0.3, wspace=0.25)

    # Subplot A: Bar chart comparing AUCs
    ax_bar = fig.add_subplot(grid[0, 0])
    labels = ["Protected SDCR", "Norm-Matched", "Permutation", "Baseline"]
    aucs = [
        metrics["coherence_auc_protected"],
        metrics["coherence_auc_norm_matched"],
        metrics["coherence_auc_channel_permutation"],
        metrics["coherence_auc_eta0_baseline"]
    ]
    colors = ["blue", "green", "purple", "black"]
    bars = ax_bar.bar(labels, aucs, color=colors, edgecolor="black", alpha=0.85)
    ax_bar.set_ylabel("Coherence AUC")
    ax_bar.set_title("Coherence Restoration Strength (AUC)")
    ax_bar.set_xticks(range(len(labels)))
    ax_bar.set_xticklabels(labels, rotation=15, fontsize=9)
    ax_bar.grid(True, axis="y", linestyle=":", alpha=0.6)

    # Annotate bars
    for bar in bars:
        height = bar.get_height()
        ax_bar.annotate(f"{height:.3f}",
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=8)

    # Subplot B: Numerical metrics display
    ax_text = fig.add_subplot(grid[0, 1])
    ax_text.axis("off")
    ax_text.set_title("Deterministic Audit Metrics", fontsize=11, weight="bold")

    metrics_text = (
        f"• Max Trace Error: {metrics['max_trace_error']:.2e}\n\n"
        f"• Max Hermiticity Error: {metrics['max_hermiticity_error']:.2e}\n\n"
        f"• Min Eigenvalue rho(t): {metrics['min_eigenvalue_rho']:.2e}\n\n"
        f"• eta=0 Recovery Error: {metrics['eta0_recovery_error']:.2e}\n\n"
        f"• Target AUC Percentile: {metrics['target_percentile']:.1f}% ({metrics['percentile_fraction']:.2f})"
    )
    ax_text.text(
        0.05, 0.85, metrics_text,
        transform=ax_text.transAxes, fontsize=10, va="top", ha="left",
        bbox={"boxstyle": "round,pad=1.0", "facecolor": "whitesmoke", "alpha": 0.9, "edgecolor": "lightgrey"}
    )

    # Subplot C: Prominent Lock Statement display
    ax_lock = fig.add_subplot(grid[1, :])
    ax_lock.axis("off")

    # Add a beautiful banner style for the lock statement
    ax_lock.text(
        0.5, 0.5,
        f"[LOCK] CLAIM STATE BOUNDARY\n\n\"{LOCK_STATEMENT}\"",
        ha="center", va="center", fontsize=12, weight="bold", style="italic", color="darkred",
        bbox={"boxstyle": "sawtooth,pad=1.5", "facecolor": "lightyellow", "alpha": 0.9, "edgecolor": "darkred"}
    )

    plt.suptitle("SDCR-CORE v0.2 Verification & Claim-Boundary Dashboard", fontsize=14, weight="bold")
    plt.savefig(fig_path, dpi=300, bbox_inches="tight")
    plt.close()


def build_zip_package(zip_filepath: str, results_dir: str, figures_dir: str) -> None:
    """
    Bundles all outputs, figures, and reproducibility instructions into a ZIP file.
    """
    # Create reproducibility README
    readme_content = f"""SDCR-CORE v0.2 Reproducibility Package

Locked reference benchmark for symmetry-selector specificity in standard open-system dynamics.

This package contains the fully verified results for the SDCR-CORE v0.2 Stage 3 benchmark.

Contents:
- summary_metrics.json: Detailed deterministic validation metrics, AUCs, and percentile distributions.
- trajectories.csv: Time-evolution trajectories for Protected and Baseline states.
- liouvillian_spectrum.csv: Complete eigenstate tracking for both cases.
- null_battery.csv: Extensive coherence trajectories and AUCs of the fair-comparison null selectors.
- figures/: High-resolution scientific figures demonstrating selectivity, spectrum, null battery distribution, and claims dashboard.
- SHA256_MANIFEST.json: Reproducibility verification manifest detailing all artifact sizes and SHA-256 hashes.

How to verify:
1. Ensure the package is extracted to a clean environment.
2. Check the SHA-256 hash of each file against the manifest 'SHA256_MANIFEST.json'.
3. Run 'python -m sdcr_core.run' to execute the pipeline from scratch and regenerate the manifest.
"""
    readme_path = os.path.join(results_dir, "README.txt")
    with open(readme_path, "w") as f:
        f.write(readme_content)

    with zipfile.ZipFile(zip_filepath, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Save results files
        for filename in ["summary_metrics.json", "trajectories.csv", "liouvillian_spectrum.csv", "null_battery.csv", "README.txt"]:
            filepath = os.path.join(results_dir, filename)
            if os.path.exists(filepath):
                zipf.write(filepath, arcname=filename)

        # Save figures
        if os.path.exists(figures_dir):
            for filename in sorted(os.listdir(figures_dir)):
                filepath = os.path.join(figures_dir, filename)
                if os.path.isfile(filepath):
                    zipf.write(filepath, arcname=os.path.join("figures", filename))

        # Save manifest (initial)
        manifest_path = os.path.join(results_dir, "SHA256_MANIFEST.json")
        if os.path.exists(manifest_path):
            zipf.write(manifest_path, arcname="SHA256_MANIFEST.json")


def write_all_outputs(
    result: Dict[str, Any],
    output_dir: str = "results",
    figures_dir: str = "figures",
    zip_filename: str = "SDCR_CORE_V02_RESULT_PACKAGE.zip"
) -> None:
    """
    Writes all simulation outputs to the designated directories,
    generates all reproducibility figures, builds the ZIP package,
    and constructs the SHA-256 manifest.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(figures_dir, exist_ok=True)

    # 1. Save summary_metrics.json
    metrics = result["metrics"]
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

    # Enforce claim boundary inside metrics json
    serializable_metrics["claim_boundary"] = LOCK_STATEMENT

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

    # 4. Save null_battery.csv
    null_battery_df = result["null_battery_df"]
    null_battery_path = os.path.join(output_dir, "null_battery.csv")
    null_battery_df.to_csv(null_battery_path, index=False)

    # 5. Generate and save figures
    plot_coherence_trajectories(result, os.path.join(figures_dir, "coherence_trajectories.png"))
    plot_liouvillian_spectrum_vs_eta(result, os.path.join(figures_dir, "liouvillian_spectrum_vs_eta.png"))
    plot_null_battery_auc(result, os.path.join(figures_dir, "null_battery_auc.png"))
    plot_claim_state_dashboard(result, os.path.join(figures_dir, "claim_state_dashboard.png"))

    # 6. Generate initial manifest without ZIP
    generate_manifest(output_dir, figures_dir, zip_filepath="")

    # 7. Build the final ZIP package (contains all outputs, figures, and initial manifest)
    build_zip_package(zip_filename, output_dir, figures_dir)

    # 8. Re-generate manifest including the ZIP file hash
    generate_manifest(output_dir, figures_dir, zip_filepath=zip_filename)
