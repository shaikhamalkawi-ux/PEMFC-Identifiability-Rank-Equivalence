"""Reproduce the parameter-symmetry and nullspace-principal-angle diagnostics."""
from __future__ import annotations
import sys, itertools
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from data.benchmark_data import W250, W250_META
from src.pemfc_identifiability import jacobian_airfed, normalized_svd

OUT = ROOT / "outputs"
FIG = ROOT / "figures"
OUT.mkdir(exist_ok=True); FIG.mkdir(exist_ok=True)

A=W250_META["A_cm2"]; L=W250_META["l_um"]; JMAX=W250_META["Jmax_Acm2"]; NCELL=W250_META["Ncell"]
LAM=13.23
BOUNDS={"xi1":(-1.19969,-0.8532),"xi2":(1e-3,5e-3),"xi3":(3.6e-5,9.8e-5),
        "xi4":(-26e-5,-9.54e-5),"lambda":(10.,24.),"beta":(0.0136,0.5),"Rc":(1e-4,8e-4)}
D=np.array([BOUNDS[k][1]-BOUNDS[k][0] for k in ("xi1","xi2","xi3","xi4","lambda","beta","Rc")])

def build(n):
    c=W250[n]
    return jacobian_airfed(c["I"],c["T"],A,L,JMAX,NCELL,LAM,c["PC"])
J={n:build(n) for n in ("c1","c2","c3","c4")}

def rank(M):
    s=np.linalg.svd(M,compute_uv=False); tol=s[0]*max(M.shape)*np.finfo(float).eps
    return int(np.sum(s>tol))
def null_basis(M):
    _,_,vt=np.linalg.svd(M,full_matrices=True); return vt[rank(M):].T
def angles(B1,B2):
    sv=np.linalg.svd(B1.T@B2,compute_uv=False); return np.sort(np.arccos(np.clip(sv,-1,1)))
def box_null(M): return null_basis(M*D.reshape(1,-1))
def box_cond(M):
    s=np.linalg.svd(M*D.reshape(1,-1),compute_uv=False); r=rank(M*D.reshape(1,-1))
    return float(s[0]/s[-1]) if r==7 else np.inf
def col_cond(M):
    s=normalized_svd(M)
    return float(s[0]/s[-1]) if rank(M/np.linalg.norm(M,axis=0,keepdims=True))==7 else np.inf

Bhi=box_null(J["c1"]); rows=[]
for n in (1,2,3):
    for subset in itertools.combinations(("c2","c3","c4"),n):
        low=np.vstack([J[x] for x in subset]); Blo=box_null(low); th=angles(Bhi,Blo)
        M=np.vstack([J["c1"],low])
        rows.append({"design":"c1+"+"+".join(subset),"low_block_rank":rank(low*D.reshape(1,-1)),
                     "low_block_nullity":Blo.shape[1],"smallest_principal_angle_deg":float(np.degrees(th[0])),
                     "parameter_box_cond2":box_cond(M),"column_normalized_cond2":col_cond(M)})
df=pd.DataFrame(rows)
df.to_csv(OUT/"nullspace_principal_angles_and_conditioning.csv",index=False)

gen=[]
for name in ("c1","c2","c3","c4"):
    c=W250[name]; T=c["T"]; Pc=c["PC"]
    d=T-273.15; ph2o=10**(29.5e-3*d-91.8e-6*d*d+14.4e-8*d**3-2.18)
    gamma=0.291/(T**0.832*A)
    a=np.log((Pc-ph2o)/((1+0.79/0.21)*5.08e6))+498/T; b=-gamma
    v1=np.array([-T,1,0,0,0,0,0.]); v2=np.array([-T*a,0,1,0,0,0,T*b])
    M=J[name]
    rel=lambda v: np.linalg.norm(M@v)/(np.linalg.norm(M)*np.linalg.norm(v))
    gen.append({"condition":name,"T_K":T,"a":a,"b_per_A":b,
                "Jv1_relative_residual":rel(v1),"Jv2_relative_residual":rel(v2)})
pd.DataFrame(gen).to_csv(OUT/"lie_generator_null_residuals.csv",index=False)
assert max(max(x["Jv1_relative_residual"],x["Jv2_relative_residual"]) for x in gen)<1e-12

fig,ax=plt.subplots(figsize=(7.2,4.8))
ax.scatter(df["smallest_principal_angle_deg"],df["parameter_box_cond2"])
for _,r in df.iterrows():
    ax.annotate(r["design"],(r["smallest_principal_angle_deg"],r["parameter_box_cond2"]),
                xytext=(4,4),textcoords="offset points",fontsize=8)
ax.set_xscale("log"); ax.set_yscale("log")
ax.set_xlabel("Smallest principal angle between box-scaled nullspaces (degrees)")
ax.set_ylabel(r"Parameter-box-scaled $\mathrm{cond}_2$")
ax.set_title("Near-common nullspaces and practical conditioning")
ax.grid(True,which="both",alpha=.3); fig.tight_layout()
fig.savefig(FIG/"Figure_S1_Principal_Angle_vs_Conditioning.png",dpi=300)
fig.savefig(FIG/"Figure_S1_Principal_Angle_vs_Conditioning.pdf")
plt.close(fig)

lookup=df.set_index("design")
assert np.isclose(lookup.loc["c1+c2","smallest_principal_angle_deg"],1.69e-4,rtol=1e-2)
assert np.isclose(lookup.loc["c1+c2+c3","smallest_principal_angle_deg"],0.377286,rtol=1e-5)
assert lookup.loc["c1+c2","column_normalized_cond2"]>1e8
assert lookup.loc["c1+c2+c3","column_normalized_cond2"]<1000
print(df.to_string(index=False))
print("SYMMETRY/NULLSPACE GEOMETRY: PASS")
