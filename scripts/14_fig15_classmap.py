#!/usr/bin/env python3

import pandas as pd
import pygmt

REGION = [100, 300, -58, 66]
PROJ = "M17c"
CLASS_COLOURS = ["#1f78b4", "#33a02c", "#e66101", "#6a3d9a", "#b15928"]

df = pd.read_csv("morphometry_classified.csv")
classes = sorted(df["class"].unique())

fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="8p,Helvetica", FONT_LABEL="9p,Helvetica",
             FONT_TITLE="11p,Helvetica-Bold", MAP_FRAME_TYPE="plain",
             MAP_GRID_PEN_PRIMARY="0.25p,white", MAP_TITLE_OFFSET="6p")

fig.coast(region=REGION, projection=PROJ, land="gray85", water="#dce9f2",
          shorelines="0.2p,gray40", resolution="i")
fig.plot(data="data/pb2002_other.txt", pen="0.3p,gray65")

for c, colour in zip(classes, CLASS_COLOURS):
    sub = df[df["class"] == c]
    fig.plot(x=sub["lon"], y=sub["lat"], style="c0.07c", fill=colour,
             pen="0.1p,white", label=f"Class {c} (n = {len(sub)})")

fig.basemap(frame=["WESN+tMorphometric classes of the Pacific trenches",
                   "xa20f10g20", "ya20f10g20"])
fig.basemap(map_scale="jBL+w3000k+f+o0.5c/0.5c+u")
fig.basemap(rose="jTR+w0.8c+f2+l,,,N+o0.5c/0.5c")
fig.legend(position="JBC+w17c+o0c/0.8c", box="+gwhite@20+p0.4p,gray50+r")

fig.text(x=REGION[0] + 8, y=-62, justify="TL", no_clip=True,
         font="7p,Helvetica,gray20",
         text="Plate boundaries: Bird (2003). Bathymetry: GEBCO. "
              "Software used for plotting figure: GMT 6.6.0. Source: authors.")

fig.savefig("fig15_classmap.pdf")
fig.savefig("fig15_classmap.png", dpi=600)
print(f"plotted {len(df)} profiles in {len(classes)} classes")
