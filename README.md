# SDCR-CORE
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/dfeen87/SDCR-CORE/actions/workflows/ci.yml/badge.svg)](https://github.com/dfeen87/SDCR-CORE/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CITATION.cff)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

**Symmetry-Driven Coherence Restoration — Reference Implementation**

A reference implementation for exploring symmetry-selection mechanisms in open quantum systems.
This software provides tools to model, compare, and validate SDCR effects within standard open-system quantum dynamics frameworks.

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

## Repository Structure

The repository is organized as follows:

```
sdcr-core/
  pyproject.toml
  README.md
  sdcr_core/
    __init__.py
    core/
      __init__.py
      gksl_locked_qubit.py
      symmetry_selector.py
      null_battery.py
      liouvillian_spectrum.py
      validation.py
    io/
      __init__.py
      outputs.py
      manifest.py
    run.py
  results/
  figures/
  notebooks/
```

- `sdcr_core/` is the **package namespace**
- `core/` holds the physics + benchmark logic
- `io/` handles saving CSVs, JSON, ZIP, manifest
- `run.py` becomes the one-click entrypoint
- `results/` and `figures/` are output folders
- `notebooks/` holds the Colab notebook

---

## Installation

To install the package in editable mode:

```bash
pip install -e .
```

---

## Running the Benchmark

You can run the benchmark using the single entrypoint command:

```bash
python -m sdcr_core.run
```

---

## License

MIT License
