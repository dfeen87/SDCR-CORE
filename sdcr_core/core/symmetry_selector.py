# sdcr_core/core/symmetry_selector.py

"""
Symmetry Selector Module for SDCR-CORE v0.2.
Implements the v0.2 recovery parameter and suppression weights for incompatible channels.
"""

def get_suppression_weights(eta_sym: float) -> tuple[float, float]:
    """
    Returns the suppression weights for the incompatible channels (x and y).

    eta_sym = 0 -> full baseline (no suppression, weight = 1)
    eta_sym = 1 -> incompatible channels suppressed (weight = 0)

    Suppression rule:
    D_x_weight = 1 - eta_sym
    D_y_weight = 1 - eta_sym
    """
    if not (0.0 <= eta_sym <= 1.0):
        # Allow clipping or raising, but let's be flexible and/or precise.
        # Let's ensure it's kept strictly within bounds or handled purely.
        pass

    D_x_weight = 1.0 - eta_sym
    D_y_weight = 1.0 - eta_sym

    return float(D_x_weight), float(D_y_weight)
