#!/usr/bin/env bash
# Drawing the two-panel coverage figure.
REG=100/300/-58/66   # the study region, 0-360 convention
gmt grdcut age_global.nc -R${REG} -Gage_pacific.nc

gmt begin fig03_datacoverage pdf,png A+m0.2c
  gmt subplot begin 2x1 -Fs11c/6.4c -M0.15c/0.45c -R${REG} -JQ11c \
              -A"(a)"+jTL+o0.15c/0.15c -Bwesn

    gmt subplot set 0  # (a) age of the oceanic lithosphere
      gmt makecpt -Cbatlow -T0/180/10 -H > age.cpt
      gmt grdimage age_pacific.nc -Cage.cpt -nn
      gmt coast -Ggray80 -W0.15p,gray40
      gmt plot data/pb2002_subduction.txt -W0.7p,black
      gmt basemap -Bxa40f20g40 -Bya30f15g30 -BWsne
      gmt colorbar -Cage.cpt -DJMR+w5.4c/0.22c+o0.35c/0c+ml -Bxa60f20+l"Age (Ma)"

    gmt subplot set 1 # (b) total sediment thickness
      gmt makecpt -Cbamako -T0/3000/250 -I -H > sed.cpt
      gmt grdimage globsed_360.nc -Csed.cpt -nn
      gmt coast -Ggray80 -W0.15p,gray40
      gmt plot data/pb2002_subduction.txt -W0.7p,black
      gmt basemap -Bxa40f20g40 -Bya30f15g30 -BWSne
      gmt colorbar -Csed.cpt -DJMR+w5.4c/0.22c+o0.35c/0c+ml \
                   -Bxa1000f250+l"Sediment thickness (m)"
  gmt subplot end
gmt end
