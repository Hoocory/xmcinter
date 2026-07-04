# Tutorial: Reading XMC Output

This tutorial starts from a completed XMC run directory and builds the two most
important tables: statistics and blobs.

```python
import pandas as pd
import xmcinter.xmcfiles as xf
```

Set the run directory:

```python
run = "/path/to/xmc/run/"
```

## Read `statistic.*`

```python
sf = xf.merge_output(runpath=run, filetype="statistic", save=False)
sf["redchi2"] = sf["chi2"] / sf["dof"]
sf = sf.sort_values("iteration").reset_index(drop=True)

sf.tail()
```

Use this table to choose a convergence cutoff.

```python
sf[["iteration", "redchi2"]].plot(x="iteration", y="redchi2")
```

## Read `deconvolution.*`

```python
df = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
df = df.sort_values("iteration").reset_index(drop=True)

df.head()
```

## Inspect Available Columns

If `parameters.txt` exists:

```python
parnames = xf.read_parnames(run)
parnames
```

The deconvolution DataFrame should already use those names:

```python
list(df.columns)
```

If `parameters.txt` is missing, XMCInter can still read the files, but it cannot
know the physical meaning of each column. Assign names from the run setup:

```python
df.columns = ["blob_kT", "blob_phi", "blob_psi", "blob_lnsigma", "blob_norm", "iteration"]
```

Do this only when you are sure the mapping matches the model used for the run.

## Read Other Text Products

```python
mean = xf.merge_output(runpath=run, filetype="mean", save=False)
sigma = xf.merge_output(runpath=run, filetype="sigma", save=False)
changed = xf.merge_output(runpath=run, filetype="changed", save=False)
```

These are useful for deeper inspection of sampler behavior, but the normal
analysis path centers on `statistic.*` and `deconvolution.*`.

## Save a Working Table

For reproducible notebook analysis, save a filtered/annotated table explicitly:

```python
df.to_csv("deconvolution_loaded.tsv", sep="\t", index=False)
```

Or reload later with Pandas:

```python
df = pd.read_table("deconvolution_loaded.tsv", sep="\t")
```
