#!/usr/bin/env bash

gmt begin seed_manila png
    gmt grdimage gebco_pacific.nc -R118.6/120.3/12.8/20.3 -JM12c -Cgeo -I+d
    gmt plot seeds/manila.txt -W1.5p,red -Sc0.1c -Gred
    gmt coast -W0.2p -Ba
gmt end show
