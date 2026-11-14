"""Gauge-fixing and prior/regularization dependence along the Ballard exact orbit."""
from __future__ import annotations
import sys
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from src.pemfc_identifiability import delta_interval
from scripts.reproduce_v7 import BALLARD_THRO, BALLARD_T, BALLARD_V, full_ballard_voltage

OUT=ROOT/'outputs'
OUT.mkdir(exist_ok=True)

BOUNDS={
    'xi1':(-1.19969,-0.8532),
    'xi2':(1.0e-3,5.0e-3),
}

theta0=BALLARD_THRO.copy()
v=np.array([-BALLARD_T,1.0])
lo,hi=delta_interval(theta0[0],theta0[1],BALLARD_T)
mid=np.array([(BOUNDS['xi1'][0]+BOUNDS['xi1'][1])/2,
              (BOUNDS['xi2'][0]+BOUNDS['xi2'][1])/2])
width=np.array([BOUNDS['xi1'][1]-BOUNDS['xi1'][0],
                BOUNDS['xi2'][1]-BOUNDS['xi2'][0]])

def select(mu,precision):
    delta=-float(v@precision@(theta0[:2]-mu))/float(v@precision@v)
    return float(np.clip(delta,lo,hi))

rules=[
    ('Published THRO representative',0.0),
    ('Raw-coordinate L2 toward zero',select(np.zeros(2),np.eye(2))),
    ('Raw-coordinate L2 toward box midpoint',select(mid,np.eye(2))),
    ('Box-normalized L2 toward box midpoint',select(mid,np.diag(1.0/width**2))),
]

v0=full_ballard_voltage(theta0)
sse0=float(np.sum((BALLARD_V-v0)**2))
rows=[]
for name,delta in rules:
    p=theta0.copy()
    p[0]=theta0[0]-BALLARD_T*delta
    p[1]=theta0[1]+delta
    pred=full_ballard_voltage(p)
    dv=float(np.max(np.abs(pred-v0)))
    dsse=float(np.sum((BALLARD_V-pred)**2)-sse0)
    assert dv==0.0
    assert dsse==0.0
    rows.append(dict(selection_rule=name,delta=delta,xi1=p[0],xi2=p[1],
                     max_abs_voltage_difference=dv,delta_SSE=dsse))

pd.DataFrame(rows).to_csv(OUT/'gauge_fixing_representatives.csv',index=False)
with open(OUT/'REPRODUCTION_V12_GAUGE.txt','w',encoding='utf-8') as f:
    f.write('PROJECT53 V12 GAUGE-FIXING REPRODUCTION\n')
    f.write(f'feasible_delta=[{lo:.15e},{hi:.15e}]\n')
    for r in rows:
        f.write(f"{r['selection_rule']}: delta={r['delta']:.15e}, xi1={r['xi1']:.15e}, xi2={r['xi2']:.15e}, max_dV={r['max_abs_voltage_difference']:.1e}, dSSE={r['delta_SSE']:.1e}\n")
    f.write('PASS\n')
print('GAUGE FIXING: PASS')
