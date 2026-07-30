#!/usr/bin/env bash
# Shifting the sediment-thickness grid to the 0--360 longitude convention used throughout.
gmt grdedit GlobSed-v3.nc -L+p -Gglobsed_360.nc
