#!/usr/bin/env bash
# Snapping the seeded trace to the local depth minimum to obtain the trench axis.
# seed -> constant along-track spacing -> perpendicular search profiles
gmt sample1d seed.txt -Af -T10k -fg > seed_nodes.txt
gmt grdtrack seed_nodes.txt -Ggebco_pacific.nc -C120k/0.5k+v -fg > search.txt
# the deepest sample on each search profile is the axis node
awk '/^>/ {if (h) print bx, by; h=0; b=1e30; next}
     $5 != "NaN" && $5 < b {b=$5; bx=$1; by=$2; h=1}
     END {if (h) print bx, by}' search.txt > axis_raw.txt
# smooth: filter1d needs the independent variable in a column, so along-track
# distance is computed first and the median filter applied to it
gmt mapproject axis_raw.txt -G+uk -fg |
    gmt filter1d -Fm25 -N2 | awk '{print $1, $2}' > axis.txt
