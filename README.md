# sdcr-core

## Overview

`sdcr-core` is a reference software implementation of **Symmetry-Driven Coherence Restoration (SDCR)** in open quantum systems.  
The repository provides a concrete, reproducible realization of the SDCR mechanism as developed in:

> **M. Krüger & D. Feeney**,  
> *Symmetry-Driven Coherence Restoration: Geometric Phase Control, Open-System Dynamics, and Phenomenological Signatures* (2025)

The purpose of this software is to translate the theoretical SDCR framework into an explicit computational form that can be inspected, tested, reproduced, and falsified using standard open-quantum-system models.

This project is intentionally conservative in scope and interpretation. It introduces **no new physics**, **no modified quantum dynamics**, and **no speculative extensions** beyond what is stated in the associated paper.

---

## Conceptual Basis

SDCR is not a new dynamical law.  
It is a **symmetry-selection mechanism** acting on the *reduced dynamics* of open quantum systems.

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
- Apply explicit **symmetry-selection operators** (Πₛᵧₘ) to reduced dynamics
- Compare baseline decoherence against symmetry-aligned evolution
- Extract observable quantities such as:
  - coherence decay rates
  - bounded phase offsets
  - Liouvillian spectral changes (where applicable)
- Demonstrate the **recovery limit**, where SDCR effects vanish when symmetry alignment is disabled
- Generate clear, parameter-controlled null tests suitable for independent verification

The implementation emphasizes clarity, traceability, and falsifiability over performance or optimization.

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

## Reproducibility and Falsifiability

A core design principle of `sdcr-core` is **explicit falsifiability**.

Every SDCR effect implemented here:
- Depends on clearly exposed control parameters
- Can be switched off to recover standard decoherence
- Produces predictions that vanish in the symmetry-free limit
- Can be tested against null results without ambiguity

The software is intended to make disagreement *easy and rigorous*, not to enforce a particular interpretation.

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

Krüger, M., & Feeney, D. (2025).
Symmetry-Driven Coherence Restoration: Geometric Phase Control,
Open-System Dynamics, and Phenomenological Signatures.

---

## Research

Symmetry-Driven Coherence Restoration:
Geometric Phase Control, Open-System Dynamics,
and Phenomenological Signatures

https://zenodo.org/records/17942413
