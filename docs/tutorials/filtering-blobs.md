# Tutorial: Filtering Blobs

This tutorial continues from the loaded blob table `df` created in
[Reading XMC Output](reading-xmc-output.md).

```python
import numpy as np
import xmcinter.wrangle as xw
```

## Filter by Iteration

Choose an iteration cutoff after inspecting the reduced chi-square curve.

```python
itmin = 500
df_conv = xw.filterblobs(df, "iteration", minvals=itmin)
```

Equivalent Pandas syntax:

```python
df_conv = df[df["iteration"] >= itmin].copy()
```

## Add Derived Blob Size

For Gaussian blobs, maps usually need `blob_sigma`.

```python
if "blob_lnsigma" in df_conv.columns:
    df_conv["blob_sigma"] = np.exp(df_conv["blob_lnsigma"])
```

## Filter by Temperature

```python
hot = xw.filterblobs(df_conv, "blob_kT", minvals=2.0)
cool = xw.filterblobs(df_conv, "blob_kT", maxvals=1.0)
```

## Filter by Emission or Norm

Many runs have `blob_norm`. Runs cleaned with `diagnostics.clean()` may also
have `blob_em`.

```python
bright = xw.filterblobs(df_conv, "blob_norm", minvals=1e-6)
```

Use `blob_em` when available:

```python
if "blob_em" in df_conv.columns:
    bright = xw.filterblobs(df_conv, "blob_em", minvals=1e58)
```

## Combine Filters

```python
hot_bright = xw.filterblobs(
    df_conv,
    ["blob_kT", "blob_norm"],
    minvals=[2.0, 1e-6],
    maxvals=[8.0, None],
    logic="and",
)
```

## Filter by Region

Use `filtercircle()` for region-style filtering:

```python
region = xw.filtercircle(
    df_conv,
    x="blob_phi",
    y="blob_psi",
    r="blob_sigma",
    x0=0.0,
    y0=0.0,
    r0=60.0,
    logic="include",
    fraction=True,
)
```

When `fraction=True`, the function adds contribution-fraction columns rather
than simply dropping every partially overlapping blob.

## Summarize the Subset

```python
median_kT = xw.weighted_median(hot_bright["blob_kT"], weights=hot_bright["blob_norm"])
std_kT = xw.weighted_std(hot_bright["blob_kT"], weights=hot_bright["blob_norm"])

median_kT, std_kT
```

## Plot Quick Checks

```python
import matplotlib.pyplot as plt

plt.hist(df_conv["blob_kT"], bins=50, alpha=0.4, label="all")
plt.hist(hot_bright["blob_kT"], bins=50, alpha=0.6, label="hot + bright")
plt.xlabel("blob_kT")
plt.legend()
plt.show()
```
