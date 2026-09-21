#!/usr/bin/env bash

set -eu

PROFDIR=${1:-profiles}
GRIDDIR=${2:-grids}
OUT=${3:-auxiliary.txt}

AGE=${GRIDDIR}/age.nc
SED=${GRIDDIR}/globsed.nc
for g in "${AGE}" "${SED}"; do
    [ -f "${g}" ] || { echo "missing grid: ${g}" >&2; exit 1; }
done

printf 'trench profile lon lat age_Ma sed_m\n' > "${OUT}"

for f in "${PROFDIR}"/*.txt; do
    t=$(basename "${f}" .txt)

    awk '/^>/ {n++; next} $3 == 0 {print $1, $2, n-1}' "${f}" > _axis.tmp
    cut -d' ' -f1,2 _axis.tmp |
        gmt grdtrack -G"${AGE}" -G"${SED}" -fg |
        paste -d' ' <(cut -d' ' -f3 _axis.tmp) - |
        awk -v t="${t}" '{print t, $0}' >> "${OUT}"
done
rm -f _axis.tmp

echo "sampled $(( $(wc -l < "${OUT}") - 1 )) profile locations -> ${OUT}"
