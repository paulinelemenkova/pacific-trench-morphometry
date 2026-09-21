#!/usr/bin/env bash

gmt grdcut GEBCO_2023.nc -R100/300/-58/66 -Ggebco_pacific.nc
gmt grdinfo gebco_pacific.nc
