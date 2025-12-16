"""
SDCR CORE — Interferometry Domain
================================

This domain contains conservative interferometric models and demonstrations
used to explore symmetry-driven, measurement-accessible phase effects
within the SDCR framework.

Public API:
- InterferometerParameters
- geometric_phase_shift
- total_phase
- fringe_intensity
"""

from .models import (
    InterferometerParameters,
    geometric_phase_shift,
    total_phase,
    fringe_intensity,
)

__all__ = [
    "InterferometerParameters",
    "geometric_phase_shift",
    "total_phase",
    "fringe_intensity",
]

