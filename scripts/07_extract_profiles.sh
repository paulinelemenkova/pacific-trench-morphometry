#!/usr/bin/env bash
# GMT routine casting trench-normal profiles along a digitised axis at fixed spacing and half-length, and sampling the bathymetric grid along each of them.
# Trench-normal profiles from the bathymetric grid, one trench at a time.
# Criteria of Section 4.3: 10 km spacing, 250 km half-length, 1 km sampling.
set -eu

GRID=${1:?bathymetric grid}          # e.g. gebco_pacific.nc
AXIS=${2:?digitised trench axis}     # lon lat, one trench
OUT=${3:?output table}

SPACING=10k                          # between successive profiles
HALFLEN=250k                         # either side of the axis
STEP=1k                              # sampling along each profile
LENGTH=500k                          # 2 x HALFLEN, as grdtrack expects

# 1. resample the axis, which arrives already traced and smoothed, at a
#    constant along-track interval
gmt sample1d "${AXIS}" -Af -T${SPACING} -fg > axis_nodes.txt

# 3. cast one cross-profile per node, perpendicular to the local strike, and
#    sample the grid along it. Columns: lon lat dist azimuth depth
gmt grdtrack axis_nodes.txt -G"${GRID}" -C${LENGTH}/${STEP}+v -fg > "${OUT}"

printf 'nodes: %d  profiles: %d\n' \
    "$(grep -cv '^>' axis_nodes.txt)" "$(grep -c '^>' "${OUT}")"
