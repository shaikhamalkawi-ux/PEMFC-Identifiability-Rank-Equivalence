"""Core formulas for the PEMFC identifiability/rank audit."""

from __future__ import annotations

import numpy as np


def water_vapor_pressure(T: float) -> float:
    """Saturation-water-pressure expression used in the audited benchmark code."""
    d = T - 273.15
    return 10.0 ** (29.5e-3*d - 91.8e-6*d*d + 14.4e-8*d**3 - 2.18)


def oxygen_partial_pressure_airfed(
    I: np.ndarray,
    A_cm2: float,
    T: float,
    P_c_bar: float,
    RH_c: float = 1.0,
) -> np.ndarray:
    """Common air-fed cathode law audited in the manuscript."""
    I = np.asarray(I, dtype=float)
    p_h2o = water_vapor_pressure(T)
    gamma = 0.291 / (T**0.832 * A_cm2)
    return (P_c_bar - RH_c*p_h2o) / (
        (1.0 + 0.79/0.21) * np.exp(gamma*I)
    )


def oxygen_concentration_airfed(
    I: np.ndarray,
    A_cm2: float,
    T: float,
    P_c_bar: float,
    RH_c: float = 1.0,
) -> np.ndarray:
    p_o2 = oxygen_partial_pressure_airfed(I, A_cm2, T, P_c_bar, RH_c)
    return p_o2 / 5.08e6 * np.exp(498.0/T)


def jacobian_airfed(
    I: np.ndarray,
    T: float,
    A_cm2: float,
    l_um: float,
    Jmax_Acm2: float,
    Ncell: int,
    lam: float,
    P_c_bar: float,
) -> np.ndarray:
    """Analytic seven-column voltage Jacobian used for the 250 W audit.

    Column order:
    (xi1, xi2, xi3, xi4, lambda, beta, Rc).
    """
    I = np.asarray(I, dtype=float)
    J = I / A_cm2
    C = oxygen_concentration_airfed(I, A_cm2, T, P_c_bar)

    eT = np.exp(4.18*(T - 303.0)/T)
    num = 181.6 * (1.0 + 0.03*J + 0.062*(T/303.0)**2 * J**2.5)
    l_cm = l_um * 1e-4
    K = (num / eT) * (l_cm / A_cm2)
    D = lam - 0.634 - 3.0*J

    return np.column_stack([
        Ncell*np.ones_like(I),
        Ncell*T*np.ones_like(I),
        Ncell*T*np.log(C),
        Ncell*T*np.log(I),
        Ncell*I*K/D**2,
        Ncell*np.log(1.0 - J/Jmax_Acm2),
        -Ncell*I,
    ])


def normalized_svd(J: np.ndarray) -> np.ndarray:
    """Singular values after unit-2-norm scaling of each Jacobian column."""
    norms = np.linalg.norm(J, axis=0, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Jacobian contains a zero column")
    Z = J / norms
    return np.linalg.svd(Z, compute_uv=False)


def numerical_rank_from_singular_values(s: np.ndarray, shape: tuple[int, int]) -> int:
    """NumPy/LAPACK-style matrix-rank criterion applied to supplied singular values."""
    tol = s[0] * max(shape) * np.finfo(float).eps
    return int(np.sum(s > tol))


def delta_interval(
    xi1: float,
    xi2: float,
    T0: float,
    L1: float = -1.19969,
    U1: float = -0.8532,
    L2: float = 0.001,
    U2: float = 0.005,
) -> tuple[float, float]:
    """Feasible fixed-temperature equivalence interval for delta."""
    lo = max((xi1-U1)/T0, L2-xi2)
    hi = min((xi1-L1)/T0, U2-xi2)
    return float(lo), float(hi)


def transformed_pair(xi1: float, xi2: float, T0: float, delta: float) -> tuple[float, float]:
    return xi1 - T0*delta, xi2 + delta


def fixed_temperature_combination(xi1: float, xi2: float, T0: float) -> float:
    return xi1 + T0*xi2
