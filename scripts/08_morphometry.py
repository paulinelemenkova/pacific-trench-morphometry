#!/usr/bin/env python3
# Python routine computing the morphometric parameter vector of a single profile: axial depth, width, flank gradients, asymmetry index, cross-sectional area and forebulge geometry.
"""Morphometric parameters of a single trench cross-profile."""
import numpy as np

DZ_ISOBATH = 1000.0   # m below the abyssal reference: the level for W and theta
FAR_KM = 200.0        # distance beyond which the profile is taken as abyssal

trapezoid = getattr(np, "trapezoid", None) or np.trapz   # renamed in NumPy 2.0

def _first_crossing(x, z, level):
    """Distance from the axis at which one flank first rises above `level`."""
    order = np.argsort(np.abs(x))
    x, z = x[order], z[order]
    above = np.flatnonzero(z > level)
    return np.abs(x[above[0]]) if above.size else np.nan

def parameters(dist_km, depth_m, landward=-1):
    """Return the eight quantities of Table 3 for one profile.

    dist_km  signed distance from the trench axis, km
    depth_m  depth below sea level, m (negative downwards)
    landward -1 or +1, the sign of `dist_km` on the landward side
    """
    x, z = np.asarray(dist_km, float), np.asarray(depth_m, float)
    if np.isnan(z).any():
        return None                                  # incomplete window

    axis = np.argmin(z)
    z_a = z[axis]
    x = x - x[axis]                                  # re-centre on the minimum

    land, sea = x * landward > 0, x * landward < 0
    far = sea & (np.abs(x) > FAR_KM)                 # abyssal plain, seaward
    z_r = np.median(z[far])                          # abyssal reference level
    level = z_r - DZ_ISOBATH                         # reference isobath
    d_l = _first_crossing(x[land], z[land], level)
    d_s = _first_crossing(x[sea], z[sea], level)
    W = d_l + d_s

    dz = abs(level - z_a)                            # Eq. 1
    theta_l = np.degrees(np.arctan(dz / (d_l * 1e3)))
    theta_s = np.degrees(np.arctan(dz / (d_s * 1e3)))
    A = (theta_l - theta_s) / (theta_l + theta_s)    # Eq. 2

    inside = (x > -d_l) & (x < d_s) if landward < 0 else (x > -d_s) & (x < d_l)
    S = trapezoid(z_r - z[inside], x[inside]) / 1e3   # Eq. 3, km^2

    outer = sea & (np.abs(x) > d_s)                  # seaward of the trench
    crest = np.argmax(z[outer])
    h_f = z[outer][crest] - z_r
    d_f = abs(x[outer][crest])

    return dict(z_a=z_a, W=W, theta_l=theta_l, theta_s=theta_s,
                A=A, S=S, h_f=h_f, d_f=d_f)
