from __future__ import annotations

import csv
import itertools
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from data.benchmark_data import BALLARD_I, BALLARD_T, BALLARD_V, W250, W250_META
from src.pemfc_identifiability import (
    complex_step_jacobian_airfed,
    delta_interval,
    jacobian_airfed,
    max_relative_column_discrepancy,
    normalized_svd,
    numerical_rank_from_singular_values,
    transformed_pair,
)

OUT = ROOT / "outputs"
OUT.mkdir(exist_ok=True)

BOUNDS = {
    "xi1": (-1.19969, -0.8532),
    "xi2": (1.0e-3, 5.0e-3),
    "xi3": (3.6e-5, 9.8e-5),
    "xi4": (-26e-5, -9.54e-5),
    "lambda": (10.0, 24.0),
    "beta": (0.0136, 0.5),
    "Rc": (1.0e-4, 8.0e-4),
}
BOX_SCALES = np.array(
    [BOUNDS[k][1]-BOUNDS[k][0] for k in ("xi1","xi2","xi3","xi4","lambda","beta","Rc")],
    dtype=float,
)

BALLARD_META = dict(
    Ncell=35, A_cm2=50.6, l_um=178.0, Jmax_Acm2=1.50,
    T=343.0, PH2_atm=1.0, PO2_atm=1.0,
)
BALLARD_THRO = np.array([
    -1.08604672,
    3.6960066540e-3,
    6.8228474681e-5,
    -16.725137922e-5,
    24.0,
    1.5884374009e-2,
    1.00e-4,
])
BALLARD_PUBLISHED_SSE = 0.813911703

FIXED_PRESSURE_SOLUTIONS = {
    "NedStack PS6": {
        "T": 343.0, "PO2": 1.0,
        "rows": [
            ("THRO", -0.9146023053, 3.1103142926e-3, 7.4078557895e-5),
            ("FLA", -1.19969, 4.2686233306e-3, 9.7464882196e-5),
            ("ECO", -0.865900221, 3.3029610113e-3, 9.80e-5),
        ],
    },
    "BCS 500W": {
        "T": 333.0, "PO2": 0.2075,
        "rows": [
            ("THRO", -1.030312131, 3.0547161500e-3, 5.8105674797e-5),
            ("FLA", -0.9904907362, 2.5927917531e-3, 3.6044730968e-5),
            ("ECO", -1.16964463, 4.0912655890e-3, 9.7939124677e-5),
        ],
    },
    "Avista SR-12": {
        "T": 323.0, "PO2": 0.2095,
        "rows": [
            ("THRO", -1.071727171, 3.0727521947e-3, 4.3042416579e-5),
            ("FLA", -0.8663266858, 3.2865944138e-3, 9.7999981070e-5),
            ("ECO", -1.109670769, 3.9627032578e-3, 9.3002042837e-5),
        ],
    },
    "Ballard Mark V": {
        "T": 343.0, "PO2": 1.0,
        "rows": [
            ("THRO", -1.08604672, 3.6960066540e-3, 6.8228474681e-5),
            ("FLA", -1.199260732, 4.4318028525e-3, 9.7231857179e-5),
            ("ECO", -1.199689993, 4.3852233888e-3, 9.3812656073e-5),
        ],
    },
}


def full_ballard_voltage(params: np.ndarray) -> np.ndarray:
    """Complete Ballard Mark V voltage model using the audited benchmark equations."""
    xi1, xi2, xi3, xi4, lam, beta, Rc = np.asarray(params)
    I = BALLARD_I.astype(params.dtype if np.iscomplexobj(params) else float)
    T = BALLARD_META["T"]
    A = BALLARD_META["A_cm2"]
    l_cm = BALLARD_META["l_um"] * 1e-4
    Jmax = BALLARD_META["Jmax_Acm2"]
    Ncell = BALLARD_META["Ncell"]
    PH2 = BALLARD_META["PH2_atm"]
    PO2 = BALLARD_META["PO2_atm"]

    E = 1.229 - 0.85e-3*(T-298.15) + 430.85e-7*T*np.log(PH2*np.sqrt(PO2))
    C = PO2/5.08e6*np.exp(498.0/T)
    Vact = -(xi1 + xi2*T + xi3*T*np.log(C) + xi4*T*np.log(I))
    j = I/A
    rho_m = 181.6*(1 + 0.03*j + 0.062*(T/303.0)**2*j**2.5) / (
        (lam-0.634-3*j)*np.exp(4.18*(T-303.0)/T)
    )
    Rm = rho_m*l_cm/A
    Vohm = I*(Rm + Rc)
    Vcon = -beta*np.log(1 - j/Jmax)
    return Ncell*(E - Vact - Vohm - Vcon)


