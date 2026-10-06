"""Reproduce the manuscript's structural-identifiability and design checks."""

from __future__ import annotations
import sys
from pathlib import Path
import numpy as np

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from data.benchmark_data import BALLARD_I,BALLARD_T,BALLARD_V,W250,W250_META
from src.pemfc_identifiability import (
    complex_step_jacobian_airfed,delta_interval,jacobian_airfed,
    max_relative_column_discrepancy,normalized_svd,
    numerical_rank_from_singular_values,transformed_pair,
)

BOUNDS={
    "xi1":(-1.19969,-0.8532),"xi2":(1e-3,5e-3),"xi3":(3.6e-5,9.8e-5),
    "xi4":(-26e-5,-9.54e-5),"lambda":(10.0,24.0),
    "beta":(0.0136,0.5),"Rc":(1e-4,8e-4),
}
BOX_SCALES=np.array([BOUNDS[k][1]-BOUNDS[k][0] for k in
                     ("xi1","xi2","xi3","xi4","lambda","beta","Rc")])

BALLARD_META=dict(Ncell=35,A_cm2=50.6,l_um=178.0,Jmax_Acm2=1.50,
                  T=343.0,PH2_atm=1.0,PO2_atm=1.0)
BALLARD_THRO=np.array([
    -1.08604672,3.6960066540e-3,6.8228474681e-5,-16.725137922e-5,
    24.0,1.5884374009e-2,1.00e-4,
])
BALLARD_PUBLISHED_SSE=0.813911703

def full_ballard_voltage(params):
    """Complete Ballard Mark V model following the audited benchmark equations."""
    xi1,xi2,xi3,xi4,lam,beta,Rc=np.asarray(params)
    I=BALLARD_I.astype(params.dtype if np.iscomplexobj(params) else float)
    T=BALLARD_META["T"]; A=BALLARD_META["A_cm2"]
    l_cm=BALLARD_META["l_um"]*1e-4; jmax=BALLARD_META["Jmax_Acm2"]
    n=BALLARD_META["Ncell"]; ph2=BALLARD_META["PH2_atm"]; po2=BALLARD_META["PO2_atm"]
    E=1.229-0.85e-3*(T-298.15)+430.85e-7*T*np.log(ph2*np.sqrt(po2))
    C=po2/5.08e6*np.exp(498.0/T)
    Vact=-(xi1+xi2*T+xi3*T*np.log(C)+xi4*T*np.log(I))
    j=I/A
    rho=181.6*(1+0.03*j+0.062*(T/303.0)**2*j**2.5)/(
        (lam-0.634-3*j)*np.exp(4.18*(T-303.0)/T))
    Rm=rho*l_cm/A
    Vohm=I*(Rm+Rc)
    Vcon=-beta*np.log(1-j/jmax)
    return n*(E-Vact-Vohm-Vcon)

def ballard_full_model_check():
    p0=BALLARD_THRO.copy(); delta=3e-4
    lo,hi=delta_interval(p0[0],p0[1],BALLARD_T)
    assert lo<=delta<=hi
    p1=p0.copy(); p1[0],p1[1]=transformed_pair(p0[0],p0[1],BALLARD_T,delta)
    v0=full_ballard_voltage(p0); v1=full_ballard_voltage(p1)
    sse0=float(np.sum((BALLARD_V-v0)**2)); sse1=float(np.sum((BALLARD_V-v1)**2))
    assert np.array_equal(v0,v1)
    assert sse0==sse1
    assert abs(sse0-BALLARD_PUBLISHED_SSE)<1e-9

    h=1e-30; cols=[]
    for q in range(7):
        z=p0.astype(complex); z[q]+=1j*h
        cols.append(np.imag(full_ballard_voltage(z))/h)
    J=np.column_stack(cols)
    C0=BALLARD_META["PO2_atm"]/5.08e6*np.exp(498.0/BALLARD_T)
    n1=np.array([-BALLARD_T,1,0,0,0,0,0.0])
    n2=np.array([-BALLARD_T*np.log(C0),0,1,0,0,0,0.0])
    for vec in (n1,n2):
        rel=np.linalg.norm(J@vec)/(np.linalg.norm(J)*np.linalg.norm(vec))
        assert rel<1e-12

    print("BALLARD COMPLETE-MODEL CHECK")
    print(f"  SSE={sse0:.15f} (published rounded {BALLARD_PUBLISHED_SSE})")
    print(f"  max |Delta V|={np.max(np.abs(v1-v0)):.1e}; Delta SSE={sse1-sse0:.1e}")
    print(f"  feasible delta=[{lo:.12e},{hi:.12e}]")

def build_condition(name,lam):
    c=W250[name]
    return jacobian_airfed(c["I"],c["T"],W250_META["A_cm2"],W250_META["l_um"],
                           W250_META["Jmax_Acm2"],W250_META["Ncell"],lam,c["PC"])

