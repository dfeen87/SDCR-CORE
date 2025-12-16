"""
SDCR CORE — Neutrinos Domain
===========================

This domain provides conservative neutrino oscillation models with optional
SDCR-induced geometric phase bias applied to measurement-accessible
oscillation phases.

The implementation is intentionally limited to two-flavor vacuum
oscillations and does not introduce new particles or interactions.

Public API:
- NeutrinoOscillationParameters
- survival_probability
- appearance_probability
"""

from .models import (
    NeutrinoOscillationParameters,
    survival_probability,
    appearance_probability,
)

__all__ = [
    "NeutrinoOscillationParameters",
    "survival_probability",
    "appearance_probability",
]

