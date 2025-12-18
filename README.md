# SDCR-CORE

**Symmetry-Driven Coherence Restoration — Reference Implementation**

A reference implementation for exploring symmetry-selection mechanisms in open quantum systems.
This software provides tools to model, compare, and validate SDCR effects within standard open-system quantum dynamics frameworks.

---

## White Paper

For the complete theoretical foundation, mathematical derivations, and phenomenological predictions, see:

**Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures**

> Krüger, M., & Feeney, D. (2025).  
> *Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures.*  
> Zenodo. [https://doi.org/10.5281/zenodo.17942413](https://doi.org/10.5281/zenodo.17942413)

---

## Conceptual Basis

**SDCR is not a new dynamical law.**  
It is a symmetry-selection mechanism acting on the reduced dynamics of open quantum systems.

Within standard formulations (e.g. Lindblad, Redfield), SDCR operates by:

- Identifying symmetry-aligned operator sectors
- Suppressing decohering channels incompatible with those symmetries
- Inducing small, systematic bounded phase corrections
- Explicitly recovering ordinary decoherence behavior when symmetry alignment is removed

All dynamics remain fully compatible with conventional open-system quantum theory.

---

## What This Software Does

This repository provides tools to:

- Define open quantum system dynamics using standard generators (Lindblad-type models)
- Apply explicit symmetry-selection operators Π<sub>sym</sub> to reduced dynamics
- Compare baseline decoherence against symmetry-aligned evolution
- Extract observable quantities such as:
  - coherence decay
  - bounded phase offsets
- Demonstrate the recovery limit, where SDCR effects vanish when symmetry alignment is disabled
- Generate explicit null tests suitable for independent verification

The implementation prioritizes **clarity, traceability, and falsifiability** over performance or optimization.

---

## What This Software Does Not Do

This project explicitly does **not**:

- Introduce new particles, interactions, or collapse mechanisms
- Modify the Schrödinger equation or violate global unitarity
- Claim performance improvements, speedups, or technological superiority
- Provide active quantum error correction or feedback control
- Serve as a general-purpose quantum simulator
- Make claims beyond those stated in the associated paper

Any algebraic structures (e.g. quaternionic or octonionic bookkeeping) are used strictly as internal organizational tools and are never interpreted as physical degrees of freedom.

---

## Repository Structure

The repository separates the core SDCR framework from domain-level demonstrations, examples, tests, and visualization utilities.

```
sdcr-core/
│
├── core/
│   ├── dynamics.py          # Open-system generators (Lindblad)
│   ├── symmetry.py          # Symmetry selectors Π_sym
│   ├── recovery.py          # Recovery / null-limit logic
│   ├── observables.py       # Coherence and phase extraction
│   └── utils.py             # Shared helpers
│
├── algebra/
│   ├── quaternionic.py      # Internal bookkeeping (non-physical)
│   └── octonionic.py        # Optional non-associative organization
│
├── domains/
│   └── interferometry/
│       ├── model.py         # Two-path interferometer mapping
│       ├── run.py           # Baseline vs SDCR vs recovery
│       └── plots.py         # Phase and visibility plots
│
├── examples/
│   ├── lindblad_basic.py    # Minimal SDCR demonstration
│   ├── null_test.py         # Explicit recovery / null test
│   └── visualize_sdcr.py    # Hardened, read-only visualization
│
├── scripts/
│   └── run_visualizer.py    # Single-entry launcher
│
├── notebooks/
│   └── sdcr_interferometry_overview.ipynb  # Read-only notebook overview
│
├── tests/
│   ├── test_recovery.py
│   ├── test_symmetry.py
│   ├── test_observables.py
│   └── test_interferometry_domain.py
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Visualization Philosophy

SDCR-CORE includes visual inspection tools, not interactive dashboards.

- Visualizations are **read-only**
- All quantum states, operators, time grids, and observables are explicitly validated
- No tunable parameters or sliders are exposed
- Baseline, SDCR-enabled, and recovery evolutions are always shown together

These tools are intended as figure-style companions to the theory, supporting inspection and reproducibility without expanding scope or interpretation.

---

## Running the Software

### Install dependencies

```bash
pip install -r requirements.txt
```

### Run core examples

```bash
python examples/lindblad_basic.py
python examples/null_test.py
```

### Run the interferometry domain demo

```bash
python -m domains.interferometry.run
```

### Run the hardened visualization (recommended)

Single command from repository root:

```bash
python scripts/run_visualizer.py
```

This launches the validated, read-only visualization showing:

- coherence decay (baseline vs SDCR vs recovery)
- bounded SDCR phase offset
- explicit recovery limit

---

## Reproducibility and Falsifiability

A core design principle of `sdcr-core` is **explicit falsifiability**.

Every SDCR effect implemented here:

- Depends on exposed control parameters
- Can be switched off to recover standard decoherence
- Produces predictions that vanish in the symmetry-free limit
- Can be tested against null results without ambiguity

The software is designed to make disagreement easy and rigorous, not to enforce a particular interpretation.

---

## Project Status

This repository represents the first stable software realization of the SDCR framework.

Development proceeds cautiously, with emphasis on:

- correctness
- transparency
- alignment with the published theory

Interfaces and internal structure may evolve incrementally as validated use cases emerge.

---

## License

This software is released under the **MIT License**, to encourage open scientific use, independent testing, and reproducibility.

---

## Citation

If you use this software in academic work, please cite:

> Krüger, M., & Feeney, D. (2025).  
> *Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures.*  
> Zenodo. [https://doi.org/10.5281/zenodo.17942413](https://doi.org/10.5281/zenodo.17942413)
