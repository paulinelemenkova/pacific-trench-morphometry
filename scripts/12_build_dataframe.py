#!/usr/bin/env python3

import os
import sys
import numpy as np
import pandas as pd

from morphometry import parameters

PROFILE_DIR = os.environ.get("PROFILE_DIR", "profiles")
AUXILIARY = os.environ.get("AUXILIARY", "auxiliary.txt")
OUT = os.environ.get("OUT", "morphometry.csv")

LANDWARD = {t: -1 for t in [
    "aleutian", "kuril-kamchatka", "japan", "izu-bonin", "mariana", "yap",
    "palau", "ryukyu", "manila", "philippine", "new_britain", "san_cristobal",
    "vityaz", "new_hebrides", "tonga", "kermadec", "hikurangi", "puysegur"]}
LANDWARD.update({"middle_america": +1, "peru-chile": +1})

def read_profiles(path):
    seg, k = [], -1
    for line in open(path):
        if line.startswith(">"):
            if len(seg) > 1:
                a = np.array(seg)
                yield k, a[:, 0], a[:, 1]
            seg, k = [], k + 1
        elif line.strip():
            f = line.split()
            seg.append((float(f[2]), float(f[4])))
    if len(seg) > 1:
        a = np.array(seg)
        yield k, a[:, 0], a[:, 1]

rows, rejected = [], {"window": 0, "axis": 0}
for fn in sorted(os.listdir(PROFILE_DIR)):
    if not fn.endswith(".txt"):
        continue
    trench = os.path.splitext(fn)[0]
    lw = LANDWARD.get(trench)
    if lw is None:
        print(f"skipped {trench}: no landward sign", file=sys.stderr)
        continue
    for k, dist, depth in read_profiles(os.path.join(PROFILE_DIR, fn)):
        if np.isnan(depth).any():
            rejected["window"] += 1
            continue
        if abs(dist[np.argmin(depth)]) > 1.0:
            rejected["axis"] += 1
            continue
        p = parameters(dist, depth, landward=lw)
        if p is None:
            rejected["window"] += 1
            continue
        rows.append(dict(trench=trench, profile=k, **p))

df = pd.DataFrame(rows)

if os.path.exists(AUXILIARY):
    aux = pd.read_csv(AUXILIARY, sep=r"\s+")
    df = df.merge(aux, on=["trench", "profile"], how="left")
else:
    print(f"note: {AUXILIARY} not found, auxiliary columns omitted",
          file=sys.stderr)

df.to_csv(OUT, index=False)
print(f"retained {len(df)} profiles from {df['trench'].nunique()} trenches")
print(f"rejected {rejected['window']} for incomplete windows, "
      f"{rejected['axis']} for axis mismatch")
print(f"written to {OUT}")
