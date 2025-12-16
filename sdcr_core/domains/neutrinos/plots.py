"""
SDCR CORE — Neutrinos Plots
==========================

Visualization utilities for neutrino oscillation phenomenology with optional SDCR bias.
"""

import matplotlib.pyplot as plt


def plot_probability_vs_energy(energies, probs, title, ylabel):
    """
    Plot probability as a function of neutrino energy.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(energies, probs)
    plt.xlabel("Neutrino Energy E (GeV)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_probability_vs_baseline(baselines, probs, title, ylabel):
    """
    Plot probability as a function of baseline length.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(baselines, probs)
    plt.xlabel("Baseline L (km)")
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()


def plot_delta_probability(xvals, deltas, xlabel, title, ylabel="ΔP (SDCR − baseline)"):
    """
    Plot SDCR-induced deviation in probability.
    """
    plt.figure(figsize=(8, 5))
    plt.plot(xvals, deltas)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.grid(True)
    plt.tight_layout()
    plt.show()

