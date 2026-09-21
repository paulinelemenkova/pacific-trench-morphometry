#!/usr/bin/env bash

set -eu

GRID=${1:?bathymetric grid}
AXIS=${2:?digitised trench axis}
OUT=${3:?output table}

SPACING=10k
HALFLEN=250k
STEP=1k
LENGTH=500k

gmt sample1d "${AXIS}" -Af -T${SPACING} -fg > axis_nodes.txt

gmt grdtrack axis_nodes.txt -G"${GRID}" -C${LENGTH}/${STEP}+v -fg > "${OUT}"

printf 'nodes: %d  profiles: %d\n' \
    "$(grep -cv '^>' axis_nodes.txt)" "$(grep -c '^>' "${OUT}")"
