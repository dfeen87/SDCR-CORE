# sdcr_core/run.py

"""
SDCR-CORE v0.2 Main Execution Entrypoint.
Integrates all components of the GKSL locked qubit benchmark, null battery simulation,
integrity validation, figure plotting, ZIP packaging, and SHA-256 manifest generation.
"""

from sdcr_core.core.gksl_locked_qubit import run_locked_qubit_benchmark
from sdcr_core.io.outputs import write_all_outputs, LOCK_STATEMENT

def main():
    print("=" * 80)
    print("SDCR-CORE v0.2 — STAGE 3/3 FULL PIPELINE INTEGRATION")
    print("=" * 80)
    print(f"🔒 {LOCK_STATEMENT}\n")

    print("Step 1: Running GKSL Locked Qubit Benchmark & Null Battery Simulation...")
    # Run the benchmark with default parameters (eta_sym=1.0)
    result = run_locked_qubit_benchmark(eta_sym=1.0)

    print("Step 2: Generating all reproducibility CSVs, JSON, figures, and ZIP packages...")
    write_all_outputs(result)

    # Extract metrics for console reporting
    metrics = result["metrics"]
    print("\n" + "=" * 50)
    print("DETERMINISTIC VERIFICATION & AUDIT RESULTS")
    print("=" * 50)
    print(f"• Max Trace Error:         {metrics['max_trace_error']:.2e}")
    print(f"• Max Hermiticity Error:   {metrics['max_hermiticity_error']:.2e}")
    print(f"• Min Eigenvalue rho(t):   {metrics['min_eigenvalue_rho']:.2e}")
    print(f"• eta=0 Recovery Error:    {metrics['eta0_recovery_error']:.2e}")
    print(f"• Coherence AUC Protected: {metrics['coherence_auc_protected']:.4f}")
    print(f"• Coherence AUC Baseline:  {metrics['coherence_auc_baseline']:.4f}")
    print(f"• Coherence AUC Norm-Matched Null: {metrics['coherence_auc_norm_matched']:.4f}")
    print(f"• Coherence AUC Permutation Null:  {metrics['coherence_auc_channel_permutation']:.4f}")
    print(f"• Null Battery Percentile: {metrics['target_percentile']:.1f}% (fraction: {metrics['percentile_fraction']:.2f})")
    print("=" * 50)

    print("\nAll reproducibility artifacts have been generated successfully:")
    print("  - results/summary_metrics.json")
    print("  - results/trajectories.csv")
    print("  - results/liouvillian_spectrum.csv")
    print("  - results/null_battery.csv")
    print("  - results/SHA256_MANIFEST.json")
    print("  - figures/coherence_trajectories.png")
    print("  - figures/liouvillian_spectrum_vs_eta.png")
    print("  - figures/null_battery_auc.png")
    print("  - figures/claim_state_dashboard.png")
    print("  - SDCR_CORE_V02_RESULT_PACKAGE.zip")
    print("\nPipeline execution complete. Ready for peer review.\n")

if __name__ == "__main__":
    main()
