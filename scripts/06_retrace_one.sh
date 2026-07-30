#!/usr/bin/env bash
# Re-tracing one trench with adjusted settings, leaving the others untouched.
sed -i '' 's|^manila .*|manila            SEED    118.6   119.9    12.8    20.3|' trenches.conf
grep '^manila' trenches.conf > one.conf
CONF=one.conf bash trace_axes.sh gebco_pacific.nc
