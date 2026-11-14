from pathlib import Path
import sys, math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data.benchmark_data import W250, W250_META
from src.pemfc_identifiability import jacobian_airfed

OUT = ROOT / "outputs" / "oed_information_geometry"
FIG = ROOT / "figures"
OUT.mkdir(parents=True, exist_ok=True)
FIG.mkdir(parents=True, exist_ok=True)

A = W250_META["A_cm2"]; L = W250_META["l_um"]; JMAX = W250_META["Jmax_Acm2"]; NCELL = W250_META["Ncell"]; LAM = 13.23
BOUNDS = {
    "xi1": (-1.19969, -0.8532), "xi2": (1.0e-3, 5.0e-3), "xi3": (3.6e-5, 9.8e-5),
    "xi4": (-26e-5, -9.54e-5), "lambda": (10.0, 24.0), "beta": (0.0136, 0.5), "Rc": (1.0e-4, 8.0e-4),
}
D = np.array([BOUNDS[k][1]-BOUNDS[k][0] for k in ("xi1","xi2","xi3","xi4","lambda","beta","Rc")], float)
MATCHED = {
    "c1": [0,2,4,6,8,10,12,14], "c2": [0,2,4,6,8,10,12,14],
    "c3": [0,2,5,7,9,12,14], "c4": [0,2,5,7,9,12,14],
}

def Jcond(name):
    c = W250[name]
    return jacobian_airfed(c["I"], c["T"], A, L, JMAX, NCELL, LAM, c["PC"])

J = {n: Jcond(n) for n in ("c1","c2","c3","c4")}
designs = {
    "c1+c2": np.vstack([J["c1"], J["c2"]]),
    "c1+c2+c3": np.vstack([J["c1"], J["c2"], J["c3"]]),
    "all four": np.vstack([J[n] for n in ("c1","c2","c3","c4")]),
    "matched 30": np.vstack([J[n][MATCHED[n]] for n in ("c1","c2","c3","c4")]),
}

def metrics(M):
    X = M * D.reshape(1,-1)
    s = np.linalg.svd(X, compute_uv=False)
    eig = s*s
    tol = s[0] * max(X.shape) * np.finfo(float).eps
    rank = int(np.sum(s > tol))
    Z = M / np.linalg.norm(M, axis=0, keepdims=True)
    sz = np.linalg.svd(Z, compute_uv=False)
    return {
        "n_obs": M.shape[0], "rank": rank,
        "box_cond2": float(s[0]/s[-1]) if rank == 7 else np.inf,
        "E_information": float(eig[-1]) if rank == 7 else 0.0,
        "D_information_geomean": float(np.exp(np.mean(np.log(eig)))) if rank == 7 else 0.0,
        "A_information": float(7.0/np.sum(1.0/eig)) if rank == 7 else 0.0,
        "trace_information": float(eig.sum()),
        "normalized_gram_det": float(np.prod(sz*sz)),
        "normalized_sigma7_distance": float(sz[-1]),
    }

df = pd.DataFrame({k: metrics(v) for k,v in designs.items()}).T
df.to_csv(OUT/"oed_information_metrics.csv")

base = df.loc["c1+c2"]; matched = df.loc["matched 30"]
ratios = {
    "Trace information": matched.trace_information/base.trace_information,
    "E-information": matched.E_information/base.E_information,
    "D-information geometric mean": matched.D_information_geomean/base.D_information_geomean,
    "A-information": matched.A_information/base.A_information,
    "Gram determinant": matched.normalized_gram_det/base.normalized_gram_det,
    "Distance to rank deficiency": matched.normalized_sigma7_distance/base.normalized_sigma7_distance,
}
pd.DataFrame({"metric": list(ratios), "matched30_over_c1c2": list(ratios.values())}).to_csv(OUT/"matched30_vs_c1c2_ratios.csv", index=False)

fig, ax = plt.subplots(figsize=(7.5,4.8))
labels = ["E-information","D-information geometric mean","A-information","Gram determinant","Distance to rank deficiency"]
vals = [ratios[x] for x in labels]
ax.bar(range(len(labels)), vals)
ax.set_yscale("log")
ax.set_xticks(range(len(labels)))
ax.set_xticklabels(["E-info","D-info","A-info","Gram det","Rank margin"], rotation=20, ha="right")
ax.set_ylabel("Matched-30 / c1+c2 improvement factor")
ax.set_title("Information-geometry improvement at equal observation count")
ax.grid(True, axis="y", which="both", alpha=0.3)
fig.tight_layout()
fig.savefig(FIG/"Figure_S2_OED_Information_Improvement.png", dpi=300)
fig.savefig(FIG/"Figure_S2_OED_Information_Improvement.pdf")
plt.close(fig)

checks = [
    (base.trace_information, 48060.38190185165, 1e-9),
    (matched.trace_information, 51313.15591429629, 1e-9),
    (base.E_information, 4.873228271537714e-13, 1e-20),
    (matched.E_information, 0.002142464970338894, 1e-15),
    (ratios["E-information"], 4396397728.4873905, 1e-3),
    (ratios["D-information geometric mean"], 44.64809052785325, 1e-10),
    (ratios["A-information"], 4320834099.036076, 1e-3),
    (base.normalized_sigma7_distance, 1.2544478413997039e-08, 1e-18),
    (matched.normalized_sigma7_distance, 0.005498554538900077, 1e-15),
    (ratios["Distance to rank deficiency"], 438324.6841705932, 1e-6),
]
for got, exp, atol in checks:
    if not math.isclose(float(got), float(exp), rel_tol=1e-10, abs_tol=atol):
        raise AssertionError((got, exp))

print(df)
print("\nRatios:")
for k,v in ratios.items(): print(f"{k}: {v:.15g}")
print("PASS: all locked v11 information-geometry values reproduced.")
