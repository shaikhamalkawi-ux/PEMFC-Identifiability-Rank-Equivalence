"""Generate the two manuscript figures from locked repository values."""

from __future__ import annotations

import sys
from pathlib import Path
import numpy as np
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.benchmark_data import W250, W250_META
from src.pemfc_identifiability import jacobian_airfed, normalized_svd

OUT = ROOT / "figures"
OUT.mkdir(exist_ok=True)

# Figure 1 — exact fixed-temperature equivalence class
T0 = 343.0
xi1 = -1.08604672
xi2 = 0.003696006654
delta = 3e-4
L1, U1 = -1.19969, -0.8532
L2, U2 = 0.001, 0.005
kappa = xi1 + T0*xi2
xi1_new = xi1 - T0*delta
xi2_new = xi2 + delta

x1_min = max(L1, kappa - T0*U2)
x1_max = min(U1, kappa - T0*L2)
x = np.linspace(x1_min, x1_max, 300)
y = (kappa - x)/T0

fig, ax = plt.subplots(figsize=(7.0, 5.0))
ax.plot(x, y, linewidth=2.2, label=r"Exact equivalence class: $\xi_1+T_0\xi_2=\kappa$")
ax.scatter([xi1], [xi2], s=70, marker="o", label="Published Ballard THRO point")
ax.scatter([xi1_new], [xi2_new], s=70, marker="s", label=r"Equivalent point, $\delta=3\times10^{-4}$")
ax.plot([xi1, xi1_new], [xi2, xi2_new], linestyle="--", linewidth=1.4)
ax.axvline(L1, linewidth=0.8); ax.axvline(U1, linewidth=0.8)
ax.axhline(L2, linewidth=0.8); ax.axhline(U2, linewidth=0.8)
ax.set_xlim(L1-0.01, U1+0.01); ax.set_ylim(L2-0.00018, U2+0.00018)
ax.set_xlabel(r"$\xi_1$"); ax.set_ylabel(r"$\xi_2$")
ax.set_title("Exact fixed-temperature equivalence class in the published parameter box")
ax.grid(True, alpha=0.3); ax.legend(loc="best", frameon=True)
fig.tight_layout()
fig.savefig(OUT/"Figure_1_Exact_Equivalence_Class.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT/"Figure_1_Exact_Equivalence_Class.pdf", bbox_inches="tight")
plt.close(fig)

# Figure 2 — singular-value spectra
A = W250_META["A_cm2"]; l_um = W250_META["l_um"]
Jmax = W250_META["Jmax_Acm2"]; Ncell = W250_META["Ncell"]
lam = 13.23

J = {}
for name in ("c1", "c2", "c3", "c4"):
    c = W250[name]
    J[name] = jacobian_airfed(c["I"], c["T"], A, l_um, Jmax, Ncell, lam, c["PC"])

designs = {
    "c1 only (rank 5)": J["c1"],
    "c2+c3+c4, same T (rank 6)": np.vstack([J["c2"], J["c3"], J["c4"]]),
    "c1+c2, two T (rank 7)": np.vstack([J["c1"], J["c2"]]),
    "all four conditions (rank 7)": np.vstack([J["c1"], J["c2"], J["c3"], J["c4"]]),
}

fig, ax = plt.subplots(figsize=(7.3, 5.2))
idx = np.arange(1, 8)
styles = {
    "c1 only (rank 5)": ("o", "-"),
    "c2+c3+c4, same T (rank 6)": ("s", "--"),
    "c1+c2, two T (rank 7)": ("^", "-."),
    "all four conditions (rank 7)": ("D", ":"),
}
for label, M in designs.items():
    marker, linestyle = styles[label]
    ax.plot(idx, normalized_svd(M), marker=marker, linestyle=linestyle,
            linewidth=1.8, label=label)
ax.set_yscale("log"); ax.set_xticks(idx)
ax.set_xlabel("Singular-value index")
ax.set_ylabel("Column-normalized singular value")
ax.set_title("Structural rank restoration and conditioning in the 250 W benchmark")
ax.grid(True, which="both", alpha=0.3); ax.legend(loc="best", frameon=True)
fig.tight_layout()
fig.savefig(OUT/"Figure_2_Normalized_Singular_Spectra.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT/"Figure_2_Normalized_Singular_Spectra.pdf", bbox_inches="tight")
plt.close(fig)

print(f"Figures written to {OUT}")
