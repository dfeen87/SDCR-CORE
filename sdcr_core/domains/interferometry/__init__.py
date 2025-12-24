"""
SDCR CORE — Interferometry Domain
================================

This domain contains conservative interferometric models and demonstrations
used to explore symmetry-driven, measurement-accessible phase effects
within the SDCR framework.

Public API:
- InterferometerParams
- build_interferometer_model
- default_initial_state
"""

from .models import (
    InterferometerParams,
    build_interferometer_model,
    default_initial_state,
)

__all__ = [
    "InterferometerParams",
    "build_interferometer_model",
    "default_initial_state",
]
