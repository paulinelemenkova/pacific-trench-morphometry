# pacific-trench-morphometry

GMT and Python workflow for a quantitative morphometric typology of the twenty
Pacific deep-sea trenches from GEBCO bathymetry, with the derived cross-profile
database.

## Workflow

Traces each trench axis from a global bathymetric grid, casts trench-normal
cross-profiles under identical criteria, reduces each profile to seven
morphometric parameters plus an asymmetry index, decorrelates them by principal
component analysis, and partitions them by unsupervised clustering with the
number of classes chosen by internal validation.

## Input data (not redistributed)

Download from the sources below; none are included here.

| Data set | Variable | Release | Source |
|---|---|---|---|
| GEBCO | Bathymetry, 15 arc-sec | GEBCO_2023 | https://www.gebco.net |
| Müller et al. (2008) | Seafloor age, 2 arc-min | age.3.6 | https://www.earthbyte.org |
| GlobSed (Straume et al., 2019) | Sediment thickness, 5 arc-min | v3 | https://www.ngdc.noaa.gov |
| Bird (2003) | Plate boundaries | PB2002 | https://doi.org/10.1029/2001GC000252 |

## scripts/ (run in numerical order)

| Script | Purpose |
|---|---|
| `01_cut_gebco.sh` | Cut the Pacific subset from the global GEBCO grid |
| `02_shift_globsed.sh` | Shift GlobSed to the 0–360 longitude convention |
| `03_fig03_datacoverage.sh` | Coverage figure (age, sediment thickness) |
| `04_trace_axes.sh` | Trace each trench axis |
| `05_check_seed.sh` | Inspect a seed against the relief |
| `06_retrace_one.sh` | Re-trace a single trench |
| `07_extract_profiles.sh` | Cast trench-normal profiles and sample the grid |
| `08_morphometry.py` | Morphometric parameter vector per profile |
| `09_pca_cluster.py` | Standardise, PCA, k-means, silhouette selection of K |
| `10_batch_extract.sh` | Batch driver over all twenty trenches |
| `11_sample_aux_grids.sh` | Sample age and sediment thickness at profiles |
| `12_build_dataframe.py` | Assemble and export the data frame |
| `13_statistics.py` | Spearman, Kruskal–Wallis, multiple-comparison correction |
| `14_fig15_classmap.py` | Map of profiles coloured by class |

## data/

Digitised trench axes (`axes/`), axis nodes, per-trench configuration
(`trenches.conf`, `trenches_extended.conf`) and the derived tables
(`morphometry.csv`, `morphometry_classified.csv`, `table_silhouette.csv`,
`table_parameter_correlations.csv`, `sensitivity_results.csv`). Input grids are
not included; `.gitignore` blocks `*.nc`, `*.grd` and `*.tif`.

## Requirements

GMT 6.6.0, pyGMT 0.19.0, Python 3.14.0, NumPy, SciPy, pandas, Matplotlib,
scikit-learn 1.9.0. See `requirements.txt`.

## Licence

Code under the MIT Licence (`LICENSE`); derived data in `data/` under CC-BY-4.0.
Input grids remain under their providers' terms.
