#!/usr/bin/env python3

import numpy as np
import pandas as pd
from scipy import stats

MORPH = ["z_a", "W", "theta_l", "theta_s", "A", "S", "h_f", "d_f"]
SUBD = ["age_Ma", "sed_m"]
ALPHA = 0.05

def effective_n(x):
    x = np.asarray(x, float)
    x = x[~np.isnan(x)]
    n = x.size
    if n < 3:
        return n
    r1 = np.corrcoef(x[:-1], x[1:])[0, 1]
    r1 = min(max(r1, 0.0), 0.99)
    return max(n * (1.0 - r1) / (1.0 + r1), 2.0)

def spearman_eff(x, y):
    m = ~(np.isnan(x) | np.isnan(y))
    rho, _ = stats.spearmanr(x[m], y[m])
    n_eff = min(effective_n(x[m]), effective_n(y[m]))
    if n_eff > 2 and abs(rho) < 1:
        t = rho * np.sqrt((n_eff - 2) / (1 - rho ** 2))
        p = 2 * stats.t.sf(abs(t), df=n_eff - 2)
    else:
        p = np.nan
    return rho, p, n_eff

def benjamini_hochberg(p):
    p = np.asarray(p, float)
    order = np.argsort(p)
    ranked = p[order] * len(p) / (np.arange(len(p)) + 1)
    ranked = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty_like(ranked)
    out[order] = np.clip(ranked, 0, 1)
    return out

df = pd.read_csv("morphometry_classified.csv")

rows = []
for m in MORPH:
    for svar in SUBD:
        if svar not in df:
            continue
        rho, p, n_eff = spearman_eff(df[m].to_numpy(), df[svar].to_numpy())
        rows.append(dict(morphometric=m, subduction=svar, rho=rho,
                         n=df[[m, svar]].dropna().shape[0], n_eff=n_eff, p=p))
corr = pd.DataFrame(rows)
corr["p_adj"] = benjamini_hochberg(corr["p"].fillna(1.0))

rows = []
for svar in SUBD:
    if svar not in df:
        continue
    groups = [g[svar].dropna().to_numpy() for _, g in df.groupby("class")]
    groups = [g for g in groups if g.size > 1]
    H, p = stats.kruskal(*groups)
    n_eff = sum(effective_n(g) for g in groups)
    rows.append(dict(variable=svar, H=H, k=len(groups),
                     n=sum(g.size for g in groups), n_eff=n_eff, p=p))
kw = pd.DataFrame(rows)
kw["p_adj"] = benjamini_hochberg(kw["p"].fillna(1.0))

corr.to_csv("table_correlations.csv", index=False)
kw.to_csv("table_kruskal.csv", index=False)
print(corr.round(3).to_string(index=False))
print()
print(kw.round(3).to_string(index=False))
print(f"\nsignificant after correction at alpha = {ALPHA}: "
      f"{(corr['p_adj'] < ALPHA).sum()} of {len(corr)} correlations, "
      f"{(kw['p_adj'] < ALPHA).sum()} of {len(kw)} class tests")
