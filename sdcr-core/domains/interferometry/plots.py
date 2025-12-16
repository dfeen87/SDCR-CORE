"""
SDCR CORE — Interferometry Plots
===============================

Visualization utilities for interferometric SDCR effects.
"""

import matplotlib.pyplot as plt
import numpy as np


def plot_phase_vs_epsilon(eps_values, phase_values):
    """
    Plot SDCR-induced phase shift as a function of ε.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(eps_values, phase_values)
    plt.xlabel("SDCR modulation parameter ε")
    plt.ylabel("Geometric phase shift (rad)")
    plt.title("SDCR-Induced Interferometric Phase Shift")
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_fringe_pattern(phases, intensities):
    """
    Plot interferometric fringe intensity pattern.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(phases, intensities)
    plt.xlabel("Phase (rad)")
    plt.ylabel("Normalized intensity")
    plt.title("Interferometric Fringe Pattern")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

