#!/usr/bin/env bash
# Cutting the Pacific subset from the global bathymetric grid.
# 100E-60W, 58S-66N: the box containing every trench axis and its 250 km flanks
gmt grdcut GEBCO_2023.nc -R100/300/-58/66 -Ggebco_pacific.nc
gmt grdinfo gebco_pacific.nc   # confirm x_inc = 0.0041667 (15 sec), z_min ~ -10900 m
