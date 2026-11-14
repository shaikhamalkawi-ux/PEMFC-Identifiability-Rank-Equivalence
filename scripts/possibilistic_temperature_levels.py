from __future__ import annotations
import math, sys
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from data.benchmark_data import W250,W250_META
from src.pemfc_identifiability import jacobian_airfed,normalized_svd,numerical_rank_from_singular_values

OUT=ROOT/'outputs'/'fuzzy_possibilistic_levels'
OUT.mkdir(parents=True,exist_ok=True)
A=W250_META['A_cm2']; L=W250_META['l_um']; JMAX=W250_META['Jmax_Acm2']; NCELL=W250_META['Ncell']; LAM=13.23
MATCHED={'c1':[0,2,4,6,8,10,12,14],'c2':[0,2,4,6,8,10,12,14],'c3':[0,2,5,7,9,12,14],'c4':[0,2,5,7,9,12,14]}
TH0=W250['c1']['T']; TL0=W250['c2']['T']; GAP=TH0-TL0

def J(k,T):
    c=W250[k]
    return jacobian_airfed(c['I'],T,A,L,JMAX,NCELL,LAM,c['PC'])

def summarize(M):
    s=normalized_svd(M); r=numerical_rank_from_singular_values(s,M.shape)
    return r,(float(s[0]/s[-1]) if r==7 else math.inf),float(s[-1])

def matrices(th,tl):
    two=np.vstack([J('c1',th),J('c2',tl)])
    matched=np.vstack([J('c1',th)[MATCHED['c1']],J('c2',tl)[MATCHED['c2']],J('c3',tl)[MATCHED['c3']],J('c4',tl)[MATCHED['c4']]])
    return two,matched

def scan(alpha,h,n=81):
    hw=h*(1-alpha)
    hs=np.linspace(TH0-hw,TH0+hw,n) if hw>0 else np.array([TH0])
    ls=np.linspace(TL0-hw,TL0+hw,n) if hw>0 else np.array([TL0])
    rec={'two_ranks':set(),'four_ranks':set(),'two_min':math.inf,'two_max':0.0,'four_min':math.inf,'four_max':0.0}
    for th in hs:
        for tl in ls:
            M2,M4=matrices(th,tl)
            r2,c2,_=summarize(M2); r4,c4,_=summarize(M4)
            rec['two_ranks'].add(r2); rec['four_ranks'].add(r4)
            if math.isfinite(c2): rec['two_min']=min(rec['two_min'],c2); rec['two_max']=max(rec['two_max'],c2)
            if math.isfinite(c4): rec['four_min']=min(rec['four_min'],c4); rec['four_max']=max(rec['four_max'],c4)
    rec['gap']=rec['two_min']/rec['four_max'] if math.isfinite(rec['two_min']) and rec['four_max']>0 else np.nan
    return rec

def ranks(s): return '/'.join(map(str,sorted(s)))

h_primary=4.9
rows=[]
for alpha in [0,.25,.5,.75,1.0]:
    rec=scan(alpha,h_primary,81)
    d=max(0.0,GAP-2*h_primary*(1-alpha))
    rows.append(dict(alpha=alpha,h_K=h_primary,min_level_separation_K=d,
                     two_rank_set=ranks(rec['two_ranks']),two_cond_min=rec['two_min'],two_cond_max=rec['two_max'],
                     matched_four_rank_set=ranks(rec['four_ranks']),matched_four_cond_min=rec['four_min'],matched_four_cond_max=rec['four_max'],
                     conservative_gap=rec['gap']))
alpha_df=pd.DataFrame(rows); alpha_df.to_csv(OUT/'alpha_cut_level_grid_h4p9.csv',index=False)

srows=[]
for h in [0.0,0.5,1,2,3,4,4.5,4.9,5.0]:
    rec=scan(0,h,61 if h<5 else 81)
    pi_eq=0.0 if h<=5 else 1-5/h
    srows.append(dict(h_K=h,min_support_separation_K=max(0,GAP-2*h),possibility_exact_temperature_coincidence=pi_eq,
                      necessity_temperature_distinct=1-pi_eq,two_rank_set=ranks(rec['two_ranks']),two_cond_min=rec['two_min'],two_cond_max=rec['two_max'],
                      matched_four_rank_set=ranks(rec['four_ranks']),matched_four_cond_min=rec['four_min'],matched_four_cond_max=rec['four_max'],conservative_gap=rec['gap']))
support_df=pd.DataFrame(srows); support_df.to_csv(OUT/'support_level_sweep.csv',index=False)

crows=[]
for T in np.linspace(335.15,361.15,53):
    r1=summarize(J('c2',T))[0]
    rsame=summarize(np.vstack([J(k,T) for k in ('c2','c3','c4')]))[0]
    crows.append(dict(T_K=T,single_condition_rank=r1,same_temperature_three_pressure_rank=rsame))
pd.DataFrame(crows).to_csv(OUT/'common_level_structural_check.csv',index=False)

fig,ax=plt.subplots(figsize=(7.2,4.8))
a=alpha_df.alpha.to_numpy()
ax.fill_between(a,alpha_df.two_cond_min,alpha_df.two_cond_max,alpha=.18,label='c1+c2 sampled range')
ax.plot(a,alpha_df.two_cond_min,marker='o'); ax.plot(a,alpha_df.two_cond_max,marker='s')
ax.fill_between(a,alpha_df.matched_four_cond_min,alpha_df.matched_four_cond_max,alpha=.18,label='matched four-condition sampled range')
ax.plot(a,alpha_df.matched_four_cond_min,marker='^'); ax.plot(a,alpha_df.matched_four_cond_max,marker='D')
ax.set_yscale('log'); ax.set_xlabel(r'$\alpha$'); ax.set_ylabel(r'Column-normalized $\mathrm{cond}_2$')
ax.set_title(r'Possibilistic temperature-level stress test ($h=4.9$ K)')
ax.grid(True,which='both',alpha=.3); ax.legend(fontsize=8); fig.tight_layout()
fig.savefig(OUT/'Figure_4_Possibilistic_Temperature_Levels.png',dpi=300); fig.savefig(OUT/'Figure_4_Possibilistic_Temperature_Levels.pdf'); plt.close(fig)

assert set(alpha_df.two_rank_set)=={'7'}
assert set(alpha_df.matched_four_rank_set)=={'7'}
assert alpha_df.conservative_gap.min()>3000
h49=support_df[support_df.h_K==4.9].iloc[0]
assert h49.two_rank_set=='7' and h49.matched_four_rank_set=='7' and h49.conservative_gap>3000
h5=support_df[support_df.h_K==5.0].iloc[0]
assert '6' in h5.two_rank_set and '6' in h5.matched_four_rank_set
assert all(x==5 for x in pd.read_csv(OUT/'common_level_structural_check.csv').single_condition_rank)
assert all(x==6 for x in pd.read_csv(OUT/'common_level_structural_check.csv').same_temperature_three_pressure_rank)

print('POSSIBILISTIC TEMPERATURE-LEVEL STRESS: PASS')
print(alpha_df.to_string(index=False))
print(support_df.to_string(index=False))
