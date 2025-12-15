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

The repository is organized to separate core SDCR logic from domain-specific representations and optional internal algebraic bookkeeping.

```text
sdcr-core/
│
├── README.md
├── LICENSE
│
├── core/
│   ├── __init__.py
│   ├── dynamics.py        # Open-system generators (Lindblad)
│   ├── symmetry.py        # Symmetry selectors Π_sym
│   ├── observables.py     # Coherence and phase extraction
│   ├── recovery.py        # Explicit recovery / null-limit logic
│   └── utils.py           # Shared helpers and validation
│
├── domains/
│   ├── interferometry/
│   │   ├── __init__.py
│   │   ├── model.py       # Interferometer phase models
│   │   ├── run.py         # Baseline vs SDCR comparison
│   │   └── plots.py       # Phase and visibility plots
│   │
│   └── neutrinos/
│       ├── __init__.py
│       ├── model.py       # Toy neutrino oscillation mapping
│       ├── run.py         # L/E scaling + SDCR offset
│       └── plots.py       # Phase residuals and null tests
│
├── algebra/
│   ├── __init__.py
│   ├── quaternionic.py    # Internal phase-channel bookkeeping
│   └── octonionic.py      # Optional non-associative organization
│
├── examples/
│   ├── lindblad_basic.py  # Minimal SDCR demonstration
│   ├── null_test.py       # Recovery-limit validation
│   └── parameter_sweep.py
│
├── tests/
│   ├── test_recovery.py
│   ├── test_symmetry.py
│   └── test_observables.py
│
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

This repository is under **active development** and reflects the first complete software realization of the SDCR framework.

The current focus is correctness, transparency, and alignment with the published theory.  
Interfaces, structure, and documentation may evolve as validation and feedback accumulate.

---

## License

This software is released under the **MIT License**, to encourage open scientific use, independent testing, and reproducibility.

---

## Citation

If you use this software in academic work, please cite:

Krüger, M., & Feeney, D. (2025). *Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures.* Zenodo. https://doi.org/10.5281/zenodo.17942413
