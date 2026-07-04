# Tutorial: Diagnostics

Diagnostics help answer two early questions:

1. Has the run converged enough to choose an iteration cutoff?
2. Do the blobs produce sensible parameter distributions, maps, and spectra?

```python
import matplotlib.pyplot as plt

import xmcinter.xmcfiles as xf
import xmcinter.wrangle as xw
import xmcinter.diagnostics as xd
import xmcinter.plots as xplt
```

## Manual Convergence Check

The most robust first step is to inspect `statistic.*` directly:

```python
sf = xf.merge_output(runpath=run, filetype="statistic", save=False)
sf["redchi2"] = sf["chi2"] / sf["dof"]
sf = sf.sort_values("iteration")
```

```python
plt.plot(sf["iteration"], sf["redchi2"])
plt.xlabel("iteration")
plt.ylabel("chi2 / dof")
plt.show()
```

Choose `itmin` after the curve settles.

```python
itmin = 500
sf_conv = xw.filterblobs(sf, "iteration", minvals=itmin)
xw.weighted_median(sf_conv["redchi2"])
```

## Bokeh Convergence Plot

When your Bokeh version is compatible:

```python
sf = xplt.chi2(runpath=run, itmin=itmin, outfile="notebook")
```

If this fails on a modern Bokeh version, use the Matplotlib plot above.

## High-Level Diagnostic Pass

`diagnostics.check()` runs several checks at once:

```python
dfall, sf = xd.check(
    runpath=run,
    outpath="analysis",
    itmin=itmin,
    display=False,
    skipspectrum=True,
    cint=False,
)
```

It can create:

- reduced chi-square plot,
- cleaned blob table,
- trace plots,
- posterior histograms,
- scatter plots,
- a basic norm map.

## Cleaning Blobs

If your deconvolution table has named columns, `clean()` adds common derived
columns:

```python
dfall = xd.clean(runpath=run, itmin=itmin, distance=3.3)
```

This can add `blob_sigma`, `blob_em`, `blob_volume`, density, and mass columns.

## Strictly In-Memory Alternative

Use this when you do not want `clean()` to write a merged file:

```python
import numpy as np
import xmcinter.astro_utilities as astro

dfall = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
dfall = xw.filterblobs(dfall, "iteration", minvals=itmin)

dfall["blob_sigma"] = np.exp(dfall["blob_lnsigma"])

dist_cm = astro.convert_distance(3.3, "kpc", "cm")
dfall["blob_em"] = astro.norm_to_em(dfall["blob_norm"], dist_cm)
```

## Trace Plot

```python
fig = xplt.trace(
    dfall[["iteration", "blob_kT", "blob_norm"]],
    outfile="notebook",
)
```

## Histogram Check

```python
plt.hist(dfall["blob_kT"], bins=50, weights=dfall.get("blob_norm"))
plt.xlabel("blob_kT")
plt.show()
```

For compatible Bokeh versions:

```python
xplt.histogram_grid(
    dfall,
    columns=["blob_kT", "blob_norm"],
    weights="blob_norm",
    outfile="notebook",
)
```
