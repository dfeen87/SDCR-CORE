# SDCR-CORE

**Symmetry-Driven Coherence Restoration: Core Implementation**

A reference implementation for exploring symmetry-selection mechanisms in open quantum systems.  
This software provides tools to model, compare, and validate SDCR effects within standard open-system quantum dynamics frameworks.

---

## White Paper

For the complete theoretical foundation, mathematical derivations, and phenomenological predictions, see:

**Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures**

Krüger, M., & Feeney, D. (2025).  
*Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures.*  
Zenodo. https://doi.org/10.5281/zenodo.17942413

---

## Conceptual Basis

SDCR is **not a new dynamical law**.  
It is a **symmetry-selection mechanism** acting on the reduced dynamics of open quantum systems.

Within standard formulations (e.g. Lindblad, Redfield), SDCR operates by:

- Identifying symmetry-aligned operator sectors
- Suppressing dominant decohering channels incompatible with those symmetries
- Inducing small, systematic phase corrections while preserving standard scaling relations
- Explicitly recovering ordinary decoherence behavior when symmetry alignment is removed

All dynamics remain fully compatible with conventional open-system quantum theory.

---

## What This Software Does

This repository provides tools to:

- Define open quantum system dynamics using standard generators (initially Lindblad-type models)
- Apply explicit symmetry-selection operators (Πₛᵧₘ) to reduced dynamics
- Compare baseline decoherence against symmetry-aligned evolution
- Extract observable quantities such as:
  - coherence decay rates
  - bounded phase offsets
  - Liouvillian spectral changes (where applicable)
- Demonstrate the recovery limit, where SDCR effects vanish when symmetry alignment is disabled
- Generate clear, parameter-controlled null tests suitable for independent verification

The implementation emphasizes **clarity, traceability, and falsifiability** over performance or optimization.

---

## What This Software Does *Not* Do

This project explicitly does **not**:

- Introduce new particles, interactions, or collapse mechanisms
- Modify the Schrödinger equation or violate unitarity at the global level
- Claim performance improvements, speedups, or technological superiority
- Provide active quantum error correction or feedback control
- Serve as a quantum simulator beyond the SDCR scope
- Make claims beyond those stated in the associated paper

Any algebraic structures (e.g. quaternionic or octonionic bookkeeping) are used **strictly as internal organizational tools** and are never interpreted as physical dimensions or degrees of freedom.

---

## Repository Structure

The repository is organized to separate the core SDCR framework from domain-specific phenomenology, examples, and optional internal algebraic bookkeeping.

```text
sdcr-core/
│
├── sdcr_core/
│   ├── __init__.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── observables.py     # Coherence and phase extraction
│   │   └── utils.py           # Shared helpers and validation
│   │
│   ├── algebra/
│   │   ├── __init__.py
│   │   ├── quaternionic.py    # Internal phase-channel bookkeeping
│   │   └── octonionic.py      # Optional non-associative organization
│   │
│   ├── domains/
│   │   ├── __init__.py
│   │   │
│   │   ├── interferometry/
│   │   │   ├── __init__.py
│   │   │   ├── models.py      # Interferometer phase models
│   │   │   ├── runs.py        # Baseline vs SDCR comparison
│   │   │   └── plots.py       # Phase and visibility plots
│   │   │
│   │   └── neutrinos/
│   │       ├── __init__.py
│   │       ├── models.py      # Two-flavor oscillation models
│   │       ├── runs.py        # L/E scaling with SDCR offset
│   │       └── plots.py       # Phase residuals and null tests
│   │
│   ├── examples/
│   │   ├── __init__.py
│   │   ├── lindblad_basic.py
│   │   ├── null_test.py
│   │   ├── neutron_lifetime_sdcr.py
│   │   └── parameter_sweep.py
│   │
│   └── tests/
│       ├── __init__.py
│       └── test_core_sanity.py
│
├── README.md
├── LICENSE
└── requirements.txt
```

---

## Reproducibility and Falsifiability

A core design principle of `sdcr-core` is **explicit falsifiability**.

Every SDCR effect implemented here:

- Depends on clearly exposed control parameters
- Can be switched off to recover standard decoherence
- Produces predictions that vanish in the symmetry-free limit
- Can be tested against null results without ambiguity

The software is intended to make disagreement **easy and rigorous**, not to enforce a particular interpretation.

---

## Project Status

This repository represents the first stable software realization of the SDCR framework and will continue to evolve incrementally as validation and feedback accumulate.

The current focus is correctness, transparency, and alignment with the published theory. Interfaces and internal structure may evolve cautiously as new validated use cases emerge.

---

## Running the Software

All examples and domain demonstrations are designed to run directly from the repository root using Python's module execution.

First, install dependencies:

```bash
pip install -r requirements.txt
```

Then run examples:

```bash
python -m sdcr_core.examples.lindblad_basic
python -m sdcr_core.examples.null_test
python -m sdcr_core.domains.interferometry.runs
```

---

## License

This software is released under the **MIT License**, to encourage open scientific use, independent testing, and reproducibility.

---

## Citation

If you use this software in academic work, please cite:

Krüger, M., & Feeney, D. (2025). *Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures.* Zenodo. https://doi.org/10.5281/zenodo.17942413
