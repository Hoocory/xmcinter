# Quick Start

This page shows the shortest path from an XMC run directory to useful tables,
filters, and maps.

```python
import numpy as np
import matplotlib.pyplot as plt

import xmcinter.xmcfiles as xf
import xmcinter.wrangle as xw
import xmcinter.xmcmap as xm
```

Set the run directory:

```python
run = "/path/to/xmc/run/"
```

## Read Convergence Statistics

```python
sf = xf.merge_output(runpath=run, filetype="statistic", save=False)
sf["redchi2"] = sf["chi2"] / sf["dof"]
sf = sf.sort_values("iteration")

sf[["iteration", "chi2", "dof", "redchi2"]].tail()
```

## Read Blob Parameters

```python
df = xf.merge_output(runpath=run, filetype="deconvolution", save=False)
df = df.sort_values("iteration").reset_index(drop=True)
```

If the run contains `parameters.txt`, `df` should already have scientific column
names. Inspect them:

```python
list(df.columns)
```

If the run does not contain `parameters.txt`, manually assign the correct names
from the XMC setup before scientific analysis:

```python
df.columns = ["blob_kT", "blob_phi", "blob_psi", "blob_lnsigma", "blob_norm", "iteration"]
```

## Filter to Converged Iterations

```python
df = xw.filterblobs(df, "iteration", minvals=500)
```

## Add a Blob Size Column

Gaussian blobs commonly store size as `blob_lnsigma`.

```python
if "blob_lnsigma" in df.columns:
    df["blob_sigma"] = np.exp(df["blob_lnsigma"])
```

## Plot a Temperature Distribution

```python
plt.hist(df["blob_kT"], bins=50, weights=df.get("blob_norm"))
plt.xlabel("blob_kT")
plt.ylabel("weighted count")
plt.show()
```

## Create a Temperature Map

```python
imgs = xm.make_map(
    df,
    paramname="blob_kT",
    paramweights="blob_norm",
    binsize=30.0,
    iteration_type="median",
    ctype="median",
    outfile="temperature",
    clobber=True,
    cint=False,
)

plt.imshow(imgs[0], origin="lower", cmap="plasma")
plt.colorbar(label="blob_kT")
plt.show()
```

`make_map()` writes a FITS file and returns a list of NumPy image arrays.
