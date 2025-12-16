"""
SDCR CORE — Octonionic Algebra
=============================

Minimal octonion utilities for structured experimentation.

This implementation focuses on:
- deterministic multiplication
- explicit structure
- numerical safety

Octonions are represented as numpy arrays of shape (8,).
No assumptions are made about physical interpretation.

NOTE:
Octonion multiplication is non-associative by construction.
"""

from typing import Iterable
import numpy as np


def as_octonion(values: Iterable[float]) -> np.ndarray:
    """
    Convert iterable to an octonion array.
    """
    o = np.asarray(values, dtype=float)
    if o.shape != (8,):
        raise ValueError("Octonion must have exactly 8 components")
    return o


def octonion_conjugate(o: np.ndarray) -> np.ndarray:
    """
    Conjugate of an octonion.
    """
    o = as_octonion(o)
    return np.concatenate(([o[0]], -o[1:]))


def octonion_norm(o: np.ndarray) -> float:
    """
    Euclidean norm of an octonion.
    """
    o = as_octonion(o)
    return float(np.linalg.norm(o))


def octonion_normalize(o: np.ndarray) -> np.ndarray:
    """
    Normalize an octonion to unit norm.
    """
    o = as_octonion(o)
    n = octonion_norm(o)
    if n == 0.0:
        raise ZeroDivisionError("Cannot normalize zero octonion")
    return o / n


# Cayley–Dickson construction
def octonion_multiply(o1: np.ndarray, o2: np.ndarray) -> np.ndarray:
    """
    Multiply two octonions using the Cayley–Dickson construction.

    Octonions are treated as pairs of quaternions:
    o = (a, b)
    """
    o1 = as_octonion(o1)
    o2 = as_octonion(o2)

    a1, b1 = o1[:4], o1[4:]
    a2, b2 = o2[:4], o2[4:]

    from .quaternionic import (
        quaternion_multiply,
        quaternion_conjugate,
    )

    a = quaternion_multiply(a1, a2) - quaternion_multiply(
        quaternion_conjugate(b2), b1
    )
    b = quaternion_multiply(b2, a1) + quaternion_multiply(
        b1, quaternion_conjugate(a2)
    )

    return np.concatenate((a, b))

