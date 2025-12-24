# examples/lindblad_basic.py
"""
Minimal SDCR demonstration using a 2-level Lindblad system.

This example shows:
1) Baseline decoherence
2) Symmetry-driven coherence restoration (SDCR)
3) Explicit recovery limit (SDCR disabled)

The goal is clarity and falsifiability, not performance.
"""

import numpy as np
import matplotlib.pyplot as plt

from sdcr_core.core.dynamics import solve_lindblad
from sdcr_core.core.symmetry import pauli_z_symmetry
from sdcr_core.core.recovery import build_selector, solve_with_recovery
from sdcr_core.core.observables import (
    coherence_01,
    phase_01,
    time_series,
)

# ----------------------------
# System definition
# ----------------------------

# Pauli matrices
sigma_x = np.array([[0, 1], [1, 0]], dtype=np.complex128)
sigma_z = np.array([[1, 0], [0, -1]], dtype=np.complex128)

# Hamiltonian (simple Rabi oscillation)
omega = 1.0
H = 0.5 * omega * sigma_x

# Lindblad operator: dephasing in z-basis
gamma = 0.4
L = np.sqrt(gamma) * sigma_z
L_ops = [L]

# Initial state: |+><+|
psi_plus = (1 / np.sqrt(2)) * np.array([1, 1], dtype=np.complex128)
rho0 = np.outer(psi_plus, np.conjugate(psi_plus))

# Time grid
t_span = (0.0, 10.0)
t_eval = np.linspace(t_span[0], t_span[1], 400)

# ----------------------------
# Baseline evolution
# ----------------------------

t_base, rhos_base = solve_lindblad(
    rho0=rho0,
    H=H,
    L_ops=L_ops,
    t_span=t_span,
    t_eval=t_eval,
)

# ----------------------------
# SDCR evolution (symmetry ON)
# ----------------------------

projector = pauli_z_symmetry(dim=2)
selector_sdcr = build_selector(projector=projector, enabled=True)

t_sdcr, rhos_sdcr = solve_with_recovery(
    rho0=rho0,
    H=H,
    L_ops=L_ops,
    t_span=t_span,
    t_eval=t_eval,
    selector=selector_sdcr,
)

# ----------------------------
# Recovery evolution (symmetry OFF)
# ----------------------------

selector_recovery = build_selector(projector=projector, enabled=False)

t_rec, rhos_rec = solve_with_recovery(
    rho0=rho0,
    H=H,
    L_ops=L_ops,
    t_span=t_span,
    t_eval=t_eval,
    selector=selector_recovery,
)

# ----------------------------
# Observables
# ----------------------------

coh_base = time_series(rhos_base, coherence_01)
coh_sdcr = time_series(rhos_sdcr, coherence_01)
coh_rec = time_series(rhos_rec, coherence_01)

phase_base = time_series(rhos_base, phase_01)
phase_sdcr = time_series(rhos_sdcr, phase_01)
phase_rec = time_series(rhos_rec, phase_01)

# ----------------------------
# Plots
# ----------------------------

plt.figure(figsize=(10, 4))

# Coherence
plt.subplot(1, 2, 1)
plt.plot(t_base, coh_base, label="Baseline", linewidth=2)
plt.plot(t_sdcr, coh_sdcr, label="SDCR (symmetry on)", linewidth=2)
plt.plot(t_rec, coh_rec, "--", label="Recovery (symmetry off)", linewidth=2)
plt.xlabel("Time")
plt.ylabel("|ρ₀₁|")
plt.title("Coherence")
plt.legend()
plt.grid(True, alpha=0.3)

# Phase
plt.subplot(1, 2, 2)
plt.plot(t_base, phase_base, label="Baseline", linewidth=2)
plt.plot(t_sdcr, phase_sdcr, label="SDCR (symmetry on)", linewidth=2)
plt.plot(t_rec, phase_rec, "--", label="Recovery (symmetry off)", linewidth=2)
plt.xlabel("Time")
plt.ylabel("arg(ρ₀₁)")
plt.title("Phase Proxy")
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.show()

# ----------------------------
# Console check (sanity)
# ----------------------------

print("Final coherence values:")
print(f"Baseline : {coh_base[-1]:.6f}")
print(f"SDCR     : {coh_sdcr[-1]:.6f}")
print(f"Recovery : {coh_rec[-1]:.6f}")
