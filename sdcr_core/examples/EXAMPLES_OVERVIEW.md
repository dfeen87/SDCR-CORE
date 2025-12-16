# SDCR CORE — Examples Overview

This directory contains runnable reference examples demonstrating how
Symmetry-Driven Coherence Restoration (SDCR) manifests in reduced dynamics,
from generic baselines to concrete, falsifiable physical applications.

The examples are intentionally ordered from framework fundamentals to
domain-specific interpretations.

## Example Files

- **`lindblad_basic.py`**  
  Baseline open-quantum-system dynamics using a Lindblad formulation.
  Serves as a reference for standard decoherence behavior without SDCR effects.

- **`null_test.py`**  
  Framework-level null test demonstrating the absence of spurious effects
  when SDCR modulation is disabled.

- **`parameter_sweep.py`**  
  Shared infrastructure for sweeping small SDCR modulation parameters (ε)
  and visualizing their impact on observable quantities.

- **`neutron_lifetime_null_test.py`**  
  Domain-specific falsification case for the neutron lifetime problem.
  Demonstrates that bottle and beam lifetimes coincide when SDCR effects
  are explicitly disabled (ε = 0).

- **`neutron_lifetime_sdcr.py`**  
  Implements Appendix D: a geometric SDCR interpretation of the neutron
  lifetime discrepancy. Reproduces the observed bottle–beam offset as a
  symmetry-dependent measurement bias without introducing new particles
  or decay channels.

## Usage Notes

All examples are designed to run standalone from this directory and rely
only on the SDCR CORE framework. Together, they form a complete progression:
baseline → null → parameterized response → falsifiable physical exemplar.
