"""
SDCR CORE — Utilities
====================

General-purpose utility functions used across SDCR CORE.

This module intentionally avoids domain-specific logic and instead provides:
- numerical safety helpers
- validation utilities
- lightweight formatting helpers

These utilities are designed to support reproducible scientific workflows
without introducing hidden behavior or side effects.
"""

from typing import Iterable, Optional
import numpy as np


# ---------------------------------------------------------------------
# Numerical safety utilities
# ---------------------------------------------------------------------

def safe_float(value, default: float = 0.0) -> float:
    """
    Safely cast a value to float.

    Parameters
    ----------
    value : any
        Value to cast.
    default : float
        Value returned if casting fails.

    Returns
    -------
    float
    """
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def is_finite(value: float) -> bool:
    """
    Check whether a value is finite (not NaN or infinite).
    """
    return np.isfinite(value)


def assert_finite(value: float, name: Optional[str] = None) -> None:
    """
    Assert that a numerical value is finite.

    Raises
    ------
    ValueError
        If the value is NaN or infinite.
    """
    if not is_finite(value):
        label = f"'{name}'" if name else "value"
        raise ValueError(f"{label} must be finite, got {value}")


# ---------------------------------------------------------------------
# Parameter validation helpers
# ---------------------------------------------------------------------

def assert_positive(value: float, name: Optional[str] = None) -> None:
    """
    Assert that a value is strictly positive.
    """
    if value <= 0.0:
        label = f"'{name}'" if name else "value"
        raise ValueError(f"{label} must be positive, got {value}")


def assert_non_negative(value: float, name: Optional[str] = None) -> None:
    """
    Assert that a value is non-negative.
    """
    if value < 0.0:
        label = f"'{name}'" if name else "value"
        raise ValueError(f"{label} must be non-negative, got {value}")


def assert_in_range(
    value: float,
    min_value: float,
    max_value: float,
    name: Optional[str] = None
) -> None:
    """
    Assert that a value lies within a closed interval [min_value, max_value].
    """
    if not (min_value <= value <= max_value):
        label = f"'{name}'" if name else "value"
        raise ValueError(
            f"{label} must be in range [{min_value}, {max_value}], got {value}"
        )


# ---------------------------------------------------------------------
# Lightweight aggregation helpers
# ---------------------------------------------------------------------

def mean(values: Iterable[float]) -> float:
    """
    Compute the mean of an iterable, returning NaN for empty input.
    """
    values = list(values)
    if not values:
        return float("nan")
    return float(np.mean(values))


def std(values: Iterable[float]) -> float:
    """
    Compute the standard deviation of an iterable, returning NaN for empty input.
    """
    values = list(values)
    if not values:
        return float("nan")
    return float(np.std(values))


# ---------------------------------------------------------------------
# Formatting helpers
# ---------------------------------------------------------------------

def format_scientific(value: float, precision: int = 3) -> str:
    """
    Format a number in scientific notation with fixed precision.
    """
    return f"{value:.{precision}e}"


def format_seconds(value: float, precision: int = 3) -> str:
    """
    Format a time value in seconds with units.
    """
    return f"{value:.{precision}f} s"