def ballard_full_model_check() -> dict:
    p0 = BALLARD_THRO.copy()
    delta = 3e-4
    lo, hi = delta_interval(p0[0], p0[1], BALLARD_T)
    assert lo <= delta <= hi
    p1 = p0.copy()
    p1[0], p1[1] = transformed_pair(p0[0], p0[1], BALLARD_T, delta)
    v0 = full_ballard_voltage(p0)
    v1 = full_ballard_voltage(p1)
    sse0 = float(np.sum((BALLARD_V-v0)**2))
    sse1 = float(np.sum((BALLARD_V-v1)**2))
    assert np.array_equal(v0, v1)
    assert sse0 == sse1
    assert abs(sse0 - BALLARD_PUBLISHED_SSE) < 1e-9
    return dict(
        delta_lo=lo, delta_hi=hi, delta=delta,
        max_abs_dV=float(np.max(np.abs(v1-v0))),
        sse=sse0, delta_sse=sse1-sse0,
        published_sse=BALLARD_PUBLISHED_SSE,
    )


def fixed_pressure_null_check() -> float:
    """Check the two exact null relations for Ballard fixed oxygen pressure."""
    p = BALLARD_THRO.copy()
    T = BALLARD_META["T"]
    C0 = BALLARD_META["PO2_atm"]/5.08e6*np.exp(498/T)
    h = 1e-30
    cols = []
    for q in range(7):
        z = p.astype(complex)
        z[q] += 1j*h
        cols.append(np.imag(full_ballard_voltage(z))/h)
    J = np.column_stack(cols)
    v1 = np.array([-T,1,0,0,0,0,0.0])
    v2 = np.array([-T*np.log(C0),0,1,0,0,0,0.0])
    rel1 = np.linalg.norm(J@v1)/(np.linalg.norm(J)*np.linalg.norm(v1))
    rel2 = np.linalg.norm(J@v2)/(np.linalg.norm(J)*np.linalg.norm(v2))
    assert rel1 < 1e-12 and rel2 < 1e-12
    return max(float(rel1), float(rel2))


def build_condition(name: str, lam: float) -> np.ndarray:
    c = W250[name]
    return jacobian_airfed(
        c["I"], c["T"], W250_META["A_cm2"], W250_META["l_um"],
        W250_META["Jmax_Acm2"], W250_META["Ncell"], lam, c["PC"],
    )


def build_designs(lam: float) -> dict[str, np.ndarray]:
    J = {n: build_condition(n,lam) for n in ("c1","c2","c3","c4")}
    return {
        "c1": J["c1"],
        "c2": J["c2"],
        "c2+c3+c4": np.vstack([J["c2"],J["c3"],J["c4"]]),
        "c1+c2": np.vstack([J["c1"],J["c2"]]),
        "c1+c2+c3": np.vstack([J["c1"],J["c2"],J["c3"]]),
        "all four": np.vstack([J[n] for n in ("c1","c2","c3","c4")]),
    }


def observation_count_matched_30(lam: float) -> tuple[np.ndarray, dict[str,list[int]]]:
    J = {n: build_condition(n,lam) for n in ("c1","c2","c3","c4")}
    idx = {
        "c1":[0,2,4,6,8,10,12,14],
        "c2":[0,2,4,6,8,10,12,14],
        "c3":[0,2,5,7,9,12,14],
        "c4":[0,2,5,7,9,12,14],
    }
    return np.vstack([J[n][idx[n]] for n in ("c1","c2","c3","c4")]), idx


def complex_step_check() -> float:
    c = W250["c1"]
    params = np.array([-1.05,0.0032,7.0e-5,-1.5e-4,13.23,0.02,1.0e-4])
    analytic = jacobian_airfed(
        c["I"],c["T"],W250_META["A_cm2"],W250_META["l_um"],
        W250_META["Jmax_Acm2"],W250_META["Ncell"],params[4],c["PC"],
    )
    numerical = complex_step_jacobian_airfed(
        params,c["I"],c["T"],W250_META["A_cm2"],W250_META["l_um"],
        W250_META["Jmax_Acm2"],W250_META["Ncell"],c["PC"],
    )
    d = max_relative_column_discrepancy(analytic,numerical)
    assert d < 1e-12
    return d


