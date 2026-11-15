"""Project 53 v13: local order of symmetry breaking under temperature separation."""

from __future__ import annotations

import itertools
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import mpmath as mp
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.benchmark_data import W250, W250_META
from src.pemfc_identifiability import jacobian_airfed

OUT = ROOT / "outputs" / "symmetry_breaking_order"
FIG = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

A = W250_META["A_cm2"]
L_UM = W250_META["l_um"]
JMAX = W250_META["Jmax_Acm2"]
NCELL = W250_META["Ncell"]
LAM = 13.23
T_LOW = W250["c2"]["T"]

BOUNDS = {
    "xi1": (-1.19969, -0.8532),
    "xi2": (1e-3, 5e-3),
    "xi3": (3.6e-5, 9.8e-5),
    "xi4": (-26e-5, -9.54e-5),
    "lambda": (10.0, 24.0),
    "beta": (0.0136, 0.5),
    "Rc": (1e-4, 8e-4),
}
BOX_WIDTHS = np.array([
    BOUNDS[key][1] - BOUNDS[key][0]
    for key in ("xi1", "xi2", "xi3", "xi4", "lambda", "beta", "Rc")
])


def condition_jacobian(name: str, temperature: float) -> np.ndarray:
    c = W250[name]
    return jacobian_airfed(
        c["I"], temperature, A, L_UM, JMAX, NCELL, LAM, c["PC"]
    )


def stacked_design(delta_t: float, low_subset: tuple[str, ...]) -> np.ndarray:
    high = condition_jacobian("c1", T_LOW + delta_t)
    low = np.vstack([condition_jacobian(name, T_LOW) for name in low_subset])
    return np.vstack([high, low])


def box_matrix(delta_t: float, low_subset: tuple[str, ...]) -> np.ndarray:
    return stacked_design(delta_t, low_subset) * BOX_WIDTHS.reshape(1, -1)


def numerical_rank(matrix: np.ndarray) -> int:
    s = np.linalg.svd(matrix, compute_uv=False)
    tol = s[0] * max(matrix.shape) * np.finfo(float).eps
    return int(np.sum(s > tol))


def sigma_min(delta_t: float, low_subset: tuple[str, ...]) -> float:
    return float(np.linalg.svd(box_matrix(delta_t, low_subset), compute_uv=False)[-1])


def first_order_opening_coefficient(
    low_subset: tuple[str, ...], step: float = 1e-5
) -> float:
    """eta_1 = ||P_{ker(A0^T)} A'(0) v0||_2 for the box-scaled matrix."""
    a0 = box_matrix(0.0, low_subset)
    derivative = (box_matrix(step, low_subset) - box_matrix(-step, low_subset)) / (2 * step)
    u, _, vt = np.linalg.svd(a0, full_matrices=True)
    rank = numerical_rank(a0)
    v0 = vt[rank:].T[:, 0]
    left_null = u[:, rank:]
    return float(np.linalg.norm(left_null.T @ (derivative @ v0)))


def fit_power_law(low_subset: tuple[str, ...]) -> tuple[float, float]:
    deltas = np.array([0.05, 0.1, 0.2, 0.5], dtype=float)
    values = np.array([sigma_min(delta, low_subset) for delta in deltas])
    exponent, log_coefficient = np.polyfit(np.log(deltas), np.log(values), 1)
    return float(exponent), float(np.exp(log_coefficient))


def build_summary() -> pd.DataFrame:
    rows = []
    for count in (1, 2, 3):
        for subset in itertools.combinations(("c2", "c3", "c4"), count):
            exponent, coefficient = fit_power_law(subset)
            rows.append({
                "low_temperature_subset": "+".join(subset),
                "number_of_low_temperature_pressures": count,
                "rank_at_deltaT_zero": numerical_rank(box_matrix(0.0, subset)),
                "first_order_transversality_eta1": first_order_opening_coefficient(subset),
                "local_power_exponent_p": exponent,
                "local_power_coefficient_C": coefficient,
                "sigma_min_at_0p1K": sigma_min(0.1, subset),
            })
    return pd.DataFrame(rows)


# High-precision verification for representative one-pressure and pressure-diverse cases.
mp.mp.dps = 80
A_MP = mp.mpf(str(A))
L_MP = mp.mpf(str(L_UM))
JMAX_MP = mp.mpf(str(JMAX))
NCELL_MP = mp.mpf(str(NCELL))
LAM_MP = mp.mpf(str(LAM))
BOX_MP = [mp.mpf(str(value)) for value in BOX_WIDTHS]


def water_vapor_mp(temperature: mp.mpf) -> mp.mpf:
    d = temperature - mp.mpf("273.15")
    return mp.power(
        10,
        mp.mpf("0.0295") * d
        - mp.mpf("0.0000918") * d**2
        + mp.mpf("0.000000144") * d**3
        - mp.mpf("2.18"),
    )


