#!/usr/bin/env bash
# Batch driver looping the profile extraction over all twenty trenches.
# Run the profile extraction (extract_profiles.sh) over all twenty trenches.
#
#   bash batch_extract.sh gebco.nc axes/ profiles/
#
# `axes/` holds one digitised axis per trench, named <trench>.txt; the profile
# tables are written to `profiles/` under the same names.
set -eu

GRID=${1:?bathymetric grid}
AXISDIR=${2:-axes}
OUTDIR=${3:-profiles}
mkdir -p "${OUTDIR}"

TRENCHES="aleutian kuril-kamchatka japan izu-bonin mariana yap palau ryukyu
          manila philippine new_britain san_cristobal vityaz new_hebrides
          tonga kermadec hikurangi puysegur middle_america peru-chile"

printf '%-18s %10s %10s\n' trench profiles status
for t in ${TRENCHES}; do
    axis="${AXISDIR}/${t}.txt"
    out="${OUTDIR}/${t}.txt"
    if [ ! -f "${axis}" ]; then
        printf '%-18s %10s %10s\n' "${t}" - "no axis"
        continue
    fi
    if bash extract_profiles.sh "${GRID}" "${axis}" "${out}" > /dev/null 2>&1; then
        n=$(grep -c '^>' "${out}")
        printf '%-18s %10d %10s\n' "${t}" "${n}" ok
    else
        printf '%-18s %10s %10s\n' "${t}" - failed
    fi
done

echo
echo "total profiles: $(cat ${OUTDIR}/*.txt | grep -c '^>')"
