"""
SDCR CORE — Algebra
==================

Foundational algebraic structures used throughout SDCR CORE.

This package provides minimal, implementation-safe algebraic utilities
(quaternionic and octonionic) intended for representing symmetry,
phase structure, and higher-dimensional geometric relationships.

No physical interpretation is enforced at this level. All algebraic
objects are treated as mathematical primitives only.

Higher-level meaning is introduced exclusively in the core logic
or in domain-specific phenomenology modules.
"""

from .quaternionic import (
    as_quaternion,
    quaternion_conjugate,
    quaternion_norm,
    quaternion_normalize,
    quaternion_multiply,
)

from .octonionic import (
    as_octonion,
    octonion_conjugate,
    octonion_norm,
    octonion_normalize,
    octonion_multiply,
)

__all__ = [
    # Quaternionic
    "as_quaternion",
    "quaternion_conjugate",
    "quaternion_norm",
    "quaternion_normalize",
    "quaternion_multiply",

    # Octonionic
    "as_octonion",
    "octonion_conjugate",
    "octonion_norm",
    "octonion_normalize",
    "octonion_multiply",
]

