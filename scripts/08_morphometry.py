#!/usr/bin/env python3

import numpy as np

DZ_ISOBATH = 1000.0
FAR_KM = 200.0

trapezoid = getattr(np, "trapezoid", None) or np.trapz

def _first_crossing(x, z, level):
    order = np.argsort(np.abs(x))
    x, z = x[order], z[order]
    above = np.flatnonzero(z > level)
    return np.abs(x[above[0]]) if above.size else np.nan

def parameters(dist_km, depth_m, landward=-1):
    x, z = np.asarray(dist_km, float), np.asarray(depth_m, float)
    if np.isnan(z).any():
        return None

    axis = np.argmin(z)
    z_a = z[axis]
    x = x - x[axis]

    land, sea = x * landward > 0, x * landward < 0
    far = sea & (np.abs(x) > FAR_KM)
    z_r = np.median(z[far])
    level = z_r - DZ_ISOBATH
    d_l = _first_crossing(x[land], z[land], level)
    d_s = _first_crossing(x[sea], z[sea], level)
    W = d_l + d_s

    dz = abs(level - z_a)
    theta_l = np.degrees(np.arctan(dz / (d_l * 1e3)))
    theta_s = np.degrees(np.arctan(dz / (d_s * 1e3)))
    A = (theta_l - theta_s) / (theta_l + theta_s)

    inside = (x > -d_l) & (x < d_s) if landward < 0 else (x > -d_s) & (x < d_l)
    S = trapezoid(z_r - z[inside], x[inside]) / 1e3

    outer = sea & (np.abs(x) > d_s)
    crest = np.argmax(z[outer])
    h_f = z[outer][crest] - z_r
    d_f = abs(x[outer][crest])

    return dict(z_a=z_a, W=W, theta_l=theta_l, theta_s=theta_s,
                A=A, S=S, h_f=h_f, d_f=d_f)
