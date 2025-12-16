"""
SDCR CORE — Quaternionic Algebra
================================

Minimal, production-safe quaternion utilities.

This module provides basic quaternion operations used for representing
rotations, phase structure, and low-dimensional symmetry behavior.
No physical interpretation is enforced at this level.

Quaternions are represented as numpy arrays of shape (4,):
[q0, q1, q2, q3] = scalar + vector components
"""

from typing import Iterable
import numpy as np


def as_quaternion(values: Iterable[float]) -> np.ndarray:
    """
    Convert iterable to a quaternion array.
    """
    q = np.asarray(values, dtype=float)
    if q.shape != (4,):
        raise ValueError("Quaternion must have exactly 4 components")
    return q


def quaternion_conjugate(q: np.ndarray) -> np.ndarray:
    """
    Conjugate of a quaternion.
    """
    q = as_quaternion(q)
    return np.array([q[0], -q[1], -q[2], -q[3]])


def quaternion_norm(q: np.ndarray) -> float:
    """
    Euclidean norm of a quaternion.
    """
    q = as_quaternion(q)
    return float(np.linalg.norm(q))


def quaternion_normalize(q: np.ndarray) -> np.ndarray:
    """
    Normalize a quaternion to unit norm.
    """
    q = as_quaternion(q)
    n = quaternion_norm(q)
    if n == 0.0:
        raise ZeroDivisionError("Cannot normalize zero quaternion")
    return q / n


def quaternion_multiply(q1: np.ndarray, q2: np.ndarray) -> np.ndarray:
    """
    Hamilton product of two quaternions.
    """
    q1 = as_quaternion(q1)
    q2 = as_quaternion(q2)

    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2

    return np.array([
        w1*w2 - x1*x2 - y1*y2 - z1*z2,
        w1*x2 + x1*w2 + y1*z2 - z1*y2,
        w1*y2 - x1*z2 + y1*w2 + z1*x2,
        w1*z2 + x1*y2 - y1*x2 + z1*w2
    ])

