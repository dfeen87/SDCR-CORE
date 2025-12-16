"""
SDCR CORE — Domains
==================

Domain-specific phenomenology modules for the SDCR framework.

Each domain provides:
- conservative physical models
- optional SDCR-induced geometric bias at the level of
  measurement-accessible observables
- runnable demonstrations and visualizations

Domains are intentionally independent and do not modify
core SDCR abstractions.

Available domains:
- interferometry
- neutrinos
"""

__all__ = [
    "interferometry",
    "neutrinos",
]
