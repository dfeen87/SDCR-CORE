"""
SDCR CORE — Core Framework
=========================

Foundational components of the Symmetry-Driven Coherence Restoration (SDCR)
framework.

This package contains the minimal abstractions and utilities required to:
- define measurement-accessible observables
- model reduced dynamics in open systems
- apply symmetry-constrained geometric bias in a controlled, falsifiable way

The core layer is intentionally conservative:
- no domain-specific phenomenology
- no executable side effects on import
- no assumptions beyond what is explicitly modeled

Higher-level physical interpretations are implemented exclusively in
`sdcr_core.domains` and `sdcr_core.examples`.
"""

from .observables import *   # noqa: F401,F403
from .utils import *         # noqa: F401,F403

__all__ = []

# Explicitly re-export public symbols from submodules
for _module in (observables, utils):  # type: ignore[name-defined]
    try:
        __all__.extend(_module.__all__)  # type: ignore[attr-defined]
    except AttributeError:
        pass

