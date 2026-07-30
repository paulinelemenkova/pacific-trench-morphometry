# pacific-trench-morphometry

GMT and Python workflow for a quantitative morphometric typology of the twenty
Pacific deep-sea trenches from GEBCO bathymetry, with the derived cross-profile
database.

This repository holds the complete software accompanying:

> Lemenkova, P., and Piskarev, A. L. Quantitative morphometric typology of
> Pacific deep-sea trenches from automated bathymetric cross-profiles.
> *Geochemistry, Geophysics, Geosystems* (submitted).

The archived release corresponding to the manuscript is preserved on Zenodo with
a DOI: **[insert DOI after tagging v1.0]**

## What the workflow does

From a single global bathymetric grid it traces the axis of each of the twenty
Pacific trenches, casts trench-normal cross-profiles under identical criteria,
reduces every profile to seven morphometric parameters plus a dimensionless
asymmetry index, decorrelates them by principal component analysis, and
partitions them by unsupervised clustering with the number of classes chosen by
internal validation. 2,876 profiles were cast and 1,867 retained.

## Input data (not redistributed here)

All input grids are open access and must be downloaded from their sources. None
are included in this repository, both because of their size and because they are
not ours to redistribute.

| Data set | Variable | Release | Source |
|---|---|---|---|
| GEBCO | Bathymetry, 15 arc-sec | GEBCO_2023 | https://www.gebco.net |
| Müller et al. (2008) | Seafloor age, 2 arc-min | age.3.6 | https://www.earthbyte.org |
| GlobSed (Straume et al., 2019) | Sediment thickness, 5 arc-min | v3 | https://www.ngdc.noaa.gov |
| Bird (2003) | Plate boundaries | PB2002 | https://doi.org/10.1029/2001GC000252 |

## Contents

### `scripts/` — run in numerical order

| Script | Purpose |
|---|---|
| `01_cut_gebco.sh` | Cut the Pacific subset from the global GEBCO grid |
| `02_shift_globsed.sh` | Shift GlobSed to the 0–360 longitude convention |
| `03_fig03_datacoverage.sh` | Two-panel coverage figure (age, sediment thickness) |
| `04_trace_axes.sh` | Trace each trench axis as the locus of deepest nodes |
| `05_check_seed.sh` | Inspect a grid-built seed against the relief before use |
| `06_retrace_one.sh` | Re-trace a single trench with adjusted settings |
| `07_extract_profiles.sh` | Cast trench-normal profiles and sample the grid |
| `08_morphometry.py` | Compute the morphometric parameter vector per profile |
| `09_pca_cluster.py` | Standardise, PCA, k-means, silhouette selection of K |
| `10_batch_extract.sh` | Batch driver over all twenty trenches |
| `11_sample_aux_grids.sh` | Sample seafloor age and sediment thickness at profiles |
| `12_build_dataframe.py` | Assemble and export the morphometric data frame |
| `13_statistics.py` | Spearman correlation, Kruskal–Wallis, multiple-comparison correction |
| `14_fig15_classmap.py` | pyGMT map of profiles coloured by morphometric class |

Scripts `07`, `08` and `09` are the three reproduced in the manuscript.

### `data/` — configuration and derived products

| File | Contents |
|---|---|
| `axes/1_Aleutian.txt` … `axes/20_Peru-Chile.txt` | Digitised trench axis of each trench, lon lat, numbered in along-margin order |
| `axis_nodes.txt` | Axis nodes produced by the tracing step |
| `trenches.conf` | Per-trench configuration read by the extraction scripts |
| `trenches_extended.conf` | Configuration for the extended run |
| `morphometry.csv` | All extracted profiles with their eight morphometric parameters |
| `morphometry_classified.csv` | The 1,867 retained profiles with PCA scores and class labels |
| `table_silhouette.csv` | Mean silhouette coefficient against K |
| `table_parameter_correlations.csv` | Parameter correlation matrix |
| `sensitivity_results.csv` | Resolution-sensitivity test results |

Input grids are **not** included; download them from the sources in the table
above. The `.gitignore` blocks `*.nc`, `*.grd` and `*.tif` so that the 1.3 GB
Pacific GEBCO subset can never be committed by accident.

## Requirements

GMT 6.6.0, pyGMT 0.19.0, Python 3.14.0, NumPy, SciPy, pandas, Matplotlib,
scikit-learn 1.9.0. See `requirements.txt`.

## Licence

Code is released under the MIT Licence (see `LICENSE`). The derived data files in
`data/` are released under CC-BY-4.0. The input grids remain under the terms of
their respective providers.

## Citation

If you use this software or the derived database, please cite the Zenodo archive
and the accompanying paper.