def summarize_svd(M: np.ndarray, scaling: str) -> dict:
    if scaling == "column_norm":
        s = normalized_svd(M)
    elif scaling == "parameter_box":
        s = np.linalg.svd(M*BOX_SCALES.reshape(1,-1),compute_uv=False)
    else:
        raise ValueError(scaling)
    r = numerical_rank_from_singular_values(s,M.shape)
    out = {"rank":r,"sigma1":float(s[0]),"sigma_min_raw":float(s[-1])}
    if r == 7:
        out.update(
            sigma_metric=float(s[-1]),
            condition_metric=float(s[0]/s[-1]),
            metric_type="full",
        )
    else:
        out.update(
            sigma_metric=float(s[r-1]),
            condition_metric=float(s[0]/s[r-1]),
            metric_type="identifiable_subspace",
        )
    return out


def lambda_sweep() -> list[dict]:
    grid = np.linspace(BOUNDS["lambda"][0],BOUNDS["lambda"][1],501)
    rows = []
    for lam in grid:
        ds = build_designs(float(lam))
        eb,_ = observation_count_matched_30(float(lam))
        ds["all-four observation-count-matched 30"] = eb
        for name,M in ds.items():
            for scaling in ("column_norm","parameter_box"):
                rec = summarize_svd(M,scaling)
                rows.append({
                    "lambda":float(lam),"design":name,"n_obs":int(M.shape[0]),
                    "scaling":scaling,**rec,
                })
    with (OUT/"lambda_scaling_sweep.csv").open("w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    return rows


def sweep_summary(rows: list[dict]) -> list[dict]:
    summary = []
    keys = sorted(set((r["design"],r["scaling"]) for r in rows))
    for design,scaling in keys:
        rr = [r for r in rows if r["design"]==design and r["scaling"]==scaling]
        ranks = sorted(set(r["rank"] for r in rr))
        sig = np.array([r["sigma_metric"] for r in rr])
        cond = np.array([r["condition_metric"] for r in rr])
        summary.append({
            "design":design,"scaling":scaling,"n_obs":rr[0]["n_obs"],
            "ranks":"/".join(map(str,ranks)),
            "sigma_metric_min":float(sig.min()),
            "sigma_metric_median":float(np.median(sig)),
            "sigma_metric_max":float(sig.max()),
            "condition_min":float(cond.min()),
            "condition_median":float(np.median(cond)),
            "condition_max":float(cond.max()),
            "metric_type":rr[0]["metric_type"],
        })
    with (OUT/"lambda_scaling_summary.csv").open("w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=summary[0].keys())
        w.writeheader(); w.writerows(summary)
    return summary


def subset_analysis(lam: float=13.23) -> list[dict]:
    J = {n:build_condition(n,lam) for n in ("c1","c2","c3","c4")}
    rows = []
    names = list(J)
    for k in range(1,5):
        for comb in itertools.combinations(names,k):
            M = np.vstack([J[n] for n in comb])
            rec = summarize_svd(M,"column_norm")
            rows.append({"conditions":"+".join(comb),"n_obs":M.shape[0],**rec})
    with (OUT/"all_condition_subsets_reference_lambda.csv").open("w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    return rows


def optimizer_collapse_table() -> list[dict]:
    rows = []
    for stack,d in FIXED_PRESSURE_SOLUTIONS.items():
        C = d["PO2"]/5.08e6*np.exp(498.0/d["T"])
        ref = None
        for alg,x1,x2,x3 in d["rows"]:
            k0 = x1+d["T"]*x2+d["T"]*np.log(C)*x3
            if ref is None:
                ref = k0
            rows.append({
                "stack":stack,"algorithm":alg,"T_K":d["T"],"PO2_atm":d["PO2"],
                "xi1":x1,"xi2":x2,"xi3":x3,"kappa0":float(k0),
                "difference_from_THRO":float(k0-ref),
            })
    with (OUT/"published_optimizer_identifiable_coordinates.csv").open("w",newline="") as f:
        w = csv.DictWriter(f,fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)
    return rows


def out_of_temperature_ambiguity() -> dict:
    lo,hi = delta_interval(BALLARD_THRO[0],BALLARD_THRO[1],BALLARD_T)
    dT = 10.0
    chosen = 3e-4
    return {
        "delta_lo":lo,"delta_hi":hi,"delta_T_K":dT,"chosen_delta":chosen,
        "chosen_abs_cell_shift_V":abs(dT*chosen),
        "chosen_abs_stack_shift_V":BALLARD_META["Ncell"]*abs(dT*chosen),
        "envelope_abs_cell_shift_V":dT*max(abs(lo),abs(hi)),
        "envelope_abs_stack_shift_V":BALLARD_META["Ncell"]*dT*max(abs(lo),abs(hi)),
    }


def reduced_coordinate_identity_check() -> float:
    c = W250["c1"]
    T = c["T"]
    area = W250_META["A_cm2"]
    I = c["I"]
    from src.pemfc_identifiability import oxygen_concentration_airfed
    lnC = np.log(oxygen_concentration_airfed(I,area,T,c["PC"]))
    b = (lnC[-1]-lnC[0])/(I[-1]-I[0])
    a = lnC[0]-b*I[0]
    p = np.array([-1.05,0.0032,7e-5,-1.5e-4,13.23,0.02,1e-4])
    ka = p[0]+T*p[1]+T*a*p[2]
    Reff = p[6]-T*b*p[2]
    original = p[0]+T*p[1]+T*lnC*p[2]-I*p[6]
    reduced = ka-I*Reff
    err = float(np.max(np.abs(original-reduced)))
    assert err < 1e-12
    return err


def main() -> None:
    full = ballard_full_model_check()
    null_err = fixed_pressure_null_check()
    cs = complex_step_check()
    red_err = reduced_coordinate_identity_check()
    rows = lambda_sweep()
    summary = sweep_summary(rows)
    subset_analysis()
    optimizer_collapse_table()
    temp = out_of_temperature_ambiguity()

    ref = build_designs(13.23)
    expected = {"c1":5,"c2":5,"c2+c3+c4":6,"c1+c2":7,"all four":7}
    for name,rank in expected.items():
        s = normalized_svd(ref[name])
        r = numerical_rank_from_singular_values(s,ref[name].shape)
        assert r == rank, (name,r,rank)
    s12 = normalized_svd(ref["c1+c2"])
    sall = normalized_svd(ref["all four"])
    assert np.isclose(s12[0]/s12[-1],1.97849689e8,rtol=5e-6)
    assert np.isclose(sall[0]/sall[-1],4.518837e2,rtol=5e-5)

    eb,idx = observation_count_matched_30(13.23)
    seb = normalized_svd(eb)
    assert numerical_rank_from_singular_values(seb,eb.shape) == 7
    assert np.isclose(seb[0]/seb[-1],447.2231388343,rtol=1e-10)

    with (OUT/"observation_count_matched_indices.txt").open("w") as f:
        for n in ("c1","c2","c3","c4"):
            f.write(f"{n}: {idx[n]}\n")

    lines = ["PROJECT 53 CORE REPRODUCTION", "", "BALLARD FULL MODEL CHECK"]
    for k,v in full.items():
        lines.append(f"  {k}: {v}")
    lines.append(f"  fixed-pressure null residual max: {null_err:.3e}")
    lines.append(f"  complex-step max relative column discrepancy: {cs:.16e}")
    lines.append(f"  five-coordinate affine-log reduction max error: {red_err:.3e}")
    lines.append("\nREFERENCE-LAMBDA DESIGNS (lambda=13.23, column normalization)")
    for name in ("c1","c2","c2+c3+c4","c1+c2","c1+c2+c3","all four"):
        rec = summarize_svd(ref[name],"column_norm")
        lines.append(
            f"  {name}: n={ref[name].shape[0]} rank={rec['rank']} "
            f"metric={rec['condition_metric']:.12g} ({rec['metric_type']})"
        )
    lines.append(
        f"  all-four observation-count-matched 30: n=30 rank=7 "
        f"cond2={seb[0]/seb[-1]:.12g}"
    )
    lines.append("\nOUT-OF-TEMPERATURE AMBIGUITY")
    for k,v in temp.items():
        lines.append(f"  {k}: {v}")
    lines.append("\nLAMBDA/SCALE SUMMARY")
    for rec in summary:
        if rec["design"] in (
            "c1","c2","c2+c3+c4","c1+c2","all four",
            "all-four observation-count-matched 30",
        ):
            lines.append("  " + ", ".join(f"{k}={rec[k]}" for k in rec))
    lines.append("\nREPRODUCTION: PASS")
    (OUT/"REPRODUCTION_V7.txt").write_text("\n".join(lines),encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