def designs(lam):
    J={n:build_condition(n,lam) for n in ("c1","c2","c3","c4")}
    return {
        "c1":J["c1"],"c2":J["c2"],
        "c2+c3+c4":np.vstack([J["c2"],J["c3"],J["c4"]]),
        "c1+c2":np.vstack([J["c1"],J["c2"]]),
        "c1+c2+c3":np.vstack([J["c1"],J["c2"],J["c3"]]),
        "all four":np.vstack([J["c1"],J["c2"],J["c3"],J["c4"]]),
    }

def balanced_30(lam):
    J={n:build_condition(n,lam) for n in ("c1","c2","c3","c4")}
    idx={
      "c1":[0,2,4,6,8,10,12,14],"c2":[0,2,4,6,8,10,12,14],
      "c3":[0,2,5,7,9,12,14],"c4":[0,2,5,7,9,12,14],
    }
    return np.vstack([J[n][idx[n]] for n in ("c1","c2","c3","c4")])

def svd_summary(M,scaling="column"):
    if scaling=="column":
        s=normalized_svd(M)
    elif scaling=="box":
        s=np.linalg.svd(M*BOX_SCALES.reshape(1,-1),compute_uv=False)
    else:
        raise ValueError(scaling)
    rank=numerical_rank_from_singular_values(s,M.shape)
    return rank,s,float(s[0]/s[-1]) if rank==7 else np.inf

def complex_step_check():
    c=W250["c1"]
    p=np.array([-1.05,0.0032,7e-5,-1.5e-4,13.23,0.02,1e-4])
    A=jacobian_airfed(c["I"],c["T"],W250_META["A_cm2"],W250_META["l_um"],
                      W250_META["Jmax_Acm2"],W250_META["Ncell"],p[4],c["PC"])
    B=complex_step_jacobian_airfed(p,c["I"],c["T"],W250_META["A_cm2"],W250_META["l_um"],
                                   W250_META["Jmax_Acm2"],W250_META["Ncell"],c["PC"])
    d=max_relative_column_discrepancy(A,B)
    assert d<1e-12
    print(f"COMPLEX-STEP max relative column discrepancy={d:.16e}")

def rank_and_observation_count_matched_check():
    d=designs(13.23)
    expected={"c1":5,"c2":5,"c2+c3+c4":6,"c1+c2":7,"all four":7}
    for name,r0 in expected.items():
        r,s,c=svd_summary(d[name])
        assert r==r0
        print(f"{name}: rank={r}, cond2={c if np.isfinite(c) else 'singular'}")
    c12=svd_summary(d["c1+c2"])[2]
    call=svd_summary(d["all four"])[2]
    c30=svd_summary(balanced_30(13.23))[2]
    c123=svd_summary(d["c1+c2+c3"])[2]
    assert np.isclose(c12,1.97849689e8,rtol=5e-6)
    assert np.isclose(call,4.518837e2,rtol=5e-5)
    assert np.isclose(c30,447.223138834,rtol=5e-9)
    assert np.isclose(c123,409.652944671,rtol=5e-9)
    print(f"observation-count-matched four-condition 30: rank=7, cond2={c30:.9f}")

def lambda_and_scaling_check():
    vals=np.linspace(BOUNDS["lambda"][0],BOUNDS["lambda"][1],501)
    acc={("c1+c2","column"):[],("all four","column"):[],("balanced30","column"):[],
         ("c1+c2","box"):[],("all four","box"):[],("balanced30","box"):[]}
    ranks={"c1":set(),"c2":set(),"c2+c3+c4":set()}
    for lam in vals:
        d=designs(float(lam)); b=balanced_30(float(lam))
        for n in ranks: ranks[n].add(svd_summary(d[n])[0])
        for n,M in (("c1+c2",d["c1+c2"]),("all four",d["all four"]),("balanced30",b)):
            for sc in ("column","box"):
                r,s,c=svd_summary(M,sc)
                assert r==7
                acc[(n,sc)].append(c)
    assert ranks=={"c1":{5},"c2":{5},"c2+c3+c4":{6}}
    for k,v in acc.items():
        print(f"lambda sweep {k}: min={min(v):.6g}, max={max(v):.6g}")
    assert min(acc[("c1+c2","column")])>1e8
    assert max(acc[("all four","column")])<600
    assert max(acc[("balanced30","column")])<600
    assert min(acc[("c1+c2","box")])>1e8
    assert max(acc[("all four","box")])<1e4
    assert max(acc[("balanced30","box")])<1e4

def extrapolation_check():
    delta=3e-4; dT=10.0
    cell=abs(dT*delta); stack=BALLARD_META["Ncell"]*cell
    assert np.isclose(cell,0.003) and np.isclose(stack,0.105)
    print(f"10 K ambiguity for delta=3e-4: {cell:.3f} V/cell; {stack:.3f} V/stack")

if __name__=="__main__":
    ballard_full_model_check()
    complex_step_check()
    rank_and_observation_count_matched_check()
    lambda_and_scaling_check()
    extrapolation_check()
    print("REPRODUCTION: PASS")