def jacobian_mp(name: str, temperature: mp.mpf) -> mp.matrix:
    condition = W250[name]
    pressure = mp.mpf(str(condition["PC"]))
    p_h2o = water_vapor_mp(temperature)
    gamma = mp.mpf("0.291") / (temperature**mp.mpf("0.832") * A_MP)
    rows = []
    for current_float in condition["I"]:
        current = mp.mpf(str(float(current_float)))
        current_density = current / A_MP
        p_o2 = (pressure - p_h2o) / (
            (1 + mp.mpf("0.79") / mp.mpf("0.21")) * mp.e**(gamma * current)
        )
        concentration = p_o2 / mp.mpf("5.08e6") * mp.e**(mp.mpf("498") / temperature)
        temperature_factor = mp.e**(
            mp.mpf("4.18") * (temperature - mp.mpf("303")) / temperature
        )
        numerator = mp.mpf("181.6") * (
            1
            + mp.mpf("0.03") * current_density
            + mp.mpf("0.062")
            * (temperature / mp.mpf("303")) ** 2
            * current_density ** mp.mpf("2.5")
        )
        membrane_factor = (
            numerator / temperature_factor
        ) * (L_MP * mp.mpf("1e-4") / A_MP)
        denominator = LAM_MP - mp.mpf("0.634") - 3 * current_density
        row = [
            NCELL_MP,
            NCELL_MP * temperature,
            NCELL_MP * temperature * mp.log(concentration),
            NCELL_MP * temperature * mp.log(current),
            NCELL_MP * current * membrane_factor / denominator**2,
            NCELL_MP * mp.log(1 - current_density / JMAX_MP),
            -NCELL_MP * current,
        ]
        rows.append([row[index] * BOX_MP[index] for index in range(7)])
    return mp.matrix(rows)


def stack_mp(matrices: list[mp.matrix]) -> mp.matrix:
    rows = []
    for matrix in matrices:
        for row_index in range(matrix.rows):
            rows.append([matrix[row_index, col] for col in range(matrix.cols)])
    return mp.matrix(rows)


def high_precision_sigma(delta_t: str, subset: tuple[str, ...]) -> mp.mpf:
    delta = mp.mpf(delta_t)
    low_temperature = mp.mpf(str(T_LOW))
    matrices = [jacobian_mp("c1", low_temperature + delta)]
    matrices.extend(jacobian_mp(name, low_temperature) for name in subset)
    matrix = stack_mp(matrices)
    eigenvalues, _ = mp.eigsy(matrix.T * matrix)
    return mp.sqrt(max(mp.re(eigenvalues[0]), mp.mpf("0")))


def make_figure(summary: pd.DataFrame) -> None:
    delta_grid = np.logspace(-3, 1, 120)
    series = {
        "c1+c2: one low-T pressure": ("c2",),
        "c1+(c2+c3): two low-T pressures": ("c2", "c3"),
        "c1+(c2+c3+c4): three low-T pressures": ("c2", "c3", "c4"),
    }
    fig, ax = plt.subplots(figsize=(7.4, 5.0))
    for label, subset in series.items():
        values = [sigma_min(delta, subset) for delta in delta_grid]
        ax.plot(delta_grid, values, label=label)

    reference_delta = np.logspace(-2, -0.3, 50)
    quadratic_coefficient = summary.loc[
        summary["low_temperature_subset"] == "c2", "local_power_coefficient_C"
    ].iloc[0]
    linear_coefficient = summary.loc[
        summary["low_temperature_subset"] == "c2+c3+c4", "local_power_coefficient_C"
    ].iloc[0]
    ax.plot(
        reference_delta,
        quadratic_coefficient * reference_delta**2,
        linestyle="--",
        linewidth=1.2,
        label=r"reference $\propto \Delta T^2$",
    )
    ax.plot(
        reference_delta,
        linear_coefficient * reference_delta,
        linestyle=":",
        linewidth=1.5,
        label=r"reference $\propto \Delta T$",
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlabel(r"Temperature separation $\Delta T$ (K)")
    ax.set_ylabel(r"Smallest singular value of box-scaled Jacobian")
    ax.set_title("Tangential versus transverse symmetry breaking")
    ax.grid(True, which="both", alpha=0.3)
    ax.legend(fontsize=8)
    fig.tight_layout()
    fig.savefig(FIG / "Figure_S3_Symmetry_Breaking_Opening_Order.png", dpi=300)
    fig.savefig(FIG / "Figure_S3_Symmetry_Breaking_Opening_Order.pdf")
    plt.close(fig)


def main() -> None:
    summary = build_summary()
    summary.to_csv(OUT / "symmetry_breaking_scaling_by_pressure_subset.csv", index=False)

    high_rows = []
    for subset in [("c2",), ("c2", "c3", "c4")]:
        for delta_text in ["0.001", "0.01", "0.1", "0.2", "0.5", "1.0"]:
            value = high_precision_sigma(delta_text, subset)
            high_rows.append({
                "low_temperature_subset": "+".join(subset),
                "deltaT_K": float(delta_text),
                "sigma_min_box_scaled_high_precision": float(value),
                "sigma_min_text_30_digits": mp.nstr(value, 30),
            })
    pd.DataFrame(high_rows).to_csv(
        OUT / "high_precision_symmetry_breaking_check.csv", index=False
    )

    make_figure(summary)

    c1c2 = summary.loc[summary.low_temperature_subset == "c2"].iloc[0]
    all_four = summary.loc[summary.low_temperature_subset == "c2+c3+c4"].iloc[0]
    ratio = all_four.sigma_min_at_0p1K / c1c2.sigma_min_at_0p1K

    assert abs(c1c2.local_power_exponent_p - 2.0) < 0.01
    assert abs(all_four.local_power_exponent_p - 1.0) < 0.01
    assert c1c2.first_order_transversality_eta1 < 1e-12
    assert all_four.first_order_transversality_eta1 > 1e-2
    assert ratio > 1e7

    print("SYMMETRY-BREAKING ORDER: PASS")
    print(f"c1+c2 eta1 = {c1c2.first_order_transversality_eta1:.16e}")
    print(f"c1+c2 fitted p = {c1c2.local_power_exponent_p:.8f}")
    print(f"all-four eta1 = {all_four.first_order_transversality_eta1:.16e}")
    print(f"all-four fitted p = {all_four.local_power_exponent_p:.8f}")
    print(f"sigma7 ratio at 0.1 K = {ratio:.8e}")


if __name__ == "__main__":
    main()
