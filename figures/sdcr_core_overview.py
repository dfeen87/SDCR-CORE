#!/usr/bin/env python3
"""
SDCR-CORE — Overview Figure
==========================

Generates a single, explanatory overview graphic summarizing the
Symmetry-Driven Coherence Restoration (SDCR) framework.

This script is intended for:
- Paper figures
- README / repository overview visuals
- Talks and presentations

It is deliberately NON-executable with respect to SDCR core logic.

This file:
- does NOT run SDCR solvers
- does NOT validate null tests
- does NOT expose tunable parameters
- does NOT replace executable visualizations

All quantitative validation lives in:
- core/
- domains/
- examples/
"""

from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

# ---------------------------------------------------------------------
# Jupyter / inline backend safety (harmless if unused)
# ---------------------------------------------------------------------
try:
    get_ipython().run_line_magic("matplotlib", "inline")
except Exception:
    pass

# ---------------------------------------------------------------------
# Figure layout configuration
# ---------------------------------------------------------------------
DPI = 180
FIGSIZE = (15, 8.5)

fig = plt.figure(figsize=FIGSIZE, dpi=DPI, facecolor="white")
gs = fig.add_gridspec(
    2,
    2,
    width_ratios=[1.2, 1.3],
    height_ratios=[1, 1],
    wspace=0.3,
    hspace=0.35,
)

ax_left = fig.add_subplot(gs[:, 0])
ax_top = fig.add_subplot(gs[0, 1])
ax_bot = fig.add_subplot(gs[1, 1])

# =====================================================================
# LEFT PANEL — Conceptual Overview
# =====================================================================
ax_left.axis("off")

# Title block
ax_left.text(
    0.0,
    1.0,
    "SDCR-CORE",
    fontsize=24,
    fontweight="bold",
    va="top",
    color="#2c3e50",
)
ax_left.text(
    0.0,
    0.94,
    "Symmetry-Driven Coherence Restoration",
    fontsize=16,
    va="top",
    color="#34495e",
)
ax_left.text(
    0.0,
    0.90,
    "Reference implementation for symmetry-selection effects in open quantum systems",
    fontsize=10.5,
    va="top",
    style="italic",
    color="#7f8c8d",
)

# Box styling
BOX = dict(
    boxstyle="round,pad=0.6",
    linewidth=1.2,
    edgecolor="#bdc3c7",
    facecolor="#f8f9fa",
)

# Core idea
core_text = (
    r"$\mathbf{Core\ Idea}$" + "\n\n"
    r"• Reduced dynamics: $\dot{\rho} = \mathcal{L}[\rho]$" + "\n"
    r"• Symmetry selector: $\Pi_{\mathrm{sym}}$ projects operator sectors" + "\n"
    r"• SDCR effect: suppresses incompatible decohering channels" + "\n"
    r"• Recovery limit: $\Pi_{\mathrm{sym}}\!\to\!0 \Rightarrow$ standard Lindblad"
)

ax_left.text(
    0.0,
    0.82,
    core_text,
    fontsize=11.5,
    va="top",
    bbox=BOX,
    linespacing=1.6,
)

# Observables
obs_text = (
    r"$\mathbf{Observables\ /\ Null\ Tests}$" + "\n\n"
    r"• Coherence decay rates $\Gamma(t)$" + "\n"
    r"• Bounded phase residuals $\Delta\varphi(t)$" + "\n"
    r"• Liouvillian spectral structure" + "\n"
    r"• Effects vanish in recovery limit"
)

ax_left.text(
    0.0,
    0.53,
    obs_text,
    fontsize=11.5,
    va="top",
    bbox=BOX,
    linespacing=1.6,
)

# Repo structure
struct_text = (
    r"$\mathbf{Repository\ Structure}$" + "\n\n"
    "sdcr_core/\n"
    "  ├── core/       (generators + observables)\n"
    "  ├── algebra/    (internal bookkeeping)\n"
    "  ├── domains/    (interferometry, neutrinos, ...)\n"
    "  └── examples/   (null tests, validation)"
)

ax_left.text(
    0.0,
    0.23,
    struct_text,
    fontsize=11,
    va="top",
    family="monospace",
    color="#2c3e50",
)

# =====================================================================
# RIGHT TOP — Coherence decay (illustrative)
# =====================================================================
t = np.linspace(0.0, 10.0, 500)

gamma_base = 0.35
gamma_sdcr = 0.22

coh_base = np.exp(-gamma_base * t)
coh_sdcr = np.exp(-gamma_sdcr * t) * (
    1.0 + 0.05 * np.sin(2 * np.pi * 0.35 * t) * np.exp(-0.15 * t)
)

ax_top.plot(
    t,
    coh_base,
    lw=3,
    color="#3498db",
    label="Standard decoherence (baseline)",
)
ax_top.plot(
    t,
    coh_sdcr,
    lw=3,
    ls="--",
    color="#27ae60",
    label="SDCR (symmetry-selected channels)",
)

ax_top.set_title(
    "Observation: Reduced Effective Decoherence",
    fontsize=13,
    fontweight="bold",
    pad=12,
)
ax_top.set_xlabel("time (arb. units)", fontsize=10)
ax_top.set_ylabel(r"coherence $|\rho_{01}|$", fontsize=10)
ax_top.grid(True, ls=":", alpha=0.6)
ax_top.legend(fontsize=9.5, frameon=True, shadow=True)

# =====================================================================
# RIGHT BOTTOM — Phase residuals (illustrative)
# =====================================================================
phase_sdcr = 0.08 * (1.0 - np.exp(-0.6 * t)) * np.exp(-0.05 * t)
phase_zero = np.zeros_like(t)

ax_bot.plot(
    t,
    phase_sdcr,
    lw=3,
    color="#e74c3c",
    label=r"$\Delta\varphi(t)$ (symmetry-induced)",
)
ax_bot.plot(
    t,
    phase_zero,
    lw=3,
    ls=":",
    color="#2c3e50",
    label=r"Recovery limit ($\Pi_{\mathrm{sym}}\to 0$)",
)

ax_bot.set_title(
    "Symmetry-Induced Phase Offsets",
    fontsize=13,
    fontweight="bold",
    pad=12,
)
ax_bot.set_xlabel("time (arb. units)", fontsize=10)
ax_bot.set_ylabel(r"phase residual $\Delta\varphi$", fontsize=10)
ax_bot.grid(True, ls=":", alpha=0.6)
ax_bot.legend(fontsize=9.5, frameon=True, shadow=True)

# =====================================================================
# Footer & save
# =====================================================================
fig.text(
    0.5,
    0.02,
    "SDCR-CORE overview figure — effects are parameter-controlled, "
    "falsifiable, and reduce to standard open-system dynamics in recovery limits.",
    ha="center",
    fontsize=10,
    style="italic",
    color="#7f8c8d",
)

OUTFILE = "sdcr_core_overview.png"
plt.savefig(OUTFILE, dpi=DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
plt.show()

print(f"Overview figure written to: {os.path.abspath(OUTFILE)}")
