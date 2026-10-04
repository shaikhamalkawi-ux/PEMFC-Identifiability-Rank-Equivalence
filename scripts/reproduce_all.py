"""Reproduce the manuscript's exact-invariance and Jacobian-rank diagnostics."""

from __future__ import annotations

import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.benchmark_data import BALLARD_I, BALLARD_T, BALLARD_V, W250, W250_META
from src.pemfc_identifiability import (
    delta_interval,
    fixed_temperature_combination,
    jacobian_airfed,
    normalized_svd,
    numerical_rank_from_singular_values,
    transformed_pair,
)


def ballard_invariance_check() -> None:
    xi1 = -1.08604672
    xi2 = 0.003696006654
    delta = 3.0e-4

    lo, hi = delta_interval(xi1, xi2, BALLARD_T)
    assert lo <= delta <= hi

    xi1_new, xi2_new = transformed_pair(xi1, xi2, BALLARD_T, delta)
    k0 = fixed_temperature_combination(xi1, xi2, BALLARD_T)
    k1 = fixed_temperature_combination(xi1_new, xi2_new, BALLARD_T)

    # The remaining voltage contribution is deliberately kept identical.
    # Its exact form is irrelevant to the xi1/xi2 invariance.
    common = -0.05*np.log(BALLARD_I) + 0.001*BALLARD_I
    v0 = -(k0) + common
    v1 = -(k1) + common

    sse0 = float(np.sum((BALLARD_V - v0)**2))
    sse1 = float(np.sum((BALLARD_V - v1)**2))

    assert k0 == k1
    assert np.array_equal(v0, v1)
    assert sse0 == sse1

    print("BALLARD EXACT INVARIANCE")
    print(f"  feasible delta interval = [{lo:.12e}, {hi:.12e}]")
    print(f"  chosen delta            = {delta:.12e}")
    print(f"  transformed pair        = ({xi1_new:.12f}, {xi2_new:.12f})")
    print(f"  max |Delta V|           = {np.max(np.abs(v1-v0)):.1e}")
    print(f"  Delta SSE               = {sse1-sse0:.1e}")
    print()


def build_condition(name: str, lam_ref: float) -> np.ndarray:
    c = W250[name]
    return jacobian_airfed(
        c["I"],
        c["T"],
        W250_META["A_cm2"],
        W250_META["l_um"],
        W250_META["Jmax_Acm2"],
        W250_META["Ncell"],
        lam_ref,
        c["PC"],
    )


def rank_design_check() -> None:
    lam_ref = 13.23
    J = {name: build_condition(name, lam_ref) for name in ("c1", "c2", "c3", "c4")}

    designs = {
        "c1": np.vstack([J["c1"]]),
        "c2": np.vstack([J["c2"]]),
        "c2+c3+c4": np.vstack([J["c2"], J["c3"], J["c4"]]),
        "c1+c2": np.vstack([J["c1"], J["c2"]]),
        "all four": np.vstack([J["c1"], J["c2"], J["c3"], J["c4"]]),
    }
    expected_rank = {"c1": 5, "c2": 5, "c2+c3+c4": 6, "c1+c2": 7, "all four": 7}

    print("250 W COLUMN-NORMALIZED JACOBIAN AUDIT")
    for name, Jd in designs.items():
        s = normalized_svd(Jd)
        rank = numerical_rank_from_singular_values(s, Jd.shape)
        assert rank == expected_rank[name]

        if rank == 7:
            kappa2 = s[0] / s[-1]
            print(f"  {name:10s} rank={rank}  sigma_min={s[-1]:.8e}  kappa2={kappa2:.8e}")
        else:
            print(f"  {name:10s} rank={rank}  sigma_min={s[-1]:.8e}  structurally singular")

    s12 = normalized_svd(designs["c1+c2"])
    sall = normalized_svd(designs["all four"])
    assert np.isclose(s12[-1], 1.25444784e-8, rtol=5e-6, atol=0)
    assert np.isclose(s12[0]/s12[-1], 1.97849689e8, rtol=5e-6, atol=0)
    assert np.isclose(sall[-1], 5.49376e-3, rtol=5e-5, atol=0)
    assert np.isclose(sall[0]/sall[-1], 4.518837e2, rtol=5e-5, atol=0)
    print()


if __name__ == "__main__":
    ballard_invariance_check()
    rank_design_check()
    print("REPRODUCTION: PASS")
