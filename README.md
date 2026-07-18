# SDCR-CORE
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/dfeen87/SDCR-CORE/actions/workflows/ci.yml/badge.svg)](https://github.com/dfeen87/SDCR-CORE/actions/workflows/ci.yml)
[![Version](https://img.shields.io/badge/version-0.2.0-informational.svg)](CITATION.cff)
[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)

---

## **Conceptual Overview**
SDCR is a **symmetry‑selection mechanism**, not a modification of quantum mechanics.  
Within standard open‑system theory, SDCR:

- identifies symmetry‑aligned operator sectors  
- suppresses incompatible dissipative channels by a tunable parameter η  
- preserves baseline Lindblad behavior when η = 0  
- produces bounded, symmetry‑aligned coherence effects  
- enables comparison against fair null selectors  

All dynamics remain fully compatible with conventional GKSL formulations.

Learn more:  
- SDCR mechanism  
- GKSL locked qubit model  
- Symmetry selector logic  

---

## **Benchmark Architecture**
SDCR‑CORE v0.2 implements the full locked reproducibility pipeline:

### **1. GKSL Locked Qubit Engine**
- Pauli matrices  
- ω/2 σ_z Hamiltonian  
- baseline + incompatible dissipators  
- row‑major vectorized Lindblad superoperators  
- deterministic trajectory solver via `scipy.linalg.expm`  

Module: **`sdcr_core/core/gksl_locked_qubit.py`**

### **2. Symmetry Selector**
Implements η‑controlled suppression of incompatible channels.

Module: **`sdcr_core/core/symmetry_selector.py`**

### **3. Null Battery (Stage 3)**
Includes:
- norm‑matched null  
- random‑axis nulls  
- channel‑permutation null  
- η = 0 recovery baseline  

Module: **`sdcr_core/core/null_battery.py`**

### **4. Liouvillian Spectral Audit**
Extracts eigenvalues for:
- baseline  
- η‑sweep  
- target SDCR  
- null selectors  

Module: **`sdcr_core/core/liouvillian_spectrum.py`**

### **5. Validation Metrics**
Reports:
- trace error  
- Hermiticity error  
- positivity  
- η = 0 recovery error  
- coherence AUC  
- null AUC distribution  
- percentile  

Module: **`sdcr_core/core/validation.py`**

### **6. Output + Manifest System**
Generates:
- CSVs  
- JSON summary  
- SHA256 manifest  
- reproducibility ZIP package  

Modules:  
- `sdcr_core/io/outputs.py`  
- `sdcr_core/io/manifest.py`  
- `sdcr_core/io/package.py`  

### **7. Reproducibility Figures**
- coherence trajectories  
- Liouvillian spectrum vs η  
- null AUC histogram  
- claim‑state dashboard  

Folder: **`figures/`**

### **8. One‑Click Colab Notebook**
Public reproducibility path.

Folder: **`notebooks/`**

---

## **Repository Structure**
```
sdcr-core/
  pyproject.toml
  README.md
  sdcr_core/
    core/
      gksl_locked_qubit.py
      symmetry_selector.py
      null_battery.py
      liouvillian_spectrum.py
      validation.py
    io/
      outputs.py
      manifest.py
      package.py
    run.py
  results/
  figures/
  notebooks/
```

---

## **Installation**
Editable mode:

```bash
pip install -e .
```

---

## **Running the Full v0.2 Benchmark**
One‑click reproducibility pipeline:

```bash
python -m sdcr_core.run
```

This produces:

- `results/summary_metrics.json`  
- `results/trajectories.csv`  
- `results/liouvillian_spectrum.csv`  
- `results/null_battery.csv`  
- `results/SHA256_MANIFEST.json`  
- `SDCR_CORE_V02_RESULT_PACKAGE.zip`  
- all figures in `figures/`  

---

## **License**
MIT License

---

## **Professional AI Assistance Acknowledgment**

> This work was completed with assistance from **Microsoft Copilot** and **Google Jules**, both of which contributed equally to drafting, structuring, and refining the software and documentation. Their support was used strictly for productivity, clarity, and organization; all technical decisions, implementations, and scientific interpretations remain my own.
